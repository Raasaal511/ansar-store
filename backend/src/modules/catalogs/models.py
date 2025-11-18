from database import Base 
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Boolean, Numeric, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from datetime import datetime
from typing import List
from decimal import Decimal 


product_tags = Table(
    'product_tags',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)

class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')


class Brand(Base):
    __tablename__ = 'brands'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    products: Mapped[list['Product']] = relationship('Product', back_populates='brand')
    
class Tag(Base): 
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    products: Mapped[list['Product']] = relationship("Product", secondary=product_tags, back_populates="tags") # Corrected 'Priduct' to 'Product'
    
    
class Review(Base):
    __tablename__ = 'reviews'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rating: Mapped[int]  = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product: Mapped["Product"] = relationship("Product", back_populates="reviews") 
 

class ProductImage(Base):
    __tablename__ = "product_images" 
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id")) 
    url: Mapped[str] = mapped_column(String)
    is_main: Mapped[bool] = mapped_column(Boolean, default=False)
    product: Mapped["Product"] = relationship("Product", back_populates="images")
    
    
class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text) 
    characteristic: Mapped[str | None] = mapped_column(Text, nullable=True) 
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    availability_count: Mapped[int] = mapped_column(Integer, default=0)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
 
 
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
 

 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow) # Added from ERD
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) # Added from ERD
	

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    brand: Mapped["Brand"] = relationship("Brand", back_populates="products")
    images: Mapped[List["ProductImage"]] = relationship("ProductImage", back_populates="product")
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary=product_tags, back_populates="products")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="product") # Corrected name from 'review' to 'reviews' list
