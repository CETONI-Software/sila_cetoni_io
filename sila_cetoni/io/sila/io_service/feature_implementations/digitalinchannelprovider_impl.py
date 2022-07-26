# Generated by sila2.code_generator; sila2.__version__: 0.8.0
from __future__ import annotations

import time
from concurrent.futures import Executor
from queue import Queue
from threading import Event
from typing import Any, Dict, List, Optional, Union

from qmixsdk.qmixdigio import DigitalInChannel
from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Metadata, Property
from sila2.server import MetadataDict, SilaServer

from sila_cetoni.application.system import ApplicationSystem

from ..generated.digitalinchannelprovider import (
    DigitalInChannelProviderBase,
    DigitalInChannelProviderFeature,
    InvalidChannelIndex,
    State,
)


class DigitalInChannelProviderImpl(DigitalInChannelProviderBase):
    __system: ApplicationSystem
    __channels: List[DigitalInChannel]
    __channel_index_metadata: FullyQualifiedIdentifier
    __state_queues: List[Queue[State]]  # same number of items and order as `__channels`
    __stop_event: Event

    def __init__(self, server: SilaServer, channels: List[DigitalInChannel], executor: Executor):
        super().__init__(server)
        self.__system = ApplicationSystem()
        self.__channels = channels
        self.__channel_index_metadata = DigitalInChannelProviderFeature["ChannelIndex"]
        self.__stop_event = Event()

        self.__state_queues = []
        for i in range(len(self.__channels)):
            self.__state_queues += [Queue()]

            # initial value
            self.update_State(
                "On" if self.__channels[i].is_on() else "Off",
                queue=self.__state_queues[i],
            )

            executor.submit(self.__make_state_updater(i), self.__stop_event)

    def __make_state_updater(self, i: int):
        def update_state(stop_event: Event):
            new_is_on = is_on = self.__channels[i].is_on()
            while not stop_event.is_set():
                if self.__system.state.is_operational():
                    new_is_on = self.__channels[i].is_on()
                if new_is_on != is_on:
                    is_on = new_is_on
                    self.update_State("On" if is_on else "Off", queue=self.__state_queues[i])
                time.sleep(0.1)

        return update_state

    def get_NumberOfChannels(self, *, metadata: MetadataDict) -> int:
        return len(self.__channels)

    def State_on_subscription(self, *, metadata: MetadataDict) -> Optional[Queue[State]]:
        channel_index: int = metadata[self.__channel_index_metadata]
        try:
            if channel_index < 0:
                raise IndexError
            return self.__state_queues[channel_index]
        except IndexError:
            raise InvalidChannelIndex(
                message=f"The sent channel index {channel_index} is invalid. The index must be between 0 and {len(self.__channels) - 1}.",
            )

    def get_calls_affected_by_ChannelIndex(
        self,
    ) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        return [DigitalInChannelProviderFeature["State"]]

    def stop(self) -> None:
        super().stop()
        self.__stop_event.set()
