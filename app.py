import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import os


# ==========================================
# LOAD DATASET
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
merged_df = pd.read_csv(os.path.join(BASE_DIR, "merged_internships_dataset.csv"))

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
# SAFE TEXT FUNCTION
# ==========================================

def safe_text(value):

    if value is None:
        return ""

    if isinstance(value, (list, tuple)):
        return " ".join(str(x) for x in value).lower()

    try:
        if pd.isna(value):
            return ""
    except:
        pass

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

    # Safely convert inputs
    skills = [
        safe_text(x)
        for x in skills
        if safe_text(x)
    ]

    field = safe_text(field)
    location = safe_text(location)
    education = safe_text(education)

    results = []

    for _, row in df.iterrows():

        score = 0

        internship_skills = safe_text(
            row.get("Skills", "")
        )

        internship_profile = safe_text(
            row.get("profile", "")
        )

        internship_location = safe_text(
            row.get("Location", "")
        )

        internship_education = safe_text(
            row.get("Education", "")
        )


        # ==================================
        # SKILLS
        # ==================================

        for skill in skills:

            if skill and skill in internship_skills:
                score += 15


        # ==================================
        # FIELD
        # ==================================

        if field:

            field_words = field.split()

            for word in field_words:

                if len(word) > 2:

                    if (
                        word in internship_profile
                        or word in internship_skills
                    ):
                        score += 20
                        break


        # ==================================
        # LOCATION
        # ==================================

        if location:

            if location in internship_location:
                score += 15


        # ==================================
        # EDUCATION
        # ==================================

        if education:

            if education in internship_education:
                score += 10


        item = row.to_dict()

        item["score"] = min(score, 100)

        results.append(item)


    # ==================================
    # SORT RESULTS
    # ==================================

    result_df = pd.DataFrame(results)

    result_df = result_df.sort_values(
        by="score",
        ascending=False
    )

    return result_df.head(15)


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
        safe_text(x)
        for x in skills
        if safe_text(x)
    ]

    interest = safe_text(interest)
    location = safe_text(location)
    education = safe_text(education)

    internship_skills = safe_text(
        row.get("Skills", "")
    )

    profile = safe_text(
        row.get("profile", "")
    )

    internship_location = safe_text(
        row.get("Location", "")
    )

    internship_education = safe_text(
        row.get("Education", "")
    )


    # ==================================
    # SKILLS
    # ==================================

    for skill in skills:

        if skill and skill in internship_skills:

            reasons.append(
                f"{skill.title()} matches your skills"
            )


    # ==================================
    # INTEREST / FIELD
    # ==================================

    if interest:

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


    # ==================================
    # LOCATION
    # ==================================

    if location:

        if location in internship_location:

            reasons.append(
                "Matches your preferred location"
            )


    # ==================================
    # EDUCATION
    # ==================================

    if education:

        if education in internship_education:

            reasons.append(
                "Education requirement matches"
            )


    # ==================================
    # DEFAULT REASON
    # ==================================

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

    try:

        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({
                "error": "Invalid JSON data"
            }), 400


        skills_text = safe_text(
            data.get("skills", "")
        )

        field = safe_text(
            data.get("field", "")
        )

        location = safe_text(
            data.get("location", "")
        )

        education = safe_text(
            data.get("education", "")
        )


        # Convert skills string into list

        skills = [
            x.strip()
            for x in skills_text.split(",")
            if x.strip()
        ]


        print("==========================================")
        print("RECOMMENDATION REQUEST")
        print("Skills:", skills)
        print("Field:", field)
        print("Location:", location)
        print("Education:", education)
        print("==========================================")


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


    except Exception as e:

        print("==========================================")
        print("ERROR:")
        print(str(e))
        print("==========================================")


        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# GEMINI AI ASSISTANT
# ==========================================

load_dotenv(os.path.join(BASE_DIR, ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


@app.route("/ai-assistant", methods=["POST"])
def ai_assistant():

    try:

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Invalid JSON data"
            }), 400

        message = safe_text(data.get("message", ""))
        profile = data.get("profile", {})

        if not message:
            return jsonify({
                "error": "Message is required"
            }), 400

        if not isinstance(profile, dict):
            profile = {}

        skills = safe_text(profile.get("skills", ""))
        field = safe_text(profile.get("field", ""))
        location = safe_text(profile.get("location", ""))
        education = safe_text(profile.get("education", ""))
        interests = safe_text(profile.get("interests", ""))

        if client is None:
            return jsonify({
                "error": "GEMINI_API_KEY is not configured on the server."
            }), 503

        prompt = f"""
You are InternMatch AI Assistant.

InternMatch is an AI-powered internship discovery platform for students in India.

Student profile:
- Skills: {skills or "Not provided"}
- Field: {field or "Not provided"}
- Location preference: {location or "Not provided"}
- Education: {education or "Not provided"}
- Career interests: {interests or "Not provided"}

Student's question:
{message}

Give a concise, practical answer specifically for this student.

Rules:

1. Do not invent internships, companies, salaries, or deadlines.

2. Use the student's profile when giving advice.

3. If the student asks what they should apply for, explain why.

4. If they have skill gaps, clearly mention them.

5. Give actionable next steps.

6. Keep the answer easy for a college student to understand.

7. Format the answer with clear spacing between sections.

8. Use simple plain text headings such as:
Internships to Target
Why They Fit
Skill Gaps
Next Steps

9. Put a blank line between every section and between major points.

10. Use simple bullet points starting with "•".

11. Do NOT use Markdown symbols such as ###, **, *, ---, or backticks.

12. Do not write extremely long paragraphs.

13. Keep the response concise and easy to scan.
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        answer = getattr(response, "text", None)

        if not answer:
            raise RuntimeError("Gemini returned an empty response.")

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("==========================================")
        print("AI ASSISTANT ERROR:")
        print(str(e))
        print("==========================================")

        return jsonify({
            "error": "AI Assistant is temporarily unavailable."
        }), 500

# ==========================================
# HOME ROUTE
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

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )
