# models/skill_predictor.py
import pandas as pd
import pickle
from tensorflow.keras.models import load_model
from tensorflow import keras

# Load everything once
with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('models/reference_columns.pkl', 'rb') as f:
    reference_columns = pickle.load(f)

with open('models/skill_columns.pkl', 'rb') as f:
    skill_columns = pickle.load(f)

with open('models/fusion_logistic_model.pkl', 'rb') as f:
    fusion_model = pickle.load(f)

mlp_model = keras.models.load_model("models/best_mlp_model.keras")
similarity_df = pd.read_csv('data/new_skill_course_similarity.csv')

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

def generate_course_recommendations(form_data, extracted_skills):

    profile_data = pd.DataFrame([{
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

    # profile_data_test = pd.DataFrame([{
    #     'degree_names': 'Bachelor',
    #     'languages': 'Unknown',
    #     'major1_mapped': 'Unknown',
    #     'major2_mapped': 'Unknown',
    #     'job1': 'Unknown',
    #     'job2': 'Unknown',
    #     'job3': 'Unknown',
    #     'matched_score': 1.0,
    #     'institution_count': -1,
    #     'max_passing_year': -1,
    #     'gpa': -1.0,
    #     'min_experience_requirement': -1,
    #     'min_age_requirement': -1,
    #     'extra_curricular': 0,
    #     'certification': 0,
    # }])

    # test = pd.DataFrame([{'result': profile_data.equals(profile_data_test)}])

    # test.to_csv('test.csv')

    # Step 2: Predict skills
    profile_data.fillna("Unknown", inplace=True)
    encoded = pd.get_dummies(profile_data, columns=[
        'degree_names', 'languages', 'major1_mapped',
        'major2_mapped', 'job1', 'job2', 'job3'
    ])
    for col in reference_columns:
        if col not in encoded.columns:
            encoded[col] = 0
    encoded = encoded[reference_columns]
    encoded[['matched_score', 'institution_count', 'max_passing_year',
             'gpa', 'min_experience_requirement', 'min_age_requirement']] = scaler.transform(
        encoded[['matched_score', 'institution_count', 'max_passing_year',
                 'gpa', 'min_experience_requirement', 'min_age_requirement']]
    )
    predicted_probs = mlp_model.predict(encoded)
    df_predictions = pd.DataFrame(predicted_probs, columns=skill_columns)
    top_targets = df_predictions.iloc[0].nlargest(20)

    top20_long = pd.DataFrame({
        'skill_rank': range(1, 21),
        'target': top_targets.index,
        'probability': top_targets.values
    })

    # Step 3: Join with course similarity and rerank
    merged = top20_long.merge(similarity_df, left_on='target', right_on='Cluster', how='left')
    merged['score_linear'] = merged['probability'] + merged['Cosine_Similarity']
    merged['predicted_score'] = fusion_model.predict_proba(
        merged[['probability', 'Cosine_Similarity', 'skill_rank']]
    )[:, 1]
    # Sort by predicted_score first so we keep the best version of each course
    merged_sorted = merged.sort_values(by='predicted_score', ascending=False)

    # Drop duplicates based on Course_Code
    unique_courses = merged_sorted.drop_duplicates(subset='Course_Code', keep='first')

    # Now get the top 50
    top = unique_courses.head(50).copy()

    # Select and reorder columns
    top = top[[
        'Course_Code', 'Course_Title', 'Cluster', 'skill_rank',
        'probability', 'Cosine_Similarity', 'predicted_score'
    ]]

    return top
