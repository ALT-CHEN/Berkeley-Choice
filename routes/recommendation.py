from flask import Blueprint, render_template, request

recommendation_bp = Blueprint("recommendation", __name__)

@recommendation_bp.route("/recommend", methods=["GET", "POST"])
def recommend():
    if request.method == "POST":
        # Extract user inputs
        field = request.form.get("field")
        career_goal = request.form.get("career_goal")
        learning_style = request.form.get("learning_style")
        resume = request.files["resume"]

        # Save resume file
        if resume.filename != "":
            pass
        
        # Dummy processing: Extract skills (Replace this with real AI logic)
        predicted_skills = ["Python", "Machine Learning", "Data Analysis", "Deep Learning"]

        # Dummy recommended courses
        recommended_courses = [
            {"title": "Deep Learning Specialization", "description": "Advanced deep learning concepts.", "link": "#"},
            {"title": "Python for Data Science", "description": "Master Python and data analysis techniques.", "link": "#"},
            {"title": "AI in Business", "description": "Understand how AI is transforming industries.", "link": "#"}
        ]

        # Pass results to the frontend
        return render_template("recommend_results.html", 
                               field=field, career_goal=career_goal, learning_style=learning_style,
                               predicted_skills=predicted_skills, recommended_courses=recommended_courses)

    return render_template("recommend.html")  # Show the recommendation form