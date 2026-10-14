def calculate_match(student_skills, career_data):

    results = []

    careers = career_data["career"].unique()

    for career in careers:

        rows = career_data[
            career_data["career"] == career
        ]

        total_points = 0
        total_weight = 0

        for _, row in rows.iterrows():

            skill = row["skill"]
            required = row["required_level"]
            weight = row["weight"]

            student = student_skills.get(skill, 0)

            score = min(student / required, 1)

            total_points += score * weight
            total_weight += weight

        match_percentage = (
            total_points / total_weight
        ) * 100

        results.append({
            "Career": career,
            "Match": round(match_percentage, 2)
        })

    results = sorted(
        results,
        key=lambda x: x["Match"],
        reverse=True
    )

    return results