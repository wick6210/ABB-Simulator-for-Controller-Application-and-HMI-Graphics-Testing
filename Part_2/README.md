# ABB HMI Simulator

## Introduction

Part_2 of this project folder contains all versions of the ABB HMI Simulator assigned during the EngineeredX Event.
This project is to design a Human Machine Interface which has graphical controls and can be used to control industrial machines. In this example, I have taken the case of a simple water tank. This also includes hardware control of the simulated water tank.

## Working

The water tank should have 2 controls:

1. Manual Mode    :    Manually switch the water pump ON or OFF according to human judgement of the water level in the tank.
2. Automatic Mode :    The controller / simulator will decide whether to turn the water pump ON or OFF absed on thresholding values.

To implement this software-level project, Python and its libraries are used.
The full details of the project working are explain in the parent folder.

## Tech Stack

### Software Tech Stack

1. Language  :    `Python 3.12.10`
2. Libraries :    `PyModBus`, `Streamlit`, `Threading`, `Time`, `Collections`
3. OS        :    Windows 11 Home

### Hardware Tech Stack

1. Breadboard
2. ESP8266 NodeMCU
3. 2x Push Buttons
4. 4x Male-to-Male Jumper Wires

Ensure that the above libraries suited for Python `3.12.10` are present before implementing this project.

## How To Run The Project

Connect the input-pullup push buttons to the NodeMCU on pins 5 and 6.

Dump the `NodeMCU.ino` code to the NodeMCU

Enter the project folder and ensure that `simulator.py` is reading from the correct `COM` Port.

Run these 2 commands in 2 separate terminal windows:

`python controller_sim.py`

`streamlit run hmi_app.py`

## Technical Details

Further details related to the working of different libraries will be mentioned in other files in this folder.
