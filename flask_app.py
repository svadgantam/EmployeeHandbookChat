# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:24:13 2023

@author: tomah
"""

from flask import Flask, request, render_template, jsonify, Response
from werkzeug.utils import secure_filename
from ChatBot import process_pdf_query

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return process_pdf_query(input)


if __name__ == '__main__':
    app.run()


    
    
        
