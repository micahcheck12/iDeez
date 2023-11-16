from flask import Flask, flash, redirect, render_template, request, session

from urllib.parse import urlparse, parse_qs

from googleconnect import videoid, channelid, number


app = Flask(__name__)
app.secret_key = '8627895d4de75d0ceabd9fae7c2d3c51786653b77ed970a08946d84f895b12f4'


app.jinja_env.filters["number"] = number

##mail = Mail(app)

@app.route("/", methods=["GET", "POST"])
def getid():
    if request.method == "POST":
        
        video_results = None 
        channel_results = None
        
        url = request.form.get("link")
        
        parsed_url = urlparse(url)
    
        if parsed_url.netloc == "www.youtube.com":

            query_params = parse_qs(parsed_url.query)

            if 'v' in query_params:

                url_video_id = query_params.get('v', [''])[0]

                my_video_id = url_video_id.split('&ab')[0]

                video_results = videoid(my_video_id)

                my_channel_id = video_results["channelId"]

                channel_results = channelid(my_channel_id)
        
        if parsed_url.netloc == "youtu.be":
            
            my_video_id = parsed_url.path[1:]
         
            video_results = videoid(my_video_id)

            channel_results = channelid(video_results["channelId"])


        if video_results != None:
            return render_template("getid.html", video_results = video_results, channel_results = channel_results)
        
        else:
            flash("Invalid URL. Please enter a valid YouTube video or channel URL.")
            return render_template("index.html")
        
        
    else:
        return render_template("index.html")
    
@app.route("/about")
def about():  
    return render_template('about.html')

@app.route("/contact", methods=["GET", "POST"])
def contact():  
    if request.method == "POST":
        return "Sent message"
    return render_template('contact.html')
