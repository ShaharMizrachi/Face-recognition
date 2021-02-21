import subprocess

def install(name):
    subprocess.call(['pip', 'install', name])

list = ['cmake' , 'face-recognition']
for l in list:
    install(l)