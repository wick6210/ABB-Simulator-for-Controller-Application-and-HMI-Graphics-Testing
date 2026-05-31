# Architecture of the Project

This file contains the architecture flow of this project.

Streamlit HMI -> Modbus TCP -> Controller Simulator -> Virtual Registers -> Finite State Machine


Once the user presses a button, the register changes , the FSM reacts and the tank level changes. All of these will be upgated in the HMI-GUI.
