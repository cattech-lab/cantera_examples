#include "cantera/core.h"
#include "cantera/zerodim.h"
#include "cantera/kinetics.h"
#include "cantera/base/Array.h"

#include <iostream>

using namespace Cantera;

static shared_ptr<Array2D> _states = nullptr;

extern "C"
{
    double ignitiondelay_(char* mechFileName, const double* temp, const double* p, ftnlen lenmech)
    {
        std::cout << "Call ignitiondelay" << std::endl;
        
        std::string strMech = std::string(mechFileName, lenmech);

        // condition
        double phi = 1.0;

        // define gas state
        auto sol = newSolution(strMech);
        auto gas = sol->thermo();
        gas->setState_TP(*temp, *p);
        gas->setEquivalenceRatio(phi, "nc7h16", "o2:1.0, n2:3.76");

        // define reactor
        IdealGasReactor r;
        r.insert(sol);

        ReactorNet sim;
        sim.addReactor(r);

        // time condition
        double tend = 0.1;
        double dt = 1.0e-6;

        // time loop
        double time = 0.0;
        int nstep = tend / dt;

        _states = shared_ptr<Array2D>(new Array2D(2, nstep));
        for (int i = 0; i < nstep; i++) {
            sim.advance(time);
            _states->value(0, i) = time;
            _states->value(1, i) = r.contents().temperature();
            time += dt;
        }

        // ignition delay time
        double diffMax = 0.0;
        int ix = 0;
        for (int i = 0; i < nstep - 1; i++) 
        {
            double diff = _states->value(1, i + 1) - _states->value(1, i);
            if (diff > diffMax) 
            {
                diffMax = diff;
                ix = i;
            }
        }
        double time_igd = _states->value(0, ix);

        return time_igd;
    }

    double getstates_(const int* i, const int* j)
    {
        if (_states == nullptr) {
            return std::nan("");
        }

        size_t ist = *i;
        size_t jst = *j;

        if (ist >= 0 && ist < _states->nRows() && jst >= 0 && jst < _states->nColumns()) {
            return _states->value(ist, jst);
        } else {
            return std::nan("");
        }
    }

    void getstatessize_(int* nr, int* nc)
    {
        if (_states == nullptr) {
            *nr = 0;
            *nc = 0;
        } else {    
            *nr = (int)_states->nRows();
            *nc = (int)_states->nColumns();
        } 
    }
}
