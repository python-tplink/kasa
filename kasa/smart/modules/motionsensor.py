"""Implementation of motion sensor module."""

from __future__ import annotations

from ...feature import Feature
from ..smartmodule import SmartModule


class MotionSensor(SmartModule):
    """Implementation of motion sensor module."""

    REQUIRED_COMPONENT = None  # we depend on availability of key
    REQUIRED_KEY_ON_PARENT = "detected"

    def _initialize_features(self):
        """Initialize features."""
        self._add_feature(
            Feature(
                self._device,
                id="motion_detected",
                name="Motion detected",
                container=self,
                attribute_getter="motion_detected",
                icon="mdi:motion-sensor",
                category=Feature.Category.Primary,
                type=Feature.Type.BinarySensor,
            )
        )

    def query(self) -> dict:
        """Query to execute during the update cycle."""
        return {}

    @property
    def motion_detected(self):
        """Return True if the motion has been detected."""
        return self._device.sys_info["detected"]
