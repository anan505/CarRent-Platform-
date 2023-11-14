### Example inspired by Tutorial at https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
### However the actual example uses sqlalchemy which uses Object Relational Mapper, which are not covered in this course. I have instead used natural sQL queries for this demo. 

from flask import Flask, render_template, url_for, flash, redirect
from forms import CompanyForm, ClientForm, loginClientForm, loginCompanyForm, selectTime, addCarForm, addTruckForm, updateForm, searchForm
import pymysql

conn = pymysql.connect(host='localhost',
                             user='amber',
                             password='amber',
                             database='RentCar',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor
                             )
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#Turn the results from the database into a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/")
@app.route("/home")

def home():

    #Display all blogs from the 'blogs' table
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("SELECT * FROM company")
    posts = c.fetchall()
    return render_template('companylist.html', posts=posts)

#在homepage能够查看每个公司有的车
@app.route('/<isin>/')
def vehicleList(isin):     
    c = conn.cursor()
    query = "SELECT * FROM `vehicles` WHERE ISIN ='" + isin + "' AND c = 1"
    c.execute(query)
    car = c.fetchall()
    query = "SELECT * FROM `vehicles` WHERE ISIN ='" + isin + "' AND c = 0"
    c.execute(query)
    p = c.fetchall()
    return render_template('vehicleList.html', posts1 = car, posts2 = p) 
    
# =============================================================================
# #NEW
# =============================================================================
@app.route("/newClient", methods=['GET', 'POST'])
def clientRegister():
    form = ClientForm()
    
    if form.validate_on_submit():
        c = conn.cursor()
        dob = form.DOB.data.strftime("%Y-%m-%d")
        query = 'INSERT INTO client VALUES (' + "'" + form.first_name.data + "'," + "'" + form.last_name.data + "'," + "'" + dob + "'," + "'" + form.email.data + "'," + "'" + form.password.data + "'" + ')'
        c.execute(query)
        conn.commit()
        
        flash(f'Account created for {form.first_name.data}!', 'success')
        return redirect(url_for('loginClient'))   
    return render_template('newClient.html', title='newClient', form=form)  

@app.route("/newCompany", methods=['GET', 'POST'])  
def companyRegister():
    form = CompanyForm()
    states = [(0,'New South Wales'), (1, 'Queensland'), (2, 'South Australia'), (3, 'Tasmanla'), (4, 'Victoria'), (5, 'Western Australia'), (6, 'Australian Capital Territory'), (7, 'Jervis Bay Territory'), (8, 'Northern Territory')]
    form.st.choices = states
    if form.validate_on_submit():
        choices = form.st.choices
        st =  (choices[form.st.data][1])
        c = conn.cursor()
        query = 'INSERT INTO company VALUES (' + "'" + form.name.data + "'," + "'" + form.city.data + "'," + "'" + st + "'," + "'" + form.ISIN.data + "'," + "'" + form.password.data + "'" + ')'
        c.execute(query)
        conn.commit()
        
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('loginCompany'))   
    return render_template('newCompany.html', title='newCompany', form=form)
        

# =============================================================================
# LOGIN
# =============================================================================
@app.route("/loginClient/", methods=['GET', 'POST'])  
def loginClient():
    form = loginClientForm()
    if form.validate_on_submit():
    #check pw
        c = conn.cursor()
        query = 'SELECT password FROM client WHERE email = ' + "'" + form.email.data + "'" 
        c.execute(query)
        res = c.fetchall()
        if res[0]['password'] == form.password.data:
            form.validate_on_submit() 
            return redirect('/booking/'+ form.email.data+'/')   
    return render_template('loginClient.html', title='loginClient', form=form)

@app.route("/loginCompany/", methods=['GET', 'POST'])  
def loginCompany():
    form = loginCompanyForm()
    if form.validate_on_submit():
    #check pw
        c = conn.cursor()
        query = 'SELECT password FROM company WHERE ISIN = ' + "'" + form.ISIN.data + "'" 
        c.execute(query)
        res = c.fetchall()
        if res[0]['password'] == form.password.data:
            form.validate_on_submit()
            return redirect('/manage/'+ form.ISIN.data+'/')  
    return render_template('loginCompany.html', title='loginCompany', form=form)

@app.route('/booking/<email>/')
def bookingList(email):     
    c = conn.cursor()
    query = "SELECT * FROM booking, bookingfee WHERE booking.booking_id = bookingfee.booking_id AND booking.client_email ='" + email + "'"
    c.execute(query)
    conn.commit()
    booking = c.fetchall()
    return render_template('bookingList.html', posts = booking, email = email) 


@app.route('/booking/delete/<email>/<bid>/')
def deleteBooking(email, bid):
    c = conn.cursor()
    query = "DELETE FROM booking WHERE client_email = " + "'" + email + "' AND booking_id = " + str(bid)
    c.execute(query)
    conn.commit()
    return redirect('/booking/'+ email +'/')

@app.route('/chooseCarList/<email>/')
def chooseCarList(email):
    c = conn.cursor()
    query = "SELECT * FROM vehicles, company WHERE vehicles.ISIN = company.ISIN AND C = 1"
    c.execute(query)
    cars = c.fetchall()
    return render_template('chooseCarList.html', post = cars, email = email) 

@app.route('/chooseTruckList/<email>/')
def chooseTruckList(email):
    c = conn.cursor()
    query = "SELECT * FROM vehicles, company WHERE vehicles.ISIN = company.ISIN AND C = 0"
    c.execute(query)
    cars = c.fetchall()
    return render_template('chooseTruckList.html', post = cars, email = email) 

    
@app.route('/chooseCarList/select/<email>/<v_id>', methods=['GET', 'POST'])
def selectOneCar(email, v_id):
    form = selectTime()
    if form.validate_on_submit():
        c = conn.cursor()
        duration = abs((form.start_date.data - form.end_date.data).days)    #number! days
        sd = form.start_date.data.strftime("%Y-%m-%d")
        ed = form.end_date.data.strftime("%Y-%m-%d")
        query = 'INSERT INTO booking(client_email, start_date, end_date, v_id) VALUES (' + "'" + email + "'," + "'" + sd + "'," + "'" + ed + "'," + "'" + v_id + "'" + ')'
        c.execute(query)
        conn.commit()
        query = "SELECT price FROM vehicles WHERE v_id = '" + v_id + "'"
        c.execute(query)
        res = c.fetchall()
        price = res[0]['price'] 
        amount = price * duration   
        query = "INSERT INTO bookingfee(amount_fee) VALUES (" + str(amount) + ")"
        c.execute(query)
        conn.commit()
        return redirect('/booking/'+ email +'/')
    return render_template('timeSelect.html', form=form, email = email) 

@app.route('/manage/<ISIN>/', methods=['GET', 'POST'])
def manageVehicleList(ISIN):
    c = conn.cursor()
    query = "SELECT * FROM `vehicles` WHERE ISIN ='" + ISIN + "' AND c = 1"
    c.execute(query)
    car = c.fetchall()
    query = "SELECT * FROM `vehicles` WHERE ISIN ='" + ISIN + "' AND c = 0"
    c.execute(query)
    p = c.fetchall()
    return render_template('manageVehicleList.html', ISIN = ISIN, posts1 = car, posts2 = p) 
    
@app.route('/addCar/<ISIN>/', methods=['GET', 'POST'])
def addCar(ISIN):
    form = addCarForm()
    YEAR_CHOICES = [(r,str(r)) for r in range(1984, 2030)]
    form.year.choices = YEAR_CHOICES
    if form.validate_on_submit():
        c = conn.cursor()
        query = "INSERT INTO vehicles VALUES ('" + form.v_id.data + "', '" + ISIN + "', '" + form.brand.data + "', '" + form.model.data + "', '" + str(form.year.data) + "', " + str(form.price.data) + ", 1, "  + str(form.seat_num.data) + ", NULL)"
        c.execute(query)
        conn.commit()
        return redirect('/manage/'+ ISIN +'/')
    return render_template('addCar.html',title='add New Car',  ISIN = ISIN, form = form) 

@app.route('/addTruck/<ISIN>/', methods=['GET', 'POST'])
def addTruck(ISIN):
    form = addTruckForm()
    YEAR_CHOICES = [(r,str(r)) for r in range(1984, 2030)]
    form.year.choices = YEAR_CHOICES
    if form.validate_on_submit():
        c = conn.cursor()
        query = "INSERT INTO vehicles VALUES ('" + form.v_id.data + "', '" + ISIN + "', '" + form.brand.data + "', '" + form.model.data + "', '" + str(form.year.data) + "', " + str(form.price.data) + ", 0, "  + "NULL, " + str(form.load_capacity.data) + ")"
        c.execute(query)
        conn.commit()
        return redirect('/manage/'+ ISIN +'/')
    return render_template('addTruck.html',title='add New Truck',  ISIN = ISIN, form = form) 

@app.route('/vehicle/delete/<ISIN>/<v_id>/')
def deleteVehicle(ISIN, v_id):
    c = conn.cursor()
    query = "DELETE FROM vehicles WHERE v_id = " + "'" + v_id + "'"
    c.execute(query)
    conn.commit()
    return redirect('/manage/'+ ISIN +'/')

@app.route('/car/update/<ISIN>/<v_id>/', methods=['GET', 'POST'])
def updateCar(ISIN, v_id):
    c = conn.cursor()
    query = "SELECT * FROM `vehicles` WHERE v_id ='" + v_id + "'"
    c.execute(query)
    car = c.fetchall()
    
    form = updateForm()
    f = [(0,'brand'), (1, 'model'), (2, 'year'), (3, 'price'), (4, 'seat number')]
    form.feature.choices = f
    if form.validate_on_submit():
        choices = form.feature.choices
        feature =  (choices[form.feature.data][1])
        if feature == 'brand':
            query = "UPDATE vehicles SET brand = '" + form.value.data + "' WHERE v_id = '" + v_id + "'"
        elif feature == 'model':
            query = "UPDATE vehicles SET model = '" + form.value.data + "' WHERE v_id = '" + v_id + "'"
        elif feature == 'year':
            query = "UPDATE vehicles SET year = '" + form.value.data + "' WHERE v_id = '" + v_id + "'"
        elif feature == 'price':
            query = "UPDATE vehicles SET price = " + form.value.data + " WHERE v_id = '" + v_id + "'"
        else: 
            query = "UPDATE vehicles SET seat_num = " + form.value.data + " WHERE v_id = '" + v_id + "'"
        c.execute(query)
        conn.commit()
        return redirect('/manage/'+ ISIN +'/')
    return render_template('updateCar.html',title='update car', form = form, post = car, ISIN = ISIN) 

@app.route('/truck/update/<ISIN>/<v_id>/', methods=['GET', 'POST'])
def updateTruck(ISIN, v_id):
    c = conn.cursor()
    query = "SELECT * FROM `vehicles` WHERE v_id ='" + v_id + "'"
    c.execute(query)
    car = c.fetchall()
    
    form = updateForm()
    f = [(0,'brand'), (1, 'model'), (2, 'year'), (3, 'price'), (4, 'load capacity')]
    form.feature.choices = f
    if form.validate_on_submit():
        choices = form.feature.choices
        feature =  (choices[form.feature.data][1])
        if feature == 'brand':
            query = "UPDATE vehicles SET brand = '" + form.value.data + "' WHERE v_id = '" + v_id + "'"
        elif feature == 'model':
            query = "UPDATE vehicles SET model = '" + form.value.data + "' WHERE v_id = '" + v_id + "'"
        elif feature == 'year':
            query = "UPDATE vehicles SET year = '" + form.value.data + "' WHERE v_id = '" + v_id + "'"
        elif feature == 'price':
            query = "UPDATE vehicles SET price = " + form.value.data + " WHERE v_id = '" + v_id + "'"
        else: 
            query = "UPDATE vehicles SET load_capacity = " + form.value.data + " WHERE v_id = '" + v_id + "'"
        c.execute(query)
        conn.commit()
        return redirect('/manage/'+ ISIN +'/')
    return render_template('updateTruck.html',title='update truck', form = form, post = car, ISIN = ISIN)

@app.route('/searchCompany', methods=['GET', 'POST'])
def searchCompany():
    c = conn.cursor()
    c.execute("SELECT v.c, com.ISIN, com.city, com.st, com.name, COUNT(*) AS ans FROM vehicles v, company com WHERE v.ISIN = com.ISIN GROUP BY com.ISIN")
    posts = c.fetchall()
    form = searchForm()
    q = [(0,'The company with most number of cars'), (1, 'The company with most number of trucks'), (2, 'The company with lowest average price of cars'), (3, 'The company with lowest average price of trucks')]
    form.question.choices = q
    if form.validate_on_submit():
        choices = form.question.choices
        question =  (choices[form.question.data][1])
        if question == 'The company with most number of cars':
            query = "SELECT x.c, x.ISIN, x.city, x.st, x.name, x.ans FROM (SELECT v.c, com.ISIN, com.city, com.st, com.name, COUNT(*) AS ans FROM vehicles v, company com WHERE v.ISIN = com.ISIN AND v.c = 1 GROUP BY v.ISIN) x WHERE x.ans = ( SELECT MAX(x.ans) FROM(SELECT COUNT(*) AS ans FROM vehicles v, company com WHERE v.ISIN = com.ISIN AND v.c = 1 GROUP BY v.ISIN) x)"
        elif question == 'The company with most number of trucks':
            query = "SELECT x.c, x.ISIN, x.city, x.st, x.name, x.ans FROM (SELECT v.c, com.ISIN, com.city, com.st, com.name, COUNT(*) AS ans FROM vehicles v, company com WHERE v.ISIN = com.ISIN AND v.c = 0 GROUP BY v.ISIN) x WHERE x.ans = ( SELECT MAX(x.ans) FROM(SELECT COUNT(*) AS ans FROM vehicles v, company com WHERE v.ISIN = com.ISIN AND v.c = 0 GROUP BY v.ISIN) x)"
        elif question == 'The company with lowest average price of cars':
            query ="SELECT x.c, x.ISIN, x.city, x.st, x.name, x.ans FROM (SELECT v.c, com.ISIN, com.city, com.st, com.name, AVG(v.price) AS ans FROM vehicles v, company com WHERE v.ISIN = com.ISIN AND v.c = 1 GROUP BY v.ISIN) x WHERE x.ans = ( SELECT MIN(x.ans) FROM(SELECT AVG(v.price) AS ans FROM vehicles v, company com WHERE v.ISIN = com.ISIN AND v.c = 1 GROUP BY v.ISIN) x)"
        elif question == 'The company with lowest average price of trucks':
            query = "SELECT x.c, x.ISIN, x.city, x.st, x.name, x.ans FROM (SELECT v.c, com.ISIN, com.city, com.st, com.name, AVG(v.price) AS ans FROM vehicles v, company com WHERE v.ISIN = com.ISIN AND v.c = 0 GROUP BY v.ISIN) x WHERE x.ans = ( SELECT MIN(x.ans) FROM(SELECT AVG(v.price) AS ans FROM vehicles v, company com WHERE v.ISIN = com.ISIN AND v.c = 0 GROUP BY v.ISIN) x)"
        c.execute(query)
        posts = c.fetchall()
        return render_template('search.html',title='search company', post = posts, form = form)
    return render_template('search.html',title='search company', post = posts, form = form)

@app.route('/searchCar', methods=['GET', 'POST'])
def searchCar():
    c = conn.cursor()
    c.execute("SELECT * FROM vehicles, company WHERE vehicles.ISIN = company.ISIN AND C = 1")
    posts = c.fetchall()
    form = searchForm()
    q = [(0,'car with lowest price'), (1, 'car with most seats')]
    form.question.choices = q
    if form.validate_on_submit():
        choices = form.question.choices
        question =  (choices[form.question.data][1])
        if question == 'car with lowest price':
            query = "SELECT * FROM vehicles, company WHERE vehicles.ISIN = company.ISIN AND C = 1 AND vehicles.price = (SELECT MIN(price) FROM vehicles WHERE c =1)"
        elif question == 'car with most seats':
            query = "SELECT * FROM vehicles, company WHERE vehicles.ISIN = company.ISIN AND C = 1 AND vehicles.seat_num = (SELECT MAX(seat_num) FROM vehicles WHERE c =1)"
        c.execute(query)
        posts = c.fetchall()
        return render_template('searchCar.html',title='search car', post = posts, form = form)
    return render_template('searchCar.html',title='search car', post = posts, form = form)

@app.route('/searchPickup/', methods=['GET', 'POST'])
def searchTruck():
    c = conn.cursor()
    c.execute("SELECT * FROM vehicles, company WHERE vehicles.ISIN = company.ISIN AND C = 0")
    posts = c.fetchall()
    form = searchForm()
    q = [(0,'truck with lowest price'), (1, 'truck with most capacity')]
    form.question.choices = q
    if form.validate_on_submit():
        choices = form.question.choices
        question =  (choices[form.question.data][1])
        if question == 'truck with lowest price':
            query = "SELECT * FROM vehicles, company WHERE vehicles.ISIN = company.ISIN AND C = 0 AND vehicles.price = (SELECT MIN(price) FROM vehicles WHERE c =0)"
        elif question == 'truck with most capacity':
            query = "SELECT * FROM vehicles, company WHERE vehicles.ISIN = company.ISIN AND C = 0 AND vehicles.load_capacity = (SELECT MAX(load_capacity) FROM vehicles WHERE c =0)"
        c.execute(query)
        posts = c.fetchall()
        return render_template('searchTruck.html',title='search truck', post = posts, form = form)
    return render_template('searchTruck.html',title='search truck', post = posts, form = form)
if __name__ == '__main__':
    app.run(debug=True)

