import requests
import urllib
import time

# API endpoint
API_ENDPOINT = "https://api.synthesia.io/v1/videos"

API_KEY = "f24e4df1a2aedb9445a4a93ff6100b5a"

def video_id():

    source_code = '{ "test": true, "input": [{ "script": "Hello, World! This is my first synthetic video, made with the Synthesia API!", "actor": "anna_costume1_cameraA", "background": "green_screen"}] }'

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

# running the function
download_video(video_url(video_id()), "videos", str(1))