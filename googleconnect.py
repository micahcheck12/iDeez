from flask import current_app as app 

import os


import googleapiclient.discovery
import googleapiclient.errors
import google_auth_oauthlib.flow

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def channelid(my_channel_id):

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    developerKey = app.config["GOOGLEDEVELOPERKEY"]

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developerKey)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=(my_channel_id)
    )
    response = request.execute()

    myitem = response["items"][0]

    channel_data = {
    "id": myitem["id"],
    "title": myitem["snippet"]["title"],
    "customUrl": myitem["snippet"]["customUrl"],
    "publishedAt": myitem["snippet"]["publishedAt"],
    "viewCount": myitem["statistics"]["viewCount"],
    "subscriberCount": myitem["statistics"]["subscriberCount"],
    "videoCount": myitem["statistics"]["videoCount"]
}
    
    return channel_data 

if __name__ == "__main__":
    channelid()



def videoid(video_id):

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    developerKey = app.config["GOOGLEDEVELOPERKEY"]

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developerKey)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=(video_id)
    )
    response = request.execute()

    myitem = response["items"][0]

    video_data = {
        "id": myitem["id"],
        "title": myitem["snippet"]["title"],
        "channel": myitem["snippet"]["channelTitle"],
        "channelId": myitem["snippet"]["channelId"],
        "publishedAt": myitem["snippet"]["publishedAt"],
        "viewCount": myitem["statistics"]["viewCount"],
        "likeCount": myitem["statistics"]["likeCount"],
        "commentCount": myitem["statistics"]["commentCount"]
    }
    
    return video_data 
    
if __name__ == "__main__":
    videoid()

def number(value):
    value=int(value)
    return f"{value:,.0f}"