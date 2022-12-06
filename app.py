import pymysql
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/Vendors/')
def Vendors():
    output = mysqlconnect("select Vname,Sec_name,Availability from Vendor")
    return render_template('./Vendors.html',output = output)
  
@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/Reservations/')
def Reservations():
    return render_template('./Reservations.html')

@app.route('/Rides/')
def Rides():
    return render_template('./Rides.html')

def mysqlconnect(query):
    # To connect MySQL database
    conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "Simba1026!",
        db='AMUSEMENT_PARK',
        )
      
    cur = conn.cursor()
 # Select query
    cur.execute(query)
    output = cur.fetchall()
      
    for i in output:
        print(i)
    # To close the connection
    conn.close()
    return output


if __name__ == "__main__":
    mysqlconnect('select Vname,Sec_name from Vendor')
    app.run
    