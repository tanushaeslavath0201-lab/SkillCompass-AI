from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_skill_gaps(student_skills, career_data, career):

    rows = career_data[
        career_data["career"] == career
    ]

    gaps = []

    for _, row in rows.iterrows():

        skill = row["skill"]
        required = row["required_level"]
        student = student_skills.get(skill, 0)

        if student < required:
            gaps.append({
                "Skill": skill,
                "Current Level": student,
                "Required Level": required,
                "Gap": required - student
            })

    return sorted(
        gaps,
        key=lambda x: x["Gap"],
        reverse=True
    )


def recommend_courses(gaps, course_data):

    recommendations = []

    for gap in gaps:

        skill = gap["Skill"]

        rows = course_data[
            course_data["skill"] == skill
        ]

        for _, row in rows.iterrows():

            recommendations.append({
                "Skill": skill,
                "Course": row["course"],
                "Project": row["practice_project"],
                "Link": row["url"]
            })

    return recommendations


def match_job_description(job_text, career_data):

    skills = career_data["skill"].unique().tolist()

    descriptions = {
        "Python": "Python programming data analysis",
        "SQL": "SQL database queries",
        "Excel": "Excel spreadsheets formulas reports",
        "Statistics": "statistics probability averages",
        "Power BI": "Power BI dashboards data visualization",
        "Machine Learning": "machine learning classification models",
        "Mathematics": "mathematics algebra calculus",
        "Communication": "communication presentations",
        "Problem Solving": "problem solving logical thinking"
    }

    skill_texts = [
        descriptions.get(skill, skill)
        for skill in skills
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        [job_text] + skill_texts
    )

    scores = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )[0]

    results = []

    for skill, score in zip(skills, scores):

        results.append({
            "Skill": skill,
            "Similarity": round(float(score) * 100, 2)
        })

    return sorted(
        results,
        key=lambda x: x["Similarity"],
        reverse=True
    )