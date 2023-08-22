# Introduction
I have a eye massager which I use a lot. It warms and massages my eyes.
But the only problem of that is when it is operating, classic music is played with very terrible sound quality.
This really got me mad everytime I use it. So a while ago I just teardown the massager and disabled speaker module.
But, I thought it would be fun if I change that song. So this is what happened.

# Teardown Eye Massager

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/a.jpg?raw=true" width="80%">

The massager looks like this.   
As you just expected, to teardown this, we need to open up the cover.  
Putting some tools into the gap in the center would be the first process.

After opening up, this board showed up.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/b.jpg?raw=true" width="80%">

In the board, we can see SoC, Power charge module, Flash memory, audio power amplifier.

And there is also a battery and speaker module aside.

If we flip the board, we can see many markings.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/c.jpg?raw=true" width="80%">

(If you noticed, yes. The GND, BAT+ line for power charging is detached. But I reattached it)

# Flash read
I first tried to read the flash on the board right away.

But it didn't work well. So I just took the chip off.
<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/1.jpg?raw=true" width="50%">

Now we have to resolder this at the end. That's bothersome process but, anyways this chip off was necessary.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/2.jpg?raw=true" width="80%">

I grabbed this flash by using ic hook clip and used raspberry pi to interact.
The flash name is `T25S16` and it is not on the flashrom supported list.
So I searched for X25S16 type flash on flashrom supported list and there was `EN25S16` which is Eon's flash.  

After that, I just used below command to read it.
<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/3.png?raw=true" width="100%">

As you can see in the image, I forced to read it as EN25S16 and it has read successfully.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/4.png?raw=true" width="100%">

Looking at the firmware data, you will see that it contains `"FAT12"`.
So I guess this is FAT12 File system.

As I knew that it is FAT12 File system, I opened this firmware with dmde(DM Disk Editor and Data Recovery Software).
<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/5.png?raw=true" width="100%">

Ta-da! We got all the sounds and musics. The file names are all in chinese. So we can guess that it is made in china.
If I translate some file names, then something like these comes out.
<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/6.png?raw=true" width="100%">

What we want is to change the music which comes out when I start the massage.
You can check the original musics and sounds in our [github](https://github.com/FirmExtract/FirmExtract-Posts/tree/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/contents)

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/7.png?raw=true" width="100%">

We have 2.2Mb free space in 4Mb. So let's change the music that isn't too big.
Anywas there's two choice for us. 

- First one is **changing the music file's name in the file system to the music we will put into the firmware**.
- Second one is **just only changing the music itself with same file names**.

The second one is definitely much easier.

But let's go with the first one so that we can study `FAT12` file system in depth and also check out the assemblies that runs the musics.

## Massager operating instructions
Before we start, let's see how FAT12 works.

---
### FAT12 File system
FAT12 file system's layout is formed in 4 structure.
1. Reserved Sectors
2. FAT Region
3. Root Directory Region
4. Data Region

In the `Reserved Sector`, there is `Boot Sector`.  Boot Sector has many informations about this file. The command that I used in the above image, `fatcat -i`, shows the informations which is in the `Boot Sector`.

`FAT Region` has File Allocation Table(FAT) which is the map for the Data region. 

`Root Directory Region` has an directory table about the root directory.

`Data Region` has the actual data about files and directories.

---
So what we are going to do is analysing boot code which is in the `Boot Sector`.

If you check the first three bytes in the FAT12 File system, we can find the jmp instruction.  

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/8.png?raw=true" width="60%">

By following this jmp instruction, we reach these interrupts.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/9.png?raw=true" width="90%">

But until this interrupts, there was no intersting codes.

After analysing whole codes, I realized that the real code which operates this device is not in the flash, but in the SoC on chip memory.

So I think changing the code to play our new music file would be impossible.

But we have another option. The **second one!** - *just only changing the music itself with same file names* - It's quite easy because we definitely have musics in the flash that are played while massaging.

## Music file changing

In the `Root Directory Region`, we can check that there is a table for the files.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/10.png?raw=true" width="80%">

What we are going to do is to find the information about the music files in here and change the data which is in the `Data region` to our music.

Start from 4200, there is a information about the music folder.

Let's see the things that we have to check.
* 0x4200 is the Directory name. (So the Directory entry starts from 0x4220)
* 0x422b has File Attributes. And 0x10 for that means it is **Subdirectory**
* 0x423A has start of file in clusters. And the number for it is 0x36.

There will be file table again at 0x36 cluster. I checked that Data region is starting at 0x7800. So adding (cluster size(0x400) * 0x36) 0xd800 with 0x7800 is 0x15000. Let's see there.
<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/11.png?raw=true" width="100%">

So there is a table of music at 0x15040, 0x15080, 0x150c0.

The music I choosed to change is this.

<iframe width="560" height="315" src="https://www.youtube.com/embed/mj8tZvS1Sko" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Well, it's actually a video that a streamer plays a drum. I recently watched this video and it was so addictive. So that's why. It would be so funny. XD

What we have to care about when we change the music is the `size` field and `cluster location` field.

`size` field indicates the files size. And `cluster location` is what we saw earlier.

We need to be careful not to overflow other files cluster.
So reminding that, I copy and pasted my mp3 data to **first file**.
And also changed the size of the first file in the table.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/12.png?raw=true" width="100%">
<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/13.png?raw=true" width="100%">
The size and the datas are well changed.

Now let's write this data and resolder the flash. So I wrote this data on the flash and resolerdered it. And below image is the result of it.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/14.jpg?raw=true" width="90%">

Umm,, The resoldered flash chip looks little awful. But anyways, let's run it.

<iframe width="560" height="315" src="https://www.youtube.com/embed/LCcCoASHXfM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
  


  
Well. It is not working. 😁

For a few days, I tried to figure out the reason why the device is dead.
So, I could think two possibilities.  
1. The mp3 format was wrong.
2. Something went wrong with the pcb in the process of detaching and resoldering the flash.

To solve these problems, I chose to buy another one.  

# MP3 File
Let's check the mp3 file we extracted on the flash with VLC media player.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/15.png?raw=true" width="60%">

And the mp3 file we put in the flash looks like this.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/16.png?raw=true" width="50%">

The datas are Codec, Format, Channel, Sample Rate, Bit per Sample.
And as you can see, the `Codec` and `sample rate` are different.

So I used the convert function on VLC media player to change these.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/17.png?raw=true" width="90%">

And just like we did above, I changed the mp3 file and wrote it in flash.

Finally, I resoldered the flash very carefully.
So this is the result.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/18.jpg?raw=true" width="80%">

Resoldered flash looks very stable and perfect. Also the mp3 file we put is fully capable with the SoC.

Now let's roll!

<iframe width="560" height="315" src="https://www.youtube.com/embed/7F508OQqlGA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

# Conclusion

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way/image/19.jpg?raw=true" width="100%">

This post took quite a lot of time to write. The main reason was that I failed to success at first try which I didn't noticed about the `mp3 file format`. And also I was quite busy because of the school project.
I also talked about this problem with **@markminchoi** and He also thought that `mp3 file format` would be the problem.  
This was quite fun experience. *Extracting flash data* and *changing the music file*, these two main tasks are simple but brings powerful outcome. Not only in this **eye massager** but also with **other various devices**.

You can check out the mp3 files I extracted in flash at our [github link.](https://github.com/FirmExtract/FirmExtract-Posts/tree/main/Changing%20terrible%20music%20of%20eye%20massager%20in%20hardware%20way)

And also, if you are interested in `Voltage Glitching Fault injection attack`, Check out my [previous post](https://firmextract.com/post.php?id=fault_injection)