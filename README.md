# KEYLOGGER
A simple keylogger made in python.

## Requirements
- Pillow
- pynput
- python-dotenv
- pywin32
- requests

You can install these requirements by running the following command in terminal : 

`pip install -r requirements.txt`

## Usage

To run the program do the following : 
- Copy the `.env_example` file and rename it to `.env`.
- Fill out the variables within the file.
- Run the script with the following command : `python keylogger.py -f "LOG LOCATION' -n "NO OF ITERATION"`

### .env file
The variables in the file is as follows.

```
SENDER=
RECEIVER=
PASSWORD=
```
- SENDER : the email address from which you are going to send the log files. (gmail only)
- RECEIVER : the email address of the receiver the sender is sending the mail to.
- PASSWORD : Application password of your google account. [Here](https://towardsdatascience.com/automate-sending-emails-with-gmail-in-python-449cc0c3c317) is how you can create one.

### Command line arguments (required)

There are two arguments available and both are required.

- `-f/--filepath` : The file path in raw string you want to save all of the keylogger files.
- `-n/--loopno` : The no of iteration(integer value only) you want to use to send mails and run all other functions.

## Credits
Created with ❤ by [DipMukherjee8591](https://github.com/DipMukherjee8591)

README and venv added by [ShambaC](https://github.com/ShambaC)


# DISCLAIMER

This project was not created with the intention to harm any entity. This was created purely for educational purposes. The author is not responsible for any harm done with the files in this repository.