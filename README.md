# SkillCompass AI

**ML-Based Career Guidance and Skill Gap Analysis**

## Problem Statement
Students often struggle to identify the skills required for careers such as Data Analyst, Data Scientist, and Business Analyst. SkillCompass AI helps students understand skill gaps and find relevant learning resources.

## Features
1. Student Profile
2. Skill Assessment
3. Career Matching
4. Skill Gap Dashboard
5. Learning Roadmap
6. NLP Job Description Analyzer

## Technologies Used
- Python
- Streamlit
- pandas
- scikit-learn
- Plotly
- CSV datasets

## Project Structure
- `app.py` — Main web application
- `data/career_skills.csv` — Sample career skill requirements
- `data/courses.csv` — Learning resources and project ideas
- `src/career_match.py` — Career alignment scoring
- `src/recommendations.py` — Skill gaps, course recommendations, and NLP similarity

## How to Run

Install the required libraries:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

Open the local URL shown in the terminal.

## How It Works
The application compares student skill levels against sample career requirements, identifies skill gaps, and recommends learning resources. Its NLP component uses TF-IDF and cosine similarity to compare job descriptions with skill descriptions.

## Limitations
The career requirements and weights are illustrative. The current application uses a rule-based career matching algorithm and an NLP similarity technique; it does not yet contain a validated, supervised career-prediction model.

## Team Members
- E. Tanusha — 325103282044
- G. Nikhitha — 325103282045

**Project:** ML Ideathon, 14 October 2026