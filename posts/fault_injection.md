# Introduction

To test voltage glitching, I made simple circuit and try to glitch it.
I failed glitching with using MCU(PIC16F84A with 16Mhz). And I'm thinking that it was because the clock hz was too small. We have to control voltage for a very short time. And using 16Mhz clock, it was hard to control precisely.

To satisfy this, I tried with FPGA. FPGA programming with verilog was my first experience. At beginning it was hard to code. But as I learned basic of verilog, it got easier. I learned verilog with [this](https://www.asic-world.com/verilog/veritut.html) site.  
So let's get start!

(Well, while writing this post, I found that the problem that voltage glitching with PIC was not because we can't control the voltage for a very short time, but the time that we controlled with PIC was too short! By reading this whole post, you will know what I'm saying. I misrecognized so hard. :P)



# What is Fault injection attack
Fault injection is an attack that inject fault into the device.
Injection fault into device can be performed with many other ways.
It could be Voltage glitching, Clock glitching, Electromagnetic glitching, etc.
And I tried fault injection by using voltage glitching.

Voltage glitching can also be perform in many attack surfaces.
Just making shortage or giving low/high power and something like these are all voltage glitching.
How we voltage glitch device is **Cut off power for a very short time**.

## Target board
The schematic diagram of the target board : 
<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Fault%20injection%20attack%20with%20PIC%20and%20FPGA/images/schematic_diagram.png?raw=true" width="100%">

Target board's code is shown below :
```C
volatile unsigned char DEBUG_FLAG = 0;

volatile unsigned int i, check;

void main(){
     TRISB = 0;
     TRISA = 0;
     PORTB = 0;
     PORTA = 0;
     while(1){
       check = 0;
       for(i=0;i<=9999;i++){
         ++check;
       }
       if(check == 10000){
         PORTB = 0b11111111;
         delay_ms(1000);
         PORTB = 0;
       }
       else{
         PORTA = 0b11111111;
         delay_ms(4000);
         PORTA = 0;
       }
     }
}
```
It adds `check` variable 10000 times and checks if it is really 10000.
If it is, `PORTB` LEDs light up. If not `PORTA` LED lights up.

By voltage glitching, we will skip the below assembly code :
```C
;Fault_Injection.c,12 :: 		for(i=0;i<=9999;i++){
	CLRF       _i+0
	CLRF       _i+1
L_main2:
	MOVF       _i+1, 0
	SUBLW      39
	BTFSS      STATUS+0, 2
	GOTO       L__main10
	MOVF       _i+0, 0
	SUBLW      15
L__main10:
	BTFSS      STATUS+0, 0
	GOTO       L_main3
;Fault_Injection.c,13 :: 		++check;
	MOVF       _check+0, 0
	ADDLW      1
	MOVWF      R0+0
	MOVLW      0
	BTFSC      STATUS+0, 0
	ADDLW      1
	ADDWF      _check+1, 0
	MOVWF      R0+1
	MOVF       R0+0, 0
	MOVWF      _check+0
	MOVF       R0+1, 0
	MOVWF      _check+1
```

# Glitching with PIC(Failed)
## Attacking Board
The schematic diagram of this board : 
<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Fault%20injection%20attack%20with%20PIC%20and%20FPGA/images/schematic_diagram1.png?raw=true" width="100%">

The source code of this board is below
```C
sbit button at PORTB.B0;
sbit power at PORTB.B1;

int main(){
    TRISB = 0b00000001;
    PORTB = 0;
    power = 1;
    while(1){
      if(button){
        power = 0;
        asm{
            nop;
        }
        power = 1;
        Delay_ms(400);
      }
      else{
        power = 1;
      }
    }
}
```
If Button is pushed, PORTB.B1 pin gets 0 for `nop` instruction second.
How many seconds will it take for `nop` instruction?

In [this](http://ww1.microchip.com/downloads/en/DeviceDoc/51702a.pdf) pdf, there is an equation of internal instruction cycle period.
<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Fault%20injection%20attack%20with%20PIC%20and%20FPGA/images/equation.png?raw=true" width="100%">
Our Processor Frequency is 16Mhz. So one cycle is 250nS.
<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Fault%20injection%20attack%20with%20PIC%20and%20FPGA/images/500.jpg?raw=true" width="100%">

And when I pushed button, it took 500ns. So it means that it takes 2 cycles.
Will it enough to voltage glitch my target board?

Let's check!

<iframe width="560" height="315" src="https://www.youtube.com/embed/0HMizLXngkU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

It seems like fault is injecting but the LED on PORTA doesn't light up.
I think 500nS is not the right time for voltage glitching this device.

Then now let's try with FPGA.

# Glitching with FPGA
Well, actually I don't have FPGA board. But luckily, there was fpga to borrow in my school.
So I got **Altera DE0 Board** for free which is fairly expensive.

I used quartus II ide for verilog coding, compiling, programming.

How should we code this fpga to use it for voltage glitching?
First, the `CLOCK` is most important componenet in here.
By counting `CLOCK`, we can control how many seconds I want to cut off the power.

Second, the `Switch` is necessary for control seconds more specifically like turning switches on makes cutting off seconds go up.

And Last, we have to set waiting time to sleep after clicking button which is the trigger for voltage glitching.
If we don't he waiting time, just clicking button once trigger voltage glitching a lot of times.

Because even if we click it very fast, in fpga it operates its code more than one time.
You know, fpga is VERY FASTER than us.

So below is the source codes that I coded.
```
module fault_injection(BUTTON, SW, LEDG, GPIO0_D, CLOCK_50);
	input [1:0]BUTTON;
	input [9:0]SW;
	input CLOCK_50;
	
	output [1:0]GPIO0_D;
	output [1:0]LEDG;
	
	reg [9:0]count;
	reg [50:0]counter;
	reg [1:0]state;
	reg gpio_reg;
	reg led_reg;

assign GPIO0_D[0] = gpio_reg;
assign LEDG[0] = led_reg;

always @ (posedge CLOCK_50) begin
	if (state == 0) begin 
		if(BUTTON[0] == 0) begin
			count <= SW;
			state <= 1;
		end
	end
	else if(state == 1) begin
		led_reg <= 1;
		gpio_reg <= 0;
		counter <= counter + 1;
		if(counter==count*100) begin
			gpio_reg <= 1;
			counter <= 0;
			state <= 2;
			led_reg <= 0;
			count <= 0;
		end
	end
	else if(state == 2) begin
		counter <= counter + 1;
		led_reg <= 0;
		if(counter == 10000000) begin
			counter <= 0;
			state <= 0;
		end
	end 
	else begin
		state <= 0;
		gpio_reg <= 1;
		led_reg <= 0;
	end
end

endmodule
```

If you can't understand this code then checkout the site that I hyperlinked on `Introduction`.
You can learn about verilog and reading this code is very easy when you just understand it.

As I said we can control specific seconds by using switch. I will start from just turning on one switch and two, three, ...
I will connect GPIO0_D pin to my target board.

And now let's check if it works well!

<iframe width="560" height="315" src="https://www.youtube.com/embed/FhQpUTU9zzw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Yay! it works well! I think turning 2~4 switch is works most reliable.
The difference between PIC and this fpga is only the `time`.
So let's check how many seconds fpga cut off.

<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Fault%20injection%20attack%20with%20PIC%20and%20FPGA/images/grabbed.jpg?raw=true" width="100%">

I grabbed emitter in transistor for power and board's gnd for ground.

Then I clicked the button with only one switch on and below image was shown on oscilloscope.
<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Fault%20injection%20attack%20with%20PIC%20and%20FPGA/images/seconds.jpg?raw=true" width="100%">
Wait.. What? It's way long seconds than pic's 500nS!!

Well the problem with PIC was not because it's time is to long. It was because it was too short.

Anyways, we succeed with using FPGA.
Now let's make the voltage glitching working with PIC too!

# Glitching with PIC(Succeed)

Final Source code :

```C
sbit button at PORTB.B0;
sbit power at PORTB.B1;

int main(){
    int i;
    TRISB = 0b00000001;
    PORTB = 0;
    power = 1;
    while(1){
      if(button){
        power = 0;
        asm{
            nop; //500nS
            nop; //750nS
            nop;
            nop;
            nop;
            nop;
            nop;
            nop; //2250nS
        }
        power = 1;
        Delay_ms(400);
      }
      else{
        power = 1;
      }
    }
}
```

I made it as 2250nS.

Let's check this with oscilloscope.
<img src="https://github.com/FirmExtract/FirmExtract-Posts/blob/main/Fault%20injection%20attack%20with%20PIC%20and%20FPGA/images/final.jpg?raw=true" width="100%">

Nice. It exactly takes 2250nS.

Now let's move on to the real target.

<iframe width="560" height="315" src="https://www.youtube.com/embed/uXNnpkIQ3NA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

It isn't that reliable compared to fpga but who cares? Anyways it works!

# Conclusion
In this post we'v learned about Fault injection: voltage glitching attack and how to use it. Actually, using fpga for voltage glitching is not that practical in real world. Because we need to set the exact time for the success of voltage glitching. But as you saw, it can be quite reliable attack tool for voltage glitching simple device like our target board.

On the other hand, using MCU is quite useful and practical. We can set the exact time to succeed voltage glitching. As clock frequency of mcu got higher, we can control the time more precisely. So MCU can also be enough precise.

Because I don't have any device for voltage glitching, I just tested with my own board. If I get any device which is vulnerable in voltage glitching, I will show how it works to you guys right away.

If you didn't have any background about electric or embedded, this post could be quite hard. So if you have question about this, feel free to ask in our facebook and twitter.

Thanks for reading!