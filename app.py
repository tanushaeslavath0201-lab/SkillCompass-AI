import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from src.career_match import calculate_match
from src.recomendations import (
    find_skill_gaps,
    recommend_courses,
    match_job_description
)

# =====================================
# PAGE SETUP
# =====================================

BASE_FOLDER = Path(__file__).parent

st.set_page_config(
    page_title="SkillCompass AI",
    page_icon="🧭",
    layout="wide"
)

# Load datasets
career_data = pd.read_csv(
    BASE_FOLDER / "data" / "career_skills.csv"
)

course_data = pd.read_csv(
    BASE_FOLDER / "data" / "courses.csv"
)

# Store the current page
if "page" not in st.session_state:
    st.session_state.page = 1

if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {}

# =====================================
# COMMON HEADER AND NAVIGATION
# =====================================

def show_header():
    st.title("🧭 SkillCompass AI")
    st.caption(
        "Your personal AI-powered career guidance assistant"
    )

    st.progress(st.session_state.page / 6)

    st.write(
        f"**Step {st.session_state.page} of 6**"
    )

    st.divider()


def navigation():
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.page > 1:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.page -= 1
                st.rerun()

    with col2:
        if st.session_state.page < 6:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.page += 1
                st.rerun()


show_header()

# =====================================
# PAGE 1: STUDENT PROFILE
# =====================================

if st.session_state.page == 1:

    st.header("👩‍🎓 1. Student Profile")

    st.write(
        "Let's get to know you before we find your career path."
    )

    name = st.text_input(
        "Enter your name",
        key="student_name"
    )

    interests = st.multiselect(
        "What are your interests?",
        [
            "Data Analysis",
            "Machine Learning",
            "Business",
            "Programming",
            "Data Visualization"
        ],
        key="student_interests"
    )

    career = st.selectbox(
        "Which career do you want to explore?",
        [
            "Data Analyst",
            "Data Scientist",
            "Business Analyst"
        ],
        key="target_career"
    )

    st.info(
        "In the next step, you will answer a short skill assessment."
    )

    navigation()


# =====================================
# PAGE 2: SKILL ASSESSMENT
# =====================================

elif st.session_state.page == 2:

    st.header("📝 2. Skill Assessment")

    st.write(
        "Answer these five beginner-level questions "
        "to check your basic knowledge."
    )

    questions = [
        {
            "skill": "Python",
            "question": "Which Python function displays output?",
            "options": [
                "input()", "print()", "len()", "type()"
            ],
            "answer": "print()"
        },
        {
            "skill": "SQL",
            "question": "Which SQL command retrieves data?",
            "options": [
                "SELECT", "DELETE", "DROP", "UPDATE"
            ],
            "answer": "SELECT"
        },
        {
            "skill": "Statistics",
            "question": "What is the mean of 2, 4, 6?",
            "options": ["2", "3", "4", "6"],
            "answer": "4"
        },
        {
            "skill": "Excel",
            "question": "Which Excel function calculates an average?",
            "options": [
                "SUM()", "AVERAGE()", "COUNTIF()", "MAX()"
            ],
            "answer": "AVERAGE()"
        },
        {
            "skill": "Machine Learning",
            "question": "Which task predicts a category?",
            "options": [
                "Classification",
                "Formatting",
                "Sorting",
                "Printing"
            ],
            "answer": "Classification"
        }
    ]

    with st.form("assessment_form"):

        answers = {}

        for i, q in enumerate(questions):

            answers[q["skill"]] = st.radio(
                f"Q{i + 1}. {q['question']}",
                q["options"],
                key=f"answer_{q['skill']}"
            )

        submitted = st.form_submit_button(
            "✅ Submit Assessment"
        )

    if submitted:

        scores = {}
        correct = 0

        for q in questions:

            skill = q["skill"]

            if answers[skill] == q["answer"]:
                scores[skill] = 100
                correct += 1
            else:
                scores[skill] = 30

        st.session_state.quiz_scores = scores
        st.session_state.quiz_submitted = True

        st.success(
            f"You answered {correct} out of "
            f"{len(questions)} questions correctly!"
        )

    if st.session_state.get("quiz_submitted", False):

        st.write("### Your assessment results")

        result_rows = [
            {"Skill": skill, "Score": score}
            for skill, score
            in st.session_state.quiz_scores.items()
        ]

        st.dataframe(
            pd.DataFrame(result_rows),
            use_container_width=True,
            hide_index=True
        )

    st.info(
        "Click Next when you are ready to explore your career matches."
    )

    navigation()


# =====================================
# PAGE 3: CAREER MATCHING
# =====================================

elif st.session_state.page == 3:

    st.header("🎯 3. Career Matching")

    st.write(
        "Rate your current skills from 0 to 100. "
        "Your quiz results are used as starting values "
        "for the skills assessed in Step 2."
    )

    skills = sorted(
        career_data["skill"].unique().tolist()
    )

    student_skills = {}

    quiz_scores = st.session_state.quiz_scores

    for skill in skills:

        default_score = int(
            quiz_scores.get(skill, 30)
        )

        student_skills[skill] = st.slider(
            skill,
            min_value=0,
            max_value=100,
            value=default_score,
            step=5,
            key=f"skill_level_{skill}"
        )

    # Save the current scores for use on later pages
    st.session_state.student_skills = student_skills

    st.divider()

    matches = calculate_match(
        student_skills,
        career_data
    )

    match_table = pd.DataFrame(matches)

    st.subheader("Your career matches")

    st.dataframe(
        match_table,
        use_container_width=True,
        hide_index=True
    )

    best = matches[0]

    st.success(
        f"Your highest skill alignment is "
        f"{best['Career']} ({best['Match']}%)."
    )

    chart = px.bar(
        match_table,
        x="Career",
        y="Match",
        color="Career",
        title="Career Skill Alignment",
        range_y=[0, 100]
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )

    st.caption(
        "These scores compare your entered skills with sample "
        "career requirements. They do not predict hiring success."
    )

    navigation()


# =====================================
# PAGE 4: SKILL GAP DASHBOARD
# =====================================

elif st.session_state.page == 4:

    st.header("📊 4. Skill Gap Dashboard")

    st.write(
        "Discover which skills you should improve "
        "for your selected career."
    )

    career = st.session_state.get(
        "target_career",
        "Data Analyst"
    )

    student_skills = st.session_state.get(
        "student_skills",
        {}
    )

    if not student_skills:

        st.warning(
            "Please complete Step 3 before viewing your skill gaps."
        )

    else:

        gaps = find_skill_gaps(
            student_skills,
            career_data,
            career
        )

        if gaps:

            gap_table = pd.DataFrame(gaps)

            st.subheader(
                f"Skills to improve for {career}"
            )

            st.dataframe(
                gap_table,
                use_container_width=True,
                hide_index=True
            )

            chart = px.bar(
                gap_table,
                x="Skill",
                y="Gap",
                color="Gap",
                title="Your Skill Gaps"
            )

            st.plotly_chart(
                chart,
                use_container_width=True
            )

            strongest_skill = max(
                student_skills,
                key=student_skills.get
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Strongest entered skill",
                strongest_skill
            )

            col2.metric(
                "Skills below target",
                len(gaps)
            )

        else:

            st.success(
                "You meet all the sample target levels "
                "for your selected career!"
            )

    navigation()


# =====================================
# PAGE 5: LEARNING ROADMAP
# =====================================

elif st.session_state.page == 5:

    st.header("🗺️ 5. Your Learning Roadmap")

    career = st.session_state.get(
        "target_career",
        "Data Analyst"
    )

    student_skills = st.session_state.get(
        "student_skills",
        {}
    )

    if not student_skills:

        st.warning(
            "Complete Step 3 first to generate your roadmap."
        )

    else:

        gaps = find_skill_gaps(
            student_skills,
            career_data,
            career
        )

        courses = recommend_courses(
            gaps,
            course_data
        )

        st.write(
            f"Here is your suggested learning plan for **{career}**."
        )

        if courses:

            for i, course in enumerate(courses, start=1):

                with st.expander(
                    f"Step {i}: Improve {course['Skill']}",
                    expanded=(i == 1)
                ):

                    st.write(
                        f"**Recommended course:** {course['Course']}"
                    )

                    st.write(
                        f"**Practice project:** {course['Project']}"
                    )

                    st.markdown(
                        f"[Open learning resource]({course['Link']})"
                    )

        else:

            st.success(
                "No skill gaps were identified. "
                "Try an advanced assessment or build a portfolio project."
            )

    navigation()


# =====================================
# PAGE 6: JOB DESCRIPTION ANALYZER
# =====================================

elif st.session_state.page == 6:

    st.header("🤖 6. AI Job Description Analyzer")

    st.write(
        "Paste a job description to discover which skills "
        "are most related to its text."
    )

    job_text = st.text_area(
        "Paste a job description here",
        height=220,
        key="job_description"
    )

    if st.button("🔍 Analyze Job Description"):

        if len(job_text.strip()) < 15:

            st.warning(
                "Please enter a longer job description."
            )

        else:

            results = match_job_description(
                job_text,
                career_data
            )

            result_df = pd.DataFrame(results)

            st.subheader("Related skills")

            st.dataframe(
                result_df.head(8),
                use_container_width=True,
                hide_index=True
            )

            chart = px.bar(
                result_df.head(8),
                x="Skill",
                y="Similarity",
                title="Job Description Skill Similarity"
            )

            st.plotly_chart(
                chart,
                use_container_width=True
            )

            st.caption(
                "This NLP feature measures text similarity. "
                "It does not verify eligibility or predict hiring outcomes."
            )

    st.success(
        "🎉 You have reached the end of SkillCompass AI!"
    )

    if st.button("🔄 Start Again"):

        st.session_state.page = 1
        st.session_state.quiz_scores = {}

        if "quiz_submitted" in st.session_state:
            del st.session_state["quiz_submitted"]

        st.rerun()

    navigation()