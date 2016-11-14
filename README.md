# wiiu-memshark

Cross platform Python app that eases TCPGecko memory manipulation.

## Motivation

I wanted to modify a couple of things in Project Hyrule. Although those modifications worked, it lead to a desire for a generic way of handling mods for other games in the vein on GameShark or GameGenie.

## Installation

Your system will need Python3. If your OS doesn't provide the TK bindings for Python with Python3, then you will need to install those as well (likely a separate package).

## Usage

Run the following in a terminal to launch the GUI.

``` Bash
python ./main.py
```

Once launched, use the tabs in the GUI to select what tools you need.

The `Exploit Server` tab can launch a web server on the machine running the GUI. Once launched, navigate to the address on the Wii U's web browser. This will provide links to run a transient kernel exploit and launch tcp gecko. These will be undone after the system is reset.

The `TCPGecko` tab controls whether or not your local machine is connected to TCPGecko running on a Wii U. You can change the IP address of the Wii U by editing `config.json`. 

Once the local TCPGecko client has connected successfully, the `Game Actions` tab can be used to send messages to TCPGecko running on the Wii U. Navigate to this tab, and then select the game you are playing. Any single value can be sent one time to clicking "Poke". The value can be sent every second by checking "Frozen".

To modify the memory values for a game, edit the JSON config file located under `games/`. Relaunch the GUI, and your changes will show up. New games can be added by dropping for JSON config files into this directory.

## Game Config Format

When specifying a `memory_pokes` in the config file, an `address` is a string literal representation of a hex location. A `v alue` can be written as either a string delimited hex literal, decimal integer literal, or another base using the `base` property.
