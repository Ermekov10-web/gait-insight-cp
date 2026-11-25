
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="NeuroKinetics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# TRANSLATIONS
# ==========================================

TRANSLATIONS = {
    "Русский": {
        "language": "Язык",
        "portal": "Выберите кабинет",
        "doctor": "Врач",
        "family": "Пациент / Родитель",
        "navigation": "Навигация",
        "overview": "Главная панель",
        "analysis": "Анализ походки",
        "patients": "Пациенты",
        "monitoring": "Мониторинг",
        "assistant": "AI-помощник",
        "experts": "Мнения экспертов",
        "dashboard": "Моя панель",
        "progress": "Мой прогресс",
        "exercises": "Мои упражнения",
        "welcome": "Интеллектуальная платформа нейрореабилитации",
        "subtitle": "Объединяем нейронауку, биомеханику и искусственный интеллект.",
        "clinical": "Клиническая панель",
        "participants": "Участники исследования",
        "conditions": "Условия исследования",
        "engine": "AI-система",
        "workspace": "Рабочее пространство",
        "upload": "Загрузить CSV-файлы",
        "baseline": "Baseline",
        "verbal": "Verbal",
        "vr": "VR",
        "choose_file": "Выберите CSV-файл",
        "data_preview": "Предварительный просмотр данных",
        "data_summary": "Сводка данных",
        "rows": "Строки",
        "columns": "Столбцы",
        "missing": "Пропущенные значения",
        "chart": "Визуализация данных",
        "select_column": "Выберите показатель",
        "select_patient": "Выберите участника",
        "monitor_title": "Еженедельный мониторинг",
        "monitor_text": "Здесь будут отображаться наблюдения и обновления прогресса.",
        "exercise_title": "Назначенные упражнения",
        "exercise_text": "Просматривайте активности, одобренные вашим специалистом.",
        "ai_title": "AI-помощник NeuroKinetics",
        "ai_text": "Задайте вопрос о работе платформы или загруженных данных.",
        "ask": "Введите ваш вопрос",
        "send": "Отправить",
        "expert_title": "Expert Voices",
        "expert_text": "Научные материалы, мнения специалистов и интервью.",
        "progress_title": "Мой прогресс",
        "progress_text": "Отслеживайте еженедельные наблюдения.",
        "disclaimer": "Платформа не ставит диагнозы и не заменяет медицинских специалистов.",
        "no_data": "Сначала загрузите CSV-файл.",
        "success": "Файл успешно загружен.",
        "select_page": "Выберите раздел в меню слева."
    },

    "Қазақша": {
        "language": "Тіл",
        "portal": "Кабинетті таңдаңыз",
        "doctor": "Дәрігер",
        "family": "Пациент / Ата-ана",
        "navigation": "Навигация",
        "overview": "Басты панель",
        "analysis": "Жүрісті талдау",
        "patients": "Пациенттер",
        "monitoring": "Мониторинг",
        "assistant": "AI-көмекші",
        "experts": "Сарапшылар пікірі",
        "dashboard": "Менің панелім",
        "progress": "Менің прогресім",
        "exercises": "Менің жаттығуларым",
        "welcome": "Нейрореабилитацияға арналған интеллектуалды платформа",
        "subtitle": "Нейроғылым, биомеханика және жасанды интеллектті біріктіреміз.",
        "clinical": "Клиникалық панель",
        "participants": "Зерттеуге қатысушылар",
        "conditions": "Зерттеу шарттары",
        "engine": "AI жүйесі",
        "workspace": "Жұмыс кеңістігі",
        "upload": "CSV файлдарын жүктеу",
        "baseline": "Baseline",
        "verbal": "Verbal",
        "vr": "VR",
        "choose_file": "CSV файлын таңдаңыз",
        "data_preview": "Деректерді алдын ала қарау",
        "data_summary": "Деректер қорытындысы",
        "rows": "Жолдар",
        "columns": "Бағандар",
        "missing": "Жетіспейтін мәндер",
        "chart": "Деректер визуализациясы",
        "select_column": "Көрсеткішті таңдаңыз",
        "select_patient": "Қатысушыны таңдаңыз",
        "monitor_title": "Апталық мониторинг",
        "monitor_text": "Мұнда бақылаулар мен прогресс жаңартулары көрсетіледі.",
        "exercise_title": "Тағайындалған жаттығулар",
        "exercise_text": "Маман мақұлдаған жаттығуларды қараңыз.",
        "ai_title": "NeuroKinetics AI-көмекшісі",
        "ai_text": "Платформа немесе жүктелген деректер туралы сұрақ қойыңыз.",
        "ask": "Сұрағыңызды енгізіңіз",
        "send": "Жіберу",
        "expert_title": "Expert Voices",
        "expert_text": "Ғылыми материалдар, мамандар пікірі және сұхбаттар.",
        "progress_title": "Менің прогресім",
        "progress_text": "Апталық бақылауларды қадағалаңыз.",
        "disclaimer": "Платформа диагноз қоймайды және дәрігерді алмастырмайды.",
        "no_data": "Алдымен CSV файлын жүктеңіз.",
        "success": "Файл сәтті жүктелді.",
        "select_page": "Сол жақ мәзірден бөлімді таңдаңыз."
    },

    "English": {
        "language": "Language",
        "portal": "Select portal",
        "doctor": "Doctor",
        "family": "Patient / Parent",
        "navigation": "Navigation",
        "overview": "Overview",
        "analysis": "Gait Analysis",
        "patients": "Patients",
        "monitoring": "Monitoring",
        "assistant": "AI Assistant",
        "experts": "Expert Voices",
        "dashboard": "My Dashboard",
        "progress": "My Progress",
        "exercises": "My Exercises",
        "welcome": "Intelligent Neurorehabilitation Platform",
        "subtitle": "Connecting neuroscience, biomechanics and artificial intelligence.",
        "clinical": "Clinical Dashboard",
        "participants": "Research Participants",
        "conditions": "Study Conditions",
        "engine": "AI System",
        "workspace": "Workspace",
        "upload": "Upload CSV Files",
        "baseline": "Baseline",
        "verbal": "Verbal",
        "vr": "VR",
        "choose_file": "Choose CSV file",
        "data_preview": "Data Preview",
        "data_summary": "Data Summary",
        "rows": "Rows",
        "columns": "Columns",
        "missing": "Missing Values",
        "chart": "Data Visualization",
        "select_column": "Select metric",
        "select_patient": "Select participant",
        "monitor_title": "Weekly Monitoring",
        "monitor_text": "Observations and progress updates will appear here.",
        "exercise_title": "Assigned Exercises",
        "exercise_text": "View activities approved by your clinician.",
        "ai_title": "NeuroKinetics AI Assistant",
        "ai_text": "Ask a question about the platform or uploaded data.",
        "ask": "Enter your question",
        "send": "Send",
        "expert_title": "Expert Voices",
        "expert_text": "Scientific resources, professional opinions and interviews.",
        "progress_title": "My Progress",
        "progress_text": "Follow your weekly observations.",
        "disclaimer": "This platform does not diagnose conditions or replace medical professionals.",
        "no_data": "Upload a CSV file first.",
        "success": "File uploaded successfully.",
        "select_page": "Select a section from the sidebar."
    }
}

# ==========================================
# SESSION STATE
# ==========================================

if "language" not in st.session_state:
    st.session_state.language = "Русский"

if "role" not in st.session_state:
    st.session_state.role = "Врач"

if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

language = st.session_state.language
t = TRANSLATIONS[language]

# ==========================================
# DESIGN
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #F3F7F1;
    color: #172820;
}

[data-testid="stSidebar"] {
    background: #123B2B;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] {
    background: white;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #172820 !important;
}

.hero {
    background: linear-gradient(120deg, #123B2B, #26764E);
    padding: 40px;
    border-radius: 24px;
    color: white;
    margin-bottom: 28px;
}

.hero h1 {
    font-size: 42px;
    font-weight: 800;
    margin: 0;
}

.hero p {
    color: #D5EBD9;
    font-size: 16px;
}

.metric-card {
    background: white;
    border: 1px solid #E2EBE1;
    border-radius: 18px;
    padding: 23px;
    min-height: 125px;
}

.metric-label {
    color: #718276;
    font-size: 14px;
}

.metric-value {
    color: #123B2B;
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}

.section-title {
    color: #123B2B;
    font-size: 24px;
    font-weight: 700;
    margin: 25px 0 15px 0;
}

.stButton > button {
    background: #26764E;
    color: white;
    border: none;
    border-radius: 12px;
    min-height: 42px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #123B2B;
    color: white;
}

div[data-testid="stFileUploader"] {
    background: white;
    border-radius: 15px;
    padding: 15px;
}

div[data-testid="stDataFrame"] {
    background: white;
    border-radius: 15px;
}

.small-note {
    color: #718276;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 🧠 NeuroKinetics")
    st.caption("AI NEUROREHABILITATION")
    st.divider()

    language = st.selectbox(
        "🌐 " + t["language"],
        ["Русский", "Қазақша", "English"],
        key="language"
    )

    t = TRANSLATIONS[language]

    st.divider()

    role = st.radio(
        t["portal"],
        [t["doctor"], t["family"]],
        key="role"
    )

    st.divider()

    if role == t["doctor"]:
        pages = [
            t["overview"],
            t["analysis"],
            t["patients"],
            t["monitoring"],
            t["assistant"],
            t["experts"]
        ]
    else:
        pages = [
            t["dashboard"],
            t["progress"],
            t["exercises"],
            t["assistant"],
            t["experts"]
        ]

    page = st.radio(
        t["navigation"],
        pages
    )

    st.divider()
    st.caption("NeuroKinetics | Version 1.0")

# ==========================================
# HERO
# ==========================================

st.markdown(f"""
<div class="hero">
    <h1>NeuroKinetics</h1>
    <p>{t["welcome"]}</p>
    <p>{t["subtitle"]}</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# DOCTOR OVERVIEW
# ==========================================

if page == t["overview"] or page == t["dashboard"]:

    st.markdown(f"## {t['clinical']}")
    st.caption(t["select_page"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t['participants']}</div>
            <div class="metric-value">29</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t['conditions']}</div>
            <div class="metric-value">03</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t['engine']}</div>
            <div class="metric-value">AI</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="section-title">{t["workspace"]}</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:
        st.info(f"**{t['analysis']}**\n\n{t['upload']}")

    with right:
        st.info(f"**{t['assistant']}**\n\n{t['ai_text']}")

# ==========================================
# GAIT ANALYSIS
# ==========================================

elif page == t["analysis"]:

    st.markdown(f"## {t['analysis']}")

    uploaded_file = st.file_uploader(
        t["choose_file"],
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            df = pd.read_csv(
                uploaded_file,
                sep=";",
                decimal=",",
                na_values=["NaN", "nan", "NA", ""],
                encoding="utf-8-sig"
            )

            df.columns = df.columns.astype(str).str.strip()

            for column in df.columns:
                converted = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )
                if converted.notna().any():
                    df[column] = converted

            st.session_state.uploaded_data = df

            st.success(t["success"])

            st.markdown(f"### {t['data_summary']}")

            c1, c2, c3 = st.columns(3)

            c1.metric(t["rows"], len(df))
            c2.metric(t["columns"], len(df.columns))
            c3.metric(t["missing"], int(df.isna().sum().sum()))

            st.markdown(f"### {t['data_preview']}")
            st.dataframe(df, use_container_width=True)

            numeric_columns = df.select_dtypes(
                include="number"
            ).columns.tolist()

            if numeric_columns:
                st.markdown(f"### {t['chart']}")

                selected_column = st.selectbox(
                    t["select_column"],
                    numeric_columns
                )

                fig = px.line(
                    df,
                    y=selected_column,
                    title=selected_column,
                    template="plotly_white"
                )

                fig.update_traces(
                    line=dict(color="#26764E", width=3)
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.warning("No numeric columns found.")

        except Exception as error:
            st.error(f"CSV loading error: {error}")

    else:
        st.info(t["no_data"])

# ==========================================
# PATIENTS
# ==========================================

elif page == t["patients"]:

    st.markdown(f"## {t['patients']}")
    st.info(
        "Patient records will be connected to a secure database "
        "in the next development stage."
    )

# ==========================================
# MONITORING
# ==========================================

elif page == t["monitoring"]:

    st.markdown(f"## {t['monitor_title']}")
    st.write(t["monitor_text"])

    st.info(
        "Monitoring records are not connected to a database yet. "
        "Clinical review will be required."
    )

# ==========================================
# FAMILY PROGRESS
# ==========================================

elif page == t["progress"]:

    st.markdown(f"## {t['progress_title']}")
    st.write(t["progress_text"])

    st.info(
        "Progress tracking will be connected to clinician-reviewed "
        "monitoring records."
    )

# ==========================================
# FAMILY EXERCISES
# ==========================================

elif page == t["exercises"]:

    st.markdown(f"## {t['exercise_title']}")
    st.write(t["exercise_text"])

    st.warning(
        "Only exercises approved by the treating clinician "
        "should be displayed here."
    )

# ==========================================
# AI ASSISTANT
# ==========================================

elif page == t["assistant"]:

    st.markdown(f"## {t['ai_title']}")
    st.write(t["ai_text"])

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input(t["ask"])

    if prompt:
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.write(prompt)

        answer = (
            "This is the NeuroKinetics assistant interface. "
            "The AI model has not been connected yet. "
            "Clinical questions must be reviewed by a qualified professional."
        )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.write(answer)

# ==========================================
# EXPERT VOICES
# ==========================================

elif page == t["experts"]:

    st.markdown(f"## {t['expert_title']}")
    st.write(t["expert_text"])

    st.info(
        "Scientific publications and verified expert interviews "
        "will be added here after source verification and permission."
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    f'<p class="small-note">NeuroKinetics · {t["disclaimer"]}</p>',
    unsafe_allow_html=True
)
