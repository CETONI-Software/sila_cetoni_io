"""
A device driver implementation for the I/O channel modules of a Revolution Pi

:author: Florian Meinicke (florian.meinicke@cetoni.de)
:date: 11.10.2022
"""

from __future__ import annotations

import logging
from typing import List, Optional

import revpimodio2 as rp2
from revpimodio2 import device as rp2_device
from revpimodio2 import io as rp2_io
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


class _RevPiIoChannelBase:
    """
    Base class for I/O channel device driver implementations for Revolution Pi modules
    """

    __instances: List[Self] = []

    _rev_pi: rp2.RevPiModIO = None
    _io_modules: List[rp2_device.DioModule] = []
    _inputs: List[rp2_io.IOBase] = []
    _outputs: List[rp2_io.IOBase] = []

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        logger.debug(f"Adding {instance} to {cls} instance list")
        cls.__instances += [instance]
        return instance

    def __init__(self) -> None:
        self._init_statics()

    @classmethod
    def _init_statics(cls):
        logger.debug(f"_init_statics for {cls}")
        if cls._rev_pi is None:
            logger.debug(f"rev_pi is still None, creating new one")
            cls._rev_pi = rp2.RevPiModIO(autorefresh=True, shared_procimg=True)
            # cls._rev_pi.cycletime = 40  # the default 20 ms cannot be held
            cls._rev_pi.mainloop(blocking=False)

            product_type = (
                (rp2.ProductType.DIO, rp2.ProductType.DI, rp2.ProductType.DO)
                if cls in (RevPiDigitalInChannel, RevPiDigitalOutChannel)
                else (rp2.ProductType.AIO, )
                if cls in (RevPiAnalogInChannel, RevPiAnalogOutChannel)
                else None
            )
            logger.debug(f"product type {product_type}")
            if product_type is None:
                logger.error(
                    f"{cls} is not one of the expected RevPi[Analog|Digital][In|Out]Channel, cannot determine product "
                    "type of I/O module to look for"
                )

            cls._io_modules = list(filter(lambda d: d.producttype in product_type, cls._rev_pi.device))
            for dev in cls._io_modules:
                exported_inputs = list(filter(lambda i: i.export, dev.get_inputs()))
                cls._inputs = [input for input in exported_inputs]
                exported_outputs = list(filter(lambda i: i.export, dev.get_outputs()))
                cls._outputs = [output for output in exported_outputs]

    @classmethod
    def _exit(cls, self: Optional[Self] = None):
        if self is not None:
            cls.__instances.remove(self)
            logger.debug(f"Removing {self} from {cls} instance list, remaining {cls.__instances}")
        if not cls.__instances:
            logger.debug("all instances destroyed -> exiting revpimodio main loop")
            cls._rev_pi.exit()

    @staticmethod
    def _index_for_name(io_list: List[rp2_io.IOBase], io_name: str) -> int:
        """
        Searches for the I/O channel with the given `io_name` in the `io_list` and returns the index of the channel with
        that name if found. Raises `ValueError` if there is no channel with the given `io_name`

        Parameters
        ----------
        io_list: List[rp2_io.IOBase]
            List of I/O channels to search
        io_name: str
            The name of the I/O channel to search for

        Returns
        -------
        int: The index of the I/O channel with the given `io_name` in the `io_list`

        Raises
        ------
        ValueError: if there is no channel in `io_list` with the desired `io_name`
        """
        for index, io in enumerate(io_list):
            if io.name == io_name:
                return index
        raise ValueError(f"No channel named {io_name} found")


class RevPiDigitalInChannel(DigitalInChannelInterface, _RevPiIoChannelBase):
    """
    Device driver implementation for Revolution Pi digital input channel modules
    """

    __input: rp2_io.IOBase

    def __init__(self, index: int) -> None:
        self.__input = self._inputs[index]

        super().__init__(self.__input.name)

        self._state = self._value_to_state(self.__input.value)
        self.__input.reg_event(self.__update_channel)

    @classmethod
    def number_of_channels(cls) -> int:
        cls._init_statics()
        num = len(cls._inputs)
        cls._exit()
        return num

    @classmethod
    def channel_at_index(cls, index: int) -> Self:
        cls._init_statics()
        channel = cls(index)
        cls._exit()
        return channel

    def __update_channel(self, io_name: str, io_value: bool):
        """
        Callback function that is called by `revpimodio` every time the value of a channel changes
        """
        self._state = self._value_to_state(io_value)

    def start(self):
        # This device does not need to be started
        pass

    def stop(self):
        self._exit(self)


class RevPiDigitalOutChannel(DigitalOutChannelInterface, _RevPiIoChannelBase):
    """
    Device driver implementation for Revolution Pi digital output channel modules
    """

    __output: rp2_io.IOBase

    def __init__(self, index: int) -> None:
        self.__output = self._outputs[index]

        super().__init__(self.__output.name)

        self._state = self._value_to_state(self.__output.value)
        self.__output.reg_event(self.__update_channel)

    @classmethod
    def number_of_channels(cls) -> int:
        cls._init_statics()
        num = len(cls._outputs)
        cls._exit()
        return num

    @classmethod
    def channel_at_index(cls, index: int) -> Self:
        cls._init_statics()
        channel = cls(index)
        cls._exit()
        return channel

    def __update_channel(self, io_name: str, io_value: bool):
        """
        Callback function that is called by `revpimodio` every time the value of a channel changes
        """
        self._state = self._value_to_state(io_value)

    @DigitalOutChannelInterface.state.setter
    def state(self, state: State):
        self.__output.value = self._state_to_bool(state)
        self._state = state

    def start(self):
        # This device does not need to be started
        pass

    def stop(self):
        self._exit(self)


if __name__ == "__main__":
    LOGGING_FORMAT = "%(asctime)s [%(threadName)-12.12s] %(levelname)-8s| %(name)s %(module)s.%(funcName)s: %(message)s"
    logging_level = logging.INFO
    try:
        coloredlogs.install(fmt=LOGGING_FORMAT, datefmt="%Y-%m-%d %H:%M:%S,%f", level=logging_level)
    except NameError:
        logging.basicConfig(format=LOGGING_FORMAT, level=logging_level)

    logging.info(f"Num input channels: {RevPiDigitalInChannel.number_of_channels()}")
    logging.info(f"Num output channels: {RevPiDigitalOutChannel.number_of_channels()}")

    input0 = RevPiDigitalInChannel(0)
    logging.info(f"Channel 0 state: {input0.state}")
    input13 = RevPiDigitalInChannel.channel_at_index(13)
    logging.info(f"Channel 13 state: {input13.state}")
    input0.stop()
    input13.stop()
