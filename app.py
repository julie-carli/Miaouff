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

@app.route('/terms_and_conditions')
def terms_and_conditions():
    return render_template('terms_and_conditions.html')

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/cookies_policy')
def cookies_policy():
    return render_template('cookies_policy.html')

if __name__ == '__main__':
    app.run(debug=True)
