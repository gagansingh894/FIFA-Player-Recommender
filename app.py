from flask import Flask, render_template, request, url_for
from RecommendationsEngine import Recommendations
import time
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, root_path=dir_path)
# app = Flask(__name__)
	
# @app.route('/')
# def hello_world():
# 	return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def getRecommendations():
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
		print(recommendedNames)
		return render_template('/index.html' , recommendedNames=recommendedNames)

	else:
		return render_template('/index.html', recommendedNames=[(0),(0),(0),(0),(0)]) 


	#, club=form_club, nationality=form_nationality, mval=form_mval)
	# recommendedNames = recommend.getTopKSimilar(name = form_name)
	# recommendedNames = recommend.getPlayerNames(name = form_name)	
	#recommendedNames=recommendedNames)

if __name__ == "__main__":
	app.run(debug=True)