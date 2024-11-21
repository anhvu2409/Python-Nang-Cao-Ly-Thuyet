class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/car_sales_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False