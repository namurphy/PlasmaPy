"""Functionality for representing one-dimensional equilibria."""

__all__ = ["HarrisSheet"]

import astropy.constants as const
import astropy.units as u
import numpy as np

from plasmapy.utils.decorators.validators import validate_quantities


class HarrisSheet:
    r"""
    Representation of a 1D Harris sheet equilibrium.

    Parameters
    ----------
    B0 : `~astropy.units.Quantity`
         Magnitude of magnetic field in the limit of :math:`y → ∞` in
         units convertible to teslas.

    delta : `~astropy.units.Quantity`
        The characteristic thickness of the current sheet in units
        convertible to meters.

    p0 : `~astropy.units.Quantity`
        The plasma pressure in the limit of :math:`y → ∞` in units
        convertible to pascals.

    Notes
    -----
    A Harris sheet is a 1D ideal MHD equilibrium which is often used as
    the initial condition for simulations of magnetic reconnection.

    In this representation, the magnetic field will be in the :math:`±x`
    direction and the current density will be in the :math:`±z`
    direction in a :math:`\hat{x} × \hat{y} = \hat{z}`
    coordinate system.

    In resistive MHD if there is any resistivity, a Harris sheet will
    not be a true equilibrium since the resistive diffusion will
    gradually smooth out the magnetic profile over time.

    Examples
    --------
    >>> import astropy.units as u
    >>> harris_sheet = HarrisSheet(delta = 1 * u.m, B0 = 1 * u.T, p0 = 0 * u.Pa)
    >>> harris_sheet.magnetic_field(y = 1 * u.m)
    <Quantity 0.761594... T>
    >>> harris_sheet.current_density(y = 1 * u.m)
    <Quantity -334204.96... A / m2>
    >>> harris_sheet.plasma_pressure(y = 1 * u.m)
    <Quantity 167102.48... Pa>
    """

    @validate_quantities(p0={"can_be_negative": False})
    def __init__(self, B0: u.T, delta: u.m, p0: u.Pa = 0 * u.Pa):
        self.B0 = B0
        self.delta = delta
        self.p0 = p0

    @validate_quantities
    def magnetic_field(self, y: u.m) -> u.T:
        r"""
        Compute the magnetic field strength.

        Parameters
        ----------
        y : `~astropy.units.Quantity`
           Orthogonal distance from the current sheet center.

        Returns
        -------
        `~astropy.units.Quantity`

        Notes
        -----
        The magnetic field of a Harris sheet is given by

        .. math::

            B_x(y) = B_0 \tanh \left( \frac{y}{δ} \right)

        In this equation, :math:`B_0` is the asymptotic magnetic field
        strength and :math:`δ` is the characteristic thickness of the
        Harris sheet.
        """
        return self.B0 * np.tanh(u.rad * y / self.delta)

    @validate_quantities
    def current_density(self, y: u.m) -> u.A / u.m**2:
        r"""
        Compute the current density.

        Parameters
        ----------
        y : `~astropy.units.Quantity`
          Orthogonal distance from the current sheet center.

        Returns
        -------
        `~astropy.units.Quantity`

        Notes
        -----
        The current in a Harris sheet is given by

        .. math::

          J_z(y) = - \frac{B_0}{δ μ_0) \mathrm{sech}^2 \left( \frac{y}{δ} \right),

        where :math:`B_0` is the asymptotic magnetic field strength,
        :math:`δ` is the characteristic thickness of the Harris sheet,
        and :math:`μ_0` is the vacuum magnetic permeability.
        """
        return (
            -self.B0 / (self.delta * const.mu0) * np.cosh(u.rad * y / self.delta) ** -2
        )

    @validate_quantities
    def plasma_pressure(self, y: u.m) -> u.Pa:
        r"""
        Compute the plasma pressure.

        Parameters
        ----------
        y : `~astropy.units.Quantity`
          Orthogonal distance from the current sheet center.

        Returns
        -------
        `~astropy.units.Quantity`

        Notes
        -----
        The plasma pressure in a Harris sheet is given by

        .. math::

            p(y) = \frac{B_0^2}{2 μ_0} \mathrm{sech}^2 \left( \frac{y}{δ} \right) + p_0,

        where :math:`B_0` is the asymptotic magnetic field strength,
        :math:`δ` is the characteristic thickness of the Harris sheet,
        :math:`p_0` is the asymptotic plasma pressure, and :math:`μ_0`
        is the vacuum magnetic permeability.
        """
        return (
            self.B0**2 / (2 * const.mu0) * (np.cosh(u.rad * y / self.delta) ** -2)
            + self.p0
        )
