from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class users_admin(db.Model):
    __tablename__ = 'users_admin'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(191), unique=True, nullable=False)
    password = db.Column(db.String(191), nullable=False)
    status = db.Column(db.Integer, nullable=False) # 0 not active 1 active
    type = db.Column(db.Integer, nullable=False) # 1 super admin 2 admin 3 karshenas 4 ...
    name = db.Column(db.String(191), nullable=False)
    phone = db.Column(db.String(191), nullable=False)
    address = db.Column(db.Text)
    email = db.Column(db.String(191), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(191), unique=True, nullable=False)
    password = db.Column(db.String(191), nullable=False)
    name = db.Column(db.String(191), nullable=False)
    phone = db.Column(db.String(191), nullable=False)
    address = db.Column(db.Text)
    email = db.Column(db.String(191), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    user_access = relationship('UserAccess', back_populates='user', cascade='all, delete-orphan')

class Neighborhood(db.Model): # این جدول محلات رو در بر دارد
    __tablename__ = 'Neighborhoods'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(191), nullable=False)
    city_id = db.Column(db.BigInteger, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    classifications = relationship('ClassificationNeighborhood', back_populates='neighborhood')

class Neighborhoods_For_Scrapper(db.Model): # این جدول محلات رو در بر دارد
    __tablename__ = 'Neighborhoods_For_Scrapper'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(191), nullable=False)
    neighborhoods_id = db.Column(db.BigInteger, nullable=False)
    scrapper_id = db.Column(db.BigInteger, nullable=False)
    city_id = db.Column(db.BigInteger, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())


#-------------------------------------
#-------------- classifications
#-------------------------------------
class UserAccess(db.Model): # این جدول دسترسی هر یوزر رو ست کرده
    __tablename__ = 'User_Access'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    factor_id = db.Column(db.BigInteger, db.ForeignKey('Factors.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    classifictions_id = db.Column(db.BigInteger, db.ForeignKey('Classifictions.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    expired_at = db.Column(db.DateTime, nullable=False)

    user = relationship('users', back_populates='user_access')  # حذف backref و استفاده از back_populates
    classification = relationship('Classification', back_populates='user_access')

class Classification(db.Model): # در این جدول دسته بندی ها با نام و ... وجود دارند
    __tablename__ = 'Classifictions'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(191), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    neighborhoods = relationship('ClassificationNeighborhood', back_populates='classification')
    user_access = relationship('UserAccess', back_populates='classification')

class ClassificationNeighborhood(db.Model): # در این جدول محلات هر دسته بندی به اون الصاق شده است
    __tablename__ = 'Classifictions_Neighborhoods'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    classifiction_id = db.Column(db.BigInteger, db.ForeignKey('Classifictions.id', ondelete='CASCADE'), nullable=False)
    neighborhood_id = db.Column(db.BigInteger, db.ForeignKey('Neighborhoods.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    classification = relationship('Classification', back_populates='neighborhoods')
    neighborhood = relationship('Neighborhood', back_populates='classifications')

class ClassificationTypes(db.Model): # در این جدول تایپ یا انواع فایل های هر دسته بندی موجود است
    __tablename__ = 'Classifictions_Types'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    classifiction_id = db.Column(db.BigInteger, db.ForeignKey('Classifictions.id', ondelete='CASCADE'), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

class Types_file(db.Model): # این جدول انواع فایل رو ذکر کرده
    __tablename__ = 'Types_file'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(191), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())