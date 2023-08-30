from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database import mongo

class Product:
    def add_product(name, description, price, image):
        product = {
            "name": name,
            "description": description,
            "price": price,
            "image": image
        }
        mongo.db.product_template.insert_one(product)
        
    def get_products():
        return list(mongo.db.products.find())
    
    def get_product(product_id):
        return mongo.db.product_template.find_one({"_id": product_id})
    
    def update_product(product_id, name, description, price, image):
        mongo.db.product_template.update_one(
            {"_id": product_id},
            {"$set": {"name": name, "description": description, "price": price, "image": image}}
        )
        
    def delete_product(product_id):
        mongo.db.product_template.delete_one({"_id": product_id})


class User(UserMixin):
    def __init__(self, username, email, password, roles):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.roles = roles

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role):
        return role in self.roles
    
class UserManager:
    @staticmethod
    def create_user(username, email, password, roles):
        password_hash = generate_password_hash(password)
        user = User(username, email, password_hash, roles)
        mongo.db.users.insert_one({
            "username": user.username,
            "email": user.email,
            "password_hash": user.password_hash,
            "roles": user.roles
        })

    @staticmethod
    def get_user_by_username(username):
        user_data = mongo.db.users.find_one({"username": username})
        if user_data:
            return User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=user_data["password_hash"],
                roles=user_data["roles"]
            )
        return None