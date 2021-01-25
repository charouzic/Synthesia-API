import requests
from requests.auth import HTTPBasicAuth



# API endpoint
API_ENDPOINT = "https://api.synthesia.io/v1/videos"

API_KEY = "f24e4df1a2aedb9445a4a93ff6100b5a"

def video_post():

    source_code = '{ "test": true, "input": [{ "script": "Hello, World! This is my first synthetic video, made with the Synthesia API!", "actor": "anna_costume1_cameraA", "background": "green_screen"}] }'

    header = {'authorization': API_KEY,
              'content-type': 'application/json'}


    # sending post request and saving response as response object
    r = requests.post(url = API_ENDPOINT, data = source_code, headers = header) 

    # extracting response text  
    pastebin_url = r.text 

    # id of the video -> later for the download
    video_id = r.json()['id']

    # this line prints the response of the API
    print("The pastebin URL is:%s"%pastebin_url) 
    print("The ID is:%s"%video_id) 


#def video_get(id ,path)
params = dict(authorization=API_KEY)
print(params)
API_ENDPOINT_GET = "https://api.synthesia.io/v1/videos/7fb0000a-8088-499c-bdec-a30b37a77b79" 
r = requests.get(url = API_ENDPOINT_GET, headers=params)
pastebin_url = r.json()
download_link = r.json()['download']
print("The pastebin URL is:%s"%pastebin_url) 
print("The download link is:%s"%download_link)
