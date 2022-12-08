"""
An interface for implementing I/O device drivers for the CETONI SiLA SDK

:author: Florian Meinicke (florian.meinicke@cetoni.de)
:date: 11.10.2022
"""

from __future__ import annotations

import logging
from abc import abstractmethod
from enum import Enum
from typing import Any, Union

from sila_cetoni.device_driver_abc import DeviceDriverABC
from typing_extensions import Self

logger = logging.getLogger(__name__)


class StrEnum(str, Enum):
    """Enum where members are also (and must be) `str`s"""


class State(StrEnum):
    """
    State of digital I/O channels
    """

    ON = "On"
    OFF = "Off"


class IOChannelInterface(DeviceDriverABC):
    """
    Interface for a digital I/O channel
    """

    _name: str

    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name

    @property
    def name(self):
        """
        Returns the name of this channel
        """
        return self._name

    def get_name(self) -> str:
        """
        Returns the name of this channel

        This function is for backwards compatibility and interoperability of device driver classes with classes directly
        from `qmixsdk` (those don't use properties but getter/setter methods)
        """
        return self._name

    @classmethod
    @abstractmethod
    def number_of_channels(cls) -> int:
        """
        Returns the number of I/O channels
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def channel_at_index(cls, index: int) -> Self:
        """
        Returns a I/O channel for the channel at the given `index`
        """
        raise NotImplementedError()


class AnalogIOChannelInterface(IOChannelInterface):
    """
    Interface for a digital I/O channel
    """

    _value: float

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._value = None

    @property
    def value(self) -> float:
        """
        Returns the value of this channel
        """
        return self._value


class AnalogInChannelInterface(AnalogIOChannelInterface):
    """
    Interface for an analog input channel
    """

    pass


class AnalogOutChannelInterface(AnalogIOChannelInterface):
    """
    Interface for an analog output channel
    """

    @AnalogIOChannelInterface.value.setter
    @abstractmethod
    def value(self, value: float):
        """
        Sets the value of this channel to `value`
        """
        raise NotImplementedError()


class DigitalIOChannelInterface(IOChannelInterface):
    """
    Interface for a digital I/O channel
    """

    _state: State

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._state = State.OFF

    @property
    def state(self) -> State:
        """
        Returns the state of this channel
        """
        return self._state

    @staticmethod
    def _value_to_state(io_value: Union[bool, Any]) -> State:
        """
        Converts the given `io_value` to a `State` if the value is convertible (i.e. if it's a `bool`), raises
        `ValueError` otherwise

        Parameters
        ----------
        io_value: Union[bool, Any]
            The value to convert

        Returns
        -------
        State: The `io_value` converted to a `State`

        Raises
        ------
        ValueError: if the `io_value` is not convertible to a `State`
        """
        if not isinstance(io_value, bool):
            raise ValueError(f"Cannot convert value {io_value} ({io_value!r}) to State")
        return State.ON if io_value else State.OFF

    @staticmethod
    def _state_to_bool(state: State) -> bool:
        """
        Converts the given `state` to a `bool`

        Parameters
        ----------
        state: State
            The state to convert

        Returns
        -------
        bool: The `state` converted to a `bool`
        """
        return state == State.ON


class DigitalInChannelInterface(DigitalIOChannelInterface):
    """
    Interface for a digital input channel
    """

    pass


class DigitalOutChannelInterface(DigitalIOChannelInterface):
    """
    Interface for a digital output channel
    """

    @DigitalIOChannelInterface.state.setter
    @abstractmethod
    def state(self, state: State):
        """
        Sets the state of this channel to `state`
        """
        raise NotImplementedError()
