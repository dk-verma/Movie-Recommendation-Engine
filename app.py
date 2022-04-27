# from ensurepip import bootstrap
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
# import recommendation as src
from recommendation import bestRatingNMovies, collabRecommendation, genreBestNMovies
# from flask_ngrok import run_with_ngrok

app = Flask(__name__)
Bootstrap(app)
# bootstrap(app)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/predict1',methods=['POST'])
def predict1():
    '''
    For rendering results from HTML GUI
    '''
    if request.method == 'POST':
        if request.form["suggest"]:
            total = int(request.form["suggest"])
        else:
            total= 5
        # df = bestRatingNMovies(total)
        name = request.form["m_nm"]
        df = collabRecommendation(name,total)

        return render_template('base.html',tables=[df.to_html(classes='data')], titles=['1'])

@app.route('/predict2',methods=['POST'])
def predict2():
    '''
    For rendering results from HTML GUI
    '''
    if request.method == 'POST':
        if request.form["suggest"]:
            total = int(request.form["suggest"])
        else:
            total= 5
        genre = request.form["gnr"]
        df = genreBestNMovies(genre,total)

        return render_template('base.html',tables=[df.to_html(classes='data')], titles=['1'])

@app.route('/predict3',methods=['POST'])
def predict3():
    '''
    For rendering results from HTML GUI
    '''
    if request.method == 'POST':
        if request.form["suggest"]:
            total = int(request.form["suggest"])
        else:
            total= 5
        df = bestRatingNMovies(total)

        return render_template('base.html',tables=[df.to_html(classes='data')], titles=['1'])

if __name__ == '__main__':
    app.run(debug=True)

# run_with_ngrok(app) 
# app.run()

