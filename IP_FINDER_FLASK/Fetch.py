# import flask
from flask import Flask, render_template, request, redirect, url_for,jsonify

import json
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'neha@1234'
app.config['MYSQL_DB'] = 'ip-finder'

mysql = MySQL(app)

app= Flask(__name__)

@app.route('/')
def INDEX():
  IP_RECORD = dict()
  return render_template('ip.html',visible=False, IP_RECORD=IP_RECORD)

@app.route('/pricing')
def Pricing():
  IP_RECORD = dict()
  return render_template('pricing.html',visible=False, IP_RECORD=IP_RECORD)

@app.route('/404')
def ERROR():
  IP_RECORD = dict()
  return render_template('error.html',visible=False, IP_RECORD=IP_RECORD)





# @app.route("/getData", methods=['POST'])
# def getData():
  
#     entry2Value = request.get_json()
#     # entry1Value = request.args.get('entry1_id')
#     print(entry2Value.values())
#     var1 =  entry2Value
#     var2 = 10
#     var3 = 15
#     return jsonify({ 'var1': var1, 'var2': var2, 'var3': var3 })


@app.route('/ip_finder', methods=['GET', 'POST'])
def ip_finder():
      


    if request.method == 'POST':
      # info = request.get_json()
      
      data = request.form.getlist('ipaddress')
      print("Data = ",data, type(data))
      
      output = []
      
      listofdata = data[0].split(",")
      
      print("listofdata = ",listofdata)
      
      for query in listofdata:
        
        # return data
        print("Query = ", query)
        conn = mysql.connection.cursor()

        sql1 = "SELECT * FROM `ip_to_country` WHERE %s between `Begin_IP_Address` and `End_IP_Address` "
        conn.execute(sql1, (query))
        country = conn.fetchone()   
        print("Country = ",country['Country'])


        # sql = "SELECT * FROM `ip_to_country` WHERE %s between `Begin_IP_Address` and `End_IP_Address` "
        # for sudo_data in country:


        # sql = "SELECT * FROM ip_range_informations where `COUNTRY` = %s and %s between `STARTINGPOINT` and `ENDINGPOINT`"
        # cursor.execute(sql, (country['Country'],data))
        # result = cursor.fetchone()
        # print("Result = ",result)



        # if result == None:
        #   print("None")
        sql = "SELECT * FROM ip_range_informations where %s between `STARTINGPOINT` and `ENDINGPOINT`"
        conn.execute(sql, (query))
        result2 = conn.fetchone()
        print("None type Result = ",result2)


        # print("Country = ",result['COUNTRY'])
        # print("ASN Number = ",result['AS_NUMBER'])
        # print("Organization = ",result['ORGANIZATION'])
        # print("Registry = ",result['REGISTRY'])
        # print("Allocated_On = ",result['ALLOCATED_ON'])
        # print("Domain = ",result['DOMAIN'])

        IP_RECORD = dict()

        if result2 == None:
          print("single")
          IP_RECORD["IP"] = query
          IP_RECORD["Country"] = country['Country']
          
          output.append(IP_RECORD)
          
          # return render_template("ip.html", IP_RECORD=IP_RECORD, info=data, visible=True)

        else:
          print("double")
          IP_RECORD["IP"] = query
          IP_RECORD["Country"] = result2['COUNTRY']
          IP_RECORD["ASN_Number"] = result2['AS_NUMBER']
          IP_RECORD["Organization"] = result2['ORGANIZATION']
          IP_RECORD["Registry"] = result2['REGISTRY']
          IP_RECORD["Allocated_On"] = result2['ALLOCATED_ON']
          IP_RECORD["Domain"] = result2['DOMAIN']
          
          
          output.append(IP_RECORD)
          # return json.dumps({'status':'OK','IP_RECORD':IP_RECORD,'info':info});
          
      print(output)
      return render_template("ip.html", output=output, visible=True)
      # return jsonify(output)
      
      # return IP_RECORDs
    else:
        return render_template("ip.html")
  

    



if __name__ == "__main__":
  app.run(debug=True)