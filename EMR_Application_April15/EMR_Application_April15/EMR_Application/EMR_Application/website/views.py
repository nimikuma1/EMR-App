from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Emr
from . import db
import json

views =  Blueprint('views',__name__)

@views.route('/')

def home():
   return render_template("login.html")

@views.route('/emr') 
def emr():
   emr_data = Emr.query.all()
   memberName = db.session.query(Emr.memberName).distinct().all()
   member_list = [id[0] for id in memberName]
   #flash(member_list)
 
   return render_template('emr2.html', emr_data=emr_data, member_list=member_list)

@views.route('/emr/<member_name>')
def show_emr(member_name):
    return emr(member_name)

def emr(member_name):
    emr_data = Emr.query.filter_by(memberName=member_name).all()
    member_list = [member_name]  # Since we are filtering by one member, we only have one member in the list
    
    return render_template('emr2.html', emr_data=emr_data, member_list=member_list)


@views.route('/api', methods=["POST"])
def api():
    if request.method == "POST":
        selected_member = request.json.get("member")
        emr_details = Emr.query.filter_by(memberName=selected_member).all()
        formatted_details = [{
            "memberID": detail.memberID,
            "memberName": detail.memberName,
            "memberSex": detail.memberSex,
            "memberDOB": detail.memberDOB,
            "payor": detail.payor,
            "clinicalNotes": detail.clinicalNotes,
            "ICDCode": detail.ICDCode,
            "procedureCode": detail.procedureCode,
            "priorAuthStatus": detail.priorAuthStatus

        } for detail in emr_details]
        return jsonify({"emr_details": formatted_details})
