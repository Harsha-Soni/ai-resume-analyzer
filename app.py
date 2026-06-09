import streamlit as st
import pdfplumber

# ==================================================
# ROLE PREDICTION FUNCTION
# ==================================================

def predict_role(text):

    text = text.lower()

    if (
        "machine learning" in text
        or "tensorflow" in text
        or "pytorch" in text
    ):
        return "Machine Learning Engineer"

    elif (
        "data science" in text
        or "pandas" in text
        or "numpy" in text
        or "scikit-learn" in text
    ):
        return "Data Scientist"

    elif (
        "sql" in text
        or "power bi" in text
        or "excel" in text
    ):
        return "Data Analyst"

    elif (
        "react" in text
        or "javascript" in text
        or "next.js" in text
    ):
        return "Frontend Developer"

    elif (
        "node.js" in text
        or "express" in text
        or "mongodb" in text
    ):
        return "Backend Developer"

    else:
        return "Software Developer"


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ==================================================
# HEADER
# ==================================================

st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume, analyze ATS score, predict career roles, and compare with job descriptions."
)

# ==================================================
# FILE UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# ==================================================
# JOB DESCRIPTION INPUT
# ==================================================

job_description = st.text_area(
    "Paste Job Description (Optional)",
    height=200,
    placeholder="Paste a job description here to calculate match score..."
)

# ==================================================
# SKILLS DATABASE
# ==================================================

skills_db = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "streamlit",
    "power bi",
    "excel",
    "data analysis",
    "data science",
    "numpy",
    "pandas",
    "scikit-learn",
    "java",
    "c++",
    "javascript",
    "react",
    "next.js",
    "node.js",
    "git",
    "github",
    "docker",
    "aws"
]

# ==================================================
# MAIN LOGIC
# ==================================================

if uploaded_file is not None:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    text_lower = text.lower()

    st.success("✅ Resume Uploaded Successfully")

    # ==================================================
    # SKILLS DETECTED
    # ==================================================

    found_skills = []

    for skill in skills_db:

        if skill in text_lower:
            found_skills.append(skill)

    missing_skills = []

    for skill in skills_db:

        if skill not in found_skills:
            missing_skills.append(skill)

    # ==================================================
    # ATS SCORE
    # ==================================================

    ats_score = int(
        (len(found_skills) / len(skills_db)) * 100
    )

    st.subheader("🎯 ATS Score")

    st.metric(
        "ATS Score",
        f"{ats_score}/100"
    )

    st.progress(ats_score)

    # ==================================================
    # ROLE PREDICTION
    # ==================================================

    st.subheader("🎯 Predicted Career Role")

    predicted_role = predict_role(text)

    st.success(
        f"Recommended Role: {predicted_role}"
    )

    # ==================================================
    # JOB DESCRIPTION MATCHING
    # ==================================================

    if job_description.strip():

        st.subheader("🤝 Resume vs Job Description Match")

        jd_text = job_description.lower()

        jd_skills = []

        for skill in skills_db:

            if skill in jd_text:
                jd_skills.append(skill)

        matching_skills = []

        for skill in jd_skills:

            if skill in found_skills:
                matching_skills.append(skill)

        missing_jd_skills = []

        for skill in jd_skills:

            if skill not in found_skills:
                missing_jd_skills.append(skill)

        if len(jd_skills) > 0:

            match_score = int(
                (len(matching_skills) / len(jd_skills)) * 100
            )

        else:

            match_score = 0

        st.metric(
            "Match Score",
            f"{match_score}%"
        )

        st.progress(match_score)

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Matching Skills")

            if matching_skills:

                for skill in matching_skills:
                    st.success(skill.title())

            else:
                st.warning("No matching skills found")

        with col2:

            st.subheader("❌ Missing Job Skills")

            if missing_jd_skills:

                for skill in missing_jd_skills:
                    st.error(skill.title())

            else:
                st.success("No missing skills")

    # ==================================================
    # SKILLS DETECTED
    # ==================================================

    st.subheader("🛠 Skills Detected")

    if found_skills:

        for skill in found_skills:
            st.success(skill.title())

    else:

        st.warning("No skills detected.")

    # ==================================================
    # MISSING SKILLS
    # ==================================================

    st.subheader("❌ Missing Skills")

    for skill in missing_skills[:8]:

        st.warning(skill.title())

    # ==================================================
    # RESUME ANALYSIS
    # ==================================================

    st.subheader("🔍 Resume Analysis")

    github_found = "github" in text_lower

    linkedin_found = "linkedin" in text_lower

    project_found = (
        "project" in text_lower
        or "projects" in text_lower
    )

    internship_found = (
        "intern" in text_lower
        or "internship" in text_lower
    )

    if github_found:
        st.success("✅ GitHub profile found")
    else:
        st.error("❌ GitHub profile not found")

    if linkedin_found:
        st.success("✅ LinkedIn profile found")
    else:
        st.error("❌ LinkedIn profile not found")

    if project_found:
        st.success("✅ Projects section found")
    else:
        st.error("❌ Projects section not found")

    if internship_found:
        st.success("✅ Internship experience found")
    else:
        st.error("❌ Internship experience not found")

    # ==================================================
    # RECOMMENDATIONS
    # ==================================================

    st.subheader("💡 Personalized Suggestions")

    suggestions = []

    if not github_found:
        suggestions.append("Add your GitHub profile link.")

    if not linkedin_found:
        suggestions.append("Add your LinkedIn profile link.")

    if not internship_found:
        suggestions.append("Include internship experience if available.")

    if ats_score < 60:
        suggestions.append("Add more relevant technical skills.")

    if len(found_skills) < 8:
        suggestions.append("Expand your technical skill set.")

    if not suggestions:
        suggestions.append(
            "Great resume! Continue adding impactful projects and achievements."
        )

    for suggestion in suggestions:
        st.info(suggestion)

    # ==================================================
    # SUMMARY
    # ==================================================

    st.subheader("📊 Resume Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Skills Found",
            len(found_skills)
        )

    with col2:
        st.metric(
            "Missing Skills",
            len(missing_skills)
        )

    with col3:
        st.metric(
            "Predicted Role",
            predicted_role
        )

    # ==================================================
    # RESUME PREVIEW
    # ==================================================

    st.subheader("📄 Resume Preview")

    st.text_area(
        "Resume Content",
        text,
        height=300
    )

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Built with Python • Streamlit • NLP Concepts"
)