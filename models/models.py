from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    ForeignKey,
    TIMESTAMP,
    Float,
)
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.orm import relationship

# Single db instance shared across the whole application
db = SQLAlchemy()


class Shelter(db.Model):
    __tablename__ = "shelters"
    shelter_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    description = Column(Text)
    image = Column(String(200))
    pets = relationship("Pet", back_populates="shelter")


class Animal(db.Model):
    __tablename__ = "animals"
    animal_id = Column(Integer, primary_key=True)
    species = Column(String(100), nullable=False)
    breed = Column(String(100), nullable=False)
    lifespan = Column(String(50))
    diet = Column(Text)
    specifics = Column(Text)
    image = Column(String(200))
    pets = relationship("Pet", back_populates="animal")


class Pet(db.Model):
    __tablename__ = "pets"
    pet_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    description = Column(Text)
    adoption_date = Column(Date, nullable=True)
    image = Column(String(200))
    shelter_id = Column(Integer, ForeignKey("shelters.shelter_id"))
    animal_id = Column(Integer, ForeignKey("animals.animal_id"))
    shelter = relationship("Shelter", back_populates="pets")
    animal = relationship("Animal", back_populates="pets")


class Category(db.Model):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    products = relationship("Product", back_populates="category")


class Product(db.Model):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price_excl_tax = Column(NUMERIC(10, 2), nullable=False)
    price_incl_tax = Column(NUMERIC(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    weight = Column(NUMERIC(10, 2), nullable=False)
    image = Column(String(200))
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    category = relationship("Category", back_populates="products")
    order_products = relationship("OrderProduct", back_populates="product")


class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    address_number = Column(String(10))
    street_name = Column(String(255))
    address_complement = Column(String(255))
    postal_code = Column(String(10))
    city = Column(String(100))
    country = Column(String(100))
    phone = Column(String(20))
    role = Column(String(50), nullable=False, default="user")
    birth_date = Column(Date)
    orders = relationship("Order", back_populates="user")

    def get_id(self):
        # Required by Flask-Login to identify the user in the session
        return str(self.user_id)


class Order(db.Model):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    order_date = Column(TIMESTAMP, nullable=False)
    status = Column(String(50), nullable=False)
    total_price_excl_tax = Column(NUMERIC(10, 2), nullable=False)
    total_price_incl_tax = Column(NUMERIC(10, 2), nullable=False)
    shipping_fee = Column(NUMERIC(10, 2), nullable=False)
    order_products = relationship("OrderProduct", back_populates="order")
    user = relationship("User", back_populates="orders")
    payments = relationship("Payment", back_populates="order")


class OrderProduct(db.Model):
    __tablename__ = "order_products"
    order_id = Column(Integer, ForeignKey("orders.order_id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), primary_key=True)
    quantity = Column(Integer, nullable=False)
    unit_price_excl_tax = Column(NUMERIC(10, 2), nullable=False)
    unit_price_incl_tax = Column(NUMERIC(10, 2), nullable=False)
    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")


class Payment(db.Model):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True)
    payment_method = Column(String(50))
    payment_status = Column(String(50))
    payment_date = Column(TIMESTAMP, nullable=False)
    payment_total = Column(Float, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    order = relationship("Order", back_populates="payments")