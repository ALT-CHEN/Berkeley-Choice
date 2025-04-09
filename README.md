# 📚 Course Recommendation System

A Flask-based web application that recommends courses based on user skills. This project features an interactive dashboard for data visualization, a recommendation engine (to be implemented), and a database to store course information and embeddings for similarity matching.

---

## 🚀 Features
- 📌 **Home Page**: Introduction to the project and team members.
- 📊 **About Page**: Interactive dashboard for visualizing course and resume datasets.
- 🎯 **Recommendation Page**: A form where users enter details, and the system predicts required skills and recommends courses.
- 🗄 **Database**: Stores course information and course description embeddings for similarity matching.
- 🏗 **Modular Flask Architecture** using Blueprints for scalability.

---

## 📂 Project Structure (keep growing...)
```
/course_recommendation/
│── app.py               # Main Flask application
│── config.py            # Configuration settings (auto-generates secret key)
│── requirements.txt     # Dependencies
│── README.md            # Project documentation
│── /data/
│   │── output.csv
│   │── courses.csv
│── /models/             # Machine Learning Models
│   │── __init__.py
│   │── ml.py            # recommendation models
│   │── rse.py           # resume skills extractor
│── /templates/          # HTML 
│   │── base.html
│   │── home.html
│   │── about.html
│   │── recommend.html
│   │── result.html
│── /routes/             # Route definitions
│   │── __init__.py
│   │── home.py          # Home page routes
│   │── about.py         # About page routes
│   │── recommendation.py # Recommendation page routes
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
