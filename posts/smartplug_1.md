# Introduction
I bought Smart Plug a while ago. It was because I want to save my smartphone battery.
I usually charge my phone when I go to sleep. But it damages battery becauses it charges after it is fully charged.
So I used smart plug to set the timer. And of course, it was tiresome.
**The function I want was to stop charging when my phone is fully charged.** So as a `hardware hacker`, not a `hardware developer`, I will make this smart plug can do it.

As this story is too long to put whole things in one post, we will break it up into two parts.

In this post I will show you how I extracted the firmware. 
And in the second post there will be the story of implementing the function.

# Smart Plug Teardown
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/1.jpg" width=60%>

By gaping sides, I could easily open it.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/2.jpg" width=60%>

Let's take the board out.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/3.jpg" width=60%>

And we can see that there's a ESP8285 chip. This chip would be a main SoC as there is no any other mcu chip.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/4.jpg" width=60%>

And also test points! That's sweet. Guessing why there are test points here, maybe they are used for the flash programming?

Maybe or maybe not. Anyways let's keep this in mind.

## ESP8285
ESP8285 is a ESP series chip which has WiFi features in it.
This is like the upgrade version of ESP8266. It has 1MB Flash which ESP8266 doesn't.

In programming ESP8285, it's just same as how to program ESP8266. So no need to search for the datasheet to extract the firmware as there are plenty of posts that explains how to program ESP8266.

But to skip reading detailed datasheet is one thing; to read the chip's datasheet is another.
So I briefly read the datasheet of the chip. 
[ESP8285 Datasheet URL](https://www.espressif.com/sites/default/files/documentation/0a-esp8285_datasheet_en.pdf)

# Firmware Extraction
Now let's move on to the next page. Let's extract the firmware!

First we have to make a circuit to connect with a UART to USB.
ESP8266 and also ESP8285 chips can use uart to control flash.
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/11.jpg" width=100%>

I referenced this image to connect with my uart/usb.
`CH-PD` is `EN` in our boards test point. And also there is GPIO 0 test point beside of the `EN` point.

**The reason that we have to follow the circuit above is becuase we have to change the boot mode to control the flash.**

You can read more details in [this document](https://docs.espressif.com/projects/esptool/en/latest/esp8266/advanced-topics/boot-mode-selection.html).

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/12.jpg" width=100%>

## Extraction Circuit

To make circuit, we have to connect with test points.
But how? My choice was this.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/6.jpg" width=70%>

I connected test pads with needle test probes. 

I didn't want to take a risk to solder it. And this could be the easiest way also! Because soldering the enameled magnet wire with the pad is... awful.

The whole circuite looks like this.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/5.jpg" width=80%>

And it is conntect with my CP210X UART/USB.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/7.jpg" width=80%>

## Firmware Extraction

There is a tool called [esptool](https://github.com/espressif/esptool). It helps us to read flash or write flash and even to print the info of the image.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/13.jpg" width=100%>

After connecting my USB/UART to the computer, I tried to read the flash using `esptool`.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/9.jpg" width=100%>

And this happened. The error message was `Device doesn't recognize a command`.
It was because I didn't download the FTDI driver.

FTDI driver is a VCP(Virtual COM Port) driver which makes us to use USB port as Serial port.
So we have to download FTDI driver to use USB/UART which is based on FTDI chipset.

My USB/UART was using CP210X chipset. So I thought downloading FTDI driver is not necessary. But it wasn't.

I downloaded the FTDI Driver in [this site](https://ftdichip.com/drivers/vcp-drivers/).

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/14.jpg" width=10%>

After downloading, it starts to read the firmware.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/8.jpg" width=100%>

Sweet!

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Transforming%20Smart%20Plug%20IoT%20-%201/images/10.jpg" width=100%>

And when we use the `image_info` command in esptool, it shows the entry point and segments.

So we successfully extracted firmware.

In the next post, we will reverse engineer this firmware and develop the function we want and finally reprogram it.