import streamlit as st

from utils.pdf_reader import extract_text
from utils.gemini import explain_report
from utils.gemini_vision import explain_image
from utils.chat import chat_with_report
from utils.medicine import explain_medicine


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="GeneGuide AI",
    page_icon="🧬",
    layout="wide"
)

# ---------------- SESSION STATE ---------------- #

if "explanation" not in st.session_state:
    st.session_state.explanation = None

if "sections" not in st.session_state:
    st.session_state.sections = {}

if "snapshot" not in st.session_state:
    st.session_state.snapshot = {}

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("🧬 GeneGuide AI")

    st.caption("Your AI Health Assistant")

    st.divider()

    st.subheader("🚀 Features")

    st.markdown("""
🏠 **Home**

📄 **Medical Report Explainer**

🩺 **AI Health Snapshot**

💬 **AI Chat**

💊 **Medicine Explainer**

🌍 **English & Urdu**

🔒 **Secure & Private**
""")

    st.divider()

    st.success("CTRL-V Hackathon 2026")


# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.stApp{
    background:#F8FAFC;
}

/* Headings */

h1{
    color:#5B21B6;
    font-weight:800;
}

h2,h3{
    color:#1E293B;
}

/* Upload Box */

div[data-testid="stFileUploader"]{
    border:3px dashed #C084FC;
    border-radius:20px;
    padding:20px;
    background:white;
}

/* Alerts */

div[data-testid="stAlert"]{
    border-radius:15px;
}

/* Tabs */

.stTabs [data-baseweb="tab-list"]{
    gap:12px;
}

.stTabs [data-baseweb="tab"]{
    background:#F3E8FF;
    color:#6D28D9;
    border-radius:15px;
    padding:12px 22px;
    font-weight:700;
}

.stTabs [aria-selected="true"]{
    background:#A855F7;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO ---------------- #

left, right = st.columns([1.3,1])

with left:

    st.title("🧬 GeneGuide AI")

    st.markdown("## Because Every Patient Deserves to Understand Their Health")

    st.write("""
A medical report should provide clarity—not confusion.

GeneGuide AI transforms complex medical language into simple,
easy-to-understand explanations so patients and families can better
understand their reports without replacing professional medical advice.

🤖 AI-powered explanations

📄 Report analysis

💬 Interactive AI assistant

💊 Medicine explanations

🌍 Multilingual support
""")
 
   

with right:

    st.image(
        "assets/robot.jpg",
        width="stretch"
        
    )

st.divider()
st.info("""
### 🎯 Our Mission

Healthcare information should be understandable by everyone.

GeneGuide AI helps patients better understand their reports,
reducing confusion while encouraging consultation with healthcare professionals.
""")
# ---------------- FEATURE CARDS ---------------- #

c1,c2,c3,c4=st.columns(4)

with c1:
    st.info("📄\n\n**Easy to Understand**")

with c2:
    st.info("🤖\n\n**AI Powered**")

with c3:
    st.info("🔒\n\n**Secure**")

with c4:
    st.info("❤️\n\n**Patient Friendly**")

st.divider()

# ---------------- LANGUAGE ---------------- #

language=st.selectbox(
    "🌍 Choose Explanation Language",
    ["English","Urdu"]
)
st.markdown("## ♿ Accessibility Features")

st.markdown("""
✅ Simple language

✅ English & Urdu

✅ AI explanations

✅ Patient-friendly summaries

✅ Medicine explanations

🔊 Voice Assistant (Coming Soon)
""")
st.divider()

st.markdown("## ⚙️ How GeneGuide AI Works")

step1, step2, step3 = st.columns(3)

with step1:
    st.info("""
### 📤 Step 1

Upload your medical report
(PDF or Image)
""")

with step2:
    st.info("""
### 🤖 Step 2

AI analyzes the report
and explains medical terms.
""")

with step3:
    st.info("""
### ❤️ Step 3

Receive an easy-to-understand
summary with recommendations.
""")
    

st.success("""
🔒 **Privacy First**

Your uploaded medical reports are analyzed only for generating explanations.
GeneGuide AI does not store your personal medical data.
""")    

# ---------------- FILE UPLOADER ---------------- #

st.subheader("📤 Upload Your Medical Report")

st.caption("Supported formats: PDF • PNG • JPG • JPEG • JFIF")

uploaded_file=st.file_uploader(
    "Choose your report",
    type=["pdf","png","jpg","jpeg","jfif"]
)

# ---------------- HELPER FUNCTIONS ---------------- #

def split_sections(text):

    sections={
        "HEALTH SNAPSHOT":"",
        "SUMMARY":"",
        "MEDICAL TERMS":"",
        "QUESTIONS FOR THE DOCTOR":"",
        "NEXT STEPS":"",
        "DISCLAIMER":""
    }

    current=None

    for line in text.splitlines():

        line=line.strip()

        if line.startswith("## HEALTH SNAPSHOT"):
            current="HEALTH SNAPSHOT"
            continue

        elif line.startswith("## SUMMARY"):
            current="SUMMARY"
            continue

        elif line.startswith("## MEDICAL TERMS"):
            current="MEDICAL TERMS"
            continue

        elif line.startswith("## QUESTIONS FOR THE DOCTOR"):
            current="QUESTIONS FOR THE DOCTOR"
            continue

        elif line.startswith("## NEXT STEPS"):
            current="NEXT STEPS"
            continue

        elif line.startswith("## DISCLAIMER"):
            current="DISCLAIMER"
            continue

        if current:
            sections[current]+=line+"\n"

    return sections


def parse_snapshot(snapshot_text):

    data={}

    for line in snapshot_text.splitlines():

        if ":" in line:

            key,value=line.split(":",1)

            data[key.strip()]=value.strip()

    return data
# ---------------- PROCESS REPORT ---------------- #

if uploaded_file:

    st.success("✅ Report uploaded successfully!")

    # ---------- IMAGE PREVIEW ---------- #

    if uploaded_file.type.startswith("image"):

        st.image(
            uploaded_file,
            caption="Uploaded Medical Report",
            width="stretch"
            
        )

    # ---------- PDF PREVIEW ---------- #

    elif uploaded_file.type == "application/pdf":

        text = extract_text(uploaded_file)

        st.subheader("📄 Extracted Report")

        st.text_area(
            "Report Text",
            text,
            height=250
        )

        if "⚠️" in text:

            st.warning(
                "Scanned PDF detected.\n\n"
                "Please upload the report as an image for better AI analysis."
            )

    st.divider()

   # ---------- ANALYZE BUTTON ---------- #

if st.button("🧬 Analyze Report with AI", width="stretch"):

    try:

       with st.spinner(
    "🧠 Reading report... 🔬 Understanding medical terminology... 🤖 Generating patient-friendly explanation..."
):

            if uploaded_file.type == "application/pdf":

                explanation = explain_report(
                    text,
                    language
                )

            else:

                explanation = explain_image(
                    uploaded_file,
                    language
                )

            st.session_state.explanation = explanation

            sections = split_sections(explanation)

            st.session_state.sections = sections

            st.session_state.snapshot = parse_snapshot(
                sections["HEALTH SNAPSHOT"]
            )

    except Exception as e:

        st.exception(e)
        st.stop()

if st.session_state.explanation:

    explanation = st.session_state.explanation
    sections = st.session_state.sections
    snapshot = st.session_state.snapshot

    # Continue with your Report Overview,
    # AI Health Snapshot,
    # Tabs,
    # Download button,
    # AI Chat,
    # Medicine Explainer, etc.        
    # ---------- SHOW RESULTS ---------- #

    if st.session_state.explanation:

        explanation = st.session_state.explanation

        sections = st.session_state.sections

        snapshot = st.session_state.snapshot

        st.success("✅ Report analyzed successfully!")

        st.markdown("## 🩺 AI Health Snapshot")

        left, right = st.columns([1, 2])

        with left:
            st.markdown("**👤 Patient**")
            st.markdown("**🫁 Body Part**")
            st.markdown("**🚨 Risk Level**")
            st.markdown("**📄 Report Type**")
            st.markdown("**🩺 Diagnosis**")
            st.markdown("**👨‍⚕️ Recommended Action**")

        with right:
            st.write(snapshot.get("Patient Name", "N/A"))
            st.write(snapshot.get("Body Part", "N/A"))
            st.write(snapshot.get("Severity", "N/A"))
            st.write(snapshot.get("Report Type", "N/A"))
            st.write(snapshot.get("Diagnosis", "N/A"))
            st.write(snapshot.get("Urgency", "Consult Doctor"))



        st.divider()

        st.subheader("📊 Report Overview")

        o1, o2, o3, o4 = st.columns(4)

        with o1:

            st.metric(
                "📄 File",
                uploaded_file.name
            )

        with o2:

            st.metric(
                "🌍 Language",
                language
            )

        with o3:

            st.metric(
                "🤖 AI Status",
                "Completed"
            )

        with o4:

            st.metric(
                "📑 Format",
                uploaded_file.type.split("/")[-1].upper()
            )

        st.divider()

        # ---------- REPORT TABS ---------- #

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📌 Summary",
            "🩺 Medical Terms",
            "👨‍⚕️ Ask Doctor",
            "🚀 Next Steps",
            "⚠️ Disclaimer"
        ])

        with tab1:

            st.markdown("### 📌 Easy Summary")

            st.info(
                sections["SUMMARY"]
            )

        with tab2:

            st.markdown("### 🩺 Medical Terms")

            st.success(
                sections["MEDICAL TERMS"]
            )

        with tab3:

            st.markdown("### 👨‍⚕️ Questions For Your Doctor")

            st.warning(
                sections["QUESTIONS FOR THE DOCTOR"]
            )

        with tab4:

            st.markdown("### 🚀 Recommended Next Steps")

            st.success(
                sections["NEXT STEPS"]
            )

        with tab5:

            st.markdown("### ⚠️ Important Disclaimer")

            st.error(
                sections["DISCLAIMER"]
            )

        st.download_button(
            "📥 Download AI Report",
            explanation,
            file_name="GeneGuide_AI_Report.txt",
            mime="text/plain",
            width="stretch"
            
        )


# ---------------- AI CHAT ---------------- #

st.divider()

st.subheader("🩺 Personal Health Assistant")

question = st.text_input(
    "Ask anything about your report...",
    key="chat_question"
)

if st.session_state.get("explanation"):

    if st.button("💬 Ask GeneGuide AI", width="stretch"):

        if question.strip():

            with st.spinner("🤖 Thinking..."):

                answer = chat_with_report(
                    st.session_state.explanation,
                    question
                )

            st.success(answer)

else:

    st.info("📄 Upload and analyze a medical report first to chat with GeneGuide AI.")

    st.button(
        "💬 Ask AI",
        disabled=True,
        width="stretch"
        
    )
# ---------------- MEDICINE EXPLAINER ---------------- #

st.divider()

st.subheader("💊 Medicine Explainer")

medicine = st.text_input(
    "Enter medicine name...",
    key="medicine"
)

if st.button("💊 Explain Medicine", width="stretch"):

    if medicine.strip():

        from utils.medicine import explain_medicine

        with st.spinner("💊 Reading medicine information..."):

            result = explain_medicine(medicine)

        st.success(result)

# ---------------- VOICE ASSISTANT ---------------- #

if st.session_state.explanation:

    st.divider()

    st.subheader("🔊 Voice Assistant")

    st.info(
        """
🎤 **Coming Soon!**

GeneGuide AI will soon be able to read your medical report aloud.

This feature is being developed to help:

• 👵 Elderly patients

• 👁️ Visually impaired users

• 📖 Users who prefer listening instead of reading
"""
    )

# ---------------- FOOTER ---------------- #

st.divider()

st.warning(
    "⚠️ GeneGuide AI provides educational information only. "
    "Always consult a qualified healthcare professional before making medical decisions."
)

st.markdown(
    """
    <center>

    <h3>🧬 GeneGuide AI</h3>

    <p>Made with ❤️ to make healthcare information accessible for everyone..</p>

    <p>Empowering patients through accessible AI-powered healthcare explanations. 🧬</p>

    <p><b>CTRL-V Hackathon 2026</b></p>

    </center>
    """,
    unsafe_allow_html=True
)        