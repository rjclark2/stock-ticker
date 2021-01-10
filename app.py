from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/graph')
def graph():
    print('hello world')

if __name__ == '__main__':
  app.run(port=33507)
