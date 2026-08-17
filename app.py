import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS


# ==========================================
# LOAD DATASET
# ==========================================

merged_df = pd.read_csv("merged_internships_dataset.csv")

print("==========================================")
print("DATASET LOADED")
print("Rows:", len(merged_df))
print("Columns:", list(merged_df.columns))
print("==========================================")


# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)
CORS(app)


# ==========================================
# HELPER FUNCTION
# ==========================================

def safe_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


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

    field = safe_text(field)
    location = safe_text(location)
    education = safe_text(education)


    # ==========================================
    # CREATE SEARCH TEXT
    # ==========================================

    def get_row_text(row, possible_columns):

        values = []

        for column in possible_columns:

            if column in row.index:

                value = row[column]

                if not pd.isna(value):

                    values.append(
                        str(value).lower()
                    )

        return " ".join(values)


    # ==========================================
    # HARD FILTER LOCATION
    # ==========================================

    if location:

        location_mask = df.apply(
            lambda row:
            location in get_row_text(
                row,
                [
                    "Location",
                    "location"
                ]
            ),
            axis=1
        )

        filtered_df = df[location_mask].copy()

    else:

        filtered_df = df.copy()


    # ==========================================
    # HARD FILTER FIELD
    # ==========================================

    if field:

        field_mask = filtered_df.apply(
            lambda row:
            any(
                word in get_row_text(
                    row,
                    [
                        "field",
                        "Field",
                        "profile",
                        "title",
                        "Skills",
                        "skills"
                    ]
                )
                for word in field.split()
                if len(word) > 2
            ),
            axis=1
        )

        field_filtered_df = filtered_df[field_mask].copy()

        # Agar field filter se kuch nahi mila,
        # location wale results ko completely remove
        # nahi karenge.
        if len(field_filtered_df) > 0:

            filtered_df = field_filtered_df


    # ==========================================
    # IF FILTERS RETURN NOTHING
    # ==========================================

    if len(filtered_df) == 0:

        return pd.DataFrame()


    # ==========================================
    # CALCULATE SCORE
    # ==========================================

    results = []


    for _, row in filtered_df.iterrows():

        score = 0


        internship_skills = get_row_text(
            row,
            [
                "Skills",
                "skills"
            ]
        )


        internship_profile = get_row_text(
            row,
            [
                "profile",
                "title"
            ]
        )


        internship_location = get_row_text(
            row,
            [
                "Location",
                "location"
            ]
        )


        internship_field = get_row_text(
            row,
            [
                "field",
                "Field"
            ]
        )


        internship_education = get_row_text(
            row,
            [
                "Education",
                "education"
            ]
        )


        # ==========================================
        # SKILLS SCORE
        # ==========================================

        for skill in skills:

            if skill in internship_skills:

                score += 15


        # ==========================================
        # FIELD SCORE
        # ==========================================

        if field:

            field_words = [
                word
                for word in field.split()
                if len(word) > 2
            ]

            for word in field_words:

                if (
                    word in internship_profile
                    or
                    word in internship_skills
                    or
                    word in internship_field
                ):

                    score += 20


        # ==========================================
        # LOCATION SCORE
        # ==========================================

        if location:

            if location in internship_location:

                score += 15


        # ==========================================
        # EDUCATION SCORE
        # ==========================================

        if education:

            if education in internship_education:

                score += 10


        # ==========================================
        # SAVE RESULT
        # ==========================================

        item = row.to_dict()

        item["score"] = min(score, 100)

        results.append(item)


    # ==========================================
    # CREATE RESULT DATAFRAME
    # ==========================================

    result_df = pd.DataFrame(results)


    if result_df.empty:

        return result_df


    # ==========================================
    # SORT BY SCORE
    # ==========================================

    result_df = result_df.sort_values(
        by="score",
        ascending=False
    )


    # ==========================================
    # RETURN MORE THAN 5 RESULTS
    # ==========================================

    return result_df.head(100)


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


    interest = safe_text(interest)
    location = safe_text(location)
    education = safe_text(education)


    internship_skills = get_row_text_for_reason(
        row,
        [
            "Skills",
            "skills"
        ]
    )


    profile = get_row_text_for_reason(
        row,
        [
            "profile",
            "title"
        ]
    )


    internship_location = get_row_text_for_reason(
        row,
        [
            "Location",
            "location"
        ]
    )


    internship_education = get_row_text_for_reason(
        row,
        [
            "Education",
            "education"
        ]
    )


    # ==========================================
    # SKILLS
    # ==========================================

    for skill in skills:

        if skill in internship_skills:

            reasons.append(
                f"{skill.title()} matches your skills"
            )


    # ==========================================
    # INTEREST / FIELD
    # ==========================================

    if interest:

        for word in interest.split():

            if len(word) > 2:

                if (
                    word in profile
                    or
                    word in internship_skills
                ):

                    reasons.append(
                        f"Matches your interest in {interest.title()}"
                    )

                    break


    # ==========================================
    # LOCATION
    # ==========================================

    if location:

        if location in internship_location:

            reasons.append(
                "Matches your preferred location"
            )


    # ==========================================
    # EDUCATION
    # ==========================================

    if education:

        if education in internship_education:

            reasons.append(
                "Education requirement matches"
            )


    # ==========================================
    # DEFAULT REASON
    # ==========================================

    if len(reasons) == 0:

        reasons.append(
            "Recommended based on your overall profile"
        )


    return reasons


# ==========================================
# HELPER FOR REASONS
# ==========================================

def get_row_text_for_reason(
    row,
    possible_columns
):

    values = []

    for column in possible_columns:

        if column in row.index:

            value = row[column]

            if not pd.isna(value):

                values.append(
                    str(value).lower()
                )

    return " ".join(values)


# ==========================================
# API ENDPOINT
# ==========================================

@app.route("/recommend", methods=["POST"])
def recommend():

    try:

        data = request.get_json()

        if not data:

            data = {}


        # ==========================================
        # GET USER DATA
        # ==========================================

        skills_text = data.get(
            "skills",
            ""
        )

        field = data.get(
            "field",
            ""
        )

        location = data.get(
            "location",
            ""
        )

        education = data.get(
            "education",
            ""
        )

        interests = data.get(
            "interests",
            ""
        )


        # ==========================================
        # CONVERT SKILLS
        # ==========================================

        if isinstance(
            skills_text,
            list
        ):

            skills = skills_text

        else:

            skills = [
                x.strip()
                for x in str(
                    skills_text
                ).split(",")
                if x.strip()
            ]


        # ==========================================
        # LOG REQUEST
        # ==========================================

        print("\n==========================================")
        print("NEW RECOMMENDATION REQUEST")
        print("Skills:", skills)
        print("Field:", field)
        print("Location:", location)
        print("Education:", education)
        print("Interests:", interests)
        print("==========================================")


        # ==========================================
        # GET RECOMMENDATIONS
        # ==========================================

        recommendations = get_recommendations_from_user(
            skills,
            field,
            location,
            education
        )


        # ==========================================
        # NO RESULTS
        # ==========================================

        if recommendations.empty:

            print("No matching internships found.")

            return jsonify([])


        # ==========================================
        # BUILD RESPONSE
        # ==========================================

        results = []


        for _, row in recommendations.iterrows():

            reasons = get_recommendation_reasons(
                row,
                skills,
                interests or field,
                location,
                education
            )


            item = row.to_dict()

            item["reasons"] = reasons


            # Convert NaN to None
            # so JSON does not break

            for key, value in item.items():

                if pd.isna(value):

                    item[key] = None


            results.append(item)


        print(
            "Returning",
            len(results),
            "internships"
        )


        return jsonify(results)


    except Exception as error:

        print(
            "ERROR:",
            str(error)
        )

        return jsonify({
            "error": str(error)
        }), 500


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "Backend is running",
        "dataset_rows": len(merged_df)
    })


# ==========================================
# LOCAL RUN
# ==========================================

if __name__ == "__main__":

    print("\n==========================================")
    print("INTERNMATCH BACKEND STARTING")
    print("Port: 5001")
    print("==========================================\n")


    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )
