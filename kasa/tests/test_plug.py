from kasa import DeviceType

from .conftest import plug_iot, plug_smart, switch_iot, switch_smart
from .test_smartdevice import SYSINFO_SCHEMA

# these schemas should go to the mainlib as
# they can be useful when adding support for new features/devices
# as well as to check that faked devices are operating properly.


@plug_iot
async def test_plug_sysinfo(dev):
    assert dev.sys_info is not None
    SYSINFO_SCHEMA(dev.sys_info)

    assert dev.model is not None

    assert dev.device_type == DeviceType.Plug or dev.device_type == DeviceType.Strip
    assert dev.is_plug or dev.is_strip


@switch_iot
async def test_switch_sysinfo(dev):
    assert dev.sys_info is not None
    SYSINFO_SCHEMA(dev.sys_info)

    assert dev.model is not None

    assert dev.device_type == DeviceType.Switch
    assert dev.is_switch


@plug_iot
async def test_plug_led(dev):
    original = dev.led

    await dev.set_led(False)
    await dev.update()
    assert not dev.led

    await dev.set_led(True)
    await dev.update()
    assert dev.led

    await dev.set_led(original)


@switch_iot
async def test_switch_led(dev):
    original = dev.led

    await dev.set_led(False)
    await dev.update()
    assert not dev.led

    await dev.set_led(True)
    await dev.update()
    assert dev.led

    await dev.set_led(original)


@plug_smart
async def test_plug_device_info(dev):
    assert dev._info is not None
    assert dev.model is not None

    assert dev.device_type == DeviceType.Plug or dev.device_type == DeviceType.Strip


@switch_smart
async def test_switch_device_info(dev):
    assert dev._info is not None
    assert dev.model is not None

    assert dev.device_type == DeviceType.Switch or dev.device_type == DeviceType.Dimmer
