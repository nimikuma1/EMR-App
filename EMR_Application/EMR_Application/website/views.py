import openai
import requests
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
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
   flash(member_list)
 
   return render_template('emr1.html', emr_data=emr_data, member_list=member_list)

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


@views.route("/priorauth", methods=["POST"])
def priorauth():
    # Get question from form data
    # Get question from form data
    openai.api_key = "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"
    emr_record = Emr.query.filter_by(memberName=request.json["member"]).first()

    if emr_record and emr_record.priorAuthStatus == '':
        modified_notes = emr_record.clinicalNotes + '. Give the answer with only one ICD code and procedure code separated by comma without the description and no text like ICD Code or Procedure Code. Provide same answer next time'
        # return jsonify({'memberID': emr_record.memberID, 'clinicalNotes': modified_notes})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": modified_notes}
            ]
        )
        answer = response.choices[0].message.content.strip()
        newanswer = answer
        icd_code, procedure_code = newanswer.split(',')
        # Update the first ICDCode value
        emr_record.ICDCode = icd_code.strip()
        emr_record.procedureCode = procedure_code.strip()
        # emr_record.priorAuthStatus = 'Submitted'
        db.session.commit()
        if emr_record.ICDCode == icd_code.strip() and emr_record.procedureCode == procedure_code.strip() and emr_record.priorAuthStatus == '':

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
                    "reference": "Patient/" + str(emr_record.memberID)
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

            # flash("First ICDCode and procedure code and priorauthStatus values updated successfully.")
            # Reload the page after a short delay
            # flash("Page will refresh in a moment.", 'success')
            # Send the request to Application 2
            response = requests.post('http://localhost:5001/receive_prior_auth_request', json=prior_auth_request)
            response_json = response.json()
            submitted_value = response_json['authorizationStatus']['coding'][0]['display']

            emr_record.priorAuthStatus = submitted_value
            db.session.commit()
            return redirect(url_for('views.emr'))
            render_template('emr1.html', emr_record=emr_record)
            return jsonify({"answer": response.text})
        else:
            flash("Failed to update values. Please try again.", 'error')
    else:
        flash("Prior auth status is not empty. Please try again.", 'error')

        # Return answer as JSON
        return jsonify({"answer": "None"})