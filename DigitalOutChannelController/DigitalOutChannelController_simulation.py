"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Digital Out Channel Controller*

:details: DigitalOutChannelController:
    Allows to control one digital output channel of an I/O module

:file:    DigitalOutChannelController_simulation.py
:authors: Florian Meinicke

:date: (creation)          2020-12-08T14:25:47.309795
:date: (last modification) 2021-07-08T12:11:17.603614

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
from .gRPC import DigitalOutChannelController_pb2 as DigitalOutChannelController_pb2
# from .gRPC import DigitalOutChannelController_pb2_grpc as DigitalOutChannelController_pb2_grpc

# import default arguments
from .DigitalOutChannelController_default_arguments import default_dict

# noinspection PyPep8Naming,PyUnusedLocal
class DigitalOutChannelControllerSimulation:
    """
    Implementation of the *Digital Out Channel Controller* in *Simulation* mode
        The SiLA 2 driver for Qmix I/O Devices
    """

    def __init__(self):
        """Class initialiser"""

        logging.debug('Started server in mode: {mode}'.format(mode='Simulation'))

    def SetOutput(self, request, context: grpc.ServicerContext) \
            -> DigitalOutChannelController_pb2.SetOutput_Responses:
        """
        Executes the unobservable command "Set Output"
            Switch a digital output channel on or off.

        :param request: gRPC request containing the parameters passed:
            request.State (State): The state to set.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        # initialise the return value
        return_value = None

        # TODO:
        #   Add implementation of Simulation for command SetOutput here and write the resulting response
        #   in return_value

        # fallback to default
        if return_value is None:
            return_value = DigitalOutChannelController_pb2.SetOutput_Responses(
                #**default_dict['SetOutput_Responses']
                EmptyResponse=silaFW_pb2.Void(value=b'')
            )

        return return_value


    def Get_NumberOfChannels(self, request, context: grpc.ServicerContext) \
            -> DigitalOutChannelController_pb2.Get_NumberOfChannels_Responses:
        """
        Requests the unobservable property Number Of Channels
            The number of digital output channels. This value is 0-indexed, i.e. the first channel has index 0, the second one index 1 and so on.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            NumberOfChannels (Number Of Channels): The number of digital output channels. This value is 0-indexed, i.e. the first channel has index 0, the second one index 1 and so on.
        """

        # initialise the return value
        return_value: DigitalOutChannelController_pb2.Get_NumberOfChannels_Responses = None

        # TODO:
        #   Add implementation of Simulation for property NumberOfChannels here and write the resulting response
        #   in return_value

        # fallback to default
        if return_value is None:
            return_value = DigitalOutChannelController_pb2.Get_NumberOfChannels_Responses(
                #**default_dict['Get_NumberOfChannels_Responses']
                NumberOfChannels=silaFW_pb2.Integer(value=1)
            )

        return return_value

    def Subscribe_State(self, request, context: grpc.ServicerContext) \
            -> DigitalOutChannelController_pb2.Subscribe_State_Responses:
        """
        Requests the observable property State
            The state of the channel.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            State (State): The state of the channel.
        """

        # initialise the return value
        return_value: DigitalOutChannelController_pb2.Subscribe_State_Responses = None

        # we could use a timeout here if we wanted
        while True:
            # TODO:
            #   Add implementation of Simulation for property State here and write the resulting
            #   response in return_value

            # create the default value
            if return_value is None:
                return_value = DigitalOutChannelController_pb2.Subscribe_State_Responses(
                    #**default_dict['Subscribe_State_Responses']
                    State=pb2.DataType_State(silaFW_pb2.String(value='default string'))
                )


            yield return_value


    def Get_FCPAffectedByMetadata_ChannelIndex(self, request, context: grpc.ServicerContext) \
            -> DigitalOutChannelController_pb2.Get_FCPAffectedByMetadata_ChannelIndex_Responses:
        """
        Requests the unobservable property FCPAffectedByMetadata Channel Index
            Specifies which Features/Commands/Properties of the SiLA server are affected by the Channel Index Metadata.

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response object with the following fields:
            AffectedCalls (AffectedCalls): A string containing a list of Fully Qualified Identifiers of Features, Commands and Properties for which the SiLA Client Metadata is expected as part of the respective RPCs.
        """

        # initialise the return value
        return_value: DigitalOutChannelController_pb2.Get_FCPAffectedByMetadata_ChannelIndex_Responses = None

        # TODO:
        #   Add implementation of Simulation for property FCPAffectedByMetadata_ChannelIndex here and write the resulting response
        #   in return_value

        # fallback to default
        if return_value is None:
            return_value = DigitalOutChannelController_pb2.Get_FCPAffectedByMetadata_ChannelIndex_Responses(
                #**default_dict['Get_FCPAffectedByMetadata_ChannelIndex_Responses']

            )

        return return_value
