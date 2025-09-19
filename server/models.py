from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Name is required.")
        duplicate_name = db.session.query(Author.id).filter_by(name = value).first()
        if duplicate_name is not None:
            raise ValueError("Name must be unique.")
        return value
        
    @validates('phone_number')
    def validate_phone(self, key, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits")
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, value):
        if len(value) < 250:
            raise ValueError("Content must be at least 250 characters long")
        return value
    
    @validates('summary')
    def validate_summary(self, key, value):
        if len(value) > 250:
            raise ValueError("Summary must be less than 250 characters long")
        return value
    
    @validates('category')
    def validate_category(self, key, value):
        if value not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be either Fiction or Non-Fiction")
        return value
    
    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError("Title is required")
        if not any(word in value for word in ["Won't Believe", "Secret", "Top", "Guess"]):
            raise ValueError("Title must be clickbait")
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
