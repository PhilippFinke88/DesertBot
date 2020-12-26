# Desert Bot
A totally overengineered autopilot for the minigame *Desert Bus* from the game compilation *Penn & Teller's Smoke and Mirrors* for the Sega CD. This project uses OpenCV with Python to detect the road's middle lane to keep the bus on track and to safely drive the non-existing passengers from Tucson to Las Vegas.

## Motivation
I came up with the idea for this project after watching the episode of the *Angry Video Game Nerd* about *Desert Bus* (you can watch the full episode [here](https://www.youtube.com/watch?v=RFi2vcseEz8 "here")). There he used a clamp to hold down the A button of the gamepad to get some kind of autopilot which didn't work as the bus is still automatically steering to the right over time.

## Installation
### Kega Fusion
**NOTE:** *Desert Bot*  can currently only be used with the Sega emulator *Kega Fusion*.

1. Follow the instructions on [https://www.fantasyanime.com/emuhelp/kegafusion](https://www.fantasyanime.com/emuhelp/kegafusion "https://www.fantasyanime.com/emuhelp/kegafusion") to install *Kega Fusion* and to set up the Sega CD BIOS files.
1. Set the resolution to 1920x1080 under **Video > Full Screen Resolution** (another resolution might work too, but I haven't tested this yet).
1. Uncheck **Video > Filtered** as image filtering will be done by *Desert Bot*.
1. Under **Options > Set Config > Controllers** redefine the the controller so that **LEFT** is **J** and the **A button** is **A** on your keyboard.

### Desert Bot
1. Download or clone this project.
1. Install depending Python packages.

`pip install opencv-python numpy keyboard pyautogui`

**NOTE:** You can also install the packages in a virtual environment which is best practise anyway (see [https://docs.python.org/3/tutorial/venv.html](https://docs.python.org/3/tutorial/venv.html "https://docs.python.org/3/tutorial/venv.html")).

## Usage
1. Start *Desert Bot* with `python3 DesertBot.py`.
1. Load *Penn & Teller's Smoke and Mirrors Disc 1* ROM in *Kega Fusion* (the ROMs can be found [here](https://hiddenpalace.org/Penn_%26_Teller%27s_Smoke_and_Mirrors_(Apr_30,_1995_prototype)).
1. Switch to fullscreen by pressing **Esc** on your keyboard.
1. Start Desert Bus in the game.
1. Press **A** on your keyboard to start the autopilot.
1. Enjoy the ride!

## Known issues
- The .cue files of the *Penn & Teller's Smoke and Mirrors* CD images might be edited as the paths to the corresponding .bin files are wrong. Open each .cue file and check if the path in first line points to the corresponding .bin file in the same folder.
- For some reason it is not possible to send virtual key strokes for the left arrow key in Python (at least under Windows). For this reason the left arrow key must be mapped to **J** in *Kega Fusion*.