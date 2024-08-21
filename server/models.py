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
    def validate_name(self, key, name):
        if not name or name in [auth.name for auth in Author.query.all()]:
            raise ValueError("Failed name validation. Key in a unique name.")
        return name

    @validates('phone_number')
    def validate_number(self, key, number):
        if type(int(number)) != int or len(number) != 10 :
            raise ValueError("Failed number validation. Key in correct phone number.") 
        return number

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
    @validates('title')
    def validate_title(self, key, title):
        if title and "Won't Believe" in title or "Secret" in title or "Top" in title or "Guess" in title:
            return title
        raise ValueError("Failed title validation. Key in an appropriate title.")
        
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Failed content validation. Content must have a minimum of 250 characters.")
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Failed summary validation. Summary must have a maximum of 250 characters.")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category == "Fiction" or category == "Non-Fiction":
            return category
        raise ValueError("Failed category validation. Category should be either Fiction or Non-Fiction.")

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
