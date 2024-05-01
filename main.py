# Import dependencies
from flask import Flask, render_template, request
import scripts

# Create database if it doesn't exist
scripts.create_database.create_database()

# Check for .WVD file and assign it a variable
WVD = scripts.wvd_check.check_for_wvd()

# If no WVD found, exit
if WVD is None:
    exit("No .wvd file found, please place one in /databases/WVDs and try again.")

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


# Route for '/login'
@app.route("/login", methods=['GET'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')


# If the script is called directly, start the flask app.
if __name__ == '__main__':
    app.run(debug=True)
