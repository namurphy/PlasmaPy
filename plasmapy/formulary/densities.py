"""Functions to calculate plasma density parameters."""
__all__ = [
    "critical_density",
    "quasineutral_mass_density",
]

import astropy.units as u

from astropy.constants.si import e, eps0, m_e
from numbers import Real
from typing import Optional

from plasmapy.particles import particle_input, ParticleLike
from plasmapy.utils.decorators import validate_quantities


@validate_quantities(
    omega={"can_be_negative": False},
    validations_on_return={
        "units": [u.m**-3],
    },
)
def critical_density(omega: u.rad / u.s) -> u.m**-3:
    r"""Calculate the plasma critical density for a radiation of a given frequency.

    Parameters
    ----------
    omega: `~astropy.units.Quantity`
        The radiation frequency in units of angular frequency.

    Returns
    -------
    n_c : `~astropy.units.Quantity`
        The plasma critical density.

    Notes
    -----
    The critical density for a given frequency of radiation is
    defined as the value at which the electron plasma frequency equals
    the frequency of the radiation.

    The critical density is given by the formula

    .. math::
        n_{c}=\frac{m_{e}\varepsilon_0\omega^{2}}{e^{2}}

    where :math:`m_{e}` is the mass of an electron,
    :math:`\varepsilon_0` is the permittivity of free space, :math:`\omega`
    is the radiation frequency, and :math:`e` is the elementary charge.

    Examples
    --------
    >>> from astropy import units as u
    >>> critical_density(5e15 * u.rad/u.s)
    <Quantity 7.85519457e+27 1 / m3>

    """

    n_c = m_e * eps0 * omega**2 / (e**2)

    return n_c.to(u.m**-3, equivalencies=u.dimensionless_angles())


@particle_input
@validate_quantities
def species_mass_density(species: ParticleLike, n: u.m**-3):
    """
    Calculate the mass density of particular species.
    """
    return species.mass * n


@particle_input
@validate_quantities
def quasineutral_mass_density(
    element: ParticleLike,
    n: u.m**-3,
    *,
    Z: Optional[Real] = None,
    mass_numb: Optional[Real] = None,
) -> u.kg * u.m**-3:
    """
    Calculate the total mass density of a single-ion or multi-ion
    quasineutral plasma.

    Parameters
    ----------
    element : |particle-like|
        ...

    n : `~astropy.units.Quantity`

    Z : real number

    mass_numb : real number

    """
