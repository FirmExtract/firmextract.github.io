## introduction

Many devices have a serial interface for debugging.

I checked that the device firmware can be extracted through these interfaces and extracted it myself.

## Disassembly and analysis

The device to extract the firmware from is GPON ONT(Optical Network Terminal).

First, I looked inside the device.

Opened the device and examined the chips on the board.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/screw.jpg" width="100%">

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/board.jpg" width="100%">


In red is the Realtek RTL9607 router SoC and heatsink.

In green is the SPI flash.

In blue is the optical transceiver.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/DSC_2078_00001.jpg" width="100%">

[Winbond W25N01GV 1Gbit SPI Nand Flash](https://datasheetspdf.com/pdf-file/1320728/Winbond/W25N01GV/1)

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/w25n01.jpg" width="100%">


A spi nand flash that is not supported by flashrom is used, so the firmware will be extracted using U-boot.

## Finding the serial port

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/DSC_2096_00001.jpg" width="100%">

There are two serial ports, but only one has a header.

The device is working at 3.3V.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/uart.jpg" width="100%">

I have connected three pins gnd, rx, tx to usb uart and opened putty with 115200bps setting.

```sh
U-Boot 2011.12.NA-svn43 (Dec 09 2020 - 11:02:12)

Board:RTL9607C, CPU:900MHz, LX:200MHz, MEM:525MHz, SPIF:100MHz, Type:DDR2
SPI-NAND Flash: EFAA21/Mode0 1x128MB
Create bbt:
Loading 16384B env. variables from offset 0xc0000
Loading 16384B env. variables from offset 0xe0000
Loaded 16384B env. variables from offset 0xe0000
Net:   LUNA GMAC
Warning: eth device name has a space!
```

You can see that the U-Boot bootloader is used.

After entering the os, a log was output to the console, but no input was provided.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/syslog.jpg" width="100%">

## U-Boot console

I accessed the console by pressing a key while U-Boot was counting down to autoboot.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/bootdelay.jpg" width="100%">

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/bootshell.jpg" width="100%">

I typed help to check the available commands.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/cmdlist.jpg" width="100%">

Here are the commands we will use to dump the firmware image:

```sh
printenv        - print environment variables
spi_nand        - SPI-NAND sub-system
md              - memory display
```

## extracting filesystem and kernel image

I checked the memory structure by printing the U-boot environment variable.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/printenv1.jpg" width="100%">

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/printenv2.jpg" width="100%">

```sh
0x00000000, 0x000c0000 (fl_boot)
0x000c0000, 0x000e0000 (fl_env)
0x000e0000, 0x00100000 (fl_env2)
0x00100000, 0x00b80000 (fl_cfgfs)
0x00b80000, 0x01080000 (fl_kernel1)
0x01080000, 0x02480000 (fl_rootfs1)
0x02480000, 0x02980000 (fl_kernel2)
0x02980000, 0x03d80000 (fl_rootfs2)

0x83000000             (freeAddr)
0x83c40000             (tftp_base)
```

I copied the data of the flash to RAM with the spi_nand command, and printing the copied data with the md command.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/spinand.jpg" width="100%">

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/mdb.jpg" width="100%">

I converted the text output from the md command into a firmware image using [uboot-mdb-dump](https://github.com/gmbnomis/uboot-mdb-dump).

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/mdb2img.jpg" width="100%">

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Extracting%20firmware%20with%20a%20serial%20port/unsquash.jpg" width="100%">

## Conclusion

In this case, I don't have OS level access. So I dumped the firmware using the bootloader console.

Next time I will find a way to enable linux console in bootloader.
