import argparse
import csv
import requests
import urllib
import time


# Initiate the parser
parser = argparse.ArgumentParser()

# mandatory argument
parser.add_argument("-s", "--script", help="script containing the video message", required=True)
# optional argument
parser.add_argument("-b", "--background", help="background of the video", required=True)
# optional argument
parser.add_argument("-d", "--data", help="path to csv file with data", required=True)
# mandatory argument
parser.add_argument("-o", "--output", help="output path for saving the video", required=True)

# example input
# personalise -s “Hey {name}. I just made my first synthetic video, made with the Synthesia API!” -b background.jpg -d data.csv -o videos

# Read arguments from the command line
args = parser.parse_args()

backgrounds = ["off_white", "warm_white", "light_pink", "soft_pink", "light_blue", "dark_blue", "soft_cyan", "light_orange", "soft_orange",
                "white_studio", "white_cafe", "luxury_lobby", "large_window", "white_meeting_room", "open_office"]

# API endpoint
API_ENDPOINT = "https://api.synthesia.io/v1/videos"

API_KEY = "f24e4df1a2aedb9445a4a93ff6100b5a"

def video_id(script):

    source_code = ' {"test": true, "input": [{ "script": "%s", "actor": "anna_costume1_cameraA", "background": "green_screen"}] }'%script
    header = {'authorization': API_KEY,
              'content-type': 'application/json'}

    # sending post request and saving response as response object
    r = requests.post(url = API_ENDPOINT, data = source_code, headers = header) 

    # extracting response text  
    pastebin_url = r.text 
    # id of the video -> later for the download
    vid_id = r.json()['id']
    return str(vid_id)

def video_url(id):
    params = dict(authorization=API_KEY)
    API_ENDPOINT_GET = "https://api.synthesia.io/v1/videos/" + id 
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

with open(args.data, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    ids = []
    names = []
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        ids.append(row['id'])   # ['1', '2']
        names.append(row['name']) # ['Jakob', 'Garry']
        line_count += 1

for i,n in zip (ids, names):
    inserted_script = args.script.replace("{name}", n)
    # running the function
    print("Creating video...")
    download_video(video_url(video_id(inserted_script)), args.output, i)
