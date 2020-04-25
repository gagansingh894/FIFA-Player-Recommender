from flask import Flask, render_template, request
from RecommendationsEngine import Recommendations

app = Flask(__name__)


@app.route('/')
def hello_world():
	return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def getRecommendations():
	recommend = Recommendations(25)	
	if request.method == 'POST':
		form_name = request.form.get('pfname')
		form_club = request.form.get('pclub')
		form_nationality = request.form.get('pnationality')
		form_mval = request.form.get('pmval')
		if len(form_mval) == 0:
			form_mval = -1
		else:
			form_mval = int(form_mval)

	recommendedNames = recommend.getTopKSimilar(name = form_name, club=form_club, nationality=form_nationality, mval=form_mval)
	return render_template('index.html', recommendedNames=recommendedNames)

if __name__ == "__main__":
	app.run(debug=True)