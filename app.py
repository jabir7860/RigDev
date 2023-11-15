from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient("mongodb+srv://user1:user123@cluster0.sj86x92.mongodb.net/", server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Connected to MongoDB")

    db = client['UserData']
    userdata = db['contactInfo']

except Exception as e:
    print(e)


@app.route('/', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        # Access form data
        username = request.form['username']
        email = request.form['email']
        phone_number = request.form['phone_number']
        time_to_contact = request.form['time_to_contact']
        message = request.form['message']

        contact_info = {
            'username': username,
            'email': email,
            'phone_number': phone_number,
            'time_to_contact': time_to_contact,
            'message': message
        }

        try:
            result = userdata.insert_one(contact_info)
            if result.inserted_id:
                return redirect(url_for('success'))
            else:
                return redirect(url_for('error'))

        except Exception as e:
            return render_template('error.html', error_message=str(e))

    return render_template('contact_form.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/error')
def error():
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
