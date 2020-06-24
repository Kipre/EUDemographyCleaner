from flask import Flask
from flask import request
import sysiden
from sysiden.sysiden import *


app = Flask(__name__)


@app.route('/', methods=['GET'])
def upload_file():
	if request.method == 'GET':
		if 'the_file' in request.files.keys() and 'cutoff_value' in request.form.keys():
			f = request.files['the_file']
			print(request.form)
			open_csv(f)

		else:
			return '400; Bad request: the request must provide a file in with the "the_file" key', 400
	return 'Hello World'

if __name__ == "__main__":
	app.run(debug=True)