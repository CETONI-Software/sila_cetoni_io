# Generated by sila2.code_generator; sila2.__version__: 0.8.0
# -----
# This class does not do anything useful at runtime. Its only purpose is to provide type annotations.
# Since sphinx does not support .pyi files (yet?), so this is a .py file.
# -----

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from typing import Iterable, Optional

    from analogoutchannelcontroller_types import SetOutputValue_Responses
    from sila2.client import (
        ClientMetadata,
        ClientMetadataInstance,
        ClientObservableProperty,
        ClientUnobservableProperty,
    )


class AnalogOutChannelControllerClient:
    """
    Allows to control one analog output channel of an I/O module
    """

    NumberOfChannels: ClientUnobservableProperty[int]
    """
    The number of analog output channels.
    """

    Value: ClientObservableProperty[float]
    """
    The value of the analog output channel.
    """

    ChannelIndex: ClientMetadata[int]
    """
    The index of the channel that should be used. This value is 0-indexed, i.e. the first channel has index 0, the second one index 1 and so on.
    """

    def SetOutputValue(
        self, Value: float, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> SetOutputValue_Responses:
        """
        Set the value of the analog output channel.
        """
        ...
