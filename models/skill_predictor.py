# models/skill_predictor.py
import pandas as pd
import pickle
from tensorflow.keras.models import load_model

# Load everything once
with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('models/reference_columns.pkl', 'rb') as f:
    reference_columns = pickle.load(f)

with open('models/skill_columns.pkl', 'rb') as f:
    skill_columns = pickle.load(f)

with open('models/fusion_logistic_model.pkl', 'rb') as f:
    fusion_model = pickle.load(f)

mlp_model = load_model('models/best_mlp_model.h5')
similarity_df = pd.read_csv('data/new_skill_course_similarity.csv')

def generate_course_recommendations(form_data, extracted_skills):
    # Step 1: Create raw profile DataFrame
    profile_data = pd.DataFrame([{
        'degree_names': form_data.get('degree_names', 'Unknown'),
        'languages': form_data.get('language', 'Unknown'),
        'major1_mapped': form_data.get('major1_mapped', 'Unknown'),
        'major2_mapped': form_data.get('major2_mapped', 'Unknown'),
        'job1': form_data.get('job1', 'Unknown'),
        'job2': form_data.get('job2', 'Unknown'),
        'job3': form_data.get('job3', 'Unknown'),
        'matched_score': float(form_data.get('matched_score', -1)),
        'institution_count': int(form_data.get('institution_count', -1)),
        'max_passing_year': int(form_data.get('max_passing_year', -1)),
        'gpa': float(form_data.get('gpa', -1)),
        'min_experience_requirement': int(form_data.get('experience', -1)),
        'min_age_requirement': int(form_data.get('age', -1)),
        'extra_curricular': int(form_data.get('extra_curricular', 0)),
        'certification': int(form_data.get('certification', 0)),
    }])

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
