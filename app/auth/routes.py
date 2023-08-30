from flask import Blueprint, render_template, request, redirect, url_for
from flask_pymongo import ObjectId
from app.auth import auth_bp
from app.database import mongo
from bson import ObjectId 
from flask import request 
from werkzeug.utils import secure_filename
import os


@auth_bp.route("/")
def index():
    products = mongo.db.product_template.find()
    return render_template("index.html", products=products)

@auth_bp.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = float(request.form["price"])
        image = request.files.get("image")
        
        # Save the image in a folder and get its filename
        image_filename = save_image(image)

        mongo.db.product_template.insert_one({
            "name": name,
            "description": description,
            "price": price,
            "image": image_filename
        })
        return redirect(url_for("auth.index"))

    return render_template("add_product.html")

@auth_bp.route("/edit_product/<product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = mongo.db.product_template.find_one({"_id": ObjectId(product_id)})
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = float(request.form["price"])
        image = request.files.get("image")  # Get the uploaded image

        if image:
            # Delete the existing image file
            if product.get("image"):
                delete_image(product["image"])

            # Save the new image and get its filename
            image_filename = save_image(image)

            mongo.db.product_template.update_one({"_id": ObjectId(product_id)}, {
                "$set": {
                    "name": name,
                    "description": description,
                    "price": price,
                    "image": image_filename
                }
            })
        else:
            # If no new image is provided, update other fields only
            mongo.db.product_template.update_one({"_id": ObjectId(product_id)}, {
                "$set": {
                    "name": name,
                    "description": description,
                    "price": price
                }
            })
        
        return redirect(url_for("auth.index"))

    return render_template("edit_product.html", product=product)


@auth_bp.route("/delete_product/<product_id>", methods=["POST"])
def delete_product(product_id):
    if request.method == "POST":
        mongo.db.product_template.delete_one({"_id": ObjectId(product_id)})
        return redirect(url_for("auth.index"))
    else:
        # Handle cases where the request method is not POST
        return "Method Not Allowed"


@auth_bp.route("/view_product/<product_id>")
def view_product(product_id):
    product = mongo.db.product_template.find_one({"_id": ObjectId(product_id)})
    if product:
        return render_template("view_product.html", product=product)
    else:
        # Handle product not found case
        return "Product not found"
    


def save_image(image):
    if image:
        image_filename = secure_filename(image.filename)
        image_directory = os.path.join("app", "static", "asset", "image")
        os.makedirs(image_directory, exist_ok=True)  # Create directory if it doesn't exist
        image_path = os.path.join(image_directory, image_filename)
        image.save(image_path)
        return image_filename
    return None


def delete_image(image_filename):
    image_path = os.path.join("app", "static", "asset", "image", image_filename)
    if os.path.exists(image_path):
        os.remove(image_path)
        

@auth_bp.route("/login")
def login():
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Hash password and store user data in the users collection
        hashed_password = generate_hashed_password(password)
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password
        }
        users_collection = mongo.db.users
        users_collection.insert_one(user_data)

        return redirect(url_for("auth.login"))

    return render_template("register.html")

# Define other authentication-related routes and functions here
# ...

def generate_hashed_password(password):
    # Use a library like bcrypt to hash the password securely
    # Return the hashed password
    pass
