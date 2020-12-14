module %{ModuleName}

    ! 
    ! %{ModuleName} interface module
    ! 
    ! Subroutines and function in this module 
    ! will be availble in the F2PY generated
    ! extension module.
    !    

    use %{ModuleName}_const
    use %{ModuleName}_impl

    implicit none

contains

    subroutine example_real(a, b, c)

        real(rk), intent(in) :: a
        real(rk), intent(in) :: b
        real(rk), intent(out) :: c

        c = a + b

    end subroutine example_real

    subroutine example_int(a, b, c)

        integer, intent(in) :: a
        integer, intent(in) :: b
        integer, intent(out) :: c

        c = a + b

    end subroutine example_int

    subroutine example_array(a, b, c)

        real(rk), intent(in) :: a
        real(rk), intent(in) :: b
        real(rk), intent(inout) :: c

        c = a + b

    end subroutine example_array

    subroutine example_intf(a, b, c)

        real(rk), intent(in) :: a
        real(rk), intent(in) :: b
        real(rk), intent(inout) :: c

        call example_impl(a, b, c)

    end subroutine example_intf

end module %{ModuleName}
