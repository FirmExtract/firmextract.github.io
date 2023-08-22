# Introduction
Recently I bought lots of IP Cameras to do vulnerability research. And to find some vulnerabilities, I need to acquire Firmware of it. 
So this post will be focused on how I acquire IP Camera firmware and get into a root shell of device.
The way I extract firmware isn't complex and also not that unique. But if you are new to firmware extraction, I recommend to check this out.

# Extraction
## IP Camera Teardown
First of all, I need to teardown ip camera and see the board of it.
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image1.jpg" width=50%><br>
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image2.jpg" width=50%><br>
So this is the ip camera I'm going to work on.
By unscrewing the 3 screws on the backside, I could disassemble it.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image3.jpg" width=50%><br>
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image4.jpg" width=50%><br>
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image5.jpg" width=50%><br>
The flash memory which is the most important part for extracting firmware is on the frontside of camera.

## Read Flash Memory
Because flash memory is non-volatile memory, it has datas to run the device. So I had to read flash memory to acquire firmware.

Flash memory uses the spi protocol to read and write memory. So I used `raspberry pi` to read it by using spi pins on the pi.
I used hook clamp to grab flash pins to connect flash and pi.
And use `flashrom` utility to read the flash.
`flashrom` supports read/write of many flash chips.

There are several steps I do when I try to read the flash using pi.

1. I try to read the flash **Onboard** which usually fails. There are many reasons why this doesn't work. And the problem is mainly in the structure of the board. 


2. If **Onboard** approach fails then I **detach** flash memory and try to read it. Now there is nothing to interrupt the signals between flash and pi. I usually use heat gun to detach flash on the board. 

<br><img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image6.jpg" width=50%><br>

After grabbing detached flash pins with hook clamp connected with pi, I used `flashrom` to read it.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image8.jpg" width=100%><br>
The name of the flash is "KH25L6433F". But as you can see `flashrom` detected it as "MX25L64". Maybe KH flash has same structure with MX flash and just using their own name. There's no exact name "MX25L6433F" on the matching flashes.
But let's just give it a try. I will go with `"MX25L6436E/MX25L6445E/MX25L6465E/MX25L6473E/MX25L6473F"`

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image9.jpg" width=100%><br>
Great! Successfully read flash.

If `binwalk` doesn't support the flash that you are going to read, try to forcefully select other chip which is similar with that flash.
Or you can just add your flash to support it at binwalk source code and build it. I recommend this method as it is quite easy but powerful.
But if these two all failed, just implement the command for reading flash.
You can check [this](https://firmextract.com/post.php?id=rpi_spinand) post how to implement reading command.

## Firmware Analysis
As I said, the reason why I'm extracting firmware is to analyse firmware. So I need the application which operates this device. And the application is stored in a file system.

So what I need is to extract the file system in the firmware. To extract file system, I used `binwalk`.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image10.jpg" width=100%><br>
`binwalk` searches signatures in the firmware and shows what is found in the firmware. (e.g. kernel, bootloader, file system).
I found squash filesystem and jffs2 filesystem in the firmware. 
By using `-e` option, I extracted these file systems.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image11.jpg" width=100%><br>
Nice. The file systems are extracted.

# Getting a root shell
## Running telnetd
First we have to add telnetd command in rcS file. rcS is a script file which runs at linux init process. rcS file is located at `/etc/init.d/rcS`.

<br><img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image12.jpg" width=50%><br>
When I read the rcS file there was telnetd command already, but commented out.
So let's uncomment this and move on to the `/etc/shadow` file.

## Remove root password

```root:$1$[REDACTED]:10933:0:99999:7:::```

A root password is set. I could use `john the ripper` to get plain password with rainbow table or brute force attack, but not that much needed.
Because I can just remove password by leaving blank at the password hash field.

```root::10933:0:99999:7:::```

By removing root password, now I can connect telnet as root user without password.

## Rebuild Our File system
I changed all the things that I needed. So now it's time to rebuild the file system!

The file system that I edited is squash file system. So using `mksquashfs`, I will rebuild our file system.

<br><img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image13.jpg" width=100%><br>

The important thing here is options.
We should set the option of compression type. Or it will be compressed as gzip which is a default setting.
And I also set the option of block size. It's not a must, but I did it for stability.

Now we have to overwrite our rebuilt file system to the firmware.
I used hxd program to overwrite it.
<br><img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image14.jpg" width=100%><br>

## Writing to flash
To write the edited firmware, I'm going to use `flashrom` again.

<br><img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image15.jpg" width=100%><br>

## Soldering
The hardest and most careful part in this tasks. Carefully soldered the legs of the flash on the board.

<br><img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image16.jpg" width=50%><br>

And it's nicely done.

## Connect with ip camera

I connected ip camera to my router.
The network setting is ready. So now, let's try telnet!

<br><img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/IP%20Camera%20Firmware%20Extration/image/image17.jpg" width=60%><br>

I got a root shell. Mission Complete!

Although it's just a beginning of a long journey to find the vulnerability, by performing hardware hacking, I successfully extracted firmware and got root shell!

As always it was fun to play with hardware. Hope to see you at next post!