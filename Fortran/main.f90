program main
    implicit none

    character(len=128) :: mechFileName
    double precision :: temp, p, time_igd
    integer :: i, nr, nc

    interface
        double precision function ignitionDelay(mechFileName, temp, p)
            character(len=*), intent(in) :: mechFileName
            double precision, intent(in) :: temp, p
        end function ignitionDelay

        double precision function getStates(i, j)
            integer, intent(in) :: i, j
        end function getStates

        subroutine getStatesSize(nr, nc)
            integer, intent(out) :: nr, nc
        end subroutine getStatesSize
    end interface

    ! input parameter
    mechFileName = "LLNL_heptane_160.yaml"
    temp = 1000.0
    p = 1.3e6

    ! ignition delay C++ function
    time_igd = ignitionDelay(trim(mechFileName), temp, p)
    write(*, *) "Ignition Delay Time: ", time_igd * 1e6, " micro sec" 

    ! output states
    open(10, file="output.csv", status="replace")
    write(10, "(a)") "time,temperature"
    call getStatesSize(nr, nc)
    do i = 0, nc-1
        write(10, "(e0.8,a1,e0.8)") getStates(0, i), ",", getStates(1, i)
    enddo
    close(10)
end program main
    