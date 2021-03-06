# Generated by sila2.code_generator; sila2.__version__: 0.8.0
from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import TYPE_CHECKING, List, Optional, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property
from sila2.server import FeatureImplementationBase, MetadataDict

from .digitaloutchannelcontroller_types import SetOutput_Responses, State

if TYPE_CHECKING:
    from sila2.server import SilaServer


class DigitalOutChannelControllerBase(FeatureImplementationBase, ABC):

    _State_producer_queue: Queue[State]

    def __init__(self, parent_server: SilaServer):
        """
        Allows to control one digital output channel of an I/O module
        """
        super().__init__(parent_server=parent_server)

        self._State_producer_queue = Queue()

    @abstractmethod
    def get_NumberOfChannels(self, *, metadata: MetadataDict) -> int:
        """
        The number of digital output channels.

        :param metadata: The SiLA Client Metadata attached to the call
        :return: The number of digital output channels.
        """
        pass

    def update_State(self, State: State, queue: Optional[Queue[State]] = None):
        """
        The state of the channel.

        This method updates the observable property 'State'.
        """
        if queue is None:
            queue = self._State_producer_queue
        queue.put(State)

    def State_on_subscription(self, *, metadata: MetadataDict) -> Optional[Queue[State]]:
        """
        The state of the channel.

        This method is called when a client subscribes to the observable property 'State'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    @abstractmethod
    def SetOutput(self, State: State, *, metadata: MetadataDict) -> SetOutput_Responses:
        """
        Switch a digital output channel on or off.


        :param State: The state to set.

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def get_calls_affected_by_ChannelIndex(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        """
        Returns the fully qualified identifiers of all features, commands and properties affected by the
        SiLA Client Metadata 'Delay'.

        **Description of 'ChannelIndex'**:
        The index of the channel that should be used. This value is 0-indexed, i.e. the first channel has index 0, the second one index 1 and so on.

        :return: Fully qualified identifiers of all features, commands and properties affected by the
            SiLA Client Metadata 'Delay'.
        """
        pass
