from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING, Dict, List, Optional, Union, overload

from sila_cetoni.application.device import CetoniDevice, Device, ThirdPartyDevice
from sila_cetoni.device_driver_abc import DeviceDriverABC
from sila_cetoni.utils import get_version

from .device_drivers import IOChannelInterface, cetoni
from .sila.io_service.server import Server

if TYPE_CHECKING:
    from sila_cetoni.application.application_configuration import ApplicationConfiguration
    from sila_cetoni.application.cetoni_device_configuration import CetoniDeviceConfiguration


__version__ = get_version(__name__)

logger = logging.getLogger(__name__)


class IODevice(Device):
    """
    Simple class to represent an I/O device with (possibly) multiple I/O channels
    """

    _io_channels: List[IOChannelInterface]

    def __init__(self, name: str, manufacturer: str, simulated: bool, *, device_type="io", **kwargs) -> None:
        # `**kwargs` for additional arguments that are not used and that might come from `ThirdPartyDevice.__init__` as
        # the result of `ThirdPartyIODevice.__init__`
        super().__init__(name=name, device_type=device_type or "io", manufacturer=manufacturer, simulated=simulated)
        self._io_channels

    @property
    def io_channels(self) -> List[IOChannelInterface]:
        return self._io_channels

    @io_channels.setter
    def io_channels(self, io_channels: List[IOChannelInterface]):
        self._io_channels = io_channels


# `CetoniIODevice` *is* a `IODevice`, as well, via duck typing
class CetoniIODevice(CetoniDevice[cetoni.IOChannelInterface]):
    """
    Simple class to represent an I/O device that has an arbitrary number of analog and digital I/O channels
    (inherited from the `CetoniDevice` class)
    """

    def __init__(self, name: str) -> None:
        super().__init__(name, "io")


class __IODeviceDummy(DeviceDriverABC):
    __parent_device: ThirdPartyIODevice

    def __init__(self, parent_device: ThirdPartyIODevice):
        self.__parent_device = parent_device

    def start(self):
        for channel in self.__parent_device.io_channels:
            channel.start()

    def stop(self):
        for channel in self.__parent_device.io_channels:
            channel.stop()


class ThirdPartyIODevice(ThirdPartyDevice[__IODeviceDummy], IODevice):
    """
    A third party I/O device
    """

    def __init__(self, name: str, json_data: Dict) -> None:
        super().__init__(name, json_data)

        self._device = __IODeviceDummy(self)

    def set_device_simulated_or_raise(self, err: Exception) -> None:
        # no simulated device driver support yet
        raise err


def parse_devices(json_devices: Optional[Dict[str, Dict]]) -> List[IODevice]:
    """
    Parses the given JSON configuration `json_devices` and creates the necessary `IODevice`s

    Parameters
    ----------
    json_devices: Dict[str, Dict] (optional)
        The `"devices"` section of the JSON configuration file as a dictionary (key is the device name, the value is a
        dictionary with the configuration parameters for the device, i.e. `"type"`, `"manufacturer"`, ...)

    Returns
    -------
    List[IODevice]
        A list with all `IODevice`s as defined in the JSON config
    """

    logger.info(f"Parsing devices from JSON config for {__name__!r}")

    devices: List[IODevice] = []
    if json_devices is not None:
        for device_name in json_devices:
            try:
                if json_devices[device_name]["type"] == "io":
                    if json_devices[device_name]["manufacturer"] == "Kunbus":
                        devices.append(ThirdPartyIODevice(device_name, json_devices[device_name]))
            except KeyError as err:
                raise RuntimeError(
                    f"Failed to parse device {device_name!r}: Expected property {err} could not be found"
                )
    return devices


@overload
def create_devices(config: ApplicationConfiguration, scan: bool = False) -> None:
    """
    Looks up all I/O devices from the current configuration and tries to auto-detect more devices if `scan` is `True`

    Parameters
    ----------
    config: ApplicationConfiguration
        The application configuration containing all devices for which SiLA Server and thus device driver instances
        shall be created
    scan: bool (default: False)
        Whether to scan for more devices than the ones defined in `config`
    """
    ...


@overload
def create_devices(config: CetoniDeviceConfiguration) -> List[CetoniIODevice]:
    """
    Looks up all CETONI devices from the given configuration `config` and creates the necessary `CetoniIODevice`s for
    them

    Parameters
    ----------
    config: CetoniDeviceConfiguration
        The CETONI device configuration

    Returns
    -------
    List[CetoniIODevice]
        A list with all `CetoniIODevice`s from the device configuration
    """
    ...


def create_devices(config: Union[ApplicationConfiguration, CetoniDeviceConfiguration], *args, **kwargs):
    from sila_cetoni.application.application_configuration import ApplicationConfiguration
    from sila_cetoni.application.cetoni_device_configuration import CetoniDeviceConfiguration

    if isinstance(config, ApplicationConfiguration):
        try:
            return create_devices_json(config, kwargs.get("scan", args[0]))
        except KeyError:
            return create_devices_json(config)
    if isinstance(config, CetoniDeviceConfiguration):
        return create_devices_cetoni(config)
    raise ValueError(
        f"Parameter 'config' must be of type 'ApplicationConfiguration' or 'CetoniDeviceConfiguration', not"
        f"{type(config)!r}"
    )


def create_devices_json(config: ApplicationConfiguration, scan: bool = False) -> None:
    """
    Implementation of `create_devices` for devices from the JSON config

    See `create_devices` for an explanation of the parameters
    """

    devices: List[IODevice] = list(filter(lambda d: d.device_type == "io", config.devices))

    for device in devices:
        if device.manufacturer == "Kunbus":

            from .device_drivers import revpi  # TODO: catch ImportError

            channels: List[revpi.IOChannelInterface] = []

            for description, ChannelType in (
                ("analog in", revpi.RevPiAnalogInChannel),
                ("analog out", revpi.RevPiAnalogOutChannel),
                ("digital in", revpi.RevPiDigitalInChannel),
                ("digital out", revpi.RevPiDigitalOutChannel),
            ):
                channel_count = ChannelType.number_of_channels()
                logger.debug(f"Number of {description} channels: {channel_count}")
                for i in range(channel_count):
                    channels.append(ChannelType.channel_at_index(i))
                    logger.debug(f"Found {description} channel {i} named {channels[-1].name}")

            device.io_channels = channels

    if scan:
        logger.warning("Automatic searching for I/O devices is not supported!")


def create_devices_cetoni(config: CetoniDeviceConfiguration) -> List[CetoniIODevice]:
    """
    Implementation of `create_devices` for devices from the CETONI device config

    See `create_devices` for an explanation of the parameters and return value
    """

    channels: List[cetoni.IOChannelInterface] = []

    for (description, ChannelType) in (
        ("analog in", cetoni.CetoniAnalogInChannel),
        ("analog out", cetoni.CetoniAnalogOutChannel),
        ("digital in", cetoni.CetoniDigitalInChannel),
        ("digital out", cetoni.CetoniDigitalOutChannel),
    ):
        channel_count = ChannelType.number_of_channels()
        logger.debug(f"Number of {description} channels: {channel_count}")
        for i in range(channel_count):
            channels.append(ChannelType.channel_at_index(i))
            logger.debug(f"Found {description} channel {i} named {channels[-1].name}")

    devices: List[CetoniIODevice] = []
    for channel in channels:
        channel_name = channel.get_name()
        # Using `config.devices` here and operating directly on these devices is somewhat contradictory to the
        # decoupling between sila_cetoni.application and the add-on packages that this method should achieve. However,
        # this seems to be the only viable way for now.
        for device in devices + config.devices:
            if device.name.rsplit("_Pump", 1)[0] in channel_name:
                logger.debug(f"Channel {channel_name} belongs to device {device}")
                device.io_channels.append(channel)
                break
        else:
            # https://regexr.com/6pv74
            device_name = re.match(
                r".*(?=((_TC)|(_AI)|(_AnIN)|(_AO)|(_DI)|(_DigIN)|(_DO)|(_DigOUT))\w{1}"
                r"((((_IN)|(_DIAG))\w{1,2})|((_PWM)|(_PT100)))?$)",
                channel_name,
            ).group()
            logger.debug(f"Standalone I/O device {device_name}")
            device = CetoniIODevice(device_name)
            logger.debug(f"Channel {channel_name} belongs to device {device}")
            device.io_channels.append(channel)
            devices.append(device)

    return devices


def create_server(device: IODevice, **server_args) -> Server:
    """
    Creates the SiLA Server for the given `device`

    Parameters
    ----------
    device: Device
        The device for which to create a SiLA Server
    **server_args
        Additional arguments like server name, server UUID to pass to the server's `__init__` function
    """
    logger.info(f"Creating server for {device}")
    return Server(io_channels=device.io_channels, **server_args)
