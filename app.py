import streamlit as st
import os
import uuid
from datetime import datetime

from clip_test import compare_images

from database import (
    initialize_database,
    add_report,
    get_reports,
    create_user,
    verify_user
)
# Initialize the database
initialize_database()

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Smart Lost & Found",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# SESSION STATE
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "report_type" not in st.session_state:
    st.session_state.report_type = None
# =========================================================
# LOGIN / SIGN UP
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 Smart Lost & Found")

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    # ---------------- LOGIN ----------------
    with login_tab:
        username = st.text_input("Username", key="login_username")
        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", use_container_width=True):

            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful! 🎉")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    # ---------------- SIGN UP ----------------
    with signup_tab:
        new_username = st.text_input(
            "Choose a username",
            key="signup_username"
        )

        new_password = st.text_input(
            "Choose a password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm password",
            type="password",
            key="confirm_password"
        )

        if st.button("Create Account", use_container_width=True):

            if not new_username or not new_password:
                st.warning("Please fill in all fields.")

            elif new_password != confirm_password:
                st.error("Passwords do not match.")

            else:
                if create_user(new_username, new_password):
                    st.success("Account created successfully! 🎉")
                    st.info("You can now log in.")
                else:
                    st.error("Username already exists.")

    # IMPORTANT:
    # Stop the rest of the website from displaying
    st.stop()
# ============================================================
# PREMIUM CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #F7F3E8;
    color: #173F32;
}

.block-container {
    max-width: 1320px;
    padding-top: 2.2rem;
    padding-bottom: 4rem;
}

/* Hide Streamlit chrome */
#MainMenu, footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* NAVIGATION */
.navbar-box {
    background: rgba(255,255,255,0.94);
    border: 1px solid #E6E0D4;
    border-radius: 0 0 24px 24px;
    padding: 18px 28px 20px;
    margin: -2.2rem -1rem 55px;
    box-shadow: 0 10px 35px rgba(23,63,50,0.06);
}

.brand-name {
    font-family: 'Manrope', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #174B3A;
    letter-spacing: -0.7px;
}

.brand-sub {
    margin-top: 3px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #34885F;
}

.nav-tagline {
    text-align: right;
    color: #708079;
    font-size: 13px;
    padding-top: 8px;
}

/* NAV BUTTONS */
div[data-testid="stHorizontalBlock"] .nav-btn button {
    border: 1px solid #DCE3DE !important;
    background: #FFFFFF !important;
    color: #174B3A !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    min-height: 42px !important;
    transition: all .18s ease !important;
}

div[data-testid="stHorizontalBlock"] .nav-btn button:hover {
    background: #174B3A !important;
    color: #FFFFFF !important;
    border-color: #174B3A !important;
}

/* HERO */
.hero {
    text-align: center;
    padding: 10px 15px 58px;
}

.eyebrow {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 5px;
    color: #398B61;
    margin-bottom: 18px;
}

.hero-title {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(48px, 6vw, 80px);
    line-height: 1;
    font-weight: 800;
    letter-spacing: -4px;
    color: #123E31;
}

.hero-title .accent {
    color: #449766;
    font-style: italic;
}

.hero-tagline {
    margin-top: 23px;
    font-family: 'Manrope', sans-serif;
    font-size: 21px;
    font-weight: 700;
    color: #195540;
}

.hero-description {
    margin-top: 12px;
    font-size: 16px;
    color: #60736C;
}

/* CARDS */
.card-shell {
    background: #FFFFFF;
    border: 1px solid #E5E0D6;
    border-radius: 26px;
    padding: 38px;
    min-height: 260px;
    box-shadow: 0 12px 35px rgba(23,63,50,0.055);
}

.card-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #719083;
    margin-bottom: 23px;
}

.card-title {
    font-family: 'Manrope', sans-serif;
    font-size: 31px;
    font-weight: 800;
    letter-spacing: -1.1px;
    color: #174B3A;
    margin-bottom: 14px;
}

.card-text {
    font-size: 15px;
    line-height: 1.7;
    color: #60766E;
    max-width: 520px;
}

/* CARD BUTTONS */
.card-button button {
    width: 100%;
    margin-top: -4px;
    border-radius: 0 0 14px 14px !important;
    border: 1px solid #174B3A !important;
    background: #174B3A !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    min-height: 48px !important;
}

.card-button button:hover {
    background: #0F392C !important;
    border-color: #0F392C !important;
}

/* SECTION */
.section {
    text-align: center;
    margin: 82px 0 34px;
}

.section-eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 4px;
    color: #49936B;
}

.section-title {
    font-family: 'Manrope', sans-serif;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #174B3A;
    margin-top: 8px;
}

/* PROCESS */
.process-card {
    background: #FFFFFF;
    border: 1px solid #E5E0D6;
    border-radius: 21px;
    padding: 28px;
    min-height: 205px;
    box-shadow: 0 8px 25px rgba(23,63,50,0.04);
}

.process-number {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #79A58E;
    margin-bottom: 32px;
}

.process-title {
    font-family: 'Manrope', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #174B3A;
    margin-bottom: 11px;
}

.process-text {
    font-size: 14px;
    line-height: 1.6;
    color: #71827C;
}

/* FORM */
.form-shell {
    background: #FFFFFF;
    border: 1px solid #E5E0D6;
    border-radius: 26px;
    padding: 34px;
    box-shadow: 0 10px 35px rgba(23,63,50,0.05);
}

.form-title {
    font-family: 'Manrope', sans-serif;
    font-size: 30px;
    font-weight: 800;
    color: #174B3A;
}

.form-subtitle {
    color: #6D7D76;
    margin-bottom: 25px;
}

/* FOOTER */
.footer {
    text-align: center;
    margin-top: 80px;
    padding-top: 25px;
    border-top: 1px solid #DCD8CD;
    color: #84928C;
    font-size: 12px;
}

/* MOBILE */
@media (max-width: 700px) {
    .navbar-box {
        margin-left: -0.5rem;
        margin-right: -0.5rem;
    }

    .hero-title {
        font-size: 48px;
        letter-spacing: -2.5px;
    }

    .hero-tagline {
        font-size: 18px;
    }

    .card-shell {
        padding: 28px;
    }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# NAVBAR
# ============================================================
st.markdown("""
<div class="navbar-box">
    <div class="brand-name">🔎 Smart Lost &amp; Found</div>
    <div class="brand-sub">CAMPUS COMMUNITY</div>
</div>
""", unsafe_allow_html=True)

nav1, nav2, nav3, nav4 = st.columns(4, gap="small")

with nav1:
    if st.button("Home", key="nav_home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

with nav2:
    if st.button("Reports", key="nav_reports", use_container_width=True):
        st.session_state.page = "Reports"
        st.rerun()

with nav3:
    if st.button("Matches", key="nav_matches", use_container_width=True):
        st.session_state.page = "Matches"
        st.rerun()

with nav4:
    if st.button("About", key="nav_about", use_container_width=True):
        st.session_state.page = "About"
        st.rerun()

# ============================================================
# HOME
# ============================================================
if st.session_state.page == "Home":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">CAMPUS COMMUNITY</div>
        <div class="hero-title">
            Smart <span class="accent">Lost</span> &amp; Found
        </div>
        <div class="hero-tagline">Find it. Return it. Together.</div>
        <div class="hero-description">
            A smarter way for students to report and find lost belongings.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="card-shell">
            <div class="card-label">LOST ITEM</div>
            <div class="card-title">I lost something</div>
            <div class="card-text">
                Can't find something on campus?<br>
                Upload a photo and tell us a few details.<br>
                Our system will look for possible matches.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Report Lost Item →", key="lost_button", use_container_width=True):
            st.session_state.report_type = "Lost"
            st.session_state.page = "Reports"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card-shell">
            <div class="card-label">FOUND ITEM</div>
            <div class="card-title">I found something</div>
            <div class="card-text">
                Found an item that belongs to someone?<br>
                Upload its photo and details to help return it<br>
                to the right person.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Report Found Item →", key="found_button", use_container_width=True):
            st.session_state.report_type = "Found"
            st.session_state.page = "Reports"
            st.rerun()

    st.markdown("""
    <div class="section">
        <div class="section-eyebrow">HOW IT WORKS</div>
        <div class="section-title">AI Matching</div>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3, p4 = st.columns(4, gap="medium")

    process = [
        ("01", "Upload", "Add a photo of the lost or found item."),
        ("02", "Analyze", "AI extracts useful visual information from the uploaded image."),
        ("03", "Compare", "The system compares the report with other reported items."),
        ("04", "Find Match", "Potential matches are shown to help reunite the item with its owner."),
    ]

    for col, (num, title, text) in zip((p1, p2, p3, p4), process):
        with col:
            st.markdown(f"""
            <div class="process-card">
                <div class="process-number">{num}</div>
                <div class="process-title">{title}</div>
                <div class="process-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# REPORTS
# ============================================================
elif st.session_state.page == "Reports":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">REPORT AN ITEM</div>
        <div class="hero-title">Tell us what happened.</div>
        <div class="hero-description">
            Add a few details so the system can help find a match.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="form-shell">
        <div class="form-title">Item Report</div>
        <div class="form-subtitle">
            Upload the item photo and provide the details below.
        </div>
    </div>
    """, unsafe_allow_html=True)

    report_type = st.radio(
    "Report type",
    ["I Lost Something", "I Found Something"],
    index=0 if st.session_state.report_type == "Lost" else 1,
    horizontal=True
)

    item_name = st.text_input(
        "Item name",
        placeholder="Example: Black backpack"
    )

    location = st.text_input(
        "Location",
        placeholder="Example: Main Block, Library"
    )

    description = st.text_area(
        "Description",
        placeholder="Describe the item, colour, brand, unique marks, etc."
    )

    image = st.file_uploader(
        "Upload item photo",
        type=["png", "jpg", "jpeg"]
    )
    if st.button("Submit Report →", key="submit_report", use_container_width=True):
        if not item_name or not description:
            st.warning("Please provide at least the item name and description.")
        else:
            # Convert report type
            report_type_value = (
                "Lost" if report_type == "I Lost Something" else "Found"
            )

            # Create uploads folder
            os.makedirs("uploads", exist_ok=True)

            # Save uploaded image
            image_path = ""

            if image is not None:
                file_extension = os.path.splitext(image.name)[1]
                unique_filename = f"{uuid.uuid4().hex}{file_extension}"
                image_path = os.path.join("uploads", unique_filename)

                with open(image_path, "wb") as file:
                    file.write(image.getbuffer())

            # Save report to database
            add_report(
                report_type=report_type_value,
                item_name=item_name,
                category="General",
                description=description,
                location=location,
                date_reported=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                image_path=image_path,
                contact=""
            )

            # Show success message
            st.success("✅ Report submitted successfully and saved to the database!")

# ============================================================
# MATCHES
# ============================================================

elif st.session_state.page == "Matches":

    st.markdown("""
<div class="hero">
<div class="eyebrow">SMART MATCHING</div>

<div class="hero-title">
Potential <span class="accent">Matches</span>
</div>

<div class="hero-description">
Possible matches between lost and found reports.
</div>

</div>
""", unsafe_allow_html=True)

    # Get all reports from database
    reports = get_reports()

    # If there are no reports
    if not reports:
        st.info(
            "No reports available yet. Submit a lost or found item "
            "to start finding matches."
        )

    else:

        # Separate Lost and Found reports
        lost_reports = [
            report for report in reports
            if report[1] == "Lost"
        ]

        found_reports = [
            report for report in reports
            if report[1] == "Found"
        ]

        matches = []

        # Compare Lost reports with Found reports
        for lost in lost_reports:

            for found in found_reports:

                score = 0

                # CLIP image similarity
                if lost[7] and found[7]:
                  image_score = compare_images(lost[7], found[7])
                  score += image_score * 0.3

                # Item name similarity
                lost_name = lost[2].lower()
                found_name = found[2].lower()

                if lost_name in found_name or found_name in lost_name:
                    score += 25

                # Description similarity
                lost_description = (lost[4] or "").lower()
                found_description = (found[4] or "").lower()

                lost_words = set(lost_description.split())
                found_words = set(found_description.split())

                common_words = lost_words.intersection(found_words)

                if common_words:
                    score += min(len(common_words) * 10, 30)

                # Location similarity
                lost_location = (lost[5] or "").lower()
                found_location = (found[5] or "").lower()

                if (
                    lost_location
                    and found_location
                    and (
                        lost_location in found_location
                        or found_location in lost_location
                    )
                ):
                    score += 20

                # Only show reasonably good matches
                if score >= 50:
                    matches.append(
                        {
                            "lost": lost,
                            "found": found,
                            "score": score
                        }
                    )

        # Display matches
        if matches:

            st.subheader("🎯 Possible Matches")

            for match in matches:

                lost = match["lost"]
                found = match["found"]
                score = match["score"]

                st.markdown("---")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 🔴 Lost Item")

                    if lost[7]:
                      st.image(lost[7], caption="Lost item photo", use_container_width=True)

                    st.write(f"**Item:** {lost[2]}")
                    st.write(f"**Description:** {lost[4]}")
                    st.write(f"**Location:** {lost[5]}")


                with col2:
                    st.markdown("### 🟢 Found Item")

                    if found[7]:
                      st.image(found[7], caption="Found item photo", use_container_width=True)

                    st.write(f"**Item:** {found[2]}")
                    st.write(f"**Description:** {found[4]}")
                    st.write(f"**Location:** {found[5]}")

                st.progress(
                    min(score / 100, 1.0),
                    text=f"Match confidence: {score}%"
                )

        else:

            st.info(
                "No possible matches found yet. "
                "Try submitting both a lost and a found report "
                "with similar item details."
            )
# ============================================================
# ABOUT
# ============================================================
elif st.session_state.page == "About":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">ABOUT THE PROJECT</div>
        <div class="hero-title">
            Built for <span class="accent">campus.</span>
        </div>
        <div class="hero-description">
            Smart Lost &amp; Found is an AI-powered platform designed
            to make reporting and recovering lost belongings easier for students.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-shell">
        <div class="card-label">OUR PURPOSE</div>
        <div class="card-title">Find it. Return it. Together.</div>
        <div class="card-text">
            Instead of relying on notice boards, WhatsApp groups, or manually
            searching through lost-and-found reports, the platform aims to use
            image and information matching to identify belongings and connect
            them with their owners.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    Smart Lost &amp; Found · AI-powered campus community platform
</div>
""", unsafe_allow_html=True)