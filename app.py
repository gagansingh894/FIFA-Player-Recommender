from flask import Flask, render_template, request, url_for
from RecommendationsEngine import Recommendations
import time
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, root_path=dir_path)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
incorrectResult = [(0,0,0,0,0,0), [(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0), (0,0,0,0,0,0)],
				   [(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0), (0,0,0,0,0,0)],
				   [(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0), (0,0,0,0,0,0)],
				   [(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0),(0,0,0,0,0,0), (0,0,0,0,0,0)]]

msg = "Player does not exist in database!"
noResult = [(msg,msg,msg,msg,msg,msg), [(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg), (msg,msg,msg,msg,msg,msg)],
				   [(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg), (msg,msg,msg,msg,msg,msg)],
				   [(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg), (msg,msg,msg,msg,msg,msg)],
				   [(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg),(msg,msg,msg,msg,msg,msg), (msg,msg,msg,msg,msg,msg)],]


# app = Flask(__name__)
	
# @app.route('/')
# def hello_world():
# 	return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def getRecommendations():
	try:
		if request.method == 'POST':
			recommend = Recommendations(5)
			form_name = request.form.get('pfname')
			# form_club = request.form.get('pclub')
			# form_nationality = request.form.get('pnationality')
			# form_mval = request.form.get('pmval')
			# if len(form_mval) == 0:
			# 	form_mval = -1
			# else:
			# 	form_mval = int(form_mval)
			recommendedNames = recommend.getTopKSimilar(name = form_name)
			if recommendedNames is not None:
				searchedName = recommendedNames[-1]
				return render_template('/index.html' , recommendedNames=recommendedNames, searchedName=searchedName)
			else: 
				# recommendedNames = [[(msg)],[(msg)],[(msg)],[(msg)],[(msg)]]
				# recommendedNames = [[("Loading..")],[("Loading..")],[("Loading..")],[("Loading..")],[("Loading..")]]
				return render_template('/index.html', recommendedNames=noResult)
		else:		
			return render_template('/index.html', recommendedNames=incorrectResult) 

	except:
			# msg = "error"
			# recommendedNames = [[(msg)],[(msg)],[(msg)],[(msg)],[(msg)]]
			return render_template('/index.html', recommendedNames=recommendedNames)

if __name__ == "__main__":
	app.run(debug=True)