from __future__ import print_function
from flask import Flask, render_template, request,url_for,session,send_file
from io import BytesIO
from wtforms import SubmitField
from flask_wtf import Form
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import mysql.connector
import re 
import datetime
import pickle
import os.path

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysql",
    database="cafe"
)
mycursor = mydb.cursor()

  
app = Flask(__name__)
@app.route('/')
def first():
    return render_template('homepage.html')



@app.route('/login', methods=['POST', 'GET'])
def signin1():
    if request.method == 'POST':
        name = request.form['name']
        ssn = request.form['ssn']
        sql = 'SELECT * FROM users WHERE name = %s AND ssn = %s'
        val = (name, ssn)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        if result is None:
            return render_template('login.html',error="Something Went wrong ")
        else:
          return render_template('userhomepage.html')
    else:
        return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        phone_number=request.form['phone_number']
        ssn = request.form['ssn']
        try:
            sql = "INSERT INTO users (name,age,phone_number,ssn) VALUES (%s,%s,%s,%s)"
            val = (name, age, phone_number, ssn,)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template('signup.html', pmsg="signed up successfully")
        except :
            return render_template('signup.html', ppmsg="invalid password")

    else:
        return render_template('signup.html')

if __name__ == '__main__':
    app.run()
