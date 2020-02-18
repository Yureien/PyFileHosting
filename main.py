from flask import Flask, render_template, request, url_for, make_response
from random import sample
import string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "/mnt/ofc.wlpizza_storage"
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Max 100 MB.
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')


@app.route('/', methods=['GET', 'POST'])
def index():
    authtoken = request.cookies.get('auth')
    if not authtoken or authtoken != AUTH_TOKEN:
        return "No."
    return render_template('index.html', auth_token=authtoken)


@app.route('/upload', methods=['POST'])
def upload():
    authtoken = request.form.get('auth')
    if not authtoken or authtoken != AUTH_TOKEN:
        return "Error: Not Authorized."
    fileob = request.files["file"]
    fext = secure_filename(fileob.filename).split('.')[-1].lower()
    filename = "{}.{}".format(''.join(sample(string.ascii_letters + string.digits, 6)), fext)
    save_path = "{}/{}".format(app.config["UPLOAD_FOLDER"], filename)
    fileob.save(save_path)
    return request.url_root + 'files/' + filename


@app.route('/authme/<auth>')
def authme(auth):
    resp = make_response("Done! Set auth to: " + auth)
    resp.set_cookie('auth', auth)
    return resp