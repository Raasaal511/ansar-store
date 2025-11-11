from datebase import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from datetime import datetime



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
    id: Mapped[int] = mapped_column(Integer, primary_key= True)
    name: Mapped[str] = mapped_column(String(50))
    products: Mapped[list['Product']] = relationship('product', back_populates='brand')
    
    
class Tag(Base): 
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    products: Mapped[list['Priduct'] = relationship("Product", secondary=product_tags, back_populates="tags")]
    
    
class Review(Base):
    __tablename__ = 'reviews'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rating: Mapped[int]  = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(255))
	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
	updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 

class ProductImage(Base):
    __tablename__ = "product_image"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    url: Mapped[str] = mapped_column(String)
    is_main: Mapped[bool] = mapped_column(Boolean, default=False)
    product: Mapped["Product"] = relationship("Product", back_populates="images")
    
    
class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    characteristic: Mapped[str] = mapped_column(String)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    availability_count: Mapped[int] = mapped_column(Integer, default=0)
