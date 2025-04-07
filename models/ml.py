import pandas as pd
import random
import os

def generate_fake_recommendations(n=20):
    # Path to your CSV
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(BASE_DIR, 'data', 'courses.csv')

    # Load course data
    df = pd.read_csv(csv_path)

    print("Columns in courses.csv:", df.columns.tolist())

    # Sample n courses randomly (handle case where df has fewer rows)
    if df.shape[0] < n:
        n = df.shape[0]

    sampled = df.sample(n=n, random_state=random.randint(0, 9999)).copy()

    sampled.rename(
        columns={
            "Course Code": "code",
            "Course Title": "title",
            "Course URL": "url"
        }, 
        inplace=True
    )

    # Assign random match scores between 0 and 1
    sampled["match_score"] = [round(random.uniform(0, 1), 4) for _ in range(n)]

    # Keep only selected columns (if they exist)
    expected_cols = ["code", "title", "match_score", "url"]
    available_cols = [col for col in expected_cols if col in sampled.columns]

    # Convert to list of dicts
    return sampled[available_cols].to_dict(orient="records")
