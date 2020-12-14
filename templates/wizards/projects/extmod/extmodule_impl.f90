module %{ModuleName}_impl

    ! 
    ! %{ModuleName} implementation module
    ! 
    ! Subroutines and function in this module 
    ! will only be availble internally for the 
    ! interface module. Not availble in the
    ! Extension module
    !        

    use %{ModuleName}_const

    implicit none

contains

    subroutine example_impl(a, b, c)

        real(rk), intent(in) :: a
        real(rk), intent(in) :: b
        real(rk), intent(inout) :: c

        c = a + b

    end subroutine example_impl

end module %{ModuleName}_impl
