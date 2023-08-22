# Introduction
Actually I was trying to port doom in the monitor I have.
The model is 271E9 made by Philips. But I couldn't find datasheet about the SoC.
So I decide to just analyse their firmware and hardware. And I could find some new stuff. Let's see!

# Teardown Montior
## Getting Board
The First thing to do is see how board is made.
To do that, let's teardown it.
At the backside of the monitor, there are two screws.
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Phillips%20Monitor%20Teardown%20%26%20Analysis/images/1.jpg" width=90%><br>

After that just open the plastic backplate.
Then there is a board. And it's covered.
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Phillips%20Monitor%20Teardown%20%26%20Analysis/images/2.jpg" width=90%><br>

Peel off the stickers and unscrew the VGA port.
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Phillips%20Monitor%20Teardown%20%26%20Analysis/images/3.jpg" width=90%><br>

Finally let's free the board!
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Phillips%20Monitor%20Teardown%20%26%20Analysis/images/4.jpg" width=90%><br>

Sweet. We can check the SoC and many other chips.
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Phillips%20Monitor%20Teardown%20%26%20Analysis/images/5.jpg" width=100%><br>

Soc is TSUMO88CDT9-1 and flash is BoyaMicro 25D40CSTIG.

# Monitor Analysis
## Firmware Extraction
I tried to grab the flash by clip but it didn't work.
So I detached it and grab it by soic 8 pin clip.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Phillips%20Monitor%20Teardown%20%26%20Analysis/images/6.jpg" width=90%><br>

The reason why I didn't use raspberry pi is because flashrom doesn't support the BM25D40 Flash.
But the programmer I had `TL866-II` Plus supports it. So I used it.

However the data changed everytime I tried to read it.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Phillips%20Monitor%20Teardown%20%26%20Analysis/images/7.jpg" width=90%><br>

I checked several times if the pins are connected correctly and it was all good!

I tried other thing like reading as many as I can and sort the datas by frequency. But yes. this is useless. Because we can't verify if it is real data.

And something just popped up in my mind.
I have SOIC 8 pin socket. Why don't we use it?

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Phillips%20Monitor%20Teardown%20%26%20Analysis/images/8.jpg" width=70%><br>

After using this, the data extracted so well. I mean we got the real data!
I still don't get it what was the problem. But anyways we got the firmware.

## Firmware Analysis
First I binwalked the firmware.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Phillips%20Monitor%20Teardown%20%26%20Analysis/images/9.jpg" width=90%><br>
But nothing shows up. But when we use Y option in binwalk to check the architecture,

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Phillips%20Monitor%20Teardown%20%26%20Analysis/images/10.jpg" width=90%><br>
binwalk says that they are using arm. 

So I used IDA to check if this baremetal firmware is made of ARM.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Phillips%20Monitor%20Teardown%20%26%20Analysis/images/11.jpg" width=90%><br>
And yes it's ARM.

But I couldn't go any further from here.
Because we don't have SoC datasheet and no debugging ports.
Then how can I know their memory layout and interrupts address!

So I stopped analysing arm codes in the firmware. But started to just look around a firmware.

And when we see the strings in here :

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Phillips%20Monitor%20Teardown%20%26%20Analysis/images/12.jpg" width=90%><br>

some command-looking strings are located. What is this?

## VCP

It's VCP codes. Virtual Control Panel(VCP) represents the functions that monitor supports. It's a single command entity in the `MCCS` language.

The first `02` code in vcp means :

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Phillips%20Monitor%20Teardown%20%26%20Analysis/images/13.jpg" width=90%><br>

So following hex codes are also like this. Meaning something individually.
Also by using [utility](https://github.com/rockowitz/ddcutil) which controls VCP, we can manually change our monitor settings.

You can check what the code up there means by reading [this document](https://milek7.pl/ddcbacklight/mccs.pdf)

# Conclusion
This project was started to play DOOM in monitor. But because of the lack of datasheet, I couldn't done it. Maybe next time!

Anyways It was fun playing around with monitor firmware.
Wish me luck resoldering the flash chip and reassemble my monitor.

And also this time I will provide the firmware that I'v extracted which we usually don't.
You can download it in [our github repo](https://github.com/FirmExtract/FirmExtract-Posts/tree/main/Phillips%20Monitor%20Teardown%20%26%20Analysis)
We are very welcome if you share your cool work with this firmware. Our Twitter and Facebook is always opened.