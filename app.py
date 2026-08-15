
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS


# ==========================================
# LOAD DATASET
# ==========================================

merged_df = pd.read_csv("merged_internships_dataset.csv")


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)
CORS(app)


# ==========================================
# RECOMMENDATION FUNCTION
# ==========================================

def get_recommendations_from_user(
    skills,
    field,
    location,
    education
):

    df = merged_df.copy()

    skills = [
        str(x).strip().lower()
        for x in skills
        if str(x).strip()
    ]

    field = str(field).strip().lower()
    location = str(location).strip().lower()
    education = str(education).strip().lower()

    results = []

    for _, row in df.iterrows():

        score = 0

        internship_skills = str(
            row.get("Skills", "")
        ).lower()

        internship_profile = str(
            row.get("profile", "")
        ).lower()

        internship_location = str(
            row.get("Location", "")
        ).lower()

        internship_education = str(
            row.get("Education", "")
        ).lower()


        # Skills
        for skill in skills:

            if skill in internship_skills:
                score += 15


        # Field
        if field:

            for word in field.split():

                if len(word) > 2:

                    if (
                        word in internship_profile
                        or word in internship_skills
                    ):

                        score += 20
                        break


        # Location
        if location:

            if location in internship_location:
                score += 15


        # Education
        if education:

            if education in internship_education:
                score += 10


        item = row.to_dict()

        item["score"] = min(score, 100)

        results.append(item)


    result_df = pd.DataFrame(results)

    result_df = result_df.sort_values(
        by="score",
        ascending=False
    )

    return result_df.head(5)


# ==========================================
# WHY RECOMMENDED
# ==========================================

def get_recommendation_reasons(
    row,
    skills,
    interest,
    location,
    education
):

    reasons = []

    skills = [
        str(x).strip().lower()
        for x in skills
        if str(x).strip()
    ]

    interest = str(interest).lower().strip()
    location = str(location).lower().strip()
    education = str(education).lower().strip()

    internship_skills = str(
        row.get("Skills", "")
    ).lower()

    profile = str(
        row.get("profile", "")
    ).lower()

    internship_location = str(
        row.get("Location", "")
    ).lower()

    internship_education = str(
        row.get("Education", "")
    ).lower()


    # Skills
    for skill in skills:

        if skill in internship_skills:

            reasons.append(
                f"{skill.title()} matches your skills"
            )


    # Interest
    for word in interest.split():

        if len(word) > 2:

            if (
                word in profile
                or word in internship_skills
            ):

                reasons.append(
                    f"Matches your interest in {interest.title()}"
                )

                break


    # Location
    if location:

        if location in internship_location:

            reasons.append(
                "Matches your preferred location"
            )


    # Education
    if education:

        if education in internship_education:

            reasons.append(
                "Education requirement matches"
            )


    if len(reasons) == 0:

        reasons.append(
            "Recommended based on your overall profile"
        )


    return reasons


# ==========================================
# API ENDPOINT
# ==========================================

@app.route("/recommend", methods=["POST"])
def recommend():

    data = request.get_json()

    skills_text = data.get("skills", "")
    field = data.get("field", "")
    location = data.get("location", "")
    education = data.get("education", "")

    skills = [
        x.strip()
        for x in skills_text.split(",")
        if x.strip()
    ]

    recommendations = get_recommendations_from_user(
        skills,
        field,
        location,
        education
    )

    results = []

    for _, row in recommendations.iterrows():

        reasons = get_recommendation_reasons(
            row,
            skills,
            field,
            location,
            education
        )

        item = row.to_dict()

        item["reasons"] = reasons

        results.append(item)

    return jsonify(results)


# ==========================================
# LOCAL RUN
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )
