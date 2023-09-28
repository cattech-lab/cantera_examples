// #include "cantera/thermo/IdealGasPhase.h"
// #include "cantera/kinetics/BulkKinetics.h"
// #include "cantera/base/Solution.h"
// #include "cantera/zerodim.h"
// #include "cantera/base/Array.h"

#include "cantera/core.h"
#include "cantera/zerodim.h"
#include "cantera/kinetics.h"
#include "cantera/base/Array.h"

#include <iostream>
#include <fstream>

using namespace Cantera;

int main()
{
    // condition
    double temp = 1000.0;
    double p = 1.3e6;
    double phi = 1.0;

    // define gas state
    auto sol = newSolution("LLNL_heptane_160.yaml");
    auto gas = sol->thermo();
    gas->setState_TP(temp, p);
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
    Array2D states(2, nstep);
    for (int i = 0; i < nstep; i++)
    {
        sim.advance(time);
        states(0, i) = time;
        states(1, i) = r.contents().temperature();
        time += dt;
    }

    // ignition delay time
    double diffMax = 0.0;
    int ix = 0;
    for (int i = 0; i < nstep - 1; i++)
    {
        double diff = states(1, i + 1) - states(1, i);
        if (diff > diffMax)
        {
            diffMax = diff;
            ix = i;
        }
    }
    double time_igd = states(0, ix);
    std::cout << "Ignition Delay Time: " << time_igd * 1e6 << " micro sec" << std::endl;

    // write csv
    std::ofstream file("output.csv");
    file << "time,temperature" << std::endl;
    for (int i = 0; i < nstep; i++)
    {
        file << states(0, i) << "," << states(1, i) << std::endl;
    }
    file.close();

    return 0;
}
