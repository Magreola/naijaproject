from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    address = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zipcode = db.Column(db.String(20))
    cake_size = db.Column(db.String(50))
    cake_type = db.Column(db.String(50))
    flavor = db.Column(db.String(50))
    design = db.Column(db.String(100))

    pickup_date = db.Column(db.Date)
    delivery_date = db.Column(db.Date)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/order')
def order():
    return render_template('order.html')
    pickup_date = db.Column(db.Date)
    delivery_date = db.Column(db.Date)

@app.route('/Contact')
def contact():
    return render_template('Contact.html')

@app.route('/submit', methods=['POST'])
def submit():
    pickup = request.form.get('pickup_date')
    delivery = request.form.get('delivery_date')

    new_order = Order(
        id=str(uuid.uuid4())[:8].upper(),
        fname=request.form.get('fname'),
        lname=request.form.get('lname'),
        address=request.form.get('address'),
        city=request.form.get('city'),
        state=request.form.get('state'),
        zipcode=request.form.get('zipcode'),
        cake_size=request.form.get('cake_size'),
        cake_type=request.form.get('cake_type'),
        flavor=request.form.get('flavor'),
        design=request.form.get('design'),  
        pickup_date=datetime.strptime(pickup, '%Y-%m-%d').date() if pickup else None,
        delivery_date=datetime.strptime(delivery, '%Y-%m-%d').date() if delivery else None
    
    )
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('view_order', order_id=new_order.id))


@app.route('/vieworder')
def view_order():
    order_id = request.args.get('order_id')
    if not order_id:
        return "Order ID missing", 400
    order = Order.query.get(order_id)
    if not order:
        return "Order not found", 404
    return render_template('vieworder.html', order=order)

@app.route('/update_order', methods=['GET', 'POST'])
def update_order():
    if request.method == 'GET':
        order_id = request.args.get('order_id')
        print("GET request — order_id =", order_id)
        order = Order.query.get(order_id)
        if not order:
            return f"Order not found for ID: {order_id}", 404
        return render_template('updateorder.html', order=order)

    if request.method == 'POST':
        order_id = request.form.get('order_id')
        print("POST request — order_id =", order_id)
        order = Order.query.get(order_id)
        if not order:
            return "Order not found", 404

        order.fname = request.form.get('fname')
        order.lname = request.form.get('lname')
        order.cake_size = request.form.get('cake_size')
        order.cake_type = request.form.get('cake_type')
        order.flavor = request.form.get('flavor')
        pickup = request.form.get('pickup_date')
        delivery = request.form.get('delivery_date')
        print("Form pickup_date:", pickup)
        print("Form delivery_date:", delivery)
        order.pickup_date = datetime.strptime(pickup, '%Y-%m-%d').date() if pickup else None
        order.delivery_date = datetime.strptime(delivery, '%Y-%m-%d').date() if delivery else None
        db.session.commit()

        return redirect(url_for('view_order', order_id=order.id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("\nAvailable Routes:")
        for rule in app.url_map.iter_rules():
            print(rule)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

