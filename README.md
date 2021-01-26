# Synthesia Python Script

## Table of contents
* [General Info](#general-info)
* [Requirements](#requirements)
* [Features](#features)
* [Setup](#setup)
* [Place for improvement](#place-for-improvement)


## General Info
This repository contains python script allowing user to programmtically create video using Synthesia API. 
By using this script, you can define the message (script) that will be transfered to message, the background 
of the video, and use csv file for setting up parameters in the script (each line of csv generates one video).


## Requirements
* [Python 3.x](https://www.python.org/downloads/)
* [ffmpeg](https://ffmpeg.org/download.html)
* [Synthesia API access](https://www.synthesia.io/apo)


## Features
* written in Python
* checks that all parameters are filled in (script, data, background, output path)
* checks that all paths exist and are correct
* checks that the image has correct resolution 1920x1080
* fills in the parameters in script from the csv file
* changes the background
* the API key and APII endpoint can be added/editted in the config.json file without changing the code


## Setup
1. clone this repository
2. navigate to the folder with the script personalise.py
3. run command
   ```
   chmod +x personalise.py
   ```
4. run command 
   ```
   cp personalise.py ~/bin/personalise
   ```
   (this makes the command globaly accessible and anytime you run "personalise" in the command line, 
   it should recognize that we want this script to run - reference [here](https://gist.github.com/umangahuja1/51da3a453803f1f67f4eee5de129d4db))
5. run the command for creating the video - e.g.:
   ```
   personalise -s "Hello {name}, how do you like your job as {job}?" -b background.jpg -d data.csv -o videos
   ```
   
   In case the previous steps are not working the script can be alternatively run by directing to the directory with script and then run:
   ```
   python3 personalise.py -s "Hello {name}, how do you like your job as {job}?" -b background.jpg -d data.csv -o videos
   ```


## Place for improvement
The place for improvement is in the exchanging of the background - was not able to find matching colour to the background as it is not pure greenscreen.
