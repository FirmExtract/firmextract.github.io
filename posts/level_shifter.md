# Introduction
I bought a router and it was using flash which is operating in 1.8V. Well, I don't have any programmer which supports 1.8V.
So I bought it. The Level shifter. A programmer is too expensive.
Level shifter was working perfectly and I was able to read the flash. Check this out.

# Background
<hr>

## Flash
The flash was ESMT `F50D1G4L8`. It is SPI NAND Flash and working at 1.8V.
Unfortunately the package is WSON-8. So there's no way to connect to the chip legs but to solder it. We will see this later.
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Reading%201.8V%20flash%20with%20Raspberry%20Pi/image/image1.jpg" width="100%"><br><br>

## Logic Level shifter
I bought a 8 Channel Level shifter(TXS0108E) which is made at Sparkfun.
It has Supply Voltage Range as below. And it should be always `VB` >= `VA` when use.


* `VA` : **1.4V** to **3.6V**<br>
* `VB` : **1.65V** to **5.5V**

So if we send signal with 3.3V in `B1`, the signal will be sent with 1.8 in `A1`. This is what Level shifter does.

A Raspberry pi use 3.3V on GPIO. So I will connect 3.3V at `VB` and connect 1.8V at `VA`. And also we should connect `VA` with `OE` to use this level shifter.
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Reading%201.8V%20flash%20with%20Raspberry%20Pi/image/image2.jpg" width="100%"><br><br>

# Extraction
<hr>

## Connecting wires
I soldered Enamel coated wires with Flash and also with Pin header which is connected with level shifter.
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Reading%201.8V%20flash%20with%20Raspberry%20Pi/image/image3.jpg" width="100%"><br>

I finished solder all the pins without #WP and #HOLD pin.
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Reading%201.8V%20flash%20with%20Raspberry%20Pi/image/image4.jpg" width="100%"><br><br>

But Raspberry pi doesn't have **1.8V** power source. So I had to connect **1.8V** power source on the device that the flash was attached.

Also when giving voltage with two different sources, we have to connect the ground of the two device. So I connected **router** and **Raspberry pi**'s ground together. 
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Reading%201.8V%20flash%20with%20Raspberry%20Pi/image/image5.jpg" width="100%"><br><br>

And lastly I connected Raspberry pi's SPI interface pins with Level shifter.
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Reading%201.8V%20flash%20with%20Raspberry%20Pi/image/image6.jpg" width="100%"><br><br>

## Read Flash Memory
After all the connections, I read the flash memory using `spidev` module in python. I couldn't use `flashrom` as it doesn't support this chip(`F50D1G4L8`).

This chip reads data per page using `13h` opcode. Then the datas are saved in the cache. The instruction sends as below.

* Command (**13h**) + 8bits dummy + 16bits addresss
  
So we have to read the cache using `03h` opcode to actually read the datas. The instruction sends as below.

* Command (**03h**) + 4bits dummy + 12bits address + 8bits dummy

But we can leave the address zero after command(**03h**). Because we don't need to set the address of the cache. But what we have to change everytime is the page address above(**13h**).

I implemented the operation I told above with python code.
```
import spidev

spi = spidev.SpiDev()

spi.open(0,0)
spi.mode = 0
spi.max_speed_hz = 20000000
ROWSIZE = 0x10000

def flash_read(f):
    for i in range(0, ROWSIZE):
        spi.xfer2([0x13] + [0x00, i >> 8, i & 0xff]) # PAGE READ 

        data = spi.xfer2([0x03] + [0x00] * 2115) # Read From Cache
        data = data[4:] # Truncating first 4 bytes
        f.write(bytes(data))
        print(hex(i))

f = open("output.bin", "xb")

flash_read(f)

f.close()
```

The page size is 2KB + 64. And it has 0x10000 pages. So this will read all the pages.
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Reading%201.8V%20flash%20with%20Raspberry%20Pi/image/image7.jpg" width="100%"><br>

And the datas are extracted successfully.
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Reading%201.8V%20flash%20with%20Raspberry%20Pi/image/image8.jpg" width="100%"><br><br>
