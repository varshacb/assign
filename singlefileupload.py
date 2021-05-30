import os
from flask import Flask, flash, request, redirect, render_template, escape
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.secret_key = 'secret key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt'


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/view/<file>')
def view_file(file):
    with open(f'uploads/{file}') as f:
        lines = []
        for l in f.readlines():
            l=l.strip()
            if l not in lines:
                lines.append(l)

    return render_template(
        'display.html', 
        filename=file,
        lines=lines
    )

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f'File successfully uploaded, view <a href="/view/{filename}">here</a>.') # Add a link here
            return redirect('/')
        else:
            flash('Please select a .txt file.')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host = '127.0.0.1', port=5000, debug=True)
