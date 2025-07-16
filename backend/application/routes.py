from flask import current_app as app, jsonify, request, abort
from .models import User, UserCardDetail
from .database import db
from flask_jwt_extended import create_access_token, current_user, jwt_required 
from functools import wraps
import random
import string
from celery.result import AsyncResult
from .tasks import csv_report, monthly_report, generate_msg

# role required decorator
def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify(msg="Access denied: insufficient role"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


# login api route 
@app.route("/api/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none() # .first()
    if not user or not user.password == password:
        return jsonify(message = "Wrong username or password"), 400

    # Notice that we are passing in the actual sqlalchemy user object here
    access_token = create_access_token(identity=user) # "user" is object
    return jsonify(access_token=access_token)

# register api route 
@app.route("/api/register", methods=["POST"])
def register():
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username = username).first()
    if user:
        return jsonify("User already exists"), 400
    
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify("User added succesfully"), 201

# dashboard
@app.route("/api/dashboard")
@jwt_required()
def dashboard():
    if current_user.role == "admin":
        users = len(User.query.filter_by(role = "user").all())
        card_requests = UserCardDetail.query.filter_by(attr_name = "status").all()
        requested = under_verification = verified = generated = 0
        card_request_json = []
        for detail in card_requests:
            detail_dict = {}
            detail_dict["username"] = detail.bearer.username
            detail_dict["cardname"] = detail.cardname
            detail_dict["status"] = detail.attr_val
            if detail.attr_val == "requested":
                requested += 1
            if detail.attr_val == "under_verification":
                under_verification += 1
            if detail.attr_val == "verified":
                verified += 1
            if detail.attr_val == "generated":
                generated += 1
            card_request_json.append(detail_dict)
        return jsonify({
            "role": current_user.role,
            "admin_name": current_user.username,
            "users": users,
            "card_requests": requested,
            "under_verification": under_verification,
            "verified": verified,
            "card_granted": generated,
            "available_cards": 4,
            "card_request_details": card_request_json
        })
    else:
        user_card_details = UserCardDetail.query.filter_by(attr_name = "status", user_id = current_user.id).all()
        available_cards = []
        card_requests = []
        for detail in user_card_details:
            detail_dict = {}
            if detail.attr_val == "generated":
                detail_dict["cardname"] = detail.cardname
                available_cards.append(detail_dict)
            else:
                detail_dict["cardname"] = detail.cardname
                detail_dict["status"] = detail.attr_val
                card_requests.append(detail_dict)
        return jsonify({
            "role": current_user.role,
            "username": current_user.username,
            "available_cards": available_cards,
            "card_requests": card_requests
        })
    

# ================ admin apis ==================

# Generate card api route
@app.route("/api/generate/<string:cardname>/<int:user_id>")
@role_required("admin")
def generate(cardname, user_id):
    # status to change to "generated"
    detail = UserCardDetail.query.filter_by(user_id=user_id,cardname=cardname,attr_name="status").first()
    detail.attr_val = "generated"
    db.session.commit()
    # creating of unique key wrt card  
    key = ""
    if cardname == "aadhar":
        key = random.randint(10**11, 10**12 - 1) # 1234 5678 9101  [1000 0000 0000 - 9999 9999 9999]
    elif cardname == "pan":
        first_part = ''.join(random.choices(string.ascii_uppercase, k=5)) # [A, B, R, U, H] --> ABRUH
        middle_part = ''.join(random.choices(string.digits, k=4))
        last_part = random.choice(string.ascii_uppercase)
        key = first_part + middle_part + last_part # ABCDE + 1234 + F
    elif cardname == "driving":
        part1 = ''.join(random.choices(string.ascii_uppercase, k=2))
        part2 = ''.join(random.choices(string.digits, k=2))
        part3 = ''.join(random.choices(string.digits, k=7))
        key = part1 + "-" + part2 + "-2025-" + part3 # AB-12-2025-3456789
    elif cardname == "election":
        first_part = ''.join(random.choices(string.ascii_uppercase, k=3))
        last_part = ''.join(random.choices(string.digits, k=7))
        key = first_part + last_part # ABC1234567
    info1 = UserCardDetail(attr_name="key",attr_val=key,cardname=cardname,user_id=user_id)
    db.session.add(info1)
    db.session.commit()
    res = generate_msg.delay(detail.bearer.username, cardname)
    return {
        "message": f"{cardname} card created for user: {user_id}",
        "key": key
    }

# Update card status api route 
@app.route("/api/update/<string:cardname>/<int:user_id>")
@role_required("admin")
def update_status(cardname, user_id):
    new_status = request.json.get("status", None)
    detail = UserCardDetail.query.filter_by(user_id=user_id,cardname=cardname,attr_name="status").first()
    old_status = detail.attr_val
    detail.attr_val = new_status
    db.session.commit()
    return jsonify(message = f"card status changed from {old_status} to {new_status}.")

# ===================== user apis ================

# Request card api route 
@app.route("/api/request/<string:cardname>", methods=['POST'])
@role_required("user")
def request_card(cardname):
    if cardname == "aadhar":
        fullname = request.json.get("fullname", None)
        dob = request.json.get("dob", None)
        address = request.json.get("address", None)
        gender = request.json.get("gender", None)
        ph = request.json.get("ph", None)

        attr1 = UserCardDetail(attr_name = "fullname", attr_val = fullname, cardname = cardname, user_id = current_user.id)
        attr2 = UserCardDetail(attr_name = "dob", attr_val = dob, cardname = cardname, user_id = current_user.id)
        attr3 = UserCardDetail(attr_name = "address", attr_val = address, cardname = cardname, user_id = current_user.id)
        attr4 = UserCardDetail(attr_name = "gender", attr_val = gender, cardname = cardname, user_id = current_user.id)
        attr5 = UserCardDetail(attr_name = "ph", attr_val = ph, cardname = cardname, user_id = current_user.id)
        attr6 = UserCardDetail(attr_name = "status", attr_val = "requested", cardname = cardname, user_id = current_user.id)

        db.session.add_all([attr1, attr2, attr3, attr4, attr5, attr6])
        db.session.commit()
    elif cardname == "pan":
        fullname = request.json.get("fullname", None)
        dob = request.json.get("dob", None)
        ph = request.json.get("ph", None)

        attr1 = UserCardDetail(attr_name = "fullname", attr_val = fullname, cardname = cardname, user_id = current_user.id)
        attr2 = UserCardDetail(attr_name = "dob", attr_val = dob, cardname = cardname, user_id = current_user.id)
        attr3 = UserCardDetail(attr_name = "ph", attr_val = ph, cardname = cardname, user_id = current_user.id)
        attr4 = UserCardDetail(attr_name = "status", attr_val = "requested", cardname = cardname, user_id = current_user.id)

        db.session.add_all([attr1, attr2, attr3, attr4])
        db.session.commit()

    elif cardname == "voter":
        fullname = request.json.get("fullname", None)
        dob = request.json.get("dob", None)
        address = request.json.get("address", None)
        ward = request.json.get("ward", None)
        ph = request.json.get("ph", None)

        attr1 = UserCardDetail(attr_name = "fullname", attr_val = fullname, cardname = cardname, user_id = current_user.id)
        attr2 = UserCardDetail(attr_name = "dob", attr_val = dob, cardname = cardname, user_id = current_user.id)
        attr3 = UserCardDetail(attr_name = "address", attr_val = address, cardname = cardname, user_id = current_user.id)
        attr4 = UserCardDetail(attr_name = "ward", attr_val = ward, cardname = cardname, user_id = current_user.id)
        attr5 = UserCardDetail(attr_name = "ph", attr_val = ph, cardname = cardname, user_id = current_user.id)
        attr6 = UserCardDetail(attr_name = "status", attr_val = "requested", cardname = cardname, user_id = current_user.id)

        db.session.add_all([attr1, attr2, attr3, attr4, attr5, attr6])
        db.session.commit()

    else:
        fullname = request.json.get("fullname", None)
        v_no = request.json.get("v_no", None)
        type = request.json.get("type", None)

        attr1 = UserCardDetail(attr_name = "fullname", attr_val = fullname, cardname = cardname, user_id = current_user.id)
        attr2 = UserCardDetail(attr_name = "v_no", attr_val = v_no, cardname = cardname, user_id = current_user.id)
        attr3 = UserCardDetail(attr_name = "type", attr_val = type, cardname = cardname, user_id = current_user.id)
        attr4 = UserCardDetail(attr_name = "status", attr_val = "requested", cardname = cardname, user_id = current_user.id)

        db.session.add_all([attr1, attr2, attr3, attr4])
        db.session.commit()

    return jsonify(message = f"request for {cardname} made successfully")

# View card api route 
@app.route("/api/view/<string:cardname>")
@role_required("user")
def view_card(cardname):
    card_details = current_user.card_details
    details_json = []
    for detail in card_details:
        detail_dict = {}
        detail_dict["attr_name"] = detail.attr_name
        detail_dict["attr_val"] = detail.attr_val
        details_json.append(detail_dict)
    return jsonify(details_json)



# backend jobs trigger
@app.route('/export_csv')
def export():
    result = csv_report.delay()
    return {
        "id": result.id,
        "result": result.result
    }

@app.route('/api/csv_result/<id>') # just create to test the status of result
def csv_result(id):
    res = AsyncResult(id)
    # return {
    #     "filename": res.result
    # }
    return send_from_directory('static', res.result)

@app.route('/api/send_mail')
def send_mail():
    res = monthly_report.delay()
    return {
        "message": res.result
    }