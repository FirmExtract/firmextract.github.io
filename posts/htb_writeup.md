# Introduction

There are many ctfs held right now. But it's hard to see the **Hardware** category in there. However there was a Hardware category in this **Hack The Box Cyber Apocalypse 2024** CTF. I was able to solve all of them during CTF. So in this post, I will show you how the challenges were solved. It was a lot of fun to have such a novel challenges. So let's see!

# Maze (very easy)
<img alt="Maze Challenge Picture" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image1.jpg" width="100%"><br><br>

## Description
* This challenge gives you a filesystem of the printer. So basicially it's analyzing printer's filesystem and get the flag. The files in the filesystem looks like `Figure1`.

Figure 1 :

```
fs
├─PJL
├─PostScript
├─saveDevice
│  └─SavedJobs
│      ├─InProgress
│      └─KeepJob
└─webServer
    ├─default
    ├─home
    ├─lib
    ├─objects
    └─permanent
```


## Solution
* There's a lot of things we can do if we get printer's filesystem. Especially, we can see stored print jobs. And yes there's a *SavedJobs* Directory in the filesystem. So maybe we should check that.
* Other directories meaning in filesystem are described below.
    * **PJL** : PJL (Printer Job Language) is a language for controlling and configuring printer's operation, such as setting printer parameters.
    * **PostScript** : PostScript is a page description language for describing the appearance of printed pages.
    * **webServer** : printer usually offers webServer. So we can easily guess that this directory is for webServer.

## Exploitation

* So let's check the SavedJobs directory and find out what's in there. Check `Figure2`. And we can find the flag in the `Factory.pdf`. Check `Figure3`.

Figure 2 :

<img alt="InProgress Directory Screenshot" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image2.jpg" width="100%"><br><br>

Figure 3 :

<img alt="The flag in Factory.pdf" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image3.jpg" width="100%"><br><br>

# BunnyPass (very easy)
<img alt="BunnyPass" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image4.jpg" width="100%"><br><br>

## Desription
* By reading synopsis, we can check that the default credentials will work. So the key point is to login to RabbitMQ instance and analyze what is happening there. Then we first have to know what RabbitMQ is. And that's what the challenge is giving us the problem.

## RabbitMQ
* RabbitMQ is open source message broker software. It is used to transmit data safer and faster between other applications by using message queue. RabbitMQ supports AMQP (Advanced Message Queue Protocol) to perform message queue and message broker. 

## Solution
* It gives you RabbitMQ instance when you spawn a docker in CTF website. And you can login with *admin*/*admin* as what synopsis said. (`Figure4`)
* And now what we can do is to check what messages are queued right now. In Queues, you can check what queues are inside the RabbitMQ instance. And there are 6 messages which is queued at *factory_idle*.(`Figure5`)

Figure 4 :

<img alt="login RabbitMQ instance" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image5.jpg" width="100%"><br><br>

Figure 5 :

<img alt="RabbitMQ queue list" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image6.jpg" width="100%"><br><br>

## Exploitation
* Now let's check what messages are in the *factory_idle*. (`Figure6`)
* And at the end of the queued messages you can find the flag (`Figure7`)

Figure 6 :

<img alt="Getting messages in queue" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image7.jpg" width="100%"><br><br>

Figure 7 :

<img alt="flag in the queued message" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image8.jpg" width="100%"><br><br>

# Rids (easy)
<img alt="Rids" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image9.jpg" width="100%"><br><br>

## Description
* Our mission is to read **W25Q128** flash to get the secret encryption key. The docker spawns a connection with a flash. So in this challenge we can learn how to read **W25Q128** flash with spi interface using python. 

## Solution
* This challenge gives us a *client.py* file for connecting the flash. Check out `Figure8`. In this code, we can check that they are passing the instruction with `exchange()`. And connecting to '127.0.0.1/1337' to interact with flash. So if we change the server ip to the challenge's docker, we can connect to the flash that we have to read.
* We have to read the flash after we connect with the server. So let's check the datasheet of the **W25Q128** to check what instruction we have to pass. In 34 page of [Datasheet](https://pdf1.alldatasheet.com/datasheet-pdf/view/506494/WINBOND/W25Q128FV.html), there is `Read Data(03h)` instruction. We need to pass 0x03 and 24-bit address following. And then the output data is sending.

Figure 8 :

```
import socket
import json

def exchange(hex_list, value=0):

    # Configure according to your setup
    host = '127.0.0.1'  # The server's hostname or IP address
    port = 1337        # The port used by the server
    cs=0 # /CS on A*BUS3 (range: A*BUS3 to A*BUS7)
    
    usb_device_url = 'ftdi://ftdi:2232h/1'

    # Convert hex list to strings and prepare the command data
    command_data = {
        "tool": "pyftdi",
        "cs_pin":  cs,
        "url":  usb_device_url,
        "data_out": [hex(x) for x in hex_list],  # Convert hex numbers to hex strings
        "readlen": value
    }
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # Serialize data to JSON and send
        s.sendall(json.dumps(command_data).encode('utf-8'))
        
        # Receive and process response
        data = b''
        while True:
            data += s.recv(1024)
            if data.endswith(b']'):
                break
                
        response = json.loads(data.decode('utf-8'))
        #print(f"Received: {response}")
    return response


# Example command
jedec_id = exchange([0x9F], 3)
print(jedec_id)
```

## Exploitation
* Let's use `exchange()` function to pass the instruction. Check `Figure9`. I imported *pwn* to use `remote()` to connect to server. And changed `sendall()` to `send()`. Lastly, I passed [0x03, 0x00, 0x00, 0x00] and recieved 10200 bytes to read whole things in the flash.
* Below code is for getting flag in the output. I used `join()` with list comprehension to get a flag with string.

`result = ''.join(chr(num) for num in data if num != 255)`
* So you can get the flag when you run this code. (`Figure10`)

Figure 9 :

```
from pwn import *
import struct
import json

server = "nc 94.237.50.51 51179"
server = server.split()

def exchange(hex_list, value=0):

    cs = 0
    usb_device_url = 'ftdi://ftdi:2232h/1'

    # Convert hex list to strings and prepare the command data
    command_data = {
        "tool": "pyftdi",
        "cs_pin":  cs,
        "url":  usb_device_url,
        "data_out": [hex(x) for x in hex_list],  # Convert hex numbers to hex strings
        "readlen": value
    }

    with remote(server[1], server[2]) as s:

        # Serialize data to JSON and send
        s.send(json.dumps(command_data).encode('utf-8'))

        # Receive and process response
        data = b''
        while True:
            data += s.recv(1024)
            if data.endswith(b']'):
                break

        response = json.loads(data.decode('utf-8'))
        #print(f"Received: {response}")
    return response


# Example command
data = exchange([0x03, 0x00, 0x00, 0x00], 10200)
result = ''.join(chr(num) for num in data if num != 255)
print(result)
```

Figure 10 :

<img alt="Rids flag" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image10.jpg" width="100%"><br><br>

# The PROM (medium)
<img alt="The PROM" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image11.jpg" width="100%"><br><br>

## Description
* This challenge tells us that we have to uncover **AT28C16**'s secret. EEPROM is non-volatile memory same as a flash. But the working mechanism is different. So we can't use the same method that we used in *Rids* challenge. Means that we have to read something in the EEPROM by controlling it.
* If we connect to the docker, it looks like `Figure11`. So what we have to do is to control this **AT28C16** EEPROM in server, and read the flag. 

Figure 11 :

<img alt="The PROM Server" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image12.jpg" width="100%"><br><br>

## Solution
* First we have to check the **AT28C16** [datasheet](https://pdf1.alldatasheet.com/datasheet-pdf/view/56113/ATMEL/AT28C16.html). In page 3, there is *Device Operation* page. And they say that we have to **low *CE*, *OE*** and **high *WE***. 
* And in page 5, there is *AC Read Characteristics* page. In there we can check the Waveform of the Read Operation. So the waveform shows that we have to set the Address in A0~A9. And low *CE* and *OE*. But the order isn't important as we have `read_byte()` in challenge server. After that, the output is coming out from Dout which is I/O0~I/O7 pins.
    * To sum it up, First we have to low *CE* and *OE* pin by using `set_ce_pin()`, `set_oe_pin()` and high *WE* by using `set_we_pin()`. 
    * Second, set the address by using `set_address_pins()`. We can set the address in 10 bits and we have to set it as a list same as the *Examples* shows us. 
    * Lastly, use `read_byte()` to read the byte in the address that we set.

## Exploitation
* So I wrote the code to read the EEPROM as we wrote at Solution. But the only thing in the output was all NULL. But the thing that we have to read wasn't a EEPROM data but the EEPROM Chip ID.
    * Check out page 3 in datasheet. There's a *DEVICE IDENTIFICATION* section. And it says by raising A9 pin to 12V and using address location 0x7E0 to 0x7EF, we can read the device Identification.
* I didn't got any hint that we have to read the EEPROM Chip ID. So there was some struggle. But at last I was able to get the flag by reading Chip ID. Check exploit code in `Figure12`.
* I made a `read_byte()` which reads one byte in EEPROM. 
    * It makes the address to binary format. And replace `1` to `5`. Because `AT28C16` EEPROM is working at 5V. And make A9 to `12` instead of `5` to read the Chip ID. And call `set_address_pins()`.
    * And we call `read_byte()` to read one byte. And we save it to `flag` string.
* Check `Figure13` to see what the result is when we run this code.

Figure 12 :
```
from pwn import *

def read_byte(address):
    global flag
    addr_binary = "{0:b}".format(address)
    addr_str = str(addr_binary).rjust(11,"0").replace("1","5")
    addr_list = [int(x) for x in list(addr_str)]
    addr_list[1] = 12 # For Only purpose for FLAG Because by setting to 12V, we can read Chip ID
    comm = "set_address_pins(" + str(addr_list) + ")"
    print(comm)
    r.sendlineafter("> ", comm)
    r.sendlineafter("> ", "read_byte()")
    r.recvuntil("Read ")
    flag += chr(int(r.recvuntil(" ")[:-1],16))
    print(r.recvuntil("\n")[:-1])
    print(flag)

server = "nc 83.136.251.7 49687"
server = server.split()

r = remote(server[1], server[2])

r.sendlineafter("> ", "set_ce_pin(0.5)")
r.sendlineafter("> ", "set_oe_pin(0.5)")
r.sendlineafter("> ", "set_we_pin(4)")

flag = ""

for i in range(0x7e0, 0x800):
    read_byte(i)

r.interactive()
```

Figure 13 : 

<img alt="The PROM flag" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image13.jpg" width="100%"><br><br>

# Flash-ing Logs(hard)
<img alt="Flash-ing Logs" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image14.jpg" width="100%"><br><br>

## Description
* In this challenge, we have to change the log of user id 0x5244. It gives us 2 files `log_event.c` and `client.py`.
    * `log_event.c` is the code for logging. The flash contain logs generated by this code.
    * `client.py` is the code for connecting to flash. We can use this python code to connect to docker. And send commands to flash.
* So our goal is to analyse the `log_event.c` code and edit the logs in flash memory.

Figure 14 : 

```
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <wiringPiSPI.h>
#include "W25Q128.h" // Our custom chip is compatible with the original W25Q128XX design

#define SPI_CHANNEL 0 // /dev/spidev0.0
//#define SPI_CHANNEL 1 // /dev/spidev0.1

#define CRC_SIZE 4 // Size of the CRC data in bytes
#define KEY_SIZE 12 // Size of the key

// SmartLockEvent structure definition
typedef struct {
    uint32_t timestamp;   // Timestamp of the event
    uint8_t eventType;    // Numeric code for type of event // 0 to 255 (0xFF)
    uint16_t userId;      // Numeric user identifier // 0 t0 65535 (0xFFFF)
    uint8_t method;       // Numeric code for unlock method
    uint8_t status;       // Numeric code for status (success, failure)
} SmartLockEvent;


// Function Prototypes
int log_event(const SmartLockEvent event, uint32_t sector, uint32_t address);
uint32_t calculateCRC32(const uint8_t *data, size_t length);
void write_to_flash(uint32_t sector, uint32_t address, uint8_t *data, size_t length);

// CRC-32 calculation function
uint32_t calculateCRC32(const uint8_t *data, size_t length) {
    uint32_t crc = 0xFFFFFFFF;
    for (size_t i = 0; i < length; ++i) {
        crc ^= data[i];
        for (uint8_t j = 0; j < 8; ++j) {
            if (crc & 1)
                crc = (crc >> 1) ^ 0xEDB88320;
            else
                crc >>= 1;
        }
    }
    return ~crc;
}


bool verify_flashMemory() {
    uint8_t jedc[3];
    uint8_t uid[8];
    uint8_t buf[256];
    uint8_t wdata[26];
    uint8_t i;

    uint16_t n;

    bool jedecid_match = true; // Assume true, prove false
    bool uid_match = true; // Assume true, prove false


    // JEDEC ID to verify against
    uint8_t expectedJedec[3] = {0xEF, 0x40, 0x18};

    // UID to verify against
    uint8_t expectedUID[8] = {0xd2, 0x66, 0xb4, 0x21, 0x83, 0x1f, 0x09, 0x2b};


    // SPI channel 0 at 2MHz.
    // Start SPI channel 0 with 2MHz
    if (wiringPiSPISetup(SPI_CHANNEL, 2000000) < 0) {
      printf("SPISetup failed:\n");
    }


    // Start Flash Memory
    W25Q128_begin(SPI_CHANNEL);

    // JEDEC ID Get
    //W25Q128_readManufacturer(buf);
    W25Q128_readManufacturer(jedc);
    printf("JEDEC ID : ");
    for (i=0; i< 3; i++) {
      printf("%x ",jedc[i]);
    }

    // Iterate over the array and compare elements
    for (int i = 0; i < sizeof(jedc)/sizeof(jedc[0]); ++i) {
        if (jedc[i] != expectedJedec[i]) {
            jedecid_match = false; // Set match to false if any element doesn't match
            break; // No need to check further if a mismatch is found
        }
    }

    if (jedecid_match) {
        printf("JEDEC ID verified successfully.\n");
    } else {
        printf("JEDEC ID does not match.\n");
        return 0;
    }

    // Unique ID
    // Unique ID Get
    W25Q128_readUniqieID(uid);
    printf("Unique ID : ");
    for (i=0; i< 8; i++) {
      printf("%x ",uid[i]);
    }
    printf("\n");

    // Iterate over the array and compare elements
    for (int i = 0; i < sizeof(uid)/sizeof(uid[0]); ++i) {
        if (uid[i] != expectedUID[i]) {
            uid_match = false; // Set match to false if any element doesn't match
            break; // No need to check further if a mismatch is found
        }
    }

    if (uid_match) {
        printf("UID verified successfully.\n");
    } else {
        printf("UID does not match.\n");
        return 0;
    }

    return 1;
}

// Implementations
int log_event(const SmartLockEvent event, uint32_t sector, uint32_t address) {

    bool memory_verified = false;
    uint8_t i;
    uint16_t n;
    uint8_t buf[256];


    memory_verified = verify_flashMemory();
    if (!memory_verified) return 0;

     // Start Flash Memory
    W25Q128_begin(SPI_CHANNEL);


    // Erase data by Sector
    if (address == 0){
        printf("ERASE SECTOR!");
        n = W25Q128_eraseSector(0, true);
        printf("Erase Sector(0): n=%d\n",n);
        memset(buf,0,256);
        n =  W25Q128_read (0, buf, 256);

    }

    uint8_t buffer[sizeof(SmartLockEvent) + sizeof(uint32_t)]; // Buffer for event and CRC
    uint32_t crc;

    memset(buffer, 0, sizeof(SmartLockEvent) + sizeof(uint32_t));

    // Serialize the event
    memcpy(buffer, &event, sizeof(SmartLockEvent));

    // Calculate CRC for the serialized event
    crc = calculateCRC32(buffer, sizeof(SmartLockEvent));

    // Append CRC to the buffer
    memcpy(buffer + sizeof(SmartLockEvent), &crc, sizeof(crc));

    // Print the SmartLockEvent for debugging
    printf("SmartLockEvent:\n");
    printf("Timestamp: %u\n", event.timestamp);
    printf("EventType: %u\n", event.eventType);
    printf("UserId: %u\n", event.userId);
    printf("Method: %u\n", event.method);
    printf("Status: %u\n", event.status);

    // Print the serialized buffer (including CRC) for debugging
    printf("Serialized Buffer (including CRC):");
    for (size_t i = 0; i < sizeof(buffer); ++i) {
        if (i % 16 == 0) printf("\n"); // New line for readability every 16 bytes
        printf("%02X ", buffer[i]);
    }
    printf("\n");


    // Write the buffer to flash
    write_to_flash(sector, address, buffer, sizeof(buffer));


    // Read 256 byte data from Address=0
    memset(buf,0,256);
    n =  W25Q128_read(0, buf, 256);
    printf("Read Data: n=%d\n",n);
    dump(buf,256);

    return 1;
}


// encrypts log events
void encrypt_data(uint8_t *data, size_t data_length, uint8_t register_number, uint32_t address) {
    uint8_t key[KEY_SIZE];

    read_security_register(register_number, 0x52, key); // register, address

    printf("Data before encryption (including CRC):\n");
    for(size_t i = 0; i < data_length; ++i) {
        printf("%02X ", data[i]);
    }
    printf("\n");

    // Print the CRC32 checksum before encryption (assuming the original data includes CRC)
    uint32_t crc_before_encryption = calculateCRC32(data, data_length - CRC_SIZE);
    printf("CRC32 before encryption: 0x%08X\n", crc_before_encryption);

    // Apply encryption to data, excluding CRC, using the key
    for (size_t i = 0; i < data_length - CRC_SIZE; ++i) { // Exclude CRC data from encryption
        data[i] ^= key[i % KEY_SIZE]; // Cycle through  key bytes
    }

    printf("Data after encryption (including CRC):\n");
    for(size_t i = 0; i < data_length; ++i) {
        printf("%02X ", data[i]);
    }
    printf("\n");


}

void write_to_flash(uint32_t sector, uint32_t address, uint8_t *data, size_t length) {
    printf("Writing to flash at sector %u, address %u\n", sector, address);

    uint8_t i;
    uint16_t n;

    encrypt_data(data, length, 1, address);

    n =  W25Q128_pageWrite(sector, address, data, 16);
    printf("page_write(0,10,d,26): n=%d\n",n);

}
```

Figure 15 :

```
import socket
import json

FLAG_ADDRESS = [0x52, 0x52, 0x52]

def exchange(hex_list, value=0):

    # Configure according to your setup
    host = '127.0.0.1'  # The server's hostname or IP address
    port = 1337        # The port used by the server
    cs=0 # /CS on A*BUS3 (range: A*BUS3 to A*BUS7)
    
    usb_device_url = 'ftdi://ftdi:2232h/1'

    # Convert hex list to strings and prepare the command data
    command_data = {
        "tool": "pyftdi",
        "cs_pin":  cs,
        "url":  usb_device_url,
        "data_out": [hex(x) for x in hex_list],  # Convert hex numbers to hex strings
        "readlen": value
    }
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # Serialize data to JSON and send
        s.sendall(json.dumps(command_data).encode('utf-8'))
        
        # Receive and process response
        data = b''
        while True:
            data += s.recv(1024)
            if data.endswith(b']'):
                break
                
        response = json.loads(data.decode('utf-8'))
        #print(f"Received: {response}")
    return response


# Example command
jedec_id = exchange([0x9F], 3)
print(jedec_id)
```

## Solution
* What we have to see in `log_event.c` is how logging works. And we can check it at `log_event()`. Check out `Figure16`. It takes 3 argument. `const SmartLockEvent event`, `uint32_t sector`, `uint32_t address`. 
    * We can assume that `sector` and `address` is for flash addressing. So let's check what `SmartLockEvent event` structure does. It has several items for event log. And especially there is `userId` which we have to edit.

``` 
typedef struct {
    uint32_t timestamp;   // Timestamp of the event
    uint8_t eventType;    // Numeric code for type of event // 0 to 255 (0xFF)
    uint16_t userId;      // Numeric user identifier // 0 t0 65535      (0xFFFF)
    uint8_t method;       // Numeric code for unlock method
    uint8_t status;       // Numeric code for status (success, failure)
} SmartLockEvent;
```

* `SmartLockEvent event` goes to `buffer`. and `buffer` goes to `write_to_flash()`.
    * `buffer` list has `SmartLockEvent` size + 4. Because the crc which has 4 bytes size is following with `event` value in `buffer`. And the crc is generated with `calculateCRC32()`.

```
uint8_t buffer[sizeof(SmartLockEvent) + sizeof(uint32_t)]; // Buffer for event and CRC
uint32_t crc;

memset(buffer, 0, sizeof(SmartLockEvent) + sizeof(uint32_t));

// Serialize the event
memcpy(buffer, &event, sizeof(SmartLockEvent));

// Calculate CRC for the serialized event
crc = calculateCRC32(buffer, sizeof(SmartLockEvent));

// Append CRC to the buffer
memcpy(buffer + sizeof(SmartLockEvent), &crc, sizeof(crc));
```

* After moving `event` and `crc` value to `buffer`, it goes to `write_to_flash()`. And in `write_to_flash()`, they encrypt `buffer` by using `encrypt_data()` and write it on the flash.

```
    // Write the buffer to flash
    write_to_flash(sector, address, buffer, sizeof(buffer));         

...

void write_to_flash(uint32_t sector, uint32_t address, uint8_t *data, size_t length) {
    printf("Writing to flash at sector %u, address %u\n", sector, address);
    
    uint8_t i;
    uint16_t n;  

    encrypt_data(data, length, 1, address);  

    n =  W25Q128_pageWrite(sector, address, data, 16);
    printf("page_write(0,10,d,26): n=%d\n",n);

}
```

* `encrypt_data()` first read `security_register` using `read_security_register()` and save it on `key`. And xor with `data` which is doing encryption. But they leave the crc value same.

```
// encrypts log events 
void encrypt_data(uint8_t *data, size_t data_length, uint8_t register_number, uint32_t address) {
    uint8_t key[KEY_SIZE];

    read_security_register(register_number, 0x52, key); // register, address
    
    printf("Data before encryption (including CRC):\n");
    for(size_t i = 0; i < data_length; ++i) {
        printf("%02X ", data[i]);
    }
    printf("\n");

    // Print the CRC32 checksum before encryption (assuming the original data includes CRC)
    uint32_t crc_before_encryption = calculateCRC32(data, data_length - CRC_SIZE);
    printf("CRC32 before encryption: 0x%08X\n", crc_before_encryption);

    // Apply encryption to data, excluding CRC, using the key
    for (size_t i = 0; i < data_length - CRC_SIZE; ++i) { // Exclude CRC data from encryption
        data[i] ^= key[i % KEY_SIZE]; // Cycle through  key bytes
    }

    printf("Data after encryption (including CRC):\n");
    for(size_t i = 0; i < data_length; ++i) {
        printf("%02X ", data[i]);
    }
    printf("\n");

}
```

* So when the `log_event()` called, they make crc based on the `SmartLockEvent` structure. And enrypt the value of structure using `security_register`. Lastly write it on the flash. Then what we have to do is to decrypt the value in flash and edit the user_id in the structure. And regenerate crc for the integrity.
    * How can we get `security_register` value? It is written in the W25Q128 [datasheet](https://pdf1.alldatasheet.com/datasheet-pdf/view/506494/WINBOND/W25Q128FV.html). Yes as always. In page 70, there is *Read Security Registers* page. It says that we can read a security register using `0x48` command and pass 24-bit address and 1 dummy byte. The code was reading first security register at 0x52.

        `read_security_register(register_number, 0x52, key); // register, address`
    * If you check 12 page in datasheet, there is a *Block Diagram*. You can check where the Security registers are placed. The first one is on 0x1000 to 0x10FF. So we should read 0x1052 to get the `key` value.

Figure 16 :

```
int log_event(const SmartLockEvent event, uint32_t sector, uint32_t address) {

    bool memory_verified = false;
    uint8_t i;
    uint16_t n;
    uint8_t buf[256];


    memory_verified = verify_flashMemory();
    if (!memory_verified) return 0;

     // Start Flash Memory
    W25Q128_begin(SPI_CHANNEL);


    // Erase data by Sector
    if (address == 0){
        printf("ERASE SECTOR!");
        n = W25Q128_eraseSector(0, true);
        printf("Erase Sector(0): n=%d\n",n);
        memset(buf,0,256);
        n =  W25Q128_read (0, buf, 256);

    }

    uint8_t buffer[sizeof(SmartLockEvent) + sizeof(uint32_t)]; // Buffer for event and CRC
    uint32_t crc;

    memset(buffer, 0, sizeof(SmartLockEvent) + sizeof(uint32_t));

    // Serialize the event
    memcpy(buffer, &event, sizeof(SmartLockEvent));

    // Calculate CRC for the serialized event
    crc = calculateCRC32(buffer, sizeof(SmartLockEvent));

    // Append CRC to the buffer
    memcpy(buffer + sizeof(SmartLockEvent), &crc, sizeof(crc));

    // Print the SmartLockEvent for debugging
    printf("SmartLockEvent:\n");
    printf("Timestamp: %u\n", event.timestamp);
    printf("EventType: %u\n", event.eventType);
    printf("UserId: %u\n", event.userId);
    printf("Method: %u\n", event.method);
    printf("Status: %u\n", event.status);

    // Print the serialized buffer (including CRC) for debugging
    printf("Serialized Buffer (including CRC):");
    for (size_t i = 0; i < sizeof(buffer); ++i) {
        if (i % 16 == 0) printf("\n"); // New line for readability every 16 bytes
        printf("%02X ", buffer[i]);
    }
    printf("\n");


    // Write the buffer to flash
    write_to_flash(sector, address, buffer, sizeof(buffer));


    // Read 256 byte data from Address=0
    memset(buf,0,256);
    n =  W25Q128_read(0, buf, 256);
    printf("Read Data: n=%d\n",n);
    dump(buf,256);

    return 1;
}
```

## Exploitation
* We can get the `key` value using 0x48 command. So now we can decrypt the flash data. But the problem is crc. Let's check how crc is generated.
    * It is not that complicate. Just xor and shifting. To generate the crc with the edited log value, I chose to just make the C code same as this one.

```
// CRC-32 calculation function
uint32_t calculateCRC32(const uint8_t *data, size_t length) {
        uint32_t crc = 0xFFFFFFFF;
        for (size_t i = 0; i < length; ++i) {
        crc ^= data[i];
        for (uint8_t j = 0; j < 8; ++j) {
                if (crc & 1)
                crc = (crc >> 1) ^ 0xEDB88320;
                else
                crc >>= 1;
        }
        }
        return ~crc;
}        
```

* I just ran the C code with my edited log value. So that I can get the new crc. Check out `Figure17`.

```
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

typedef struct {
        uint32_t timestamp;   // Timestamp of the event
        uint8_t eventType;    // Numeric code for type of event // 0 to 255 (0xFF)
        uint16_t userId;      // Numeric user identifier // 0 t0 65535 (0xFFFF)
        uint8_t method;       // Numeric code for unlock method
        uint8_t status;       // Numeric code for status (success, failure)
} SmartLockEvent;

// CRC-32 calculation function
uint32_t calculateCRC32(const uint8_t *data, size_t length) {
        uint32_t crc = 0xFFFFFFFF;
        for (size_t i = 0; i < length; ++i) {
        crc ^= data[i];
        for (uint8_t j = 0; j < 8; ++j) {
                if (crc & 1)
                crc = (crc >> 1) ^ 0xEDB88320;
                else
                crc >>= 1;
        }
        }
        return ~crc;
}

int main(){
        uint8_t dat1[] = {35, 197, 21, 102, 214, 0, 160, 3, 1, 1, 0, 0, 207, 91, 108, 133};
        uint8_t dat2[] = {191, 243, 21, 102, 187, 0, 160, 3, 3, 1, 0, 0, 236, 104, 129, 205};
        uint8_t dat3[] = {227, 21, 22, 102, 187, 0, 160, 3, 3, 1, 0, 0, 134, 173, 71, 208};
        uint8_t dat4[] = {239, 127, 22, 102, 214, 0, 160, 3, 3, 1, 0, 0, 209, 155, 216, 44};
        uint32_t crc;
        crc = calculateCRC32(dat1, 12);
        printf("%x\n", crc);
        crc = calculateCRC32(dat2, 12);
        printf("%x\n", crc);
        crc = calculateCRC32(dat3, 12);
        printf("%x\n", crc);
        crc = calculateCRC32(dat4, 12);
        printf("%x\n", crc);
        return 0;
}
```

* Check out `Figure18` to see the final exploit code. I first read the security register and 0x9c0 where the `user_id` 0x5244 is placed.
    * If you want to write new data in the flash, you have to erase that area and write it. Not overwrite. So we got to remove the data in 0x9c0 but it wasn't available to remove only that part. But to just erase by Sector(0x1000 bytes).
* And then I cleared the logs with `user_id` 0x5244 only. I've done it with reading whole logs and erase the flash, and then write the logs that I read except `user_id` 0x5244 logs. So that's what `erase_only_specific()` does.
* Now decrypt the event logs with 0x5244 and change the `user_id` to 0x3a0. And encrypt it with `encrypt_data()`. And finally write it on flash with `write_payload()`. 
* Check out `Figure19` to see the code running.

Figure 17 : 

<img alt="new crc" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image15.jpg" width="50%"><br><br>

Figure 18 :

```
from pwn import *
import socket
import json

server = "nc 94.237.57.155 58163"
server = server.split()

s = remote(server[1], server[2])

FLAG_ADDRESS = [0x52, 0x52, 0x52]

crc_list = [[0x20, 0xe4, 0xca, 0x0d], [0x03, 0xd7, 0x27, 0x45], [0x69,0x12, 0xe1, 0x58], [0x3e, 0x24, 0x7e, 0xa4]] // Little endian

'''
dcae420
4527d703
58e11269
a47e243e
'''


def erase_mem():
    exchange([0x06]) # Write Enable
    exchange([0x20, 0x00, 0x00, 0x00])

def program_pages(original):
    for i in range(0, 0x9c0, 0x100):
        exchange([0x06]) # Write Enable
        exchange([0x02, 0x00, 0x00+(i>>8), 0x00]+original[i:i+0x100])

def erase_only_specific():
    original = exchange([0x03, 0x00, 0x00, 0x00], 2496)
    erase_mem()
    program_pages(original)
    original = exchange([0x03, 0x00, 0x00, 0x00], 2496)

def decrypt_data(data,j,on):
    edit = [data[i] ^ key[i] for i in range(12)]
    if on:
        return edit + crc_list[j/16]
    if not on:
        return edit + data[12:]

def write_payload(pay, i):
    exchange([0x06]) # Write Enable
    exchange([0x02, 0x00, 0x09, 0xc0+i]+pay)
#    print("write_payload : ")
#    print(pay)

def prettify(data):
    timestamp = (data[3] << 24) + (data[2] << 16) + (data[1] << 8) + data[0]
    eventType = data[4] #data[5] is NULL
    userId = (data[7] << 8) + data[6]
    method = data[8]
    status = data[9]
    # data[10] and data[11] is for padding bytes.
    crc = (data[15] << 24) + (data[14] << 16) + (data[13] << 8) + data[12]
    print("_______________")
    print("timestamp : " + str(hex(timestamp)))
    print("eventType : " + str(hex(eventType)))
    print("userId : " + str(hex(userId)))
    print("method : " + str(hex(method)))
    print("status : " + str(hex(status)))
    print("crc : " + str(hex(crc)))
    return userId

def encrypt_data(data):
    encrypt = [data[i] ^ key[i] for i in range(12)]
    encrypt += data[12:]
    return encrypt

def exchange(hex_list, value=1):

    # Configure according to your setup
    cs=0 # /CS on A*BUS3 (range: A*BUS3 to A*BUS7)

    usb_device_url = 'ftdi://ftdi:2232h/1'

    # Convert hex list to strings and prepare the command data
    command_data = {
        "tool": "pyftdi",
        "cs_pin":  cs,
        "url":  usb_device_url,
        "data_out": [hex(x) for x in hex_list],  # Convert hex numbers to hex strings
        "readlen": value
    }

    # Serialize data to JSON and send
    s.send(json.dumps(command_data).encode('utf-8'))

    # Receive and process response
    data = b''
    while True:
        data += s.recv(1024)
        if data.endswith(b']'):
            break

    response = json.loads(data.decode('utf-8'))
    #print(f"Received: {response}")

    return response


# Example command
data = exchange([0x48, 0x00, 0x10, 0x52, 0x00], 12)
key = data
data = exchange([0x03, 0x00, 0x09, 0xc0], 200-80)

erase_only_specific()

for i in range(0, len(data)-60,16):
    payload = decrypt_data(data[i:i+16], i, 1)
#    print(payload)

    payload_ = decrypt_data(data[i:i+16], i, 0)
#    print(payload_ )

    print("BEFORE : ")
    userId = prettify(payload_)

    if(userId == 0x5244):
        payload[7] = 0x3
        payload[6] = 0xa0
        enc_payload = encrypt_data(payload)
        write_payload(enc_payload, i)
        check = exchange([0x03, 0x00, 0x09, 0xc0+i], 16)
        check = decrypt_data(check, i,0)
        print("AFTER : ")
        prettify(check)
#        print(check)

data = exchange([0x03, 0x52, 0x52, 0x52], 100)
flag = ''.join(chr(x) for x in data if data != 255)
print(flag)
```

Figure 19 :

<img alt="Flash-ing Logs flag" src="https://raw.githubusercontent.com/FirmExtract/FirmExtract-Posts/main/HTB%20Cyber%20Apocalypse%202024%20Hardware%20Challenge%20Writeup/images/image16.jpg" width="100%"><br><br>

## Conclusion
I really enjoyed solving these challenges. Especially, the ones like 'The PROM' and 'Flash-ing Logs' were quite innovative. I wonder how these challenges were made. I hope to see more hardware challenges like these in the future.
