from flask import Blueprint, render_template, request, session, redirect, url_for
from models.rse import extract_skills_from_resume
from models.ml import generate_fake_recommendations
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

        if resume_file:
            upload_dir = os.path.join(BASE_DIR, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            resume_path = os.path.join(upload_dir, resume_file.filename)
            resume_file.save(resume_path)

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

@recommendation_bp.route("/recommend/result", methods=["GET"])
def result():
    form_data = session.get('form_data', {})
    resume_filename = session.get('resume_filename', '')

    extracted_skills = []

    if resume_filename:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        resume_path = os.path.join(BASE_DIR, 'uploads', resume_filename)

        # Check if file exists before calling the function
        if os.path.exists(resume_path):
            _, extracted_skills = extract_skills_from_resume(resume_path)
        else:
            extracted_skills = ["⚠️ Resume file not found."]

    recommended_courses = generate_fake_recommendations()
    

    return render_template(
        "result.html",
        recommendations=recommended_courses,
        user_data=form_data,
        extracted_skills=extracted_skills)
