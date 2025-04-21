from sqlalchemy import Column, Integer, String, Boolean, Float, Date, Text, ForeignKey
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(50))  # admin, returns, hub, billing

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date)
    first_name = Column(String(100))
    last_name = Column(String(100))
    shipment_id = Column(String(50))
    client_order_id = Column(String(50))
    pi = Column(String(50))
    order_quantity = Column(Integer)
    hub = Column(String(100))
    client_id = Column(String(50))
    shipping_method = Column(String(100))
    address = Column(Text)

class Return(Base):
    __tablename__ = "returns"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    order_date = Column(Date)
    first_name = Column(String(100))
    last_name = Column(String(100))
    shipment_id = Column(String(50))
    client_order_id = Column(String(50))
    pi = Column(String(50))
    order_quantity = Column(Integer)
    hub = Column(String(100))
    client_id = Column(String(50))
    shipping_method = Column(String(100))
    address = Column(Text)
    r_shipping_method = Column(String(100))
    r_tracking_info = Column(String(100))
    r_date_returned = Column(Date)
    r_items_returned = Column(Integer)
    r_retuned_hub = Column(Boolean)
    r_return_reason = Column(String(100))
    r_condition = Column(String(100))
    r_comments = Column(String(100))
    r_processed_date = Column(Date)
    h_booked_back = Column(Boolean)
    h_condition = Column(String(100))
    h_comments = Column(String(100))
    h_processed_date = Column(Date)
    b_billed = Column(Boolean)
    b_billing_Value = Column(Float)
