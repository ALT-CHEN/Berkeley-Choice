# 🎓 Course Recommendation System

A **Flask-based web application** that recommends courses tailored to user profiles using **Neural Networks**, **Natural Language Processing (NLP)**, and **Clustering**. This project provides personalized course suggestions by extracting relevant skills and matching them with course descriptions through semantic similarity.

<p align="center">
  <img src="https://img.shields.io/badge/Framework-Flask-blue?logo=flask" />
  <img src="https://img.shields.io/badge/Language-Python-yellow?logo=python" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" />
  <img src="https://img.shields.io/github/last-commit/ALT-CHEN/Berkeley-Choice" />
</p>

---

## ✨ Features

- 🧠 **Skill Prediction** — Predict skills from user inputs using trained ML models.
- 📚 **NLP Matching** — Match predicted skills with courses using Sentence-BERT and similarity scores.
- 🧩 **Modular Architecture** — Flask Blueprints enable easy scaling and maintenance.
- 💾 **Form Memory** — Last submission is remembered for logged-in users.
- 🧑‍💻 **User-Friendly Interface** — Clean and modern frontend for ease of use.

---

## 🌐 Pages Overview

| Page            | Description                                                         |
|-----------------|---------------------------------------------------------------------|
| 🏠 **Home**       | Introduction to the project and team                               |
| 📈 **About**      | Interactive data dashboard for resume and course datasets          |
| 🎯 **Recommend**  | Multi-step form to predict skills and display course suggestions   |
| 📞 **Contact**    | Contact form and team contact info                                 |

---

## 📁 Project Structure
```
/course_recommendation/
│── app.py                                   # Main Flask application
│── config.py                                # Configuration settings (auto-generates secret key)
│── requirements.txt                         # Dependencies
│── README.md                                # Project documentation
│── /data/
│   │── output.csv
│   │── courses.csv
│   │── New_Cluster_Record.csv
│   │── new_skill_course_similarity.csv
│   │── ...
│── /models/                                 # Machine Learning Models
│   │── __init__.py
│   │── skill_predictor.py                   
│   │── rse.py
│   │── user.py
│   │── ...
│── /templates/          
│   │── base.html
│   │── home.html
│   │── about.html
│   │── recommend.html
│   │── result.html
│   │── contact.html
│── /routes/             # Route definitions
│   │── __init__.py
│   │── home.py          # Home page routes
│   │── about.py         # About page routes
│   │── recommendation.py # Recommendation page routes
│   │── ...
│── ...
```

---

## 🔧 Installation and Setup
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/<username>/Berkeley-Choice.git
cd Berkeley-Choice
```

### 2️⃣ Set Up a Virtual Environment
```sh
python -m venv env
```
- **Activate on macOS/Linux**:
  ```sh
  source env/bin/activate
  ```
- **Activate on Windows**:
  ```sh
  env\Scripts\activate
  ```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).

---

🚀 **Now you're all set! Start coding and contributing to the Course Recommendation System!** 😊
