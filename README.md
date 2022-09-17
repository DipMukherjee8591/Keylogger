
# Simple Keylogger using Python

Keylogger is a powerful python tool to track the records of a user by capturing their 
key strokes, clipboard information, sysytem information, screenshots. It acan also 
send emails to your email address, so that once the keylogger is running, you don't 
need to access the system manually.


## Installation

1. Clone the project using-
```bash
  git clone https://github.com/DipMukherjee8591/Keylogger.git
```
2. Run the program with-
```bash
  python keylogger.py
```
You need to input several arguements to run the program. To get more information you can use
-h arguement. 

You can also convert Keylogger to EXE using PyInstaller or any similar tool.
    
## Note
You need to install following modules in the system before running the program-
    
    pywin32
    pynput
    requests
    pillow
This modules can simply install by using-

    pip install module_name

Also, there is another thing regarding sending mails using gmail. You need to activate 2FA and 
generate app password for Python to use the program. The app password is required in the 
program to continue.