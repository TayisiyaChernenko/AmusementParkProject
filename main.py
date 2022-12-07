import pymysql
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route('/Vendors/')
def Vendors():
    output = mysqlconnect("select Vname,Sec_name,Availability from Vendor")
    return render_template('./Vendors.html',output = output)
  
@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/Reservations/',methods = ['POST', 'GET'])
def Reservations():
    if request.method == 'POST':
        print("'" + request.form['start date'] + " " + request.form['start time'] + ":00', '")
        print("'" + request.form['end date'] + " " + request.form['end time'] + ":00', '")
        print("'" + request.form['section'] + "', ")
        print(request.form['guests'] + ", ")
        print(request.form['gid'] + ")")
        mysqlconnect("insert into reservation values('" 
                        + request.form['start date'] + " " + request.form['start time'] + ":00', '"
                        + request.form['end date'] + " " + request.form['end time'] + ":00', '"
                        + request.form['section'] + "', "
                        + request.form['guests'] + ", "
                        + request.form['gid'] + ")")
    sections = mysqlconnect("select sec_name from section")
    sections = map(lambda n: n[0], sections)
    output = mysqlconnect("select * from Reservation")
    return render_template('./Reservations.html', output = output, sections = sections)

@app.route('/Rides/')
def Rides():
    return render_template('./Rides.html')

def mysqlconnect(query):
    print(query)
    # To connect MySQL database
    conn = pymysql.connect(
        host='localhost',
        user='server', 
        password = "password",
        db='AMUSEMENT_PARK',
        )
      
    cur = conn.cursor()
 # Select query
    cur.execute(query)
    conn.commit()
    output = cur.fetchall()
      
    for i in output:
        print(i)
    # To close the connection
    conn.close()
    return output


if __name__ == "__main__":
    mysqlconnect('select Vname,Sec_name from Vendor')
    app.run
    
