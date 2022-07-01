# foldershare build script for windows & linux
# NOT TESTED ON WINDOWS!
# might work on Mac
import os
import shutil

linux_cmd = """pyinstaller -w -F --add-data "templates:templates" --add-data "static:static" -n foldershare main.py"""
windows_cmd = """pyinstaller -w -F --add-data "templates;templates" --add-data "static;static" -n foldershare main.py"""

if os.name == 'nt':
    os.system(windows_cmd)
    shutil.rmtree('build')
    os.remove('foldershare.spec')
    os.rename('dist/foldershare.exe', 'foldershare.exe')
    shutil.rmtree('dist')
    print('Move the exe into the folder you want to share and then run it!')
else:
    os.system(linux_cmd)
    shutil.rmtree('build')
    os.remove('foldershare.spec')
    os.rename('dist/foldershare', 'foldershare')
    shutil.rmtree('dist')
    print('Run the file in the working directory you want to share!')