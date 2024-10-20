from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/animals')
def animals():
    return "Page des animaux"

@app.route('/products')
def products():
    return "Page des produits"

@app.route('/blog')
def blog():
    return "Blog"

@app.route('/faq')
def faq():
    return "FAQ"

if __name__ == '__main__':
    app.run(debug=True)
