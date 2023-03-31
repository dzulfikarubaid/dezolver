from flask import Flask,render_template,request, Response
import requests
from bs4 import BeautifulSoup
import cv2

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def scrape():
    data = []
    if request.method == 'POST' and 'q-url' in request.form:
        key = request.form.get('q-url')
        headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }
        page = requests.get(key, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        lists = soup.findAll('script')
        for list in lists:
            if 'videoUrl' in list.text:
                videoUrl = list.text.strip()
                index = videoUrl.find("videoUrl")
                start_index = index+12
                end_index = start_index+36
                videoUrl = videoUrl[start_index:end_index]

                result = 'https://cdn.numerade.com/encoded/{}.mp4'.format(videoUrl)
                result = requests.get(result,headers=headers)
                if result.status_code == 200:
                    result = 'https://cdn.numerade.com/encoded/{}.mp4'.format(videoUrl)
                    data.append(result)
                    
                else:
                    result = 'https://cdn.numerade.com/ask_video/{}.mp4'.format(videoUrl)
                    data.append(result)
    data = ''.join(data)
    data = str(data)
    
    return render_template("index.html", output=data)

camera=cv2.VideoCapture(0)

def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')