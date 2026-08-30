# InternMatch

## AI-Based Internship Recommendation Engine for PM Internship Scheme

InternMatch is a web-based internship discovery and recommendation platform designed to help students discover internship opportunities based on their skills, interests, education, preferred field, and location.

The platform provides students with a simple way to create their profile, explore internship opportunities, search and filter results, and receive profile-based internship recommendations.

---
## PROBLEM

Students often struggle to find internship opportunities that match their individual skills, interests, education, and preferred location.

With a large number of internship opportunities available, manually searching and comparing opportunities can be time-consuming. Students may also find it difficult to determine which internships are most relevant to their profile.

InternMatch aims to simplify this process by connecting student profile information with available internship opportunities and presenting relevant results through a single platform.

---

## Proposed Solution

InternMatch provides a centralized platform where students can:

- Create and update their profile
- Add their education, skills, interests, field, and preferred location
- Explore internship opportunities
- Search internships using keywords
- Filter internships by field and location
- View profile-based recommendations
- View internship match scores
- Understand why an opportunity was recommended
- Explore individual internship opportunities

The frontend communicates with a Flask-based recommendation backend through an API.

The backend receives student profile information, processes it against the available internship dataset, and returns suitable internship opportunities.

---

## Features

### Student Profile

Students can create and update their profile with information such as:

- Education
- Skills
- Field of interest
- Interests
- Preferred location

This information is used as input for the recommendation process.

### Internship Discovery

Students can explore available internship opportunities through the internship discovery page.

Each internship can display:

- Internship role
- Company
- Location
- Duration
- Stipend
- Required skills
- Match score
- Recommendation reasons

### Internship Search

Students can search for opportunities using keywords related to:

- Internship roles
- Skills
- Companies
- Fields

### Internship Filters

Internships can be filtered according to:

- Field
- Location

### Profile-Based Recommendations

The student's profile information is sent to the recommendation backend.

The backend processes the profile information and returns internship recommendations.

### Match Score

Recommended opportunities can include a match percentage indicating how closely the internship matches the student's profile.

Example:

```text
82% MATCH
```

### Recommendation Reasons

The platform can display reasons associated with a recommendation.

Example:

```text
✓ Python matches your skills
✓ Matches your interest
✓ Relevant to your profile
```

### Result Sorting

The result page provides options for exploring recommendations such as:

- Best Match
- Latest
- Remote

---

## How It Works

```text
Student
   ↓
Create / Update Profile
   ↓
Profile Information
   ↓
Frontend JavaScript
   ↓
POST /recommend
   ↓
Flask Backend
   ↓
Internship Dataset
   ↓
Recommendation Processing
   ↓
Recommended Internships
   ↓
Results Page
   ↓
Search / Filter / Explore
```

---

## System Architecture

```text
                    ┌─────────────────────┐
                    │       Student       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Student Profile   │
                    │                     │
                    │ Skills              │
                    │ Education           │
                    │ Interests           │
                    │ Field               │
                    │ Location            │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Frontend       │
                    │    HTML/CSS/JS      │
                    └──────────┬──────────┘
                               │
                         POST /recommend
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Flask Backend    │
                    │ Recommendation API  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Internship Dataset  │
                    │        CSV          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Recommendation      │
                    │ Processing           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Internship Results  │
                    └─────────────────────┘
```

---

## Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Flask
- Flask-CORS
- Pandas

### Dataset

- Internship dataset in CSV format

### Storage

- Browser LocalStorage for the current prototype

---

## Project Structure

```text
InternMatch/
│
├── index.html
├── internships.html
├── result.html
├── profile.html
├── login.html
├── about.html
├── help.html
├── accessibility.html
│
├── style.css
│
├── app.py
├── merged_internships_dataset.csv
│
└── README.md
```

---

## Main Pages

### index.html

Landing page of the InternMatch platform.

### profile.html

Used by students to create and update their internship profile.

### internships.html

Provides the internship discovery interface with search and filtering functionality.

### result.html

Displays internship recommendations returned by the backend.

### login.html

Provides the student login interface.

### about.html

Provides information about the InternMatch platform.

---

## Backend API

The frontend communicates with the Flask recommendation backend using a REST API.

### Endpoint

```text
POST /recommend
```

### Backend URL

```text
https://internship-recommender-egnc.onrender.com/recommend
```

### Request Format

The frontend sends student profile information in JSON format.

Example:

```json
{
    "skills": "Python, SQL, Machine Learning",
    "field": "Artificial Intelligence",
    "location": "Delhi",
    "education": "BSc AI & ML",
    "interests": "Artificial Intelligence, Data Science"
}
```

### Response Format

The backend returns internship recommendation data.

Example:

```json
[
    {
        "profile": "Machine Learning Intern",
        "company": "Example Company",
        "Location": "Delhi",
        "Duration": "6 Months",
        "Stipend": "₹15,000 - 25,000/month",
        "Skills": "Python, Machine Learning, SQL",
        "score": 82,
        "reasons": [
            "Python matches your skills",
            "Matches your interest in Artificial Intelligence"
        ]
    }
]
```

---

## Data Flow

```text
Student Profile
      ↓
LocalStorage
      ↓
Frontend JavaScript
      ↓
POST Request
      ↓
Flask API
      ↓
Internship Dataset
      ↓
Recommendation Processing
      ↓
JSON Response
      ↓
Recommendation Cards
```

---

## Local Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Open the Project

```bash
cd InternMatch
```

### 3. Install Dependencies

Make sure Python is installed.

Install the required packages:

```bash
pip install flask flask-cors pandas
```

### 4. Start the Backend

```bash
python app.py
```

### 5. Run the Frontend

Open the project in VS Code and run the frontend using a local development server such as Live Server.

Open:

```text
index.html
```

---

## Profile Data

The current frontend prototype uses browser LocalStorage for storing profile information.

The profile is stored using:

```text
userProfile
```

Recommendation results can be stored using:

```text
internshipRecommendations
```

This allows different frontend pages to access the profile and recommendation information.

---

## Recommendation Results

An internship recommendation can contain:

```text
Internship Role
Company
Location
Duration
Stipend
Skills
Match Score
Recommendation Reasons
```

Example:

```text
82% MATCH

Machine Learning Intern

Example Company

📍 Delhi
⏱ 6 Months
💰 ₹15,000 - 25,000/month

Skills:
Python
Machine Learning
SQL

WHY RECOMMENDED

✓ Python matches your skills
✓ Matches your interest in Artificial Intelligence
```

---

## Current Project Status

```text
Status: Working Prototype
Project Type: Web Application
Frontend: HTML / CSS / JavaScript
Backend: Python / Flask
Recommendation API: Flask REST API
Dataset: Internship CSV Dataset
```

The current prototype supports:

- Student profile creation
- Profile-based recommendations
- Internship discovery
- Internship search
- Field filtering
- Location filtering
- Match scores
- Recommendation reasons
- Result sorting
- Opportunity exploration

---

## Current Limitations

The current implementation is a prototype and has some limitations:

- Recommendation quality depends on the available internship dataset and backend recommendation logic.
- Internship information depends on the dataset being used.
- Profile information is currently stored using browser LocalStorage.
- A production database is not currently integrated into the frontend.
- Production-level authentication and security are not yet implemented.
- Real-time internship availability is not guaranteed.
- The recommendation system can be further improved with advanced AI/ML techniques.

---

## Future Scope

### Advanced AI/ML Recommendation

The recommendation system can be enhanced using advanced machine learning or semantic matching techniques to better understand relationships between:

- Student skills
- Internship requirements
- Interests
- Education
- Career goals

### Resume-Based Recommendations

Students could upload resumes and the system could extract:

- Skills
- Education
- Projects
- Experience
- Certifications

This information could then be used to improve internship recommendations.

### Semantic Skill Matching

The system could understand related skills instead of relying only on exact keyword matching.

For example:

```text
Python
   ↓
Pandas
   ↓
Data Analysis
   ↓
Machine Learning
```

### Application Tracking

Students could track internship applications through stages such as:

```text
Saved
Applied
Interview
Selected
Rejected
```

### Deadline Notifications

Students could receive notifications about upcoming internship application deadlines.

### Database Integration

LocalStorage can be replaced with a secure database for storing:

- Student profiles
- Internship opportunities
- Applications
- Saved opportunities
- Recommendation history

### Company Dashboard

A future version could provide companies with dashboards to:

- Post internships
- Manage opportunities
- View applications
- Manage candidates

### Verified Internship Sources

The platform can be extended to include verified internship opportunities from trusted organizations and government sources.

---

## Hackathon Relevance

InternMatch is developed as a student-focused solution for internship discovery and recommendation.

The project demonstrates:

- Student profile management
- Internship data processing
- Profile-based recommendation
- Frontend-backend integration
- Search functionality
- Internship filtering
- Match scoring
- Recommendation explanations
- Internship opportunity exploration

The current prototype provides the foundation for an AI-powered internship recommendation platform and can be further enhanced with more advanced recommendation models.

---

## Team

InternMatch was developed as a student team project for a hackathon.

---

## License

This project is developed for educational and hackathon purposes.
