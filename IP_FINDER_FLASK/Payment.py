from flask import Flask, render_template, request, redirect, url_for,jsonify
import json
from flask_sqlalchemy import SQLAlchemy
import razorpay


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'vhsdivusdhvjdvwe875478wefwe5f4'

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)


db.create_all()
   
@app.route('/', methods=['GET', 'POST'])
def Index():
    
    if request.method == "POST":
        email = request.form.get('email')
        amount = request.form.get('amount')
        
        user = Users(email=email, amount=amount)
        
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('Pay', id=user.id))
    
    return render_template('index.html')

@app.route('/pay/<id>', methods=['GET', 'POST'])
def Pay(id):
    
    user = Users.query.filter_by(id = id).first()
    
    client = razorpay.Client(auth = ("rzp_test_B9G310atHwH1mj", "DoVc75GlrjPVZ8wYy8oX8j1"))
    payment = client.order.create({'amount': int(user.amount)*100, 'currrency':'INR', 'payment_capture':1})
    
    return render_template('pay.html', payment=payment)


@app.route('/success', methods=['GET', 'POST'])
def Success():
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True)