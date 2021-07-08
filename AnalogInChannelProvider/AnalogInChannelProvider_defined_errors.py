"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Analog In Channel Provider_defined_errors*

:details: AnalogInChannelProvider Defined SiLA Error factories:
    Allows to control one analog input channel of an I/O module

:file:    AnalogInChannelProvider_defined_errors.py
:authors: Florian Meinicke

:date: (creation)          2021-07-08T11:41:57.958199
:date: (last modification) 2021-07-08T11:41:57.958199

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
from sila2lib.error_handling.server_err import SiLAExecutionError


class InvalidChannelIndex(SiLAExecutionError):
    """
    The sent channel index is not known.
    """

    def __init__(self, channel_id: int = None, extra_message: str = ""):
        """

        :param channel_id: The channel index that is invalid
        :param extra_message: extra message, that can be added to the default message
        """
        msg = "The sent channel index{index} is not known.{extra_message}".format(
            index=f" ({channel_id})" if channel_id else "",
            extra_message='\n'+extra_message if extra_message else ""
        )
        super().__init__(error_identifier="sila2.de.cetoni/io/AnalogInChannelProvider/v1/DefinedError/InvalidChannelIndex",
                         msg=msg)
