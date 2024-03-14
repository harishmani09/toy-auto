from flask import Flask,render_template, flash,request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from sel_app import CreateForm
import random
import time 
import openpyxl
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common import WebDriverException


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach',True)

driver = None 
df = None 
url = None 


UPLOAD_FOLDER = "static/files"
ALLOWED_EXTENSIONS = {'csv','xlsx','xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['SECRET_KEY'] = 'supersecret#key'




@application.route('/')
def home():
    filenames = os.listdir(application.config['UPLOAD_FOLDER'])
    return render_template('index.html',files=filenames)

@application.route('/delete', methods=['POST'])
def delete_file():
    files_to_delete = request.form.getlist('file')
    for file_name in files_to_delete:
        os.remove(os.path.join(application.config['UPLOAD_FOLDER'],file_name))  
    return redirect(url_for('home'))


@application.route('/upload',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        #check if the post reuqest has file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'],filename))
            # return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
        return redirect('/')
            # return redirect(url_for('download',name=filename))
    return render_template('index.html')
    


@application.route('/process', methods=['GET','POST'])
def process():
    global df, driver, url 
    if driver is None:
        driver = webdriver.Chrome(options=chrome_options)
    if df is None:
        df = pd.read_excel('static/files/tutorial_ninja.xlsx')
    if url is None:
        url = "https://tutorialsninja.com/demo/index.php?route=account/register"
    
    create_profile = CreateForm(driver,url)
    create_profile.process_data(df)
    
    driver.quit()   
    return redirect(url_for('home'))

    



if __name__ == '__main__':
    application.run(debug=True)
    