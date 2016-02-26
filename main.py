import os
import sys
sys.path.append('lib')
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    #create_file('naks')
    return '<form method="POST">XPLAN ID<input name="text"><input type="submit" value="submit"></form>'

@app.route("/", methods=['POST'])
def echo():
	aa = request.form['text']
    	aa = aa.strip()
	os.chdir('lib')
    	os.system('./client_partner_detailsV2.py "' + aa + '"')
    	aa = os.popen('cat test2.json').read()
    	return aa

if __name__ == "__main__":
	while True:
		app.run(host='0.0.0.0', port=8080, debug=True)

#sudo kill -9 `ps -fA |grep hello | awk '{print $2}'`
