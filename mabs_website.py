import streamlit as st
from openai import OpenAI
import pandas as pd
import os
from datetime import datetime

# 1. Setup & Data Engine
st.set_page_config(page_title="MABS Academy", page_icon="🎓", layout="wide")
DATA_FILE = "mabs_inquiries.csv"

def save_inquiry(name, email, phone, course, message):
    df = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": name, "Email": email, "Phone": phone, "Course": course, "Message": message
    }])
    df.to_csv(DATA_FILE, mode='a', index=False, header=not os.path.exists(DATA_FILE))

def get_ai_response(query, api_key):
    if not api_key: return "⚠️ Please enter an OpenAI API Key in the sidebar settings."
    try:
        client = OpenAI(api_key=api_key)
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful expert tutor at MABS Academy assisting Miran Biswas. Answer clearly and step-by-step for Science, Maths, or Biology."},
                {"role": "user", "content": query}
            ], max_tokens=500
        )
        return res.choices.message.content
    except Exception as e: return f"⚠️ Connection failed: {str(e)}"

# 2. Sidebar Navigation
st.sidebar.title("🎓 MABS Academy")
page = st.sidebar.radio("Navigate:", ["Home & Faculty", "Our Courses & Fees", "AI Doubt Solver", "Contact Us"])
st.sidebar.markdown("---")
client_key = st.sidebar.text_input("OpenAI API Key Settings", type="password", help="Client's private billing key")

# 3. Main Application Routing
if page == "Home & Faculty":
    st.title("🚀 Welcome to MABS Academy")
    st.subheader("Nurturing Excellence, Achieving Dreams")
    st.image("https://unsplash.com", use_column_width=True)
    st.write("Led by expert educator *Miran Biswas*, MABS Academy provides high-tier academic guidance, core foundations, and competitive medical entrance preparation.")
    
    c1, c2, c3 = st.columns(3)
    c1.markdown("### 👨‍🏫 Miran Biswas\nDirect expert mentorship across high school and senior secondary levels.")
    c2.markdown("### 📚 Integrated Study\nComprehensive material customized for board exams and competitive tracks.")
    c3.markdown("### 📈 Proven Method\nRigorous regular test patterns paired with clear conceptual breakdown frameworks.")

elif page == "Our Courses & Fees":
    st.title("📚 Programs, Schedules & Batches")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("### 📐 Foundation Track (Class 6 - 10)")
            st.write("*Subjects:* Mathematics & Science (AP Curriculum Map Included)\n\n*Focus:* Conceptual depth, board benchmarks, and analytical skills.")
        with st.container(border=True):
            st.markdown("### 🩺 NEET Medical Intensive")
            st.write("*Target:* Medical Aspirants & Droppers\n\n*Focus:* High-yield Biology practice, rigorous mock cycles, and core NCERT breakdown.")
    with col2:
        with st.container(border=True):
            st.markdown("### 🧬 Higher Secondary Biology (Class 11 & 12)")
            st.write("*Subjects:* Advanced Biology Core\n\n*Focus:* Complete human/plant physiology, genetics, and board excellence modules.")

    st.markdown("### 💳 Active Academic Batches")
    st.table({
        "Course Level": ["Class 6 to 10 (Maths/Science/AP)", "Class 11 & 12 (Biology Board)", "NEET Biology Intensive"],
        "Schedule": ["3 Days / Week", "2 Days / Week", "4 Days / Week + Mock Tests"],
        "Seat Limit": ["25 Students Max", "30 Students Max", "30 Students Max"]
    })

elif page == "AI Doubt Solver":
    st.title("🤖 24/7 AI Doubt Solver")
    query = st.text_area("Type your question here:", placeholder="e.g., Explain the steps of cellular respiration, or solve 3x + 7 = 22")
    if st.button("Solve My Doubt ✨"):
        if not query.strip(): st.warning("Please type a query first.")
        else:
            with st.spinner("Generating step-by-step solution..."):
                st.markdown("### 📝 AI Tutor Solution:")
                st.write(get_ai_response(query, client_key))

elif page == "Contact Us":
    st.title("📞 Secure Your Seat")
    with st.form("contact", clear_on_submit=True):
        name = st.text_input("Student / Parent Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone / WhatsApp Number")
        course = st.selectbox("Program of Interest", ["Class 6-10 (Maths & Science)", "Class 6-10 (Advanced AP)", "Class 11/12 Biology Board", "NEET Prep", "General Inquiry"])
        msg = st.text_area("Specific Requirements or Questions")
        
        if st.form_submit_button("Submit Application"):
            if name and email and phone:
                save_inquiry(name, email, phone, course, msg)
                st.success(f"Success! Data registered securely into '{DATA_FILE}'.")
            else: st.error("Please fill out the mandatory fields (Name, Email, and Phone).")

st.markdown("---\n<p style='text-align: center; color: gray;'>© 2026 MABS Academy. All Rights Reserved.</p>", unsafe_allow_html=True)
