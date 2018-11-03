from typing import Dict, Union, Callable
from numbers import Real, Integral


from plasmapy.atomic import (
    IonizationStates,
)




class NEI:


    def __init__(
        self,
        inputs,
        abundances = None,
        T_e: Union[Callable, u.K] = np.nan * u.K,
        n: Union[Callable, u.m ** -3] = np.nan * u.m ** -3,
        time_input: u.s = np.nan * u.s,
        time_start: u.s = np.nan * u.s,
        time_max: u.s = np.nan * u.s,
        max_steps: Integral = 10000,
        tol: Real = 1e-15,
        dt: u.s = np.nan * u.s,
        dt_max: u.s = np.inf * u.s,
        adapt_dt: bool = False,
        verbose: bool = False,
    ):

        try:
            self.time_input = time_input
            self.time_start = time_start
            self.time_max = time_max
            self.T_e_input = T_e
            self.n_input = n
            self.max_steps = max_steps
            self.dt_input = dt

            if np.isnan(self.dt_input):
                self._dt = self.time_max / max_steps
            else:
                self._dt = self.dt_input

            self.dt_min = dt_min
            self.dt_max = dt_max
            self.adapt_dt = adapt_dt
            self.safety_factor = safety_factor
            self.verbose = verbose
            self.tol = tol

            # T_e_init = self.electron_temperature(self.time_start)
            # n_init = self.hydrogen_number_density(self.time_start)


            self.initial = IonizationStates(
                inputs=inputs,
                abundances=abundances,
                T_e=T_e_init,
                n=n_init,
                tol = self.tol,
            )

#            self.elements = self.initial.elements  # put in setting self.initial
            
# Create _inputs defaultdict that defaults to None

        except Exception as exc:
            raise NonEqIonError
