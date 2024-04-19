from flask import Flask, request_started
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from .models import PriorauthVal
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import openai, requests,json
import os
from .models import Emr

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        password = request.form.get('password')
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            # new_emr = Emr(memberID=2, memberSex='M',memberDOB = datetime.strptime("2000-05-15", "%Y-%m-%d").date(), payor = 'UHG', clinicalNotes = 'Knee Surgery is needed' )  #providing the schema for the note
            # db.session.add(new_emr) #adding the note to the database
            # db.session.commit()
            # flash('Emr added!', category='success')

            # new_emr = Emr(memberID=1,memberName = 'John Doe', memberSex='M',memberDOB = datetime.strptime("2000-05-15", "%Y-%m-%d").date(), payor = 'UHG', clinicalNotes = 'Knee Surgery is needed' )  #providing the schema for the note
            # db.session.add(new_emr) #adding the note to the database
            # db.session.commit()
            # flash('Emr added!', category='success')

            return redirect(url_for('views.emr'))
        else:
            flash('Incorrect password, try again.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(
                password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("base.html", user=current_user)


# Define route for API endpoint
@auth.route("/priorauth", methods=["POST"])
def priorauth():
    # Get question from form data
  # Get question from form data
    openai.api_key = "sk-proj-MBQjxEiylpZfNbZMdSRsT3BlbkFJDoEgQ1VVPD2D1CgyHpV5"
    emr_record = Emr.query.filter_by(memberName=request.json["member"]).first()
    
    if emr_record and emr_record.priorAuthStatus == '':
        modified_notes = emr_record.clinicalNotes + '. Give the answer with only one ICD code and procedure code separated by comma without the description and no text like ICD Code or Procedure Code. Provide same answer next time'
        #return jsonify({'memberID': emr_record.memberID, 'clinicalNotes': modified_notes})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": modified_notes}
            ],
            temperature=0.0
        )
        answer = response.choices[0].message.content.strip()
        newanswer = answer
        icd_code, procedure_code = newanswer.split(',')
       # Update the first ICDCode value
        emr_record.ICDCode = icd_code.strip()
        emr_record.procedureCode = procedure_code.strip()
        memberName = request.json["member"]
        #emr_record.priorAuthStatus = 'Submitted'
        db.session.commit()
        flash(icd_code.strip())
        #existing_icd_code = PriorauthVal.query.filter_by(ICDCode = icd_code.strip()).first()
        existing_icd_code = PriorauthVal.query.filter_by().all()
        flash(existing_icd_code)
        #if existing_icd_code:
        if emr_record.ICDCode == icd_code.strip() and  emr_record.procedureCode == procedure_code.strip() and emr_record.priorAuthStatus == '':
                    
                    prior_auth_request = {
                        "resourceType": "AuthorizationRequest",
                        "id": str(emr_record.memberID),
                        "text": {
                            "status": "generated",
                            "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">AuthorizationRequest for Prior Authorization</div>"
                        },
                        "status": "active",
                        "intent": "order",
                        "subject": {
                            "reference": "Patient/" + str(emr_record.memberID),
                            "display": memberName  # Add member's name her
                        },
                        "insurance": [
                            {
                                "reference": "Coverage/" + emr_record.payor 
                            }
                        ],
                        "supportingInfo": [

                            {
                                "sequence": 1,
                                "category": {
                                    "coding": [
                                        {
                                            "system": "http://terminology.hl7.org/CodeSystem/claiminformationcategory",
                                            "code": "pharmacy",
                                            "display": "Pharmacy"
                                        }
                                    ]
                                },
                                "code": {
                                    "coding": [
                                        {
                                            "system": "http://terminology.hl7.org/CodeSystem/claiminformationcategory",
                                            "code": "priorauth",
                                            "display": "Prior Authorization"
                                        }
                                    ]
                                },
                                "valueReference": {
                                    "reference": "MedicationRequest/example"
                                }
                            },
                            {
                                "sequence": 2,
                                "category": {
                                    "coding": [
                                        {
                                            "system": "http://terminology.hl7.org/CodeSystem/claiminformationcategory",
                                            "code": "diagnosis",
                                            "display": "Diagnosis"
                                        }
                                    ]
                                },
                                "code": {
                                    "coding": [
                                        {
                                            "system": "http://hl7.org/fhir/sid/icd-10",
                                            "code": emr_record.ICDCode,
                                            "display": "Diagnosis Code"
                                        }
                                    ]
                                }
                            },
                            {
                                "sequence": 3,
                                "category": {
                                    "coding": [
                                        {
                                            "system": "http://terminology.hl7.org/CodeSystem/claiminformationcategory",
                                            "code": "procedure",
                                            "display": "Procedure"
                                        }
                                    ]
                                },
                                "code": {
                                    "coding": [
                                        {
                                            "system": "http://www.ama-assn.org/go/cpt",
                                            "code": emr_record.procedureCode,
                                            "display": "Procedure Code"
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                    
                    #flash("First ICDCode and procedure code and priorauthStatus values updated successfully.")
                    # Reload the page after a short delay
                # flash("Page will refresh in a moment.", 'success')
                # Send the request to Application 2
                    response = requests.post('http://localhost:5001/receive_prior_auth_request', json=prior_auth_request)
                    response_json = response.json()
                    submitted_value = response_json['authorizationStatus']['coding'][0]['display']

                    emr_record.priorAuthStatus = submitted_value
                    db.session.commit()



                    emr_data = Emr.query.filter_by(memberName=memberName).first()
                    member_list = [memberName]  # Since we are filtering by one member, we only have one member in the list
                    emr_record_dict = {
                                "memberID": emr_data.memberID,
                                "memberName": emr_data.memberName,
                                "memberSex": emr_data.memberSex,
                                "memberDOB": emr_data.memberDOB,
                                "payor": emr_data.payor,
                                "clinicalNotes": emr_data.clinicalNotes,
                                "ICDCode":  emr_data.ICDCode,
                                "procedureCode":  emr_data.procedureCode,
                                "priorAuthStatus": emr_data.priorAuthStatus
                            }
                    #flash(emr_record_dict)
            # Return both the answer and the emr_record dictionary
                    return jsonify({"answer": "Success", "emr_record": emr_record_dict})
                    # Return both the answer and the emr_record
                    return jsonify({"answer": "Success", "emr_record": emr_data[0].to_dict()})

                    emr_data = Emr.query.filter_by(memberName=memberName).all()
                    member_list = [memberName]  # Since we are filtering by one member, we only have one member in the list
        
                    return render_template('emr1.html', emr_data=emr_data, member_list=member_list)
                    
                    #return redirect(url_for('views.emr'))
                    #return render_template('emr1.html', emr_record=emr_record)
                    #return jsonify({"answer": response.text})
            
                    
        #else:
           # flash("The ICD Code does not require priorauth.", 'info')
           # emr_record.priorAuthStatus = 'Prior Auth Not required'
            #'Not Required'
            #db.session.commit()
            #emr_data = Emr.query.filter_by(memberName=memberName).first()
            #member_list = [memberName]  # Since we are filtering by one member, we only have one member in the list
            #emr_record_dict = {
             #           "memberID": emr_data.memberID,
              #          "memberName": emr_data.memberName,
               #         "memberSex": emr_data.memberSex,
               #         "memberDOB": emr_data.memberDOB,
               #         "payor": emr_data.payor,
                #        "clinicalNotes": emr_data.clinicalNotes,
               #         "ICDCode":  emr_data.ICDCode,
               #         "procedureCode":  emr_data.procedureCode,
               #         "priorAuthStatus": emr_data.priorAuthStatus
                #    }
            #flash(emr_record_dict)
    # Return both the answer and the emr_record dictionary
            #return jsonify({"answer": "Success", "emr_record": emr_record_dict})
            
            

            #emr_record.priorAuthStatus = existing_icd_code.ICDCode
            #'Not Required'
            #db.session.commit()
            #return jsonify({"answer": existing_icd_code})
            #return redirect(url_for('views.api'))

    else:
        flash("Prior auth status is not empty. Please try again.", 'error')

    # Return answer as JSON
        return jsonify({"answer": "None"})
    
@auth.route('/receive_prior_auth_approval_request', methods=['POST'])
def receive_prior_auth_approval_request():
    if request.method == 'POST':
        return render_template("base.html", user=current_user)
        prior_auth_approval_response = request.json
        prior_auth_id = prior_auth_approval_response.get('id')
        submitted_value = prior_auth_approval_response['authorizationStatus']['coding'][0]['display']
        #return render_template("emr1.html", emr_record=emr_record)
        emr_record = Emr.query.filter_by(memberID=int(prior_auth_id))
        emr_record.priorAuthStatus =  submitted_value
        db.session.commit()

        render_template('emr1.html', emr_record=emr_record)
        return jsonify({"answer": prior_auth_approval_response})
    else:
        flash("I am here")
        return "Method not allowed", 405    
