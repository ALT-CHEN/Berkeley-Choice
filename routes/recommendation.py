from flask import Blueprint, render_template, request
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
        # Extract user inputs
        field = request.form.get("field")
        career_goal = request.form.get("career_goal")
        learning_style = request.form.get("learning_style")
        resume = request.files["resume"]

        # Save resume file
        if resume.filename != "":
            pass
        

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