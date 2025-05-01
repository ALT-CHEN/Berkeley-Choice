from flask import Blueprint, render_template, request, session, redirect, url_for
from models.rse import extract_skills_from_resume
from models.skill_predictor import generate_course_recommendations
import pandas as pd
import os
import tensorflow_hub as hub
import tensorflow as tf

from flask_login import current_user
from models.user import UserFormData  # assuming your new model is defined there
from models import db

import numpy as np

def get_similarity(course, skills, embed):
    """
    course: str (course description)
    skills: list of str (skill set)
    embed: loaded USE model
    """
    course_emb = embed([course])[0].numpy()
    skills_emb = embed(skills).numpy()
    avg_skill_emb = np.mean(skills_emb, axis=0)
    similarity = np.dot(course_emb, avg_skill_emb) / (np.linalg.norm(course_emb) * np.linalg.norm(avg_skill_emb))
    return similarity

recommendation_bp = Blueprint("recommendation", __name__)

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# use4_path = os.path.join(BASE_DIR, 'models', 'use4')
# embed = hub.load(use4_path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
use4_path = os.path.join(BASE_DIR, 'models', 'use4')

if not os.path.exists(use4_path):
    print("USE4 model not found locally. Downloading from TensorFlow Hub...")
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    
    # Optional: Save it for future use
    tf.saved_model.save(embed, use4_path)
    print(f"Model saved to {use4_path}")
else:
    embed = hub.load(use4_path)


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

    form_data = {}

    if current_user.is_authenticated:
        saved_data = UserFormData.query.filter_by(user_id=current_user.id).first()
        if saved_data:
            form_data = saved_data.data

    if request.method == "POST":
        form_data = request.form.to_dict()
        resume_file = request.files.get('resume')

        if resume_file:
            upload_dir = os.path.join(BASE_DIR, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            resume_path = os.path.join(upload_dir, resume_file.filename)
            resume_file.save(resume_path)

        if current_user.is_authenticated:
            user_form = UserFormData.query.filter_by(user_id=current_user.id).first()
            if user_form:
                user_form.data = form_data
            else:
                user_form = UserFormData(user_id=current_user.id, data=form_data)
                db.session.add(user_form)
            db.session.commit()

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
                           max_inst=max_inst,
                           form_data=form_data)

@recommendation_bp.route("/recommend/result", methods=["GET"])
def result():
    form_data = session.get('form_data', {})
    resume_filename = session.get('resume_filename')

    extracted_skills = []
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # --- NEW: Generate course recommendations ---
    recommended_df = generate_course_recommendations(form_data, extracted_skills)

    recommended_courses = recommended_df.to_dict(orient="records")
    recommended_df['course_code'] = recommended_df['Course_Code'].astype(str).str.replace('\xa0', ' ').str.strip()

     # Path to the full course information
    csv_path = os.path.join(BASE_DIR, 'data', 'courses.csv')
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    desc_path = os.path.join(BASE_DIR, 'data', 'Course_Description.csv')
    desc_df = pd.read_csv(desc_path)
    desc_df.columns = desc_df.columns.str.strip().str.lower().str.replace(" ", "_")
    desc_df['course_code'] = desc_df['course_code'].astype(str).str.replace('\xa0', ' ').str.strip()


    # Parse course_units_parsed column safely
    import ast
    df["course_units_parsed"] = df["course_units_parsed"].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])

    # 🔗 Merge recommended course codes with full course info
    full_courses = recommended_df.merge(df, on="course_code", how="left")
    full_courses = full_courses.drop_duplicates(subset="Course_Code", keep="first")

    full_courses = full_courses.merge(desc_df[['course_code', 'description']], on="course_code", how="left")

    if resume_filename:
        # print('resume')
        resume_path = os.path.join(BASE_DIR, 'uploads', resume_filename)
        if os.path.exists(resume_path):
            code, extracted_skills = extract_skills_from_resume(resume_path)
            if code == 200:
                full_courses['skill_similarity'] = full_courses['description'].apply(
                    lambda desc: get_similarity(desc, extracted_skills, embed)
                )
                full_courses.drop(columns=['description'], inplace=True)
        else:
            extracted_skills = ["⚠️ Resume file not found."]


    # full_courses.to_csv('test.csv')

    # Convert to dictionary format for rendering in Jinja
    recommended_courses = full_courses.to_dict(orient="records")

    # Extract filter options
    major_options = sorted(full_courses["major"].dropna().unique())
    grading_options = sorted(full_courses["grading"].dropna().unique())
    course_levels = sorted(full_courses["course_level"].dropna().unique())
    summer_options = sorted(full_courses["summer_schedule"].dropna().unique())
    unit_options = sorted(set(unit for units in full_courses["course_units_parsed"] for unit in units))

    return render_template(
        "result.html",
        recommendations=recommended_courses,
        major_options=major_options,
        grading_options=grading_options,
        course_levels=course_levels,
        summer_options=summer_options,
        unit_options=unit_options
    )
