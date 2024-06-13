"""Module for base energy module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from warnings import warn

from ..emeterstatus import EmeterStatus
from ..feature import Feature
from ..module import Module


class Energy(Module, ABC):
    """Base interface to represent a LED module."""

    def _initialize_features(self):
        """Initialize features."""
        device = self._device
        self._add_feature(
            Feature(
                device,
                name="Current consumption",
                attribute_getter="current_consumption",
                container=self,
                unit="W",
                id="current_consumption",
                precision_hint=1,
                category=Feature.Category.Primary,
            )
        )
        self._add_feature(
            Feature(
                device,
                name="Today's consumption",
                attribute_getter="consumption_today",
                container=self,
                unit="kWh",
                id="consumption_today",
                precision_hint=3,
                category=Feature.Category.Info,
            )
        )
        self._add_feature(
            Feature(
                device,
                id="consumption_this_month",
                name="This month's consumption",
                attribute_getter="consumption_this_month",
                container=self,
                unit="kWh",
                precision_hint=3,
                category=Feature.Category.Info,
            )
        )
        if self.has_total_consumption:
            self._add_feature(
                Feature(
                    device,
                    name="Total consumption since reboot",
                    attribute_getter="consumption_total",
                    container=self,
                    unit="kWh",
                    id="consumption_total",
                    precision_hint=3,
                    category=Feature.Category.Info,
                )
            )
        if self.has_voltage_current:
            self._add_feature(
                Feature(
                    device,
                    name="Voltage",
                    attribute_getter="voltage",
                    container=self,
                    unit="V",
                    id="voltage",
                    precision_hint=1,
                    category=Feature.Category.Primary,
                )
            )
            self._add_feature(
                Feature(
                    device,
                    name="Current",
                    attribute_getter="current",
                    container=self,
                    unit="A",
                    id="current",
                    precision_hint=2,
                    category=Feature.Category.Primary,
                )
            )

    @property
    @abstractmethod
    def status(self) -> EmeterStatus:
        """Return current energy readings."""

    @property
    @abstractmethod
    def current_consumption(self) -> float | None:
        """Get the current power consumption in Watt."""

    @property
    @abstractmethod
    def consumption_today(self) -> float | None:
        """Return today's energy consumption in kWh."""

    @property
    @abstractmethod
    def consumption_this_month(self) -> float | None:
        """Return this month's energy consumption in kWh."""

    @property
    @abstractmethod
    def consumption_total(self) -> float | None:
        """Return total consumption since last reboot in kWh."""

    @property
    @abstractmethod
    def current(self) -> float | None:
        """Return the current in A."""

    @property
    @abstractmethod
    def voltage(self) -> float | None:
        """Get the current voltage in V."""

    @property
    @abstractmethod
    def has_voltage_current(self) -> bool:
        """Return True if the device reports current and voltage."""

    @property
    @abstractmethod
    def has_total_consumption(self) -> bool:
        """Return True if device reports total energy consumption since last reboot."""

    @abstractmethod
    async def get_status(self):
        """Return real-time statistics."""

    @property
    @abstractmethod
    def has_periodic_stats(self) -> bool:
        """Return True if device can report statistics for different time periods."""

    @abstractmethod
    async def erase_stats(self):
        """Erase all stats."""

    @abstractmethod
    async def get_daystat(self, *, year=None, month=None, kwh=True) -> dict:
        """Return daily stats for the given year & month.

        The return value is a dictionary of {day: energy, ...}.
        """

    @abstractmethod
    async def get_monthstat(self, *, year=None, kwh=True) -> dict:
        """Return monthly stats for the given year."""

    _deprecated_attributes = {
        "emeter_today": "consumption_today",
        "emeter_this_month": "consumption_this_month",
        "realtime": "status",
        "get_realtime": "get_status",
        "erase_emeter_stats": "erase_stats",
    }

    def __getattr__(self, name):
        if attr := self._deprecated_attributes.get(name):
            msg = f"{name} is deprecated, use {attr} instead"
            warn(msg, DeprecationWarning, stacklevel=1)
            return getattr(self, attr)
        raise AttributeError(f"Energy module has no attribute {name!r}")
