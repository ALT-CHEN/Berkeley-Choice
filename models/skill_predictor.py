# models/skill_predictor.py
import pandas as pd
import pickle
from tensorflow.keras.models import load_model

# Helper functions
def safe_int(val, default=-1):
    try:
        return int(val)
    except (ValueError, TypeError):
        return default

def safe_float(val, default=-1.0):
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def safe_str(val, default='Unknown'):
    if val == '':
        return default
    else:
        return val

def generate_course_recommendations(form_data, extracted_skills, n=20):

    raw_profile_df = pd.DataFrame([{
        'degree_names': safe_str(form_data.get('degree_names', 'Unknown')),
        'languages': safe_str(form_data.get('language', 'Unknown')),
        'major1_mapped': safe_str(form_data.get('major1_mapped', 'Unknown')),
        'major2_mapped': safe_str(form_data.get('major2_mapped', 'Unknown')),
        'job1': safe_str(form_data.get('job1', 'Unknown')),
        'job2': safe_str(form_data.get('job2', 'Unknown')),
        'job3': safe_str(form_data.get('job3', 'Unknown')),
        'matched_score': safe_float(form_data.get('correlation', -1)),
        'institution_count': safe_int(form_data.get('institution_count', -1)),
        'max_passing_year': safe_int(form_data.get('max_passing_year', -1)),
        'gpa': safe_float(form_data.get('gpa', -1)),
        'min_experience_requirement': safe_int(form_data.get('experience', -1)),
        'min_age_requirement': safe_int(form_data.get('age', -1)),
        'extra_curricular': safe_int(form_data.get('extra_curricular', 0), 0),
        'certification': safe_int(form_data.get('certification', 0), 0),
    }])


    # 1. Fill missing values
    categorical_cols = ['degree_names', 'languages', 'major1_mapped', 'major2_mapped', 'job1', 'job2', 'job3']
    numerical_cols = ['matched_score', 'institution_count', 'max_passing_year',
                      'gpa', 'min_experience_requirement', 'min_age_requirement']

    raw_profile_df[categorical_cols] = raw_profile_df[categorical_cols].fillna("Unknown")
    raw_profile_df[numerical_cols] = raw_profile_df[numerical_cols].fillna(-1)

    # 2. One-hot encode
    encoded_profile = pd.get_dummies(raw_profile_df, columns=categorical_cols)

    # 3. Align columns with training set
    # Load the saved reference column list
    with open('models/reference_columns.pkl', 'rb') as f:
        reference_columns = pickle.load(f)
    encoded_profile = encoded_profile.reindex(columns=reference_columns, fill_value=0)

    # 4. Standardize numeric features
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    encoded_profile[numerical_cols] = scaler.transform(encoded_profile[numerical_cols])

    # --- Load model and make prediction ---
    mlp_model = load_model("models/best_mlp_model.h5")
    predictions = mlp_model.predict(encoded_profile)

    ############################################
    # Load skill column names
    with open('models/skill_columns.pkl', 'rb') as f:
        skill_columns = pickle.load(f)

    # Convert prediction array to DataFrame (assuming `pred` is shape (1, n))
    df_predictions = pd.DataFrame(predictions, columns=skill_columns)

    # Extract top 20 predictions for the single sample
    top_targets = df_predictions.iloc[0].nlargest(20)

    # Long format output
    top20_long = pd.DataFrame({
        'skill_rank': range(1, 21),
        'target': top_targets.index,
        'probability': top_targets.values
    })

    skill_course_similarity = pd.read_csv("data/new_skill_course_similarity.csv")
    merged = top20_long.merge(skill_course_similarity, left_on="target", right_on="Cluster", how="left")
    merged["score_linear"] = merged["probability"] + merged["Cosine_Similarity"]

    with open("models/fusion_logistic_model.pkl", "rb") as f:
        model = pickle.load(f)
    # Predict the score (probability of label = 1) for each course using the trained model
    merged["predicted_score"] = model.predict_proba(
        merged[["probability", "Cosine_Similarity", "skill_rank"]]
    )[:, 1]


    # Clean and normalize Course_Code
    merged["Course_Code"] = merged["Course_Code"].astype(str).str.strip().str.replace('\xa0', ' ', regex=False)

    # Format, sort, and remove duplicates
    top_recommendations = (
        merged[[
            "Course_Code", "Course_Title", "Cluster", "skill_rank",
            "probability", "Cosine_Similarity", "predicted_score"
        ]]
        .sort_values(by="predicted_score", ascending=False)
        .drop_duplicates(subset="Course_Code", keep="first")
    )

    test_df = top_recommendations.head(n)
    test_df.to_csv('test1.csv')

    return top_recommendations.head(n)
