"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class MenuItem(BaseModel):
    """
    Menu items offered by Flavor Factory
    Collection name: "menuitem"
    """
    name: str = Field(..., description="Dish name")
    description: Optional[str] = Field(None, description="Short description of the dish")
    price: float = Field(..., ge=0, description="Price in local currency")
    category: str = Field(..., description="e.g., Burgers, Mains, Sides, Drinks, Dessert")
    is_drive_thru_friendly: bool = Field(True, description="Suitable for quick drive‑thru service")
    image: Optional[str] = Field(None, description="Image URL")

class Inquiry(BaseModel):
    """
    Contact or booking inquiries from the website
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Customer name")
    email: str = Field(..., description="Customer email")
    message: str = Field(..., description="Inquiry details")
    location: Optional[str] = Field(None, description="Preferred city/location")
    guests: Optional[int] = Field(None, ge=1, description="Guests for reservation if applicable")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
