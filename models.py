from sqlalchemy import Column, Integer, String, DateTime, Float, Date, Time, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from database import Base

class Product(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

    ventas = relationship("Sale", back_populates="producto")


class Sale(Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    hora =Column(Time, nullable=False)
    cantidad =Column(Integer, nullable=False)
    id_producto =Column(Integer, ForeignKey("productos.id"), nullable=False)
    precio_total =Column(Integer, nullable=True )

    producto = relationship("Product", back_populates="ventas")

