Bitstream Format
=================

Structure
----------

GateMate bitstreams consist of command blocks. There is no specific header to distinguish them from other files, but each one starts with the CMD_PATH command to set the first die on the chip.

.. list-table::
   :widths: 20 20 10 35 15
   :header-rows: 1

   * - Command
     - Length
     - CRC1
     - Data
     - CRC2
   * - 1 byte
     - 1 or 2 bytes
     - 2 bytes
     - n bytes
     - 2 bytes


Each command byte is followed by data length, and that is one byte, except in the case of the CMD_FRAM command where we used two bytes in little endian format.
CRC following it, contains current (header only) CRC and is written in big endian format.  CRC is calculated with the so-called CRC-16/ISO-HDLC or CRC-16/X-25 algorithm ( poly  0x1021, init 0xffff, xored output 0xffff). Number of data bytes following is defined in the header. Second CRC contains complete CRC for all previous bytes delivered in block (including header). Some commands require additional bytes after CRC and those are fixed valued, in some cases they are just NOP bytes (0x00), and some require “execute command byte” (0x33) surrounded by multiple NOPs.


Command list
------------------

.. list-table::
   :widths: 25 5 7 63
   :header-rows: 1

   * - Command
     - Hex
     - Len Size
     - Description
   * - **CMD_PLL**
     - C1
     - 1
     - PLL configuration
   * - **CMD_CFGMODE**
     - C2
     - 1
     - Change configuration mode
   * - **CMD_CFGRST**
     - C3
     - 1
     - Reset all configuration latches
   * - **CMD_FLASH**
     - C5
     - 1
     - SPI flash access
   * - **CMD_DLXP**
     - C6
     - 1
     - Latch configuration X pattern
   * - **CMD_DLYP**
     - C7
     - 1
     - Latch configuration Y pattern
   * - **CMD_LXLYS**
     - C8
     - 1
     - Latch configuration X,Y location
   * - **CMD_ACLCU**
     - C9
     - 1
     - Address counter
   * - **CMD_DLCU**
     - CA
     - 1
     - Configuration data
   * - **CMD_DRXP**
     - CC
     - 1
     - RAM configuration X pattern
   * - **CMD_RXRYS**
     - CE
     - 1
     - RAM configuration X,Y location
   * - **CMD_FRAM**
     - D2
     - 2
     - Block ram fill data
   * - **CMD_SERDES**
     - D7
     - 1
     - Serdes configuration
   * - **CMD_D2D**
     - D8
     - 1
     - Enable/disable die-to-die direction
   * - **CMD_PATH**
     - D9
     - 1
     - Enable forwarding configuration to die
   * - **CMD_JUMP**
     - DA
     - 1
     - Jump to address in configuration
   * - **CMD_CHG_STATUS**
     - DB
     - 1
     - FPGA configuration change
   * - **CMD_WAIT_PLL**
     - DC
     - 1
     - Wait for PLL lock
   * - **CMD_SPLL**
     - DD
     - 1
     - Select PLLs
   * - **CMD_SLAVE_MODE**
     - DE
     - 1
     - Set SPI slave mode
