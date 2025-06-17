from flask import current_app as app, jsonify, request, abort
from .models import User
from flask_jwt_extended import create_access_token, current_user, jwt_required 

def role_required(required_role):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify(message = "You are not authorized"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none() # .first()
    if not user or not user.password == password:
        return jsonify("Wrong username or password"), 401

    # Notice that we are passing in the actual sqlalchemy user object here
    access_token = create_access_token(identity=user) # "user" is object
    return jsonify(access_token=access_token)

# @app.route("/who_am_i", methods=["GET"])
# @jwt_required()
# def protected():
#     # We can now access our sqlalchemy User object via `current_user`.
#     return jsonify(
#         id=current_user.id,
#         username=current_user.username,
#         email=current_user.email,
#         password=current_user.password,
#         role=current_user.role
#     )

# dashboard
@app.route("/dashboard")
@jwt_required()
def dashboard():
    if current_user.role == "admin":
        return "welcome to admin dashboard!"
    else:
        return "welcome to user dashboard!"

@app.route("/onlyadmin")
@role_required("admin")
def admin_enpoint():
    return "Only admin is allowed"

# ===================== decorator syntax ===================
# def decorator_name():
#     def wrapper(func):
#         # additional functioanlity is added here
#         func()
#         return func 
#     return wrapper 

# @decorator_name()


# def decorator_name(argument):
#     def wrapper(func):
#         def decor(*args, **kwargs)
#             # additional functioanlity is added here
#             return func(*args, **kwargs)
#         return decor
#     return wrapper 
# @decorator_name("argument")