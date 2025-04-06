from flask import Blueprint, render_template, request, session, redirect, url_for
import pandas as pd
import os

recommendation_bp = Blueprint("recommendation", __name__)

@recommendation_bp.route("/recommend", methods=["GET", "POST"])
def recommend():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(BASE_DIR, 'data', 'output.csv')

    df = pd.read_csv(csv_path)

    degree_options = sorted(df['degree_names'].dropna().unique())
    language_options = sorted(df['languages'].dropna().unique())
    major1_options = sorted(df['major1_mapped'].dropna().unique())
    major2_options = sorted(df['major2_mapped'].dropna().unique())
    job1_options = sorted(df['job1'].dropna().unique())
    job2_options = sorted(df['job2'].dropna().unique())
    job3_options = sorted(df['job3'].dropna().unique())
    min_inst = int(df['institution_count'].min())
    max_inst = int(df['institution_count'].max())


    if request.method == "POST":
        form_data = request.form.to_dict()
        resume_file = request.files.get('resume')

        # Store in session (optional; better for prototyping)
        session['form_data'] = form_data
        session['resume_filename'] = resume_file.filename if resume_file else None

        return redirect(url_for('recommendation.result'))
        

    return render_template("recommend.html",
                       degree_options=degree_options,
                       language_options=language_options,
                       major1_options=major1_options,
                       major2_options=major2_options,
                       job1_options=job1_options,
                       job2_options=job2_options,
                       job3_options=job3_options,
                       min_inst=min_inst,
                       max_inst=max_inst)

@recommendation_bp.route("/result", methods=["GET"])
def result():
    form_data = session.get('form_data', {})
    resume_filename = session.get('resume_filename', '')

    # 🧠 Here you can call your recommendation model using form_data and resume

    recommended_courses = [
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        {"code": "CS 188", "name": "Intro to AI", "score": 99},
        {"code": "IEOR 142", "name": "Supply Chain Analytics", "score": 98},
        # ... More mock or real data
    ]

    return render_template("result.html", recommendations=recommended_courses, user_data=form_data)
