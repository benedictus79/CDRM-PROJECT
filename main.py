# Import dependencies
from flask import Flask, render_template, request
import scripts

# Create database if it doesn't exist
scripts.create_database.create_database()

# Define Flask app object, give template and static arguments.
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

# Route for root '/'
@app.route("/", methods=['GET'])
def main_page():
    if request.method == 'GET':
        return render_template('index.html')


# Route for '/cache'
@app.route("/cache", methods=['GET'])
def cache_page():
    if request.method == 'GET':
        return render_template('cache.html')


# Route for '/faq'
@app.route("/faq", methods=['GET'])
def faq_page():
    if request.method == 'GET':
        return render_template('faq.html')


# If the script is called directly, start the flask app.
if __name__ == '__main__':
    app.run(debug=True)
