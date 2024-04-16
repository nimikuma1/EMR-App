from flask import Flask, request_started
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
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