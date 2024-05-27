# Import dependencies
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import scripts
import uuid

# Create database if it doesn't exist
scripts.create_database.create_database()

# Check for .WVD file and assign it a variable
WVD = scripts.wvd_check.check_for_wvd()

# If no WVD found, exit
if WVD is None:
    exit("No .wvd file found, please place one in /databases/WVDs and try again.")

# Define Flask app object, give template and static arguments.
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

# Create a secret key for logins
app.secret_key = str(uuid.uuid4())


# Route for root '/'
@app.route("/", methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        decrypt_response = scripts.decrypt.decrypt_content(
            in_pssh=request.json['PSSH'],
            license_url=request.json['License URL'],
            headers=request.json['Headers'],
            json_data=request.json['JSON'],
            cookies_data=request.json['Cookies'],
            wvd=WVD
        )
        return jsonify(decrypt_response)


# Route for '/cache'
@app.route("/cache", methods=['GET', 'POST'])
def cache_page():
    if request.method == 'GET':
        return render_template('cache.html')
    if request.method == 'POST':
        results = scripts.vault_check.check_database(pssh=request.json['PSSH'])
        message = {
            'Message': results
        }
        return jsonify(message)

@app.route("/key_count", methods=['GET'])
def key_count():
    if request.method == 'GET':
        results = scripts.key_count.count_keys()
        results = 'Total Keys: ' + str(results)
        message = {
            'Message': results
        }
        return jsonify(message)

# Route for '/faq'
@app.route("/faq", methods=['GET'])
def faq_page():
    if request.method == 'GET':
        return render_template('faq.html')


@app.route("/api", methods=['GET', 'POST'])
def api_page():
    if request.method == 'GET':
        return render_template('api.html')
    elif request.method == 'POST':
        return

# Route for '/login'
@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        if session.get('logged_in'):
            return redirect('/profile')
        else:
            return render_template('login.html')
    if request.method == 'POST':
        username = request.json['Username']
        if scripts.check_user.check_username_exist(username=username.lower()):
            if scripts.check_user.check_password(username=username.lower(), password=request.json['Password']):
                session['logged_in'] = True
                return {
                    'Message': 'Success'
                }
            else:
                return {
                    'Message': 'Failed to Login'
                }
        else:
            return {
                'Message': 'Username does not exist'
            }


# Route for '/register'
@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.json['Username']
        if username == '':
            return {
                'Message': 'Username cannot be empty'
            }
        if not scripts.check_user.check_username_exist(username=username.lower()):
            scripts.check_user.insert_user(username=username.lower(), password=request.json['Password'])
            session['logged_in'] = True
            return {
                'Message': 'Success'
            }
        else:
            return {
                'Message': 'Username already taken'
            }


# Route for '/profile'
@app.route("/profile", methods=['GET'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')

# If the script is called directly, start the flask app.
if __name__ == '__main__':
    app.run(debug=True)
