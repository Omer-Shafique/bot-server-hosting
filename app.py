from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from bot import process_file

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Variables to track bot progress and last message data
people_covered = 0
messages_sent = 0
bot_status = "Idle"
last_person_username = None
last_message_sent = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global people_covered, messages_sent, bot_status, last_person_username, last_message_sent

    if request.method == 'POST':
        return redirect(url_for('upload_file'))

    return render_template('index.html',
                           people_covered=people_covered,
                           messages_sent=messages_sent,
                           bot_status=bot_status,
                           last_person_username=last_person_username,
                           last_message_sent=last_message_sent)

@app.route('/upload', methods=['POST'])
def upload_file():
    global people_covered, messages_sent, bot_status, last_person_username, last_message_sent

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the uploaded file
        process_file(file_path)

        # Update variables based on the bot progress
        # You might want to fetch this data from the bot processing logic
        people_covered += 1
        messages_sent += 1
        bot_status = "Running"
        last_person_username = "JohnDoe"  # Example username
        last_message_sent = "Hello, how are you?"  # Example message

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)