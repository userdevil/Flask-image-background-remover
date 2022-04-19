from flask import*
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config["UPLOAD_FOLDER"] = "static/"

@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/success', methods = ['GET', 'POST'])
def display_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)

        f.save(app.config['UPLOAD_FOLDER'] + filename)

        file = open(app.config['UPLOAD_FOLDER'] + filename,"rb")
        content = file.read()
        import requests
        import random

        n = random.choice([1,2,3,4,5,6,7,8,9])
        num = str(n)
        path = app.config['UPLOAD_FOLDER'] + filename
        response = requests.post(
          'https://api.remove.bg/v1.0/removebg',
           files={'image_file': open(path, 'rb')},
           data={'size': 'auto'},
           headers={'X-Api-Key': 'KRAwgLBL583cxtaZ5UdQf32k'},
        )
        if response.status_code == requests.codes.ok:
               name = filename +'-Remove.png'
               with open(name, 'wb') as out:
                out.write(response.content)
               return send_file(name, as_attachment=True)
        else:
           print("Error:", response.status_code, response.text)
           er = "Error:", response.status_code, response.text
           flash(er, 'error')

    return render_template('index.html')
     		
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
