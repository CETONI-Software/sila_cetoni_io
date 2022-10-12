# Generated by sila2.code_generator; sila2.__version__: 0.8.0
from __future__ import annotations

import logging
import time
from concurrent.futures import Executor
from queue import Queue
from threading import Event
from typing import Any, Dict, List, Optional, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Metadata, Property
from sila2.server import MetadataDict, SilaServer
from sila_cetoni.application.system import ApplicationSystem

from sila_cetoni.io.device_drivers import DigitalOutChannelInterface

from ..generated.digitaloutchannelcontroller import (
    DigitalOutChannelControllerBase,
    DigitalOutChannelControllerFeature,
    InvalidChannelIndex,
    SetOutput_Responses,
    State,
)

logger = logging.getLogger(__name__)


class DigitalOutChannelControllerImpl(DigitalOutChannelControllerBase):
    __system: ApplicationSystem
    __channels: List[DigitalOutChannelInterface]
    __channel_index_metadata: Metadata
    __state_queues: List[Queue[State]]  # same number of items and order as `__channels`
    __stop_event: Event

    def __init__(self, server: SilaServer, channels: List[DigitalOutChannelInterface], executor: Executor):
        super().__init__(server)
        self.__system = ApplicationSystem()
        self.__channels = channels
        self.__channel_index_metadata = DigitalOutChannelControllerFeature["ChannelIndex"]
        self.__stop_event = Event()

        self.__state_queues = []
        for i in range(len(self.__channels)):
            self.__state_queues += [Queue()]

            # initial value
            self.update_State(self.__channels[i].state, queue=self.__state_queues[i])

            executor.submit(self.__make_state_updater(i), self.__stop_event)

    def __make_state_updater(self, i: int):
        def update_state(stop_event: Event):
            new_state = state = self.__channels[i].state
            while not stop_event.wait(0.1):
                if self.__system.state.is_operational():
                    new_state = self.__channels[i].state
                if new_state != state:
                    state = new_state
                    self.update_State(state, queue=self.__state_queues[i])

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

    def SetOutput(self, State: State, *, metadata: MetadataDict) -> SetOutput_Responses:
        channel_index: int = metadata[self.__channel_index_metadata]
        logger.debug(f"channel id: {channel_index}")
        try:
            self.__channels[channel_index].state = State
        except IndexError:
            raise InvalidChannelIndex(
                message=f"The sent channel index {channel_index} is invalid. The index must be between 0 and {len(self.__channels) - 1}.",
            )

    def get_calls_affected_by_ChannelIndex(
        self,
    ) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        return [
            DigitalOutChannelControllerFeature["State"],
            DigitalOutChannelControllerFeature["SetOutput"],
        ]

    def stop(self) -> None:
        super().stop()
        self.__stop_event.set()
