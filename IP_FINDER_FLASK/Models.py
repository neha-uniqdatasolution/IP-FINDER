from dataclasses import dataclass
from genericpath import exists
from itertools import count
from typing import ParamSpec
from flask import Flask, session
from flask import *
# from flask_session import Session
from flask import Blueprint, render_template, redirect, url_for
from urllib3 import HTTPResponse
from flask_mysqldb import MySQL
from geopy.geocoders import Nominatim
from flask_mail import Mail, Message
import re

from shapely.geometry import Point, Polygon
# from ast import literal_eval
app = Flask(__name__)

# app.config['MYSQL_HOST'] = '182.70.125.202'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 4306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Swastik1058@QWE'
app.config['MYSQL_DB'] = 'geo-location'



mysql = MySQL(app)

app.secret_key = "12DFEFRfjiryfhuw"


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'q5630025@gmail.com'
app.config['MAIL_PASSWORD'] = 'bfakbuxstnkrqsrm'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
# conn = connect(host='localhost',port=4306,user='root',password="",database='geo-location')
# cs1 = conn.cursor()


mail = Mail(app)

@app.route("/",methods = ["POST","GET"])  

def register():
   
    if request.method == "POST": 
        First_name = request.form['First_name']
        Last_name = request.form['Last_name']
        Email = request.form.get("Email")
        Phone = request.form["Phone"]  
        Password = request.form.get("Password")
        c_password = request.form.get("conformPassword")
        params = [Email]
        


        print(First_name, Last_name, Email, Phone)
       
        
        cursor = mysql.connection.cursor()
        
        params = [Email]
        print(params)
        count = cursor.execute('select * from users where Email=%s', params)
        print('count',count)
        if count == 0:
            cursor.execute("""INSERT INTO users (First_name,Last_name,Email,Password,Phone) VALUES (%s,%s,%s,%s,%s)""", (First_name, Last_name, Email, Password, Phone))
            msg = Message('Hello from the other side!', sender ='q5630025@gmail.com', recipients = [Email])

            msg.body = "Registration Done, You are successfully registered to our website."
            val = mail.send(msg)
            mysql.connection.commit()
            cursor.close()
            
            return redirect('/login')
        else:
            pass
            
        
    return render_template('reg.html')



 
@app.route('/login',methods = ["POST", "GET"])  
def login():  
    if request.method == "POST":  
        Email = request.form.get('Email')
        # print('username',Email)
        Password = request.form.get('Password')
        cursor = mysql.connection.cursor()
        para = [Email]
        que = cursor.execute('select * from users where Email=%s', para)
        account = cursor.fetchone()
       
 
        if account:
            que = cursor.execute('select * from users where Email=%s', para)
            
            session["Email"] = que
            session['id'] = account[0]
            
            print('session', session['Email'])
            return redirect("/addform")
        else:
            msg = "Invalid Credentials"
        return render_template('loginpage.html',msg = msg)

    return render_template('loginpage.html')




@app.route('/logout')
def logout():
    del session['id']
    return redirect('/login')


# # @app.route("/loadform",methods = ["POST","GET"])
# # def loadform():
# #     ids = session['id']
# #     print('ids = ',ids)
# #     cood = Coordinates.query.filter(Coordinates.user_id==ids)
 
# #     print(cood)

# #     return render_template('mapform.html', cood = cood)

@app.route("/addform",methods = ["POST","GET"])  
def addform():

    # geolocator = Nominatim(user_agent="geoapiExercises")
    
    if request.method == 'POST':
    
        user_id =  session["id"]
        o_name = request.form.get('o_name')
        # location = geolocator.geocode('address')
        address = request.form.get('address')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        coordinate = request.form.get('coordinate')
        para = [latitude]
        parar = [longitude]
        cursor = mysql.connection.cursor()
        # exist_LL = Coordinates.query.filter_by(latitude=latitude, longitude=longitude).all()
        que = cursor.execute('select * from coordinate where latitude=%s', para)
        que1 = cursor.execute('select * from coordinate where longitude=%s', parar)
        exist_LL = que , que1
        print("exist_LL = ",len(exist_LL), exist_LL)
        cursor = mysql.connection.cursor()
        if len(exist_LL) != 1:
            print("coordinate = ", coordinate, len(coordinate))
            if len(coordinate) != 0:
                cursor.execute("""INSERT INTO coordinate (user_id,o_name,address,latitude,longitude, coordinate) VALUES (%s,%s,%s,%s,%s,%s)""", (user_id, o_name, address, latitude, longitude, coordinate))
        
                mysql.connection.commit()
                cursor.close()
                return redirect('/getcoor')
            
            else:
                msg = "Please select area"
                return render_template('mapform.html', msg = msg)
            
        else:
            msg = "Given Latitude and Longitude is alredy in system..."
            return render_template('mapform.html', msg = msg)
    

    else:

        return render_template('mapform.html')


@app.route('/getcoor', methods = ['POST', 'GET'])
def getcoor():
    
    
    userid = session['id']  
    # print('user_id', userid)
    final_list = []
    data = []
    cursor = mysql.connection.cursor()
    
    
    data = cursor.execute('select coordinate from coordinate where user_id=%s', (userid,))
    print("getcoor",data)
    account = cursor.fetchall()
    # newdata = str(account)
    # print('account', newdata)


    # print('data', type(newdata))
  
    for item in account:
        
        if item == 0:
            break
        
        l = []
        # list_data = item.split(',')
        # print('list_data = ', list_data)
        for value in range(0, len(item) ,2): 
            # print(value)  
            coor = item[value]
            # print('coor', coor)
            d = coor.split(',')
            print('data', type(d))
            for val in range(0, len(d) ,2):
                print(d[val])
                l.append([float(d[val]), float(d[val+1])])

        final_list.append(l)

        print("final_list = ",final_list)

    return render_template('pointer.html', final_list = final_list, length_of_list = len(final_list))



@app.route('/userlocation', methods = ['POST', 'GET'])
def userlocation():
    return render_template('user.html')


@app.route('/usercoor', methods = ['POST', 'GET'])
def usercoor():
    userid = session['id']  
    final_list = []

    
    # othercoor = Coordinates.query.filter(Coordinates.user_id==userid).all()
    cursor = mysql.connection.cursor()
    data = cursor.execute('select coordinate from coordinate where user_id=%s', (userid,))
    print("getcoor",data)
    account = cursor.fetchall()

    if request.method == 'POST': 
        # print(request.method)
        # print("----------------------------------------",request.form['latitude'], type(request.form['latitude']))

        latitude = float(request.form.get('latitude'))

        longitude = float(request.form.get('longitude'))# in str

    
    
        p1 = Point(latitude, longitude)
        
        data = cursor.execute('select latitude from coordinate where user_id=%s', (userid,))
        latitude = cursor.fetchone()
        data = cursor.execute('select longitude from coordinate where user_id=%s', (userid,))
        longitude = cursor.fetchone()
        def convertTuple(tup):
                str = ''.join(tup)
                return str
        long = convertTuple(longitude)
        print("long",long)
        latitude_one = convertTuple(latitude)
        print("latitude",latitude_one)

        print(long,latitude_one)
        for data in account:
            l = []



            # inlist = data.coordinate.split(',')
            # for i in range(0,len(inlist),2):
            #     l.append((float(inlist[i+1]), float(inlist[i])))

            for value in range(0, len(data) ,2): 
            # print(value)  
                coor = data[value]
            # print('coor', coor)
            d = coor.split(',')
            # print('data', type(d))
            for val in range(0, len(d) ,2):
                # print(d[val])
                l.append([float(d[val]), float(d[val+1])])
            
            # print("List",l)
                
            

            poly = Polygon(l)

            if p1.within(poly):
                # print("found = ", l)
                final_list = []
 
                for i in l:
                    final_list.append([i[1], i[0]])

                
                # print("IN LIST = ",final_list)
                # print(data.longitude)
                print(final_list)
            
                return jsonify({'final_list': final_list,'long':long,'lat':latitude_one})

            else:
                pass

        return jsonify({'final_list': "user not in range"})
    
    return jsonify({'final_list': "in get"})


# if '__name__' == '__main__':
#     app.run(host='localhost') 


if __name__ == "__main__":
    app.run()