from flask import Flask
from flask import request
from sysiden.sysiden import *


app = Flask(__name__)


@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		if 'trajectories' in request.files.keys() and 'cutoff_value' in request.form.keys():
			f = request.files['trajectories']
			cutoff_value = float(request.form['cutoff_value'])
			max_degree = int(request.form['max_degree'])
			result = identify_system(f, cutoff_value, max_degree)

		else:
			return '400; Bad request: the request must provide a file in with the "trajectories" key', 400
	return result, 200

if __name__ == "__main__":
	app.run(debug=True)