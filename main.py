import pymysql
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route('/Vendors/', methods = ['POST', 'GET'])
def Vendors():
    output = mysqlconnect("select Vname,Sec_name from Vendor")
    if request.method == 'POST':
        # try catch to avoid field mismatch crashing executor
        try:
            if(request.form['Vendor name'] is not None):
                sql_parameterized_query = """ select * from Menu,Vendor where Menu.VID = Vendor.VID and Vendor.Vname= %s"""
                extraInfo = preparedQuery(sql_parameterized_query = sql_parameterized_query,formresult=request.form['Vendor name'] )
                by = 0
                return render_template('./Vendors.html', output = output, extraInfo = extraInfo, by = by)
        except: 
            pass
        try:
            if(request.form['Item'] is not None):
                sql_parameterized_query = """ select Item,Cost,Vname,Sec_name,Availability from Menu,Vendor where Menu.VID = Vendor.VID and Menu.Item= %s"""
                extraInfo = preparedQuery(sql_parameterized_query = sql_parameterized_query,formresult=request.form['Item'] )
                by = 1 
                print(extraInfo)
                return render_template('./Vendors.html', output = output, extraInfo = extraInfo, by = by)
        except:
            pass
    return render_template('./Vendors.html',output = output,extraInfo = None)
  
@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/Signin/', methods = ['POST', 'GET'])
def Signin():
    failed = False
    if request.method == 'POST' :
        employee = mysqlconnect("select * from employee where EID=" + request.form['EID'])
        if len(employee) != 0 :
            print("\n")
            print(url_for('Hours', EID=request.form['EID'] ) )
            print("\n")
            return redirect(url_for('Hours', EID=request.form['EID'] ), code=302)
        failed = True
    return render_template('./Signin.html', failed = failed)

@app.route('/Hours/')
def Hours():
    print(request)
    hours = mysqlconnect("select * from work_hours where EID=" + request.args['EID'] )
    total = mysqlconnect("select * from employee_hours where EID=" + request.args['EID'] )
    return render_template('./Hours.html', hours = hours, total = total)

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

@app.route('/Rides/', methods = ['POST', 'GET'])
def Rides():
    if request.method == 'POST':
        print(request.form)
        output = mysqlconnect("select Name from Ride")
        extraInfo = mysqlconnect("select * from Ride where Name='" + request.form['name'] + "'")
        return render_template('./Rides.html', output = output, extraInfo = extraInfo)
    output = mysqlconnect("select Name from Ride")
    return render_template('./Rides.html', output = output, extraInfo = None)

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

def preparedQuery(sql_parameterized_query, formresult):
    conn = pymysql.connect(
        host='localhost',
        user='server', 
        password = "password",
        db='AMUSEMENT_PARK',
        )
    # this will retun MySQLCursorPrepared object
    cursor = conn.cursor()
    #this will execute the prepared method 
    cursor.execute(sql_parameterized_query, formresult)
    #this will return the rows of the query output
    result = cursor.fetchall()
    return result


if __name__ == "__main__":
    app.run
    
