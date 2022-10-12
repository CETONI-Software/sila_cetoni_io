"""
A device driver implementation for the CETONI I/O devices

:author: Florian Meinicke (florian.meinicke@cetoni.de)
:date: 11.10.2022
"""


from __future__ import annotations

import logging

from qmixsdk import qmixanalogio, qmixdigio
from typing_extensions import Self

from .abc import IOChannelInterface  # export
from .abc import (
    AnalogInChannelInterface,
    AnalogIOChannelInterface,
    AnalogOutChannelInterface,
    DigitalInChannelInterface,
    DigitalIOChannelInterface,
    DigitalOutChannelInterface,
    State,
)

try:
    import coloredlogs
except (ModuleNotFoundError, ImportError):
    pass

logger = logging.getLogger(__name__)


class CetoniAnalogInChannel(AnalogInChannelInterface):
    """
    A thin wrapper class around `qmixanalogio.AnalogInChannel`
    """

    __channel: qmixanalogio.AnalogInChannel

    def __init__(self, index: int) -> None:
        self.__channel = qmixanalogio.AnalogInChannel()
        self.__channel.lookup_channel_by_index(index)

        super().__init__(self.__channel.get_name())

    @classmethod
    def number_of_channels(cls) -> int:
        return qmixanalogio.AnalogInChannel.get_no_of_channels()

    @classmethod
    def channel_at_index(cls, index: int) -> Self:
        return cls(index)

    @AnalogIOChannelInterface.value.getter
    def value(self) -> float:
        self._value = self.__channel.read_input()
        return self._value

    def start(self):
        # This device does not need to be started
        pass

    def stop(self):
        # This device does not need to be stopped
        pass


class CetoniAnalogOutChannel(AnalogOutChannelInterface):
    """
    A thin wrapper class around `qmixanalogio.AnalogOutChannel`
    """

    __channel: qmixanalogio.AnalogOutChannel

    def __init__(self, index: int) -> None:
        self.__channel = qmixanalogio.AnalogOutChannel()
        self.__channel.lookup_channel_by_index(index)

        super().__init__(self.__channel.get_name())
        # super().__init__("name")

    @classmethod
    def number_of_channels(cls) -> int:
        return qmixanalogio.AnalogOutChannel.get_no_of_channels()

    @classmethod
    def channel_at_index(cls, index: int) -> Self:
        return cls(index)

    @AnalogOutChannelInterface.value.getter
    def value(self) -> float:
        self._value = self.__channel.get_output_value()
        return self._value

    @value.setter
    def value(self, value: float):
        self.__channel.write_output(value)
        self._value = value

    def start(self):
        # This device does not need to be started
        pass

    def stop(self):
        # This device does not need to be stopped
        pass


class CetoniDigitalInChannel(DigitalInChannelInterface):
    """
    A thin wrapper class around `qmixdigio.DigitalInChannel`
    """

    __channel: qmixdigio.DigitalInChannel

    def __init__(self, index: int) -> None:
        self.__channel = qmixdigio.DigitalInChannel()
        self.__channel.lookup_channel_by_index(index)

        super().__init__(self.__channel.get_name())

    @classmethod
    def number_of_channels(cls) -> int:
        return qmixdigio.DigitalInChannel.get_no_of_channels()

    @classmethod
    def channel_at_index(cls, index: int) -> Self:
        return cls(index)

    @DigitalIOChannelInterface.state.getter
    def state(self) -> State:
        self._state = self._value_to_state(self.__channel.is_on())
        return self._state

    def start(self):
        # This device does not need to be started
        pass

    def stop(self):
        # This device does not need to be stopped
        pass


class CetoniDigitalOutChannel(DigitalOutChannelInterface):
    """
    A thin wrapper class around `qmixdigio.DigitalOutChannel`
    """

    __channel: qmixdigio.DigitalOutChannel

    def __init__(self, index: int) -> None:
        self.__channel = qmixdigio.DigitalOutChannel()
        self.__channel.lookup_channel_by_index(index)

        super().__init__(self.__channel.get_name())

    @classmethod
    def number_of_channels(cls) -> int:
        return qmixdigio.DigitalOutChannel.get_no_of_channels()

    @classmethod
    def channel_at_index(cls, index: int) -> Self:
        return cls(index)

    @DigitalIOChannelInterface.state.getter
    def state(self) -> State:
        self._state = self._value_to_state(self.__channel.is_output_on())
        return self._state

    @state.setter
    def state(self, state: State):
        self.__channel.write_on(self._state_to_bool(state))
        self._state = state

    def start(self):
        # This device does not need to be started
        pass

    def stop(self):
        # This device does not need to be stopped
        pass
