
import requests
import json

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['JWT_SECRET_KEY'] = 'myjwtsecretkey'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# Routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.email)
        return jsonify({"token": access_token}), 200  # Return token on successful login
    return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password,username=username)
    db.session.add(new_user)


    # Replace with your actual data
    tezkit_app_p_data = {
        "auth_key": "amV3ZWxlcnlraW5nX19TRVBSQVRPUl9fdjJhcHAx",
        "tenant": "jeweleryking",
        "tenant_id": "1",
        "app_name": "v2app1",
    }
    user_data = {
        "uid": new_user.username,
    }

    req_url = "https://gfxb0jf19k.execute-api.ap-south-1.amazonaws.com/prod/onboarding"

    headers = {
        "Accept": "*/*",
        "User-Agent": "Python Requests",  # Optional, can be customized
        "X-API-Key": tezkit_app_p_data["auth_key"],
        "Content-Type": "application/json",
    }

    payload = {
        "tenant": tezkit_app_p_data["tenant"],
        "tenant_id": tezkit_app_p_data["tenant_id"],
        "uid": user_data["uid"],
        "app_name": tezkit_app_p_data["app_name"],
    }

    # try:
    response = requests.post(req_url, headers=headers, json=payload)


    response.raise_for_status()  # Raises HTTPError if the response status code is 4xx, 5xx

    data = response.json()  # Parse JSON response
    print("Response data:", data)

    
    print("new_user.username",new_user.username)



    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # Extract email from form data
        password = request.form.get('password')  # Extract password from form data

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.email)
            return jsonify({"token": access_token}), 200  # Returning token to the frontend
        return jsonify({'error': 'Invalid credentials'}), 401

    # Handle GET request: render login form
    return render_template('login.html')


@app.route('/api/profile')
@jwt_required()
def api_profile():
    current_user = get_jwt_identity()
    print("current user",current_user)
    user = User.query.filter_by(email=current_user).first()
    
    user_data = {
        'username': user.username,
        'email': user.email,
    }
    
    return jsonify(user_data)

@app.route('/profile')
def profile_page():
    # Just return the profile page without passing data to it
    return render_template('profile.html')



@app.route('/products')
def products():
    products_list = Product.query.all()
    return render_template('products.html', products=products_list)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=5001)
