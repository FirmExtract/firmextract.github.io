# introduction

There was a spi nand flash in the device I used in the last article, but I couldn't find a program that can read and write spi nand flash, so I'm trying to make it.

## Connect Flash to Raspberry Pi

I removed the spi nand flash from the device in the [previous article]().

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Trying%20to%20read%20spi%20nand%20flash%20with%20raspberry%20pi/chipoff.jpg?raw=true" width="100%">

I soldered the flash to the dip package conversion board and connected it to the raspberry pi.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Trying%20to%20read%20spi%20nand%20flash%20with%20raspberry%20pi/dip.jpg?raw=true" width="100%">

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Trying%20to%20read%20spi%20nand%20flash%20with%20raspberry%20pi/spi_pin.jpg?raw=true" width="100%">

The pinout is the same as the spi nor flash, so I connected it the same way.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Trying%20to%20read%20spi%20nand%20flash%20with%20raspberry%20pi/pi.jpg?raw=true" width="100%">

I decided to read the data using python and spidev library.

First, I enabled the spi interface in raspi-config.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Trying%20to%20read%20spi%20nand%20flash%20with%20raspberry%20pi/rpiconfig.jpg?raw=true" width="100%">

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Trying%20to%20read%20spi%20nand%20flash%20with%20raspberry%20pi/rpiconfig_spi.jpg?raw=true" width="100%">

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Trying%20to%20read%20spi%20nand%20flash%20with%20raspberry%20pi/rpiconfig_spien.jpg?raw=true" width="100%">

And read the id of the chip to see if the flash is working properly.

I looked in the datasheet and the instruction to read the id is 0x9f.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Trying%20to%20read%20spi%20nand%20flash%20with%20raspberry%20pi/read_id.jpg?raw=true" width="100%">

I wrote and tested a code that transmits 0x9f and receives data.

```py
import spidev

spi = spidev.SpiDev()

spi.open(0,0)
spi.mode = 0
spi.max_speed_hz = 1000000

data = spi.xfer2([0x9F] + [0x00]*4)
print([hex(x) for x in data[2:]])
```

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Trying%20to%20read%20spi%20nand%20flash%20with%20raspberry%20pi/spi
_id.jpg?raw=true" width="100%">

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Trying%20to%20read%20spi%20nand%20flash%20with%20raspberry%20pi/id.jpg?raw=true" width="100%">

The values were output according to the datasheet.

## read flash

I wrote and tested the code that sends the read_data instruction and receives data.

```py
import spidev

spi = spidev.SpiDev()

spi.open(0,0)
spi.max_speed_hz = 1000000

data = spi.xfer3([0x03, 0x00] + [0x00] * 2112)

with open("test.bin", "wb") as f:
    f.write(bytes(data))
```

When I check the data, it seems that the memory contents are printed out well.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Trying%20to%20read%20spi%20nand%20flash%20with%20raspberry%20pi/dump_result.jpg?raw=true" width="100%">

But it doesn't seem to dump properly after 1070 bytes.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Trying%20to%20read%20spi%20nand%20flash%20with%20raspberry%20pi/0xff.jpg?raw=true" width="100%">

## Conclusion

Next time, I'll check what the problem is and dump the entire memory.

I will also look into the spi nand flash driver in the kernel.

