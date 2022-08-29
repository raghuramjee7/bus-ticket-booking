from flask import Flask, render_template, request, redirect
import random
from sqlQueries import *

app = Flask(__name__)


# Search Page
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

# Search bar for updating
@app.route('/update', methods = ["GET", "POST"])
def update():
    if request.method=="POST":
        id = request.form['id']
        return redirect(f"/change/{id}")
    return render_template('update.html')

# Update Page
@app.route('/change/<id>')
def change(id):
    busd = booking_details(id)
    if busd == []:
        return render_template('404.html')
    return render_template('change.html', busd = busd)

# Booking details page, here we got an option for update or delete
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

# Booking update page
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

# Returns all bus details
@app.route('/search/<from12>/<to12>')
def search(from12, to12):
    details = allbus(to12, from12)
    return render_template('search.html', det = details)

# Page for booking
@app.route('/book/<int:busid>')
def book(busid):
    busd = busdetails(busid)
    seat = busd[0][7]
    seats = [i for i in range(1,seat+1)]
    return render_template('book.html', busd = busd, seats = seats)

# Booking a ticket
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
    
    app.run(debug=True)