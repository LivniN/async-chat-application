# Asynchronous Chat Server Application
![enter image description here](https://img.shields.io/badge/python-3.7-blue)

> Asynchronous client server terminal chat application

Requirements
------------
*  python >= 3.7

#  Installation

 - Before running the server make sure that the port you are using in the
   configuration file is also exposed in the docker-compose.yml and that it is configured the same in the client configuration file.

#### Server:
 1. The server is delivered with option to run on **docker**
 2. Clone the repo and run `docker build . -t chat_server:1.0`
 3. Run `docker-compose up`
 4. Great! the server should be up running,this is what you should see:
 
![enter image description here](https://lh3.googleusercontent.com/P9FJneFxrmLkz2iFUf5p8YobAzYFK-BuKhfTLjMxzcCcyTjfJzo1pqZJiQR7yT796_L8JeP8YTU)

**of course you can also just run it by `python3 -m app.server`**(works with 3.7, didn't test it on older versions)
 #### Client:
 1. Make sure you are in the root directory of the project
 2. Run from terminal `python3 -m app.client`
 
![enter image description here](https://lh3.googleusercontent.com/G_W-kRzw9pg2Xa89QfNyHbJnaD_4UVrvcx2T_4jgC0BYkF67_w23xV_M15UHm13n6BN9D50OPQc)

## Chat conventions

 1. I implemented the register protocol and the message function with a simple idea. the client is connecting and first thing sending his user name (unless he uses to config file for it).
 2. Each message from the client is automatically attached with the client machine's time and the date printed in the message is the date in the sending client's machine.
 3. In order to send message to **specific recipients**, the client should use: `@sis @mom @dad` after his text message. for example: `how are you? @sis @mom @dad`, if there are no @s or non of those users exists,  the message will be public to all.
 4. The client will be **disconnected** (with Bye! message) after 1 minute of **inactivity** , this can be configured in the server configuration file.
 5. In order to change the input to asynchronous one, I had to change some console configuration during runtime, because of that the **client app will work only on UNIX consoles**  
 6. You can type and during typing receive messages, the message buffer won't be harmed and when hitting ENTER the message will be sent. (it is pretty ugly because the only way to see what you are typing is to print back each char typed, I will be happy to hear about a better way)
---
### Some Facts

 - The base framework for both server and client is asyncio which is built in Python. ([asyncio docs](https://docs.python.org/3/library/asyncio.html))
- I used some more built in libraries which I'm familiar with like logging, configparser and collections.namedtuple
 ---
 # Thanks for reading! 
