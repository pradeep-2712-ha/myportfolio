import sqlite3
from pathlib import Path

from app.core.config import settings
from app.core.database import init_db


def _db_path() -> Path:
    prefix = "sqlite:///"
    return Path(settings.database_url.replace(prefix, "", 1))


def seed() -> None:
    init_db()
    path = _db_path()
    conn = sqlite3.connect(path)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM skills")
        cursor.execute("DELETE FROM projects")
        cursor.execute("DELETE FROM experience")
        cursor.execute("DELETE FROM education")
        cursor.execute("DELETE FROM certifications")
        cursor.execute("DELETE FROM portfolio")

        cursor.execute(
            """
            INSERT INTO portfolio (
                name, title, tagline, about, contact_email, location, phone, linkedin_url, github_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "Pradeep Sai Domala",
                "B.Tech CSE (AI & ML) Student | Aspiring Full-Stack & AI Engineer",
                "Building practical AI and web applications with Python, React, Node.js, and machine learning.",
                (
                    "Computer Science student specializing in Artificial Intelligence and Machine Learning. "
                    "Hands-on experience in Python development, deep learning projects, and full-stack web basics. "
                    "Focused on shipping clean, practical software and continuously improving problem-solving skills."
                ),
                "pradeepnani2703@gmail.com",
                "Kompally, Hyderabad, 500055",
                "+91 8712299253",
                "https://www.linkedin.com",
                "https://github.com"
            )
        )
        portfolio_id = int(cursor.lastrowid)

        skills = [
            ("C", "Intermediate", "Languages", portfolio_id),
            ("Java", "Intermediate", "Languages", portfolio_id),
            ("Python", "Intermediate", "Languages", portfolio_id),
            ("JavaScript", "Intermediate", "Languages", portfolio_id),
            ("OOP", "Intermediate", "Core Concepts", portfolio_id),
            ("Data Structures", "Intermediate", "Core Concepts", portfolio_id),
            ("Aptitude", "Intermediate", "Core Concepts", portfolio_id),
            ("ReactJS", "Intermediate", "Frameworks", portfolio_id),
            ("Node.js", "Intermediate", "Frameworks", portfolio_id),
            ("Machine Learning (Basics)", "Beginner", "AI/Data", portfolio_id),
            ("NumPy", "Beginner", "AI/Data", portfolio_id),
            ("Pandas", "Beginner", "AI/Data", portfolio_id),
            ("Data Analysis", "Beginner", "AI/Data", portfolio_id)
        ]
        cursor.executemany(
            "INSERT INTO skills (name, level, category, portfolio_id) VALUES (?, ?, ?, ?)",
            skills
        )

        projects = [
            (
                "Enhanced Weapon Detection using Deep Learning",
                (
                    "Built an end-to-end weapon detection and classification pipeline for real-time "
                    "image/video surveillance. Trained Faster R-CNN on a custom annotated dataset "
                    "(1,057 images) and achieved around 73% detection accuracy. Built a VGG-based "
                    "CNN for 7-class weapon classification using 5,214 images with up to 98.4% accuracy."
                ),
                "Python,Deep Learning,CNN,Faster R-CNN,OpenCV",
                "https://github.com/example/enhanced-weapon-detection",
                portfolio_id
            ),
            (
                "Brain Tumour Disease Detection using ML and DL",
                (
                    "Developed a brain tumor detection workflow using MRI preprocessing, tumor region "
                    "segmentation, feature extraction, and deep learning classification. "
                    "Designed the pipeline for practical diagnostic support scenarios."
                ),
                "Python,Machine Learning,Deep Learning,CNN,Data Analysis",
                "https://github.com/example/brain-tumour-detection",
                portfolio_id
            )
        ]
        cursor.executemany(
            "INSERT INTO projects (title, summary, stack_csv, link, portfolio_id) VALUES (?, ?, ?, ?, ?)",
            projects
        )

        experiences = [
            (
                "Python Intern",
                "Triad Techno Services",
                "07/2024",
                (
                    "Developed a weather forecasting system using Python and Auto Regressive (AR) time-series models||"
                    "Applied data preprocessing, feature extraction, and model evaluation to build predictive pipelines||"
                    "Gained hands-on experience in collaborative development and real-world software practices"
                ),
                portfolio_id
            )
        ]
        cursor.executemany(
            "INSERT INTO experience (role, company, period, highlights_csv, portfolio_id) VALUES (?, ?, ?, ?, ?)",
            experiences
        )

        education = [
            (
                "Bachelor of Technology - Computer Science and Engineering (AI & ML)",
                "CMR Institute of Technology",
                "2022 - 2026 (GPA: 8.5)",
                portfolio_id
            ),
            (
                "Intermediate (Mathematics, Physics, Chemistry)",
                "Sri Chaitanya Junior College, Ammenpur",
                "2020 - 2022 (Percentage: 97%)",
                portfolio_id
            ),
            (
                "Secondary Education",
                "Nalanda High School",
                "2020 (GPA: 10.0)",
                portfolio_id
            )
        ]
        cursor.executemany(
            "INSERT INTO education (degree, institution, year, portfolio_id) VALUES (?, ?, ?, ?)",
            education
        )

        certifications = [
            ("Python Programming", "Infosys Springboard - Basics of Python", "", portfolio_id),
            ("HTML5, CSS, JavaScript, React.js", "Infosys Springboard - Basics of Front End", "", portfolio_id),
            (
                "Introduction to Artificial Intelligence and Deep Learning",
                "Infosys Springboard - Algorithms in AIML",
                "",
                portfolio_id
            )
        ]
        cursor.executemany(
            "INSERT INTO certifications (name, issuer, year, portfolio_id) VALUES (?, ?, ?, ?)",
            certifications
        )

        conn.commit()
        print("Seed completed successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    seed()
