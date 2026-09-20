import streamlit as st
import pandas as pd
import os
from datetime import date, datetime

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="RA Care",
    page_icon="🦋",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #555;
    font-size: 18px;
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
    margin-bottom: 18px;
}

.small-card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    margin-bottom: 12px;
}

.notification {
    background: #eef6ff;
    padding: 15px;
    border-radius: 12px;
    border-left: 5px solid #3b82f6;
    margin-bottom: 10px;
}

.warning {
    background: #fff7ed;
    padding: 15px;
    border-radius: 12px;
    border-left: 5px solid #f97316;
    margin-bottom: 10px;
}

.footer {
    text-align: center;
    color: #777;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# FILE
# ---------------------------------------------------------
DATA_FILE = "ra_care_logs.csv"

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = 0

if "record_saved" not in st.session_state:
    st.session_state.record_saved = False

if "name" not in st.session_state:
    st.session_state.name = ""

if "gender" not in st.session_state:
    st.session_state.gender = ""

if "dob" not in st.session_state:
    st.session_state.dob = None

if "stiffness" not in st.session_state:
    st.session_state.stiffness = 0

if "pain" not in st.session_state:
    st.session_state.pain = 0

if "joints" not in st.session_state:
    st.session_state.joints = []

if "notes" not in st.session_state:
    st.session_state.notes = ""

if "food" not in st.session_state:
    st.session_state.food = ""

if "exercise" not in st.session_state:
    st.session_state.exercise = ""

if "medicine" not in st.session_state:
    st.session_state.medicine = ""

if "water" not in st.session_state:
    st.session_state.water = 0

if "sleep" not in st.session_state:
    st.session_state.sleep = 0

# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------
def next_page():
    st.session_state.page += 1
    st.rerun()

def previous_page():
    if st.session_state.page > 0:
        st.session_state.page -= 1
        st.rerun()

def home_page():
    st.session_state.page = 0
    st.rerun()

# ---------------------------------------------------------
# SAVE DATA
# ---------------------------------------------------------
def save_record():

    record = {
        "Date": str(date.today()),
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Name": st.session_state.name,
        "Gender": st.session_state.gender,
        "Date of Birth": str(st.session_state.dob),
        "Morning Stiffness (minutes)": st.session_state.stiffness,
        "Pain Score": st.session_state.pain,
        "Swollen / Discomfort Areas": ", ".join(st.session_state.joints),
        "Food Choice": st.session_state.food,
        "Exercise Choice": st.session_state.exercise,
        "Medicine Status": st.session_state.medicine,
        "Water (glasses)": st.session_state.water,
        "Sleep (hours)": st.session_state.sleep,
        "Notes": st.session_state.notes
    }

    new_df = pd.DataFrame([record])

    if os.path.exists(DATA_FILE):
        old_df = pd.read_csv(DATA_FILE)
        final_df = pd.concat([old_df, new_df], ignore_index=True)
    else:
        final_df = new_df

    final_df.to_csv(DATA_FILE, index=False)

# ---------------------------------------------------------
# NOTIFICATIONS
# ---------------------------------------------------------
def show_notifications():

    st.markdown("### 🔔 Notifications")

    notifications = [
        "💧 Don't forget to drink enough water today.",
        "🧘 Take a few minutes for gentle stretching.",
        "😴 Try to maintain a regular sleep schedule.",
        "📊 Remember to update your daily health check-in.",
        "🥗 Choose balanced and nutritious food whenever possible."
    ]

    for message in notifications:
        st.markdown(
            f'<div class="notification">{message}</div>',
            unsafe_allow_html=True
        )

# ---------------------------------------------------------
# PAGE 0 - HOME
# ---------------------------------------------------------
if st.session_state.page == 0:

    st.markdown('<div class="title">🦋 RA Care</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="subtitle">Smart Rheumatoid Arthritis Wellness Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="card">
        <h2>🌷 Welcome to RA Care</h2>
        <p>
        RA Care is a simple wellness monitoring application designed
        to help users track daily symptoms, lifestyle habits and
        wellness activities.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🩺 **Health Tracking**\n\nTrack pain and morning stiffness.")

    with col2:
        st.success("🥗 **Healthy Lifestyle**\n\nFood and activity guidance.")

    with col3:
        st.warning("🔔 **Smart Reminders**\n\nDaily notifications and wellness tips.")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Start RA Care", use_container_width=True):
        next_page()

# ---------------------------------------------------------
# PAGE 1 - USER DETAILS
# ---------------------------------------------------------
elif st.session_state.page == 1:

    st.title("👤 User Details")

    st.markdown(
        '<div class="card">Please enter your basic details before starting the assessment.</div>',
        unsafe_allow_html=True
    )

    st.session_state.name = st.text_input(
        "Name",
        value=st.session_state.name
    )

    st.session_state.gender = st.selectbox(
        "Gender",
        ["Select", "Female", "Male", "Other"],
        index=0 if not st.session_state.gender else
        ["Select", "Female", "Male", "Other"].index(st.session_state.gender)
    )

    st.session_state.dob = st.date_input(
        "Date of Birth",
        value=st.session_state.dob if st.session_state.dob else date(2004, 1, 1)
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            previous_page()

    with col2:
        if st.button("Next ➡️", use_container_width=True):
            if not st.session_state.name.strip():
                st.warning("Please enter your name.")
            elif st.session_state.gender == "Select":
                st.warning("Please select your gender.")
            else:
                next_page()

# ---------------------------------------------------------
# PAGE 2 - HEALTH ASSESSMENT
# ---------------------------------------------------------
elif st.session_state.page == 2:

    st.title("🩺 Health Assessment")

    st.session_state.stiffness = st.slider(
        "🌅 Morning Stiffness (minutes)",
        min_value=0,
        max_value=180,
        value=st.session_state.stiffness
    )

    st.session_state.pain = st.slider(
        "🔥 Pain Level",
        min_value=0,
        max_value=10,
        value=st.session_state.pain
    )

    st.session_state.joints = st.multiselect(
        "🖐️ Swollen / Discomfort Areas",
        [
            "Hands / Fingers",
            "Wrists",
            "Elbows",
            "Shoulders",
            "Knees",
            "Feet / Ankles",
            "Other"
        ],
        default=st.session_state.joints
    )

    st.session_state.notes = st.text_area(
        "📝 Additional Notes",
        value=st.session_state.notes,
        placeholder="Write any notes about today's condition..."
    )

    if st.session_state.pain >= 8:
        st.warning(
            "⚠️ Your recorded pain level is high. "
            "If severe or persistent, consider contacting a healthcare professional."
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            previous_page()

    with col2:
        if st.button("Next ➡️", use_container_width=True):
            next_page()

# ---------------------------------------------------------
# PAGE 3 - FOOD GUIDANCE
# ---------------------------------------------------------
elif st.session_state.page == 3:

    st.title("🥗 Food Guidance")

    st.markdown("""
    <div class="card">
    Choose balanced foods that support general wellness.
    This section provides general educational guidance and is
    not a personalized medical diet plan.
    </div>
    """, unsafe_allow_html=True)

    foods = [
        ("🥦 Vegetables", "Leafy greens, broccoli, carrots and other vegetables."),
        ("🍎 Fruits", "Fresh fruits such as apples, oranges, berries and bananas."),
        ("🥜 Nuts & Seeds", "Nuts and seeds can be included as part of a balanced diet."),
        ("🌾 Whole Grains", "Oats, brown rice and other whole-grain choices."),
        ("🐟 Healthy Protein", "Fish, eggs, beans, pulses and other balanced protein sources."),
        ("🥑 Healthy Fats", "Foods such as avocado, nuts and suitable cooking oils.")
    ]

    for title, description in foods:
        st.markdown(
            f"""
            <div class="small-card">
            <h3>{title}</h3>
            <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.warning(
        "⚠️ Try to limit highly processed foods, excess added sugar "
        "and foods high in saturated fat."
    )

    st.session_state.food = st.selectbox(
        "🍽️ Today's Food Choice",
        [
            "Not selected",
            "Balanced Meal",
            "Vegetables & Fruits",
            "Whole Grains",
            "Protein-rich Meal",
            "Other"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            previous_page()

    with col2:
        if st.button("Next ➡️", use_container_width=True):
            next_page()

# ---------------------------------------------------------
# PAGE 4 - ACTIVITY
# ---------------------------------------------------------
elif st.session_state.page == 4:

    st.title("🧘 Activity & Workout Guidance")

    activities = [
        ("🚶 Walking", "Gentle walking can support general mobility."),
        ("🤸 Stretching", "Gentle stretching may help maintain flexibility."),
        ("🧘 Yoga", "Choose gentle movements and avoid movements that cause pain."),
        ("🏊 Water Exercise", "Low-impact water activities may be comfortable for some people."),
        ("🔄 Range of Motion", "Gentle range-of-motion movements can support mobility."),
        ("😴 Rest & Recovery", "Allow adequate rest when your body needs it.")
    ]

    for title, description in activities:
        st.markdown(
            f"""
            <div class="small-card">
            <h3>{title}</h3>
            <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.warning(
        "⚠️ Do not push through significant pain. "
        "Stop an activity if it causes concerning symptoms."
    )

    st.session_state.exercise = st.selectbox(
        "🏃 Today's Activity",
        [
            "Not selected",
            "Walking",
            "Gentle Stretching",
            "Yoga",
            "Water Exercise",
            "Range of Motion",
            "Rest / Recovery"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            previous_page()

    with col2:
        if st.button("Next ➡️", use_container_width=True):
            next_page()

# ---------------------------------------------------------
# PAGE 5 - MEDICINE & DAILY CARE
# ---------------------------------------------------------
elif st.session_state.page == 5:

    st.title("💊 Medicine & Daily Care")

    st.info(
        "💡 RA Care does not prescribe, change or recommend medicines. "
        "Follow your healthcare professional's instructions."
    )

    st.session_state.medicine = st.selectbox(
        "💊 Prescribed Medicine Status",
        [
            "Not selected",
            "Taken as prescribed",
            "Not taken",
            "Not applicable"
        ]
    )

    st.session_state.water = st.number_input(
        "💧 Water Intake (glasses)",
        min_value=0,
        max_value=20,
        value=st.session_state.water
    )

    st.session_state.sleep = st.number_input(
        "😴 Sleep (hours)",
        min_value=0.0,
        max_value=24.0,
        value=float(st.session_state.sleep),
        step=0.5
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            previous_page()

    with col2:
        if st.button("Next ➡️", use_container_width=True):
            next_page()

# ---------------------------------------------------------
# PAGE 6 - DAILY REMINDER + NOTIFICATIONS
# ---------------------------------------------------------
elif st.session_state.page == 6:

    st.title("🔔 Daily Reminder & Notifications")

    st.markdown("""
    <div class="card">
        <h2>⏰ Your Daily Wellness Reminder</h2>
        <p>
        Make a small effort every day to track your symptoms,
        stay hydrated, move gently and maintain healthy sleep.
        </p>
    </div>
    """, unsafe_allow_html=True)

    show_notifications()

    st.markdown("### ⏰ Reminder Checklist")

    reminder1 = st.checkbox("💧 Drink enough water")
    reminder2 = st.checkbox("🧘 Do gentle movement")
    reminder3 = st.checkbox("🥗 Choose a balanced meal")
    reminder4 = st.checkbox("😴 Maintain good sleep")
    reminder5 = st.checkbox("📊 Complete today's health check-in")

    completed = sum([
        reminder1,
        reminder2,
        reminder3,
        reminder4,
        reminder5
    ])

    st.progress(completed / 5)

    st.write(f"### 🎯 Daily Reminder Progress: {completed}/5")

    if completed == 5:
        st.success("🎉 Great! You completed all your daily wellness reminders.")
    elif completed >= 3:
        st.info("👍 Good progress! Try to complete the remaining reminders.")
    else:
        st.warning("🌷 Start with one small wellness activity today.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            previous_page()

    with col2:
        if st.button("Next ➡️", use_container_width=True):
            next_page()

# ---------------------------------------------------------
# PAGE 7 - SMART INSIGHTS
# ---------------------------------------------------------
elif st.session_state.page == 7:

    st.title("🧠 Smart Daily Insights")

    if st.session_state.pain >= 8:
        st.warning(
            "⚠️ Your pain score is high. If this is severe, worsening "
            "or persistent, consider contacting a healthcare professional."
        )
    elif st.session_state.pain >= 5:
        st.info(
            "💡 Your recorded pain is moderate. Consider gentle activity "
            "and adequate rest."
        )
    else:
        st.success(
            "😊 Your recorded pain level is relatively low today."
        )

    if st.session_state.stiffness >= 60:
        st.warning(
            "🌅 Morning stiffness is prolonged today. "
            "Track how it changes over time and discuss persistent concerns "
            "with a healthcare professional."
        )
    else:
        st.info(
            "🌷 Keep tracking morning stiffness to understand your daily pattern."
        )

    if st.session_state.water < 6:
        st.info("💧 Reminder: try to maintain adequate hydration.")
    else:
        st.success("💧 Good hydration tracking today.")

    if st.session_state.sleep < 7:
        st.info("😴 Your recorded sleep is below 7 hours. Consider a regular sleep routine.")
    else:
        st.success("😴 Good sleep tracking today.")

    st.markdown("### 🌟 Personalized Wellness Tip")

    tips = [
        "Take short movement breaks during long periods of sitting.",
        "Choose comfortable, gentle physical activity.",
        "Keep a regular sleep routine.",
        "Track symptoms consistently.",
        "Stay hydrated throughout the day."
    ]

    tip_index = int(st.session_state.pain) % len(tips)

    st.success("💡 " + tips[tip_index])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            previous_page()

    with col2:
        if st.button("Next ➡️", use_container_width=True):
            next_page()

# ---------------------------------------------------------
# PAGE 8 - DASHBOARD
# ---------------------------------------------------------
elif st.session_state.page == 8:

    st.title("📊 Progress Dashboard")

    # Save current record only once
    if not st.session_state.record_saved:

        save_record()
        st.session_state.record_saved = True

        st.success("✅ Today's health record saved successfully!")

    if os.path.exists(DATA_FILE):

        df = pd.read_csv(DATA_FILE)

        # KPI
        total_checkins = len(df)

        avg_pain = pd.to_numeric(
            df["Pain Score"], errors="coerce"
        ).mean()

        avg_stiffness = pd.to_numeric(
            df["Morning Stiffness (minutes)"], errors="coerce"
        ).mean()

        avg_sleep = pd.to_numeric(
            df["Sleep (hours)"], errors="coerce"
        ).mean()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📅 Total Check-ins", total_checkins)

        with col2:
            st.metric(
                "🔥 Average Pain",
                f"{avg_pain:.1f}" if pd.notna(avg_pain) else "0"
            )

        with col3:
            st.metric(
                "🌅 Avg. Stiffness",
                f"{avg_stiffness:.1f} min"
                if pd.notna(avg_stiffness) else "0"
            )

        with col4:
            st.metric(
                "😴 Average Sleep",
                f"{avg_sleep:.1f} hrs"
                if pd.notna(avg_sleep) else "0"
            )

        # Wellness Goal
        st.markdown("### 🎯 Daily Wellness Goal")

        goals = 0

        if st.session_state.water >= 6:
            goals += 1

        if st.session_state.sleep >= 7:
            goals += 1

        if st.session_state.food != "Not selected":
            goals += 1

        if st.session_state.exercise != "Not selected":
            goals += 1

        st.progress(goals / 4)

        st.write(f"**{goals}/4 wellness goals completed**")

        if goals == 4:
            st.success("🏆 Excellent! You completed today's wellness goals.")
        elif goals >= 2:
            st.info("👍 Good progress. Keep going!")
        else:
            st.warning("🌱 Start with small daily wellness goals.")

        # Pain chart
        st.markdown("### 📈 Pain Trend")

        chart_df = df.copy()

        chart_df["Pain Score"] = pd.to_numeric(
            chart_df["Pain Score"],
            errors="coerce"
        )

        chart_df["Check-in"] = range(1, len(chart_df) + 1)

        st.line_chart(
            chart_df.set_index("Check-in")["Pain Score"]
        )

        st.markdown("### 📋 Previous Records")

        st.dataframe(
            df,
            use_container_width=True
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            previous_page()

    with col2:
        if st.button("Next ➡️", use_container_width=True):
            next_page()

# ---------------------------------------------------------
# PAGE 9 - DOWNLOAD REPORT
# ---------------------------------------------------------
elif st.session_state.page == 9:

    st.title("📄 Download Report")

    st.markdown("""
    <div class="card">
        <h2>📑 RA Care Health Report</h2>
        <p>
        Download your recorded wellness data as a CSV file.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if os.path.exists(DATA_FILE):

        report_df = pd.read_csv(DATA_FILE)

        st.dataframe(
            report_df,
            use_container_width=True
        )

        csv_data = report_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download RA Care Report",
            data=csv_data,
            file_name="RA_Care_Health_Report.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.success(
            "✅ Your report is ready to download."
        )

    else:
        st.info("No health records available yet.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            previous_page()

    with col2:
        if st.button("Next ➡️", use_container_width=True):
            next_page()

# ---------------------------------------------------------
# PAGE 10 - SAFETY NOTIFICATIONS
# ---------------------------------------------------------
elif st.session_state.page == 10:

    st.title("🆘 Safety Notifications")

    st.markdown("""
    <div class="card">
        <h2>⚠️ Important Wellness Information</h2>
        <p>
        RA Care is a wellness tracking and educational application.
        It is not a diagnostic or emergency medical system.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.pain >= 8:

        st.error(
            "⚠️ High pain level recorded. "
            "If the pain is severe, worsening or persistent, "
            "consider contacting a healthcare professional."
        )

    if st.session_state.stiffness >= 120:

        st.warning(
            "🌅 Prolonged morning stiffness recorded. "
            "Continue monitoring your symptoms and discuss persistent concerns "
            "with a healthcare professional."
        )

    if st.session_state.pain < 8 and st.session_state.stiffness < 120:

        st.success(
            "😊 No high-level wellness notification was triggered "
            "by today's recorded values."
        )

    st.markdown("### 📌 General Safety Reminders")

    safety_items = [
        "Do not stop or change prescribed medicines without professional advice.",
        "Do not push through significant pain during exercise.",
        "Seek professional medical advice for severe or persistent symptoms.",
        "Use RA Care as a tracking and wellness-support tool."
    ]

    for item in safety_items:
        st.markdown(
            f'<div class="warning">⚠️ {item}</div>',
            unsafe_allow_html=True
        )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            previous_page()

    with col2:
        if st.button("Next ➡️", use_container_width=True):
            next_page()

# ---------------------------------------------------------
# PAGE 11 - ABOUT PROJECT
# ---------------------------------------------------------
elif st.session_state.page == 11:

    st.title("📚 About RA Care")

    st.markdown("""
    <div class="card">
        <h2>🦋 Smart Rheumatoid Arthritis Wellness Assistant</h2>

        <p>
        RA Care is a Streamlit-based wellness monitoring application
        designed to help users record daily health information,
        monitor symptoms and receive general wellness guidance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Project Objective")

    st.write(
        "To provide a simple digital platform for daily symptom tracking, "
        "wellness monitoring, reminders and report generation."
    )

    st.markdown("### ⭐ Key Features")

    features = [
        "👤 User Details",
        "🩺 Health Assessment",
        "🥗 Food Guidance",
        "🧘 Activity & Workout Guidance",
        "💊 Medicine & Daily Care Tracking",
        "🔔 Normal App Notifications",
        "⏰ Daily Wellness Reminder",
        "🧠 Smart Daily Insights",
        "📊 Progress Dashboard",
        "📄 Downloadable CSV Report",
        "🆘 Safety Notifications",
        "📚 About Project"
    ]

    for feature in features:
        st.write("• " + feature)

    st.markdown("### 💻 Technologies Used")

    tech_col1, tech_col2, tech_col3 = st.columns(3)

    with tech_col1:
        st.info("🐍 Python")

    with tech_col2:
        st.success("🌐 Streamlit")

    with tech_col3:
        st.warning("📊 Pandas")

    st.markdown("### 🔮 Future Scope")

    st.write(
        "Future versions can include secure user accounts, advanced analytics, "
        "mobile notifications, database integration and professionally reviewed "
        "wellness content."
    )

    st.markdown("### ⚠️ Disclaimer")

    st.warning(
        "RA Care is for educational and wellness tracking purposes only. "
        "It does not diagnose rheumatoid arthritis, prescribe medicines, "
        "or replace professional medical advice."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            previous_page()

    with col2:
        if st.button("Next ➡️", use_container_width=True):
            next_page()

# ---------------------------------------------------------
# PAGE 12 - THANK YOU
# ---------------------------------------------------------
elif st.session_state.page == 12:

    st.markdown(
        '<div class="title">🎉 Thank You!</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="card">
        <h2 style="text-align:center;">🦋 Thank you for using RA Care</h2>

<<p style="text-align:center;">
Stay healthy, stay active, and take care! 💙
</p>
    </div>
    """, unsafe_allow_html=True)

    st.success("🌷 Small daily habits can support your overall wellness.")

    if st.button("🏠 Back to Home", use_container_width=True):
        home_page()

    if st.button("🔄 Start New Check-in", use_container_width=True):
        st.session_state.page = 1
        st.session_state.record_saved = False
        st.rerun()

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown(
    '<div class="footer">🦋 RA Care | Smart Wellness Monitoring System</div>',
    unsafe_allow_html=True
)