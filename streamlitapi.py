import streamlit as st

def calculate_gpa(courses):
    """Calculate GPA for a semester based on grades and credit units."""
    total_units = sum(course["units"] for course in courses)
    total_points = sum(course["gp"] * course["units"] for course in courses)
    return round(total_points / total_units, 2) if total_units > 0 else 0.0

def get_grade_and_gp(score, grading_system, max_gp):
    """Convert total score into grade and grade points based on the selected system."""
    for grade, (lower_bound, gp) in grading_system.items():
        if score >= lower_bound:
            return grade, gp
    return "F", 0  # Default to "F" if no condition matches

def classify_cgpa(cgpa, system):
    """Classify CGPA into honours divisions."""
    if system == "5-Point System":
        if cgpa >= 4.50:
            return "First Class Honours", "green"
        elif cgpa >= 3.50:
            return "Second Class Honours (Upper Division)", "blue"
        elif cgpa >= 2.40:
            return "Second Class Honours (Lower Division)", "blue"
        elif cgpa >= 1.50:
            return "Third Class Honours", "orange"
        else:
            return "Below Third Class", "red"
    
    elif system == "4-Point System":
        if cgpa >= 3.50:
            return "First Class Honours", "green"
        elif cgpa >= 3.00:
            return "Second Class Honours (Upper Division)", "blue"
        elif cgpa >= 2.00:
            return "Second Class Honours (Lower Division)", "blue"
        elif cgpa >= 1.00:
            return "Third Class Honours", "orange"
        else:
            return "Below Third Class", "red"
    
    else:  # Custom System (No Classification)
        return "Custom Classification", "black"

st.set_page_config(page_title="CGPA Calculator", layout="wide")
st.title("🎓 Customizable CGPA Calculator")

with st.sidebar:
    st.header("Settings")
    
    # Select CGPA system
    cgpa_system = st.radio("Select CGPA system:", ["5-Point System", "4-Point System", "Custom"])
    
    # Define max grade points based on selection
    if cgpa_system == "5-Point System":
        max_gp = 5
    elif cgpa_system == "4-Point System":
        max_gp = 4
    else:
        max_gp = st.number_input("Enter max grade point:", min_value=1, max_value=10, step=1, key="custom_gp")

    # Customizable Grading System
    st.subheader("Customize Grading System (Optional)")
    grading_system = {
        "A": (st.number_input("Min score for A:", min_value=0, max_value=100, value=70, key="A"), max_gp),
        "B": (st.number_input("Min score for B:", min_value=0, max_value=100, value=60, key="B"), max_gp - 1),
        "C": (st.number_input("Min score for C:", min_value=0, max_value=100, value=50, key="C"), max_gp - 2),
        "D": (st.number_input("Min score for D:", min_value=0, max_value=100, value=45, key="D"), max_gp - 3),
        "E": (st.number_input("Min score for F:", min_value=0, max_value=100, value=40, key="E"), max_gp - 4),
    }
    grading_system = dict(sorted(grading_system.items(), key=lambda item: item[1][0], reverse=True))

# Main CGPA Input Section
st.subheader("📌 Student Details")
name = st.text_input("Enter student name:")

st.subheader("📚 Semester Details")
num_semesters = st.number_input("Number of semesters:", min_value=1, step=1, key="num_semesters")

# Variables to store cumulative data
total_qp = 0  # Total Quality Points
total_cu = 0  # Total Credit Units

for sem in range(1, num_semesters + 1):
    with st.expander(f"📖 Semester {sem} Details", expanded=False):
        num_courses = st.number_input(f"Number of courses for Semester {sem}:", min_value=1, step=1, key=f"num_courses_{sem}")
        semester_courses = []

        for i in range(1, num_courses + 1):
            course_name = st.text_input(f"Course {i} (Semester {sem}):", key=f"course_name_{sem}_{i}")
            units = st.number_input(f"Credit Units for {course_name}:", min_value=1, step=1, key=f"units_{sem}_{i}")
            total_score = st.number_input(f"Total Score (0-100) for {course_name}:", min_value=0, max_value=100, step=1, key=f"score_{sem}_{i}")

            if course_name:
                grade, gp = get_grade_and_gp(total_score, grading_system, max_gp)
                semester_courses.append({"course": course_name, "units": units, "gp": gp})

        # Calculate GPA for the semester
        if semester_courses:
            gpa = calculate_gpa(semester_courses)
            total_qp += sum(course["gp"] * course["units"] for course in semester_courses)
            total_cu += sum(course["units"] for course in semester_courses)
            st.success(f"📊 GPA for Semester {sem}: {gpa}")

# Calculate and Display Final CGPA
if total_cu > 0:
    cgpa = round(total_qp / total_cu, 2)
    classification, color = classify_cgpa(cgpa, cgpa_system)
    
    st.subheader("🎖 Final CGPA & Classification")
    st.markdown(f"<h2 style='color: {color};'>Your Final CGPA: {cgpa} ({classification})</h2>", unsafe_allow_html=True)
else:
    st.warning("⚠ Please enter valid course details.")

st.markdown("---")
st.caption("Developed using Streamlit for an interactive user experience.")
