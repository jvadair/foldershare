#!/bin/python3
from flask import Flask, render_template, redirect, request, send_from_directory, abort, flash
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/57471(-455375')

@app.route('/<path:path>/')  # :path makes it work properly
def index(path):
    if not os.path.exists(path) and path != '':
        return abort(404)
    if os.path.isfile(f'./{path}'):
        return send_from_directory(os.getcwd(), path)
    wrkdir = os.listdir(f'./{path}')
    fmtdir = {}
    for file in wrkdir:
        stats = {}
        stats['created'] = datetime.fromtimestamp(os.path.getctime(f'./{path}/{file}')).strftime('%x')
        stats['modified'] = datetime.fromtimestamp(os.path.getmtime(f'./{path}/{file}')).strftime('%x')
        if os.path.isfile(f'./{path}/{file}'):
            stats['type'] = 'file'
        elif os.path.isdir(f'./{path}/{file}'):
            stats['type'] = 'dir'
        elif os.path.islink(f'./{path}/{file}'):
            stats['type'] = 'link'
        fmtdir[file] = stats

    return render_template('index.html', dir=fmtdir, path=path, root=os.path.basename(os.getcwd()))

@app.route('/<path:path>/upload', methods=['POST'])
def savefile(path):
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        print('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(path, filename))
        return redirect(f'.')

@app.route('/')
def main_reroute():
    return index('')

@app.route('/upload', methods=['POST'])
def upload_reroute():
    return savefile('')

if __name__ == '__main__':
    app.secret_key = os.urandom(16)
    app.run(host='0.0.0.0', port='7654')
