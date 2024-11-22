Bitstream Commands
===================

CMD_PATH
---------
To be able to specify die to program it is required to properly forward JTAG to specific
direction and set mode accordingly. To program first die we use 0x10 value for this command
and it first one to be executed.

.. list-table::
   :widths: 10 40
   :header-rows: 1

   * - Bit
     - Description
   * - 0
     - Reset to default state
   * - 1
     - Set to path to top
   * - 2
     - Set to path to right
   * - 3
     - Enable forwarding mode
   * - 4
     - Enable programming mode

.. warning::
    This command have data after payload, and it consists of 9 bytes ``0x00 0x00 0x00 0x00 0x33 0x00 0x00 0x00 0x00`` and
    it is used to execute this JTAG command.


CMD_LXLYS
----------
Before sending any configuration data it is required to specify location of a specific TILE, and for latch configuration that configures all
logic and IO blocks it is this command.

.. list-table::
   :widths: 10 10 40
   :header-rows: 1

   * - Byte
     - Range
     - Description
   * - 0
     - 0..81
     - X location (column)
   * - 1
     - 0..65
     - Y location (row)

CMD_DLXP
---------
Alternate way of setting location for configuration data is by setting pattern for both column and row.

This commands sets row pattern and each bit represent one of the rows. There are total of 9 bytes used in payload.

CMD_DLYP
---------
This commands sets column pattern and each bit represent one of the columns. There are total of 11 bytes used in payload.

CMD_DLCU
---------
After location is set with one of previous commands, it is required to set a data payload.

For configuring logic and IO tiles data payload is 112 bytes max. Payload can be smaller, but programming
will act as it is zero padded till full size.
This command is also used to configure RAM blocks, there we expect 27 bytes of payload maximum. 

CMD_RXRYS
----------
Similar to **CMD_LXLYS** command, there is a command to specify RAM block to program.

.. list-table::
   :widths: 10 10 40
   :header-rows: 1

   * - Byte
     - Range
     - Description
   * - 0
     - 0..3
     - X location (column)
   * - 1
     - 0..7
     - Y location (row)

CMD_DRXP
---------
As alternative to **CMD_RXRYS** command we can use this one to specify a pattern, note that
each bit of one byte payload is used to set one of 4 columns.

CMD_CFGRST
-----------
Resets all configuration latches to value of a byte from payload.

CMD_PLL
--------

CMD_CFGMODE
------------

CMD_FLASH
----------

CMD_ACLCU
----------

CMD_FRAM
---------

CMD_SERDES
-----------

CMD_D2D
--------

CMD_JUMP
--------

CMD_CHG_STATUS
---------------

CMD_WAIT_PLL
-------------

CMD_SPLL
---------

CMD_SLAVE_MODE
---------------
