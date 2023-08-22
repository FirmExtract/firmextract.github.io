# Introduction
Broken LCD is very common reason to change your old phone.
Or you can use your broken phone as.. SERVER!
That was what I thought when I dropped my phone and even stepped on it.
It's LCD was totally crashed and that LCD was my second one which I replaced.
But as a linux server, we don't need screen anymore. So it would be the perfect upgrade for my broken phone!
However there is a problem. Server needs to be always be on. But how can we handle battery swelling?
Here comes the hardware part! I will remove battery and replace it to dc cable. So that we can power the smartphone by dc adaptor.
Now let's start our journey to make my phone more fancy!

# Preparing parts
## Broken Rooted Phone 

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/image.jpg" width=50%><br>
So this is my phone which is totally broken. But I rooted this phone despite of this LCD. And the result is following image:

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/telnet.jpg" width=80%><br>
I successfully accessed shell on my phone!

## Battery teardown
You know that we can't just use the battery that phone is using now.
Because if I fail with that battery there's no more battery to use! I just have to wait with phone without battery while another battery shipped.

So I just ordered new one!

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/image%20(1).jpg" width=60%><br>
From this, what we need is a **connector** part.

So I peeled off the top part.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/image%20(2).jpg" width=50%><br>
You can see that the +, - pole is connected here.
Maybe if we give power to this part, we will be able to power the phone with right connector.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/image%20(3).jpg" width=50%><br>
After all, I just tear out the connector part.
And now we got nice connector to use!

## DC adaptor teardown
<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/image%20(4).jpg" width=50%><br>
I brought random dc adaptor which was in my house.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/image%20(6).jpg" width=50%><br>
If you cut the lines of this, you will see the two lines which is + and -.

Now what we gonna do is to connect this lines to the connector!

# Changing power supply
## Connecting lines
Before we connect dc adaptor's two lines to the connector, we have to change the voltage!
The dc adaptor has 12V and battery has 4V.
Therefore we have to drop the voltage using this.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/image%20(5).jpg" width=50%><br>
This is the module which drops the voltage.
Now let's connect the lines!

Dc adaptor to voltage drop module :

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/image%20(7).jpg" width=50%><br>
Dropped 12V to 4V!

module to connector :

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/image%20(8).jpg" width=50%><br>

### Phone teardown
It's time to open the phone to replace the battery.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/image%20(9).jpg" width=50%><br>

And..

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/image%20(10).jpg" width=50%><br>
Yup! We just removed the battery and detached battery connector. All we gotta do is to __connect the lines__.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/image%20(11).jpg" width=50%><br>
Cool! Time to test it!

## Let's Test!

<iframe width="560" height="315" src="https://www.youtube.com/embed/kv2urqKJ2Fk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Working perfectly at once.

## Makeing Web Server

Now let's make it as a web server.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/httpd.jpg" width=60%><br>

Running httpd in busybox.
And we got this.

<img src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/Now%20power%20your%20smartphone%20with%20DC%20adapter.%20Not%20Battery/image/website.jpg" width=60%><br>

Smartphone to Server is successfully done!