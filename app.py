from flask import Flask, render_template, request, redirect
import mysql.connector
import random

app = Flask(__name__)

def book_passengers(bookid):
    mycursor = mydb.cursor()
    sql = "SELECT passengers FROM booking WHERE booking_id = '" + str(bookid) + "'"
    mycursor.execute(sql)
    seats = mycursor.fetchall()
    return seats[0][0]

def get_bus_seats(busid):
    mycursor = mydb.cursor()
    sql = "SELECT capacity FROM bus WHERE busid = '" + str(busid) + "'"
    mycursor.execute(sql)
    seats = mycursor.fetchall()
    return seats

def update_bus_passengers(busid, newpass):
    mycursor = mydb.cursor()
    updtbk = "update bus set capacity = capacity-" + str(newpass) + " where busid = '" + str(busid) + "'"
    mycursor.execute(updtbk)
    mydb.commit()

def generateid():
    id = random.randint(11111,99999)
    return id

def allbus(to_, from_):

    mycursor = mydb.cursor()
    sql = "SELECT * FROM bus WHERE to_ = " + "'" + str(to_) + "'" + " AND from_ = " + "'" + from_ + "'"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()
    return myresult

def busdeatils(busid):
    mycursor = mydb.cursor()
    sql = "SELECT * FROM bus WHERE busid = " + "'" + str(busid) + "'"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()
    return myresult

def userinsert(det):
    mycursor = mydb.cursor()

    sql = "INSERT INTO user (userid, username, phone, email, bookid) VALUES (%s, %s, %s, %s, %s)"
    val = tuple(det)
    mycursor.execute(sql, val)
    mydb.commit()
    return

def bookinginsert(det):
    mycursor = mydb.cursor()

    sql = "INSERT INTO booking (booking_id, userid, busid, passengers) VALUES (%s, %s, %s, %s)"
    val = tuple(det)
    mycursor.execute(sql, val)

    mydb.commit()
    return

def booking_details(id):
    mycursor = mydb.cursor()
    sql1 = "SELECT * FROM booking WHERE booking_id = " + "'" + str(id) + "'"
    mycursor.execute(sql1)
    result1 = mycursor.fetchall()
    sql2 = "select * from user where userid in ( select userid from booking where booking_id = " + "'" + str(id) + "'" + ");"
    mycursor.execute(sql2)
    result2 = mycursor.fetchall()
    sql3 = "select * from bus where busid in ( select busid from booking where booking_id = " + "'" + str(id) + "'" + ");"
    mycursor.execute(sql3)
    result3 = mycursor.fetchall()
    return result1+result2+result3

def delete(bookid):
    try:
        det = booking_details(bookid)
        userid = det[0][1]
        mycursor = mydb.cursor()

        sql1 = "delete from booking where booking_id = '" + str(bookid) + "'"
        mycursor.execute(sql1)
        mydb.commit()

        sql2 = "delete from user where userid = '" + str(userid) + "'"
        mycursor.execute(sql2)

        mydb.commit()
    except:
        pass
    return

    return

def updatebookingpassengers(bookid, pas):
    mycursor = mydb.cursor()
    pas = pas[0]
    updtbk = "update booking set passengers = " + str(pas) + " WHERE booking_id = '" + str(bookid) + "'"
    print(updtbk)
    mycursor.execute(updtbk)
    mydb.commit()

def updatebookuser(user, book, bookid):
    mycursor = mydb.cursor()
    sql = "SELECT userid FROM booking WHERE booking_id = '" + str(bookid) + "'"
    mycursor.execute(sql)
    userid = mycursor.fetchall()
    userid = userid[0][0]
    pas = book
    updatebookingpassengers(bookid, pas)
    

    name, phno, email = user
    updtus = "update user set username = '" + str(name) + "',phone = '" + str(phno) + "',email = '" + str(email) + "' where userid = '" + str(userid) + "'"
    mycursor.execute(updtus)
    mydb.commit()

@app.route('/', methods = ["GET", "POST"])
def index():
    if request.method=="POST":
        from12 = request.form['from']
        to12 = request.form['to']
        if from12==to12:
            return render_template('404.html')
        else:
            return redirect(f"/search/{from12}/{to12}")
    return render_template('index.html')

@app.route('/update', methods = ["GET", "POST"])
def update():
    if request.method=="POST":
        id = request.form['id']
        return redirect(f"/change/{id}")
    return render_template('update.html')

@app.route('/change/<id>')
def change(id):
    busd = booking_details(id)
    if busd == []:
        return render_template('404.html')
    return render_template('change.html', busd = busd)

@app.route('/updel/<int:bookid>', methods = ["GET", "POST"])
def updel(bookid):
    if request.method=="POST":
        req = request.form['op']
        if req=="update":
            busd = booking_details(bookid)
            seat = busd[2][7]
            
            seats = [i for i in range(1,seat+1)]
            return render_template("updateBooking.html", busd = busd, seats = seats)
        else:
            busd = booking_details(bookid)
            busid = busd[0][2]
            passengers = book_passengers(bookid)
            update_bus_passengers(busid, -passengers)
            delete(bookid)
            return render_template("deleted.html")

@app.route('/updatebook/<int:bookid>', methods = ["GET", "POST"])
def updatebook(bookid):
    if request.method=="POST":
        name = request.form['name']
        phno = request.form['phno']
        email = request.form['email']
        passengers = request.form['passengers']

        user_new_details = [name, phno, email]
        booking_new_details = [passengers]
        busd = booking_details(bookid)
        busid = busd[0][2]
        oldpassengers = book_passengers(bookid)
        updatebookuser(user_new_details, booking_new_details, bookid)
        
        new_passengers = int(passengers)-oldpassengers
        print(new_passengers)
        update_bus_passengers(busid, new_passengers)

    return render_template("updated.html")


@app.route('/search/<from12>/<to12>')
def search(from12, to12):
    details = allbus(to12, from12)
    return render_template('search.html', det = details)

@app.route('/book/<int:busid>')
def book(busid):
    busd = busdeatils(busid)
    seat = busd[0][7]
    seats = [i for i in range(1,seat+1)]
    return render_template('book.html', busd = busd, seats = seats)


@app.route('/booked/<int:busid>', methods = ["GET", "POST"])
def booked(busid):
    if request.method=="POST":
        name = request.form['name']
        phno = request.form['phno']
        email = request.form['email']
        passengers = request.form['passengers']

        userid = generateid()
        bookingid = generateid()

        update_bus_passengers(busid, passengers)
        user_details = [userid, name, phno, email, bookingid]
        booking_details = [bookingid, userid, busid ,passengers]
        userinsert(user_details)
        bookinginsert(booking_details)
    return render_template('booked.html', id=bookingid)


if __name__ == '__main__':

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="projectdb"
    )
    
    app.run(debug=True)