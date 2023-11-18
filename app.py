from flask import Flask, flash, redirect, render_template, request, session

from urllib.parse import urlparse, parse_qs

from googleconnect import videoid, channelid, number

import smtplib

from email.message import EmailMessage

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
            flash("Invalid URL. Please enter a valid YouTube video.")
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

@app.route("/mail", methods=["GET", "POST"])
def mail():
    if request.method == "POST":

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        message = request.form.get('message')  
        
        html_content = render_template("contactsubmission.html", 
                                       first_name=first_name, 
                                       last_name=last_name, 
                                       email=email, 
                                       message=message)
        
        msg = EmailMessage()
        msg.set_content(html_content, subtype='html')  

        msg['Subject'] = f'iDeez Contact Submission'
        msg['From'] = 'contactideez@gmail.com'
        msg['To'] = 'contactideez@gmail.com'

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.ehlo()
        s.starttls()

        username = 'contactideez@gmail.com'
        password = 'umvc rvif sodl lgrk'
        s.login(username, password)

        s.send_message(msg)
        s.quit()

        return render_template("mailsent.html")

    else:
        return render_template("contact.html")