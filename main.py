#!/bin/python3
from flask import Flask, render_template, redirect, request, send_from_directory, abort, send_file, session
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from sys import argv

HELP = """
--help, -h              : Show this message and then exit.
--disable-uploads, -d   : Disables the dability to upload files.
--password <str>        : Enables password protection for the server.
--port, -p <int>        : Changes which port the server runs on
"""
# Arg parsing
# First, merge words so passwords can have spaces
previous_arg = ''
new_argv = []
for arg in argv:
    if not previous_arg.startswith('-') and not arg.startswith('-'):
        arg = ' '.join((arg, previous_arg))
    previous_arg = arg
long_args = []
short_args = []
for arg in argv:
    if arg.startswith('--'):
        long_args.append(arg[2:])
    elif arg.startswith('-'):
        short_args.append(arg[1:])
# Arg handling
if 'help' in long_args or 'h' in short_args:
    print(HELP)
    quit()
if 'disable-uploads' in long_args or 'd' in short_args:
    DISABLE_UPLOADS = True
else:
    DISABLE_UPLOADS = False
if 'password' in long_args:
    PASSWORD = argv[argv.index('--password')+1]
else:
    PASSWORD = None
if 'port' in long_args:
    PORT = int(argv[argv.index('--port')+1])
elif 'p' in short_args:
    PORT = int(argv[argv.index('-p')+1])
else:
    PORT = 7654

app = Flask(__name__, static_url_path='/57471(-455375')

@app.before_request
def check_pw():
    if PASSWORD:
        base_path = request.path.split('/')[1]
        if not session.get('authenticated') and not base_path in ('submit_password', '57471(-455375'):
            return render_template('password.html', failed=False, redirect=request.path)

@app.route('/submit_password', methods=['POST'])
def validate_pw():
    pw = request.form.get('password')
    if pw == PASSWORD:
        session['authenticated'] = True
        return redirect(request.args.get('redirect'))
    else:
        return render_template('password.html', failed=True, redirect=request.args.get('redirect'))

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

    return render_template('index.html', dir=fmtdir, path=path, root=os.path.basename(os.getcwd()), disable_upload_button=DISABLE_UPLOADS)

@app.route('/<path:path>/upload', methods=['POST'])
def savefile(path):
    # Makes sure uploads are enabled
    if DISABLE_UPLOADS:
        return 'Uploads not allowed', 401
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

@app.route('/favicon.ico')
def send_icon():
    return redirect('/57471(-455375/img/icon.ico')

if __name__ == '__main__':
    app.secret_key = os.urandom(16)
    app.run(host='0.0.0.0', port=PORT)
