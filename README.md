# ABB HMI Simulator

## Introduction

This folder contains all versions of the ABB HMI Simulator assigned during the EngineeredX Event.
This project is to design a Human Machine Interface which has graphical controls and can be used to control industrial machines. In this example, I have taken the case of a simple water tank.
This `README.md` file applies to Part_1 of this project. A separate `README.md` file exists within Part_2 of this project folder.

## Working

The water tank should have 2 controls:

1. Manual Mode    :    Manually switch the water pump ON or OFF according to human judgement of the water level in the tank.
2. Automatic Mode :    The controller / simulator will decide whether to turn the water pump ON or OFF absed on thresholding values.

To implement this software-level project, Python and its libraries are used.

## Tech Stack

1. Language  :    `Python 3.13.13`
2. Libraries :    `PyModBus`, `Streamlit`, `Threading`, `Time`, `Collections`
3. OS        :    `Ubuntu 24.02` on `WSL2`

Ensure that the above libraries are present before implementing this project.

## How To Run The Project

Enter the project folder and run these 2 commands in 2 separate terminal windows:

`python controller_sim.py`

`streamlit run hmi_app.py`

## Technical Details

Further details related to the working of different libraries will be mentioned in other files in this folder.