Before running the program, makesure that the system is installed with python 2.7 or above.

Run the setup.bat file to start installation of all packages and configure them.

If some packages arnt installing, try installing the specific packages alone

pip install <package_name>

if the error continues, download the whl file.

The url below links to all the archives, find the required package by searching the list and download correct version as specified in the requirments.txt file.

https://www.lfd.uci.edu/~gohlke/pythonlibs/

then use pip install filename.whl

You can run the setup.bat file multiple times.

If there are no errors during the setup process, run the main.py file.

the chatbot should start working,

If there is some errors regarding, 

Go to cmd and type the following one by one:

python

import nltk

nltk.download('all')

Ctrl Z

Enter

Try running the chatbot, It should work properly.



The chatbot get input using voice and in some cases will ask to confirm by typing the requests.

Please follow the following while typing:

Use of dates and time:

date must be strictly DD.MM.YYYY or d.m.yy
time can be '6 am', '06:00', '6 o clock', etc...

Currently the chat bot can set reminders and create events, find attendence of specific department and year. 


