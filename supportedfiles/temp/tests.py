import base64
import requests

url = "http://127.0.0.1:8000/cluemedia/"
filename="D:/Projects/SARWeb/static/img/cluesamples/video_topview.png"
#encoded = base64.b64encode(open(filename, "rb").read())
files = {'photo': open(filename, 'rb')}

#post
'''
r=requests.post('http://127.0.0.1:8000/cluemedia/',
    auth=('saradmin','searchandrescue'),
    data = {'id':'3', 'name':'Drone3','longitude':'-80.543407', 'latitude':'37.196209', 'description':'Thermal camera people under the tree'},
    files={'photo':open(filename, 'rb')}
    )
'''
r=requests.patch('http://127.0.0.1:8000/cluemedia/4/',
    auth=('saradmin','searchandrescue'),
    data = {'id':'3', 'name':'Drone3','longitude':'-80.552373', 'latitude':'37.212021', 'description':'Thermal camera people under the tree'},
    files={'photo':open(filename, 'rb')}
    )

print (r.text)
