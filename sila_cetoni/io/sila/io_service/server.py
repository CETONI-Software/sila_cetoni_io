from __future__ import annotations

from typing import List, Optional, Union, cast
from uuid import UUID

from sila_cetoni.core.sila.core_service.server import Server as CoreServer
from sila_cetoni.io.device_drivers import (
    AnalogInChannelInterface,
    AnalogOutChannelInterface,
    DigitalInChannelInterface,
    DigitalOutChannelInterface,
    IOChannelInterface,
)

from .feature_implementations.analoginchannelprovider_impl import AnalogInChannelProviderImpl
from .feature_implementations.analogoutchannelcontroller_impl import AnalogOutChannelControllerImpl
from .feature_implementations.digitalinchannelprovider_impl import DigitalInChannelProviderImpl
from .feature_implementations.digitaloutchannelcontroller_impl import DigitalOutChannelControllerImpl
from .generated.analoginchannelprovider import AnalogInChannelProviderFeature
from .generated.analogoutchannelcontroller import AnalogOutChannelControllerFeature
from .generated.digitalinchannelprovider import DigitalInChannelProviderFeature
from .generated.digitaloutchannelcontroller import DigitalOutChannelControllerFeature


class Server(CoreServer):
    def __init__(
        self,
        io_channels: List[IOChannelInterface],
        server_name: str = "",
        server_type: str = "",
        server_description: str = "",
        server_version: str = "",
        server_vendor_url: str = "",
        server_uuid: Optional[Union[str, UUID]] = None,
    ):
        from ... import __version__

        super().__init__(
            server_name=server_name or "I/O Service",
            server_type=server_type or "TestServer",
            server_description=server_description or "The SiLA 2 driver for CETONI I/O modules",
            server_version=server_version or __version__,
            server_vendor_url=server_vendor_url or "https://www.cetoni.com",
            server_uuid=server_uuid,
        )

        analog_in_channels = cast(
            List[AnalogInChannelInterface],
            list(filter(lambda c: isinstance(c, AnalogInChannelInterface), io_channels)),
        )
        analog_out_channels = cast(
            List[AnalogOutChannelInterface],
            list(filter(lambda c: isinstance(c, AnalogOutChannelInterface), io_channels)),
        )
        digital_in_channels = cast(
            List[DigitalInChannelInterface],
            list(filter(lambda c: isinstance(c, DigitalInChannelInterface), io_channels)),
        )
        digital_out_channels = cast(
            List[DigitalOutChannelInterface],
            list(filter(lambda c: isinstance(c, DigitalOutChannelInterface), io_channels)),
        )

        if analog_in_channels:
            self.analoginchannelprovider = AnalogInChannelProviderImpl(self, analog_in_channels)
            self.set_feature_implementation(AnalogInChannelProviderFeature, self.analoginchannelprovider)
        if analog_out_channels:
            self.analogoutchannelcontroller = AnalogOutChannelControllerImpl(self, analog_out_channels)
            self.set_feature_implementation(AnalogOutChannelControllerFeature, self.analogoutchannelcontroller)
        if digital_in_channels:
            self.digitalinchannelprovider = DigitalInChannelProviderImpl(self, digital_in_channels)
            self.set_feature_implementation(DigitalInChannelProviderFeature, self.digitalinchannelprovider)
        if digital_out_channels:
            self.digitaloutchannelcontroller = DigitalOutChannelControllerImpl(self, digital_out_channels)
            self.set_feature_implementation(DigitalOutChannelControllerFeature, self.digitaloutchannelcontroller)
