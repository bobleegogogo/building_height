import json, requests
import time
import shutil


def download(key):
    try:
        url = ('https://images.mapillary.com/{}/thumb-2048.jpg').format(key)
        # get the request with no timeout in case API is slow
        r = requests.get(url, stream=all, timeout=None)
        # check if request failed, if failed, keep trying - 200 is a success
        while r.status_code != 200:
            print("sleep 60 seconds for code: " + str(r.status_code))
            time.sleep(60)
            r = requests.get(url, stream=all, timeout=None)
    except Exception as e:
        print(e.message)
        time.sleep(0.5)
    # save r.content
    with open("img/" + key + ".jpg", 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
    # sleep 1 seconds
    time.sleep(0.5)


with open('HD_images_20170101_20210101.geojson') as file:  # set output filename
    file_data = json.load(file)
    feature_list = file_data["features"]
    count = 0
    for feature in feature_list:
        key = feature["properties"]["key"]
        count += 1
        download(key)
        print("done with image: " + str(count))
