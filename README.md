# Focus Pocus Pipeline

Application used to monitor user focus during study sessions and provide neurofeedback using brain computer interfaces.

## Setup
- install python 3.9
- create virtual environment

`python3 -m venv venv`
this will create a directory \venv

to activate the environment on windows
`.\venv\Scripts\Activate.ps1`

to activate the environment on mac
`source venv/Scripts/activate`

- install packages
`pip install -r requirements.txt`

- run pipeline
you need to find the com port on which the dongle is connected. 
    - on windows you can look at device manager for a serial port. 
    - on mac you can run the following and find which port folder is open
    ` ls /dev/tty.*`

run the script using the port you found above
`python focus.py --port <port>`

## Pipes
to write a new pipe create a python file in \pipes and create one function. the input to the function will be an array of raw eeg data sampled at a specified interval. Examples are in the \pipes.




