import json, requests

# set our building blocks
client_id = 'dV9pcWcxMUFmZ2ZZT1VXUzM5SWRodzpiMzg4Y2Q5YTVkMTk3Njdi'  # client ID
start_time = '2018-01-01'  # string in ISO format
end_time = '2021-01-01'  # string in ISO format
bbox = "8.573,49.352,8.794,49.459"
#username = 'chrisbeddow'

# API call URL with sort_by=key which enables pagination, insert building blocks
url = (
    'https://a.mapillary.com/v3/images?client_id={}&bbox={}&start_time={}&end_time={}&per_page=1000&sort_by=key').format(
    client_id, bbox, start_time, end_time)

# create an empty GeoJSON to collect all images we find
output = {"type": "FeatureCollection", "features": []}

with open('HD_images_20170101_20210101.geojson', 'w') as outfile:  # set output filename

    # print the API call, so we can click it to preview the first response
    print(url)

    # get the request with no timeout in case API is slow
    r = requests.get(url, timeout=None)

    # check if request failed, if failed, keep trying - 200 is a success
    while r.status_code != 200:
        print("the non200 return code" + str(r.status_code))
        r = requests.get(url, timeout=None)

    data = r.json()  # get a JSON format of the response
    data_length = len(data['features'])  # get a count of how many images
    for feature in data['features']:
        output['features'].append(feature)  # append each image to our empty geojson

    # if we receive 1000 items, response was full and should be a next page
    while data_length == 1000:

        # get the URL for a next page
        link = r.links['next']['url']

        # retrieve the next page in JSON format
        r = requests.get(link)

        # try again if the request fails
        while r.status_code != 200:
            print("the non200 return code" + str(r.status_code))
            r = requests.get(url, timeout=None)

        data = r.json()

        for feature in data['features']:
            output['features'].append(feature)

        print('Total images: {}'.format(len(output['features'])))  # print total count
        data_length = len(data['features'])  # update data length

    # send collected features to the local file
    json.dump(output, outfile)

print('DONE')  # once all images are pushed to a GeoJSON and saved, we finish
