import pandas as pd
import random
import os

def generate_fake_recommendations(n=20):
    # Path to your CSV
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(BASE_DIR, 'data', 'courses.csv')

    # Load course data
    df = pd.read_csv(csv_path)

    # Sample n courses randomly
    sampled = df.sample(n=n, random_state=random.randint(0, 9999)).copy()

    # Assign random match scores between 0 and 1
    sampled["match_score"] = [round(random.uniform(0, 1), 4) for _ in range(n)]

    # Return selected columns
    return sampled[["Course Code", "Course Title", "match_score"]] if "Course Code" in sampled.columns else sampled
