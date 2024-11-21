from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Car, Sale
from config import Config
from datetime import datetime
from sqlalchemy import extract, func
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    cars = Car.query.filter_by(status='available').all()
    return render_template('index.html', cars=cars)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:  # Trực tiếp so sánh mật khẩu
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
            
        user = User(
            username=username,
            password=password,  # Lưu trực tiếp mật khẩu
            email=email
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/add_car', methods=['GET', 'POST'])
@login_required
def add_car():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        car = Car(
            brand=request.form['brand'],
            model=request.form['model'],
            year=int(request.form['year']),
            price=float(request.form['price']),
            description=request.form['description'],
            image_url=request.form['image_url']
        )
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_car.html')

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('car_detail.html', car=car)

@app.route('/purchase_history')
@login_required
def purchase_history():
    # Lấy tất cả các giao dịch mua của người dùng
    sales = Sale.query.filter_by(user_id=current_user.id).all()
    return render_template('purchase_history.html', sales=sales)


@app.route('/buy/<int:car_id>', methods=['POST'])
@login_required
def buy_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.status != 'available':
        flash('Car is not available')
        return redirect(url_for('car_detail', car_id=car_id))
        
    sale = Sale(
        car_id=car.id,
        user_id=current_user.id,
        price=car.price
    )
    car.status = 'sold'
    db.session.add(sale)
    db.session.commit()
    flash('Car purchased successfully')
    return redirect(url_for('index'))

@app.route('/monthly_sales')
@login_required
def monthly_sales():
    # Kiểm tra quyền admin
    if current_user.role != 'admin':
        flash('Unauthorized access')
        return redirect(url_for('index'))
    
    # Lấy tháng và năm hiện tại
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Truy vấn tổng doanh số trong tháng hiện tại
    monthly_stats = db.session.query(
        func.count(Sale.id).label('total_cars'),
        func.sum(Sale.price).label('total_revenue')
    ).filter(
        extract('month', Sale.sale_date) == current_month,
        extract('year', Sale.sale_date) == current_year
    ).first()
    
    # Lấy chi tiết các xe đã bán trong tháng
    monthly_sales = db.session.query(
        Sale, Car
    ).join(
        Car, Sale.car_id == Car.id
    ).filter(
        extract('month', Sale.sale_date) == current_month,
        extract('year', Sale.sale_date) == current_year
    ).all()
    
    return render_template(
        'monthly_sales.html',
        total_cars=monthly_stats.total_cars or 0,
        total_revenue=monthly_stats.total_revenue or 0,
        monthly_sales=monthly_sales,
        current_month=datetime.now().strftime('%B %Y')
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)