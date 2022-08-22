from email import generator
from email.headerregistry import Address
from enum import unique
from mailbox import Message

from msilib.schema import Feature
import numbers
from pyexpat.errors import messages
from sqlite3 import Date
from tkinter import INSERT

from traceback import print_tb
from xml.etree.ElementInclude import default_loader
from zoneinfo import available_timezones
from django.test import modify_settings
from flask import Flask, flash, render_template, request, redirect, session, url_for,jsonify

from flask_sqlalchemy import SQLAlchemy
import random
from datetime import date, datetime, time
from flask import Flask
from flask_mail import Mail, Message
import random   

from datetime import date, datetime
from flask_mysqldb import MySQL

import razorpay

app = Flask(__name__)
from flask import Flask, session
app.secret_key = '125896jhyuio'



app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'q5630025@gmail.com'
app.config['MAIL_PASSWORD'] = 'bfakbuxstnkrqsrm'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
mail = Mail()

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'neha@1234'
app.config['MYSQL_DB'] = 'ip_finder'

mysql = MySQL(app)

@app.route('/admin', methods=['POST', 'GET'])
def adlogin():
    if request.method == "POST":
        username = request.form.get('username')
        pwd = request.form.get('password')
        para = [username]
        conn = mysql.connection.cursor()
        print(username)
        
        que = conn.execute('select * from admin where username=%s', para)
        account = conn.fetchone()
        print(account)
        if account:
            que = conn.execute('select * from admin where username=%s', para)
            
            session["username"] = que
            
            print('session', session['username'])
            return redirect("/dashboared")
        else:
            msg = "Invalid Credentials"

    else:
        msg = "Please enter correct login details"
   

    return render_template('adminlogin.html',msg=msg)

@app.route('/userindex', methods=['POST', 'GET'])
def userindex():
    conn = mysql.connection.cursor()


    feat = conn.execute('SELECT id, Feature FROM featuremaster')
    fea = conn.fetchall()
    print(fea)
    if request.method == 'POST':
        plan_name = request.form['plan_name']
        plan_price = request.form['plan_price']
        plan_type = request.form.get('plan_type')
        numrquest = request.form.get('numrquest')
        Descriptaion= request.form.get('Descriptation')
        plan = request.form.getlist('Feature[]')
        datee = datetime.now()
        
        amin=request.form.getlist("feature_id[]")
        str1 = ','.join(amin)
        print('new  id  malvu ',str1)
        print(str1)
        IS_Delete = 0
        IS_Active = 1
        company_id=1
       
        conn = mysql.connection.cursor()
        que = conn.execute('INSERT into planmaster(plan_name, plan_price, plan_type, number_of_api_request, Descriptation,CreateDate, IS_Active,IS_Delete, feature_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)' ,( plan_name, plan_price, plan_type, numrquest, Descriptaion,datee, IS_Active, IS_Delete, str1))
        print('data', que)
        mysql.connection.commit()
        conn.close()
        return redirect('/plantable')
    return render_template('userindex.html', fea = fea)


@app.route('/edit/<int:id>')
def edit_plan(id):
    conn = mysql.connection.cursor()
    feat = conn.execute('SELECT id, Feature FROM featuremaster')
    fea = conn.fetchall()
    print(fea)
   
    conn = mysql.connection.cursor()
    
    conn.execute("SELECT * FROM planmaster WHERE id=%s", (id,))
    row = conn.fetchone()
    print('edit for polan', row)
    if row:
        return render_template('edit.html', row=row, fea=fea)
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/update', methods=['POST', 'GET'])
def update_user():
    plan_name = request.form.get('plan_name')
    plan_price = request.form.get('plan_price')
    plan_type = request.form.get('plan_type')
    number_of_api_request = request.form.get('number_of_api_request')
    Descriptation = request.form.get('Descriptation')
    CreateDate = request.form.get('CreateDate')
    
    IS_Active = 0
    IS_Delete = 1
    amin=request.form.getlist("feature_id[]")
    str1 = ','.join(amin) 
    id = request.form.get('id')
    # validate the received values
    if plan_name and plan_price and plan_type and number_of_api_request and Descriptation and CreateDate and IS_Active and IS_Delete and str1 and id and request.method == 'POST':
        conn = mysql.connection.cursor()
        query = conn.execute("UPDATE planmaster SET plan_name=%s, plan_price=%s, plan_type=%s,number_of_api_request=%s, Descriptation=%s, CreateDate=%s, IS_Active=%s, IS_Delete=%s, feature_id=%s   WHERE id=%s", (plan_name, plan_price, plan_type, number_of_api_request,Descriptation,CreateDate,IS_Active, IS_Delete, str1 ,id))
        print(query)
        mysql.connection.commit()
        conn.close()
        return redirect('/plantable')
    else:
        return 'Error while updating user'
@app.route('/dashboared')
def dashboared():
    return render_template('dashboared.html')

@app.route('/delete/<int:id>')
def delete_user(id):
    conn = None
   
    conn = mysql.connection.cursor()
    
    conn.execute("DELETE FROM planmaster WHERE id=%s", (id,))
    mysql.connection.commit()
    
    return redirect('/plantable')

        

@app.route('/plantable', methods=['POST', 'GET'])
def plantable():
    conn = mysql.connection.cursor()
    cursor = mysql.connection.cursor()
    sql_select_query = """select * from planmaster """
    # set variable in query
    val  = cursor.execute("""select * from planmaster """)

    record = cursor.fetchall()
    print(record)

    return render_template('plantable.html', record=record)


@app.route('/usertable', methods=['POST', 'GET'])
def usertable():
    conn = mysql.connection.cursor()
    cursor = mysql.connection.cursor()
    sql_select_query = """select * from compnaymaster """
    # set variable in query
    val  = cursor.execute("""select * from compnaymaster """)

    record = cursor.fetchall()
    print(record)
 
    return render_template('companydetail.html', data = record)

@app.route('/companyplandetail', methods=['POST', 'GET'])
def companyplandetail():
    conn = mysql.connection.cursor()
    cursor = mysql.connection.cursor()
    sql_select_query = """select * from company_plan_detail """
    # set variable in query
    val  = cursor.execute("""select * from company_plan_detail""")

    record = cursor.fetchall()
    print(record)
 
    return render_template('companyplandetail.html', data = record)

@app.route('/pricetable',methods=['GET','POST'])
def pricetable():
    
    conn = mysql.connection.cursor()

  
    val  = conn.execute("""select * from planmaster """)

    data = conn.fetchall()

    print(data)

       
    return render_template('price-table1.html' , record = data)

@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('index1.html')

@app.route('/payment', methods = ['POST', 'GET'])
def payment():
    return render_template('payment.html')

def pay():
    return render_template('pay.html')

        
# @app.route('/record', methods=['GET', 'POST'])
# def record():
#     if request.method == 'POST':
#         # api_key = request.form.get['id']
#         Tototalrequest = request.form['Tototalrequest']
#         Availablerequest = request.form['Availablerequest']

    
#         rec = RecordMaster(Totalrequest=Tototalrequest,availablerequest=Availablerequest)
#         db.sessiondb.add(rec)
#         db.session.commit()

#         return redirect('/signup')
#     else:
#         pass
#     return render_template('payment.html')


if __name__ == "__main__":
    app.run(debug=True)
            














