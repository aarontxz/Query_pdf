from flask import Flask, request, jsonify, render_template
import json
import os
from llama import create_tree_index_query_engine, create_list_index_query_engine
import pandas as pd
from langchain.llms import OpenAI
import os

##os.environ["OPENAI_API_KEY"] = "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"
# Load the BART model
llm = OpenAI()


uploaded_files = []

for file_name in os.listdir('data'):
    # Add the file name to the list
    uploaded_files.append(file_name)

try:
    db = create_tree_index_query_engine()
except:
    db = None

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('frontend.html', uploaded_files=uploaded_files)


import datetime

@app.route('/dbQuery', methods=['POST'])
def dbQuery():
    data = request.get_json()
    user_input = data['input_string']
    reply = db.query(user_input)
    reply = str(reply)
    prompt = 'relevant data will be provided, ' + user_input + ' relevant data: ' + str(reply)
    full_sentence = llm.predict(prompt)
    full_sentence = reply
    # Log user input and full sentence
    time = f"[{datetime.datetime.now()}]\n"
    first = f"prompt: {prompt}\n"
    second = f"output: {full_sentence}\n"
    with open('log.txt', 'a') as log_file:
        log_file.write(time)
        log_file.write(first)
        log_file.write(second)
        log_file.write('----------------------\n')

    return jsonify({'full_sentence': full_sentence})


@app.route('/upload', methods=['POST'])
def upload():
    global db
    file = request.files['fileUpload']  # Get the uploaded file
    filename = file.filename
    # Save the file to the data folder
    upload_directory = os.path.join(os.getcwd(), 'data')  # Assumes 'data' folder is in the same directory as the Python file
    if not os.path.exists(upload_directory):
        os.makedirs(upload_directory)
    file_path = os.path.join(upload_directory, filename)
    file.save(file_path)
    
    if filename not in uploaded_files:
        uploaded_files.append(filename)  # Store the filename in the list
    db = create_tree_index_query_engine()
    return jsonify({'success': True, 'uploaded_files': uploaded_files})

@app.route('/fileList')
def file_list():
    return jsonify({'uploaded_files': uploaded_files})

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)