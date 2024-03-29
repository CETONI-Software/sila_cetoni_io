# Generated by sila2.code_generator; sila2.__version__: 0.8.0
from __future__ import annotations

import math
import time
from concurrent.futures import Executor
from queue import Queue
from threading import Event
from typing import Any, Dict, List, Optional, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Metadata, Property
from sila2.server import MetadataDict, SilaServer
from sila_cetoni.application.system import ApplicationSystem

from sila_cetoni.io.device_drivers import AnalogInChannelInterface

from ..generated.analoginchannelprovider import (
    AnalogInChannelProviderBase,
    AnalogInChannelProviderFeature,
    InvalidChannelIndex,
)


class AnalogInChannelProviderImpl(AnalogInChannelProviderBase):
    __system: ApplicationSystem
    __channels: List[AnalogInChannelInterface]
    __channel_index_metadata: Metadata
    __value_queues: List[Queue[float]]  # same number of items and order as `__channels`
    __stop_event: Event

    def __init__(self, server: SilaServer, channels: List[AnalogInChannelInterface], executor: Executor):
        super().__init__(server)
        self.__system = ApplicationSystem()
        self.__channels = channels
        self.__channel_index_metadata = AnalogInChannelProviderFeature["ChannelIndex"]
        self.__stop_event = Event()

        self.__value_queues = []
        for i in range(len(self.__channels)):
            self.__value_queues += [Queue()]

            # initial value
            self.update_Value(self.__channels[i].value, queue=self.__value_queues[i])

            executor.submit(self.__make_value_updater(i), self.__stop_event)

    def __make_value_updater(self, i: int):
        def update_value(stop_event: Event):
            new_value = value = self.__channels[i].value
            while not stop_event.wait(0.1):
                if self.__system.state.is_operational():
                    new_value = self.__channels[i].value
                if not math.isclose(new_value, value):
                    value = new_value
                    self.update_Value(value, queue=self.__value_queues[i])

        return update_value

    def get_NumberOfChannels(self, *, metadata: MetadataDict) -> int:
        return len(self.__channels)

    def Value_on_subscription(self, *, metadata: MetadataDict) -> Optional[Queue[float]]:
        channel_index: int = metadata[self.__channel_index_metadata]
        try:
            if channel_index < 0:
                raise IndexError
            return self.__value_queues[channel_index]
        except IndexError:
            raise InvalidChannelIndex(
                message=f"The sent channel index {channel_index} is invalid. The index must be between 0 and {len(self.__channels) - 1}.",
            )

    def get_calls_affected_by_ChannelIndex(
        self,
    ) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        return [AnalogInChannelProviderFeature["Value"]]

    def stop(self) -> None:
        super().stop()
        self.__stop_event.set()
