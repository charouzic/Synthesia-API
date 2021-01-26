#!/usr/bin/python3

import argparse
import csv
import requests
import urllib
import time
import subprocess
import os
from PIL import Image
import json



def argument_parser():
    # Initiate the parser
    parser = argparse.ArgumentParser()

    # mandatory argument
    parser.add_argument("-s", "--script", help="script containing the video message (e.g.: 'Hello {name}, this is my first Synthesia video')", required=True)
    # optional argument
    parser.add_argument("-b", "--background", help="jpg file of background of the video in resolution 1920x1080 (e.g.: data/background.jpg)", required=True)
    # optional argument
    parser.add_argument("-d", "--data", help="path to csv file with data (e.g.: data/data.csv)", required=True)
    # mandatory argument
    parser.add_argument("-o", "--output", help="output path for saving the video", required=True)

    # example input
    # personalise -s “Hey {name}. I just made my first synthetic video, made with the Synthesia API!” -b background.jpg -d data.csv -o videos

    # Read arguments from the command line
    args = parser.parse_args()
    return (args)



def sripts_from_csv(path, script):
    # creating list of csv data
    csv_fields = []
    csvReader = csv.reader(open(path), delimiter=',')
    for row in csvReader:
        csv_fields.append(row)

    id_list = [i[0] for i in csv_fields[1:]]
    
    to_be_replaced = []
    for x in csv_fields[0][1:]:
        to_be_replaced.append("{" + x + "}") 

    n=1
    output_scripts = []
    while n < len(csv_fields):
        temp_script = script
        for f,r in zip(csv_fields[n][1:],to_be_replaced):
            output_script = temp_script.replace(r,f)
            temp_script = output_script
        n += 1
        output_scripts.append(output_script) 
    return (output_scripts, id_list)

def video_id(script, api_key, api_endpint):

    source_code = ' {"test": true, "input": [{ "script": "%s", "actor": "anna_costume1_cameraA", "background": "green_screen"}] }'%script
    header = {'authorization': api_key,
              'content-type': 'application/json'}

    # sending post request and saving response as response object
    r = requests.post(url = api_endpint, data = source_code, headers = header) 

    # extracting response text  
    pastebin_url = r.text 
    # id of the video -> later for the download
    vid_id = r.json()['id']
    return str(vid_id)

def video_url(id, api_key, api_endpint):
    params = dict(authorization=api_key)
    API_ENDPOINT_GET = f"{api_endpint}/{id}" 
    r = requests.get(url = API_ENDPOINT_GET, headers=params)
    while r.json()['status']=="IN_PROGRESS":
        time.sleep(10)
        r = requests.get(url = API_ENDPOINT_GET, headers=params)

    print("Video created")
    download_link = r.json()['download']
    return str(download_link)

def download_video(download_url, output_path, file_name):
    r = requests.get(download_url)
    export_path = f"{output_path}/{file_name}.mp4"
    with open(export_path, 'wb') as f:
        f.write(r.content)  
        print("File succesfully downloaded: %s"%export_path)
    
    change_background(args.background, args.output, file_name)


def change_background(background_img, file_path, file_name):

    video_path = f"{file_path}/{file_name}.mp4"
    output_file = f"{file_path}/tmp_{file_name}.mp4"
    
    # 1. change the background
    print("Changing background...")
    # the color filter is not the best --> place for improvement
    subprocess.call(f'ffmpeg -i {background_img} -i {video_path} -filter_complex "[1:v]chromakey=0x3BBD1E:0.1:0.2[ckout];[0:v][ckout]overlay[o]" -map [o] -map 1:a {output_file}', shell=True)

    # 2. delete the original video
    subprocess.call(f"rm {video_path}", shell=True)

    # 3. rename the new file
    subprocess.call(f"mv {output_file} {video_path}", shell=True)

    print("\nVideo successfully created: %s"%video_path)


def image_size_check(img):
    im = Image.open(img)
    width, height = im.size
    if width == 1920 and height == 1080:
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        # loading config.json
        config = json.load(open("config.json"))
        API_KEY = config["API_KEY"]
        API_ENDPOINT = config["API_ENDPOINT"]

        args = argument_parser()
        if not os.path.exists(args.data):
            print("Data file does not exist")
            exit()
        if not os.path.exists(args.output):
            print("Output path does not exist")
            exit()
        if not os.path.exists(args.background):
            print("Background image file does not exist")
            exit()
        if image_size_check(args.background) == False:
            print("Background image does not have resolution 1920x1080")
            exit()

        scripts_and_ids = sripts_from_csv(args.data, args.script)
        scripts = scripts_and_ids[0]
        ids = scripts_and_ids[1]

        for i,script in zip (ids, scripts):
            print("\nCreating video...")
            download_video(video_url(video_id(script, API_KEY, API_ENDPOINT), API_KEY, API_ENDPOINT), args.output, i)
    except Exception as e:
        print("Error occured: %s"%e)



