from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT

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

#-------------------------------------
#-------------- cluster
#-------------------------------------
class Classifictions_FOR_Factors(db.Model): # در این جدول طبقه بندی های دسته بندی ها وجود دارند با نام و قیمت
    __tablename__ = 'Classifictions_FOR_Factors'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(191), nullable=False)
    price = db.Column(db.BigInteger, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

class PER_Classifictions_FOR_Factors(db.Model): # در این جدول به هر طبقه بندی دسته بندی های جدا الصاق شده اند
    __tablename__ = 'PER_Classifictions_FOR_Factors'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    Classifictions_id_created = db.Column(db.BigInteger, nullable=False) # classification id
    Classifictions_FOR_Factors_id_created = db.Column(db.BigInteger, nullable=False) # cluster id
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

#-------------------------------------
#-------------- Files
#-------------------------------------
class Posts(db.Model):
    __tablename__ = 'Posts'
    #----------------- start
    # general details
    id = db.Column(db.BigInteger, primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(191), unique=True, nullable=False)
    # number
    number = db.Column(db.String(191), nullable=False)
    # location details
    city = db.Column(db.BigInteger, nullable=False)
    city_text = db.Column(db.String(191), nullable=False)
    mahal = db.Column(db.BigInteger, nullable=False)
    mahal_text = db.Column(db.String(191), nullable=False)
    map = db.Column(db.Text)
    # type
    type = db.Column(db.BigInteger, nullable=False)
    type_text = db.Column(db.String(191), nullable=False)
    # title and desck and images
    title = db.Column(db.String(191), nullable=False)
    desck = db.Column(db.Text)
    Images = db.Column(db.Text)
    # more details
    price = db.Column(db.BigInteger, nullable=False)
    price_two = db.Column(db.BigInteger, nullable=False)
    meter = db.Column(db.BigInteger, nullable=False)
    Otagh = db.Column(TINYINT(unsigned=True))
    Make_years = db.Column(db.BigInteger)
    # true false details
    PARKING = db.Column(db.Boolean, default=False)
    ELEVATOR = db.Column(db.Boolean, default=False)
    CABINET = db.Column(db.Boolean, default=False)
    BALCONY = db.Column(db.Boolean, default=False)
    # dict data
    details = db.Column(db.Text)
    # date
    date_created_persian = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default= datetime.now())  # Use datetime.utcnow for default value
    