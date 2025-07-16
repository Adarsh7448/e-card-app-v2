from celery import shared_task 
import csv
from jinja2 import Template
from .mail import send_email
from .models import User, UserCardDetail
import datetime
import requests
# from flask import request
# from string import Template

# task 1 - Download CSV report for user.
# User(client) triggered async job 
@shared_task(ignore_results = False, name = "download_csv_report")
def csv_report():
    card_details = UserCardDetail.query.all() # card details
    csv_file_name = f"card_{datetime.datetime.now().strftime("%f")}.csv" #card_123456.csv
    with open(f'static/{csv_file_name}', 'w', newline = "") as csvfile:
        sr_no = 1
        card_csv = csv.writer(csvfile, delimiter = ',')
        card_csv.writerow(['Sr No.', 'Attribute Name', 'Attribute Type', 'Card Name', 'User ID'])
        for c in card_details:
            this_card = [sr_no, c.attr_name, c.attr_val, c.cardname, c.user_id]
            card_csv.writerow(this_card)
            sr_no += 1

    return csv_file_name


# task 2 - Monthly report sent via mail 
# scheduled job via crontab 
@shared_task(ignore_results = False, name = "monthly_report")
def monthly_report():
    users = User.query.all()
    for user in users[1:]:
        user_data = {}
        user_data['username'] = user.username
        user_data['email'] = user.email
        details = []
        card_details = UserCardDetail.query.filter_by(attr_name = "status", user_id = user.id)
        for info in card_details:
            info_dict = {}
            info_dict["cardname"] = info.cardname
            info_dict["status"] = info.attr_val
            details.append(info_dict)
        user_data['details'] = details 
        # till this point you get user data in list of dict form
        mail_template = """
        <h3>Dear {{user_data.username}}</h3>
        <p>Please find the current status of your cards in the table below.</p>
        <p>Visit our ecard app at http://127.0.0.1:5173 for details.</p>
        <table>
            <tr>
                <th>Card Name</th>
                <th>Status</th>
            </th>
            </tr>
            {% for detail in user_data.details %}
            <tr>
                <td>{{detail.cardname}}</td>
                <td>{{detail.status}}</td>
            </tr>
            {% endfor %}
        </table>
        <h5>Regards<br>
        <h5>E card V2<br>
        <h5>IITM BS Degree</h5>
        """
        message = Template(mail_template).render(user_data = user_data)
        # the data is then rendered into a mail body
        send_email(user.email, subject = "Monthly card detail Report - E card", message = message)
    return "Monthly reports sent" 

# user_data = {
#     username: 
#     email:
#     details: [
#         {
#             Cardname:
#             status:
#         }
#     ]
# }

# task 3 - Card generation update sent via G-chat webhook
# Backend(endpoint) triggered async job
@shared_task(ignore_results = False, name = "generate_msg")
def generate_msg(username, cardname):
    text = f"Hi {username}, your {cardname} card has been generated. Please check the app at http://127.0.0.1:5173"
    response = requests.post("https://chat.googleapis.com/v1/spaces/AAAAGfF3foI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=gpn4rKlqCta9pKqgherO4fwknc0i4YMj06UkaRJW4CU", json = {"text": text})
    print(response.status_code)
    return "The delivery is sent to user"


# requests.<method>(url, json = {})
# https://chat.googleapis.com/v1/spaces/AAQAiO_PXAU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Mf5TP2Cxf2kPQAdmbETBFkRXdGTfxALSQDgt3XZ8Pfw

