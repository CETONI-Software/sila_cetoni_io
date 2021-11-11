"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Digital In Channel Provider*

:details: DigitalInChannelProvider:
    Allows to control one digital input channel of an I/O module

:file:    DigitalInChannelProvider_real.py
:authors: Florian Meinicke

:date: (creation)          2020-12-08T14:25:47.300795
:date: (last modification) 2021-07-08T11:44:13.707564

.. note:: Code generated by sila2codegenerator 0.3.6

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.1.0"

# import general packages
import logging
import time         # used for observables
import uuid         # used for observables
import grpc         # used for type hinting only

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2

# import gRPC modules for this feature
from .gRPC import DigitalInChannelProvider_pb2 as DigitalInChannelProvider_pb2
# from .gRPC import DigitalInChannelProvider_pb2_grpc as DigitalInChannelProvider_pb2_grpc

# import default arguments
from .DigitalInChannelProvider_default_arguments import default_dict

from qmixsdk.qmixdigio import DigitalInChannel

from application.system import ApplicationSystem, SystemState


# noinspection PyPep8Naming,PyUnusedLocal
class DigitalInChannelProviderReal:
    """
    Implementation of the *Digital In Channel Provider* in *Real* mode
        The SiLA 2 driver for Qmix I/O Devices
    """

    def __init__(self):
        """
        Class initialiser
        """

        self.states = {True: 'On', False: 'Off'}
        self.system = ApplicationSystem()

        logging.debug('Started server in mode: {mode}'.format(mode='Real'))

    def Subscribe_State(self, request, channel: DigitalInChannel, context: grpc.ServicerContext) \
            -> DigitalInChannelProvider_pb2.Subscribe_State_Responses:
        """
        Requests the observable property State
            The state of the channel.

        :param request: An empty gRPC request object (properties have no parameters)
        :param channel: The channel to operate on
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            State (State): The state of the channel.
        """

        new_state = channel.is_on() and self.system.state.is_operational()
        state = not new_state # force sending the first value
        while not self.system.state.shutting_down():
            new_state = channel.is_on() and self.system.state.is_operational()
            if new_state != state:
                state = new_state
                yield DigitalInChannelProvider_pb2.Subscribe_State_Responses(
                    State=DigitalInChannelProvider_pb2.DataType_State(
                        State=silaFW_pb2.String(value=self.states[state])
                    )
                )
            time.sleep(0.1) # give client some time to catch up
