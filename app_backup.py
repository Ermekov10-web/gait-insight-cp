import streamlit as st
import pandas as pd
import plotly.express as px
from modules.gait_3d import show_gait_3d

from modules.data_loader import (
    load_gait_csv,
    validate_gait_data,
    get_data_summary
)
from modules.report_generator import generate_medical_report


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="NeuroKinetics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# TRANSLATIONS
# ==================================================

T = {
    "Русский": {
        "portal": "Выберите кабинет",
        "doctor": "Врач",
        "family": "Пациент / Родитель",
        "navigation": "Навигация",
        "overview": "Обзор",
        "gait": "Анализ походки",
        "patients": "Участники исследования",
        "weekly": "Еженедельный мониторинг",
        "ai": "ИИ-ассистент",
        "experts": "Мнения экспертов",
        "dashboard": "Моя панель",
        "progress": "Мой прогресс",
        "exercises": "Мои упражнения",
        "welcome": "Интеллектуальный анализ движений",
        "subtitle": "Объединяем нейронауку, биомеханику и искусственный интеллект.",
        "clinical": "Клинический обзор",
        "participants": "Участники исследования",
        "conditions": "Условия исследования",
        "engine": "Аналитическая система",
        "workspace": "Рабочая область",
        "upload": "Загрузить CSV-файлы",
        "upload_help": "Выберите файлы с параметрами походки.",
        "uploaded": "Загруженные данные",
        "no_data": "Пока нет загруженных данных.",
        "coming": "Этот раздел находится в разработке.",
        "analysis": "Результаты анализа",
        "condition": "Условие исследования",
        "all": "Все условия",
        "metric": "Показатель",
        "compare": "Сравнение условий",
        "summary": "Сводная статистика",
        "missing": "Пропущенные значения",
        "rows": "Количество строк",
        "columns": "Количество столбцов",
        "numeric": "Числовые показатели",
        "download": "Скачать сводный отчёт",
        "valid": "Данные успешно проверены",
        "disclaimer": "NeuroKinetics — платформа поддержки исследований и реабилитации. Она не ставит диагнозы и не заменяет решения медицинских специалистов.",
        "individual": "Индивидуальный анализ участника",
        "participant": "Выберите участника",
        "side": "Сторона",
        "left": "Левая (LEFT)",
        "right": "Правая (RIGHT)",
        "individual_empty": "Для выбранного участника нет данных.",
        "individual_missing": "Для анализа нужны Participant_ID и Study_Side.",
        "baseline_change": "Изменение относительно Baseline (%)",
        "asymmetry": "Анализ асимметрии походки",
        "side_comparison": "Сравнение левой и правой стороны",
        "asymmetry_percent": "Асимметрия (%)",
        "asymmetry_missing": "Для сравнения нужны данные LEFT и RIGHT.",
        "asymmetry_note": "Процентная разница является описательной метрикой и сама по себе не устанавливает нарушение походки или диагноз.",
        "no_numeric": "В загруженных таблицах нет числовых показателей.",
        "pdf_report": "PDF-отчёт участника",
        "download_pdf": "Скачать PDF-отчёт"
    },

    "Қазақша": {
        "portal": "Кабинетті таңдаңыз",
        "doctor": "Дәрігер",
        "family": "Пациент / Ата-ана",
        "navigation": "Навигация",
        "overview": "Шолу",
        "gait": "Жүрісті талдау",
        "patients": "Зерттеуге қатысушылар",
        "weekly": "Апталық мониторинг",
        "ai": "ЖИ көмекшісі",
        "experts": "Сарапшылар пікірі",
        "dashboard": "Менің панелім",
        "progress": "Менің прогресім",
        "exercises": "Менің жаттығуларым",
        "welcome": "Қозғалысты интеллектуалды талдау",
        "subtitle": "Нейроғылымды, биомеханиканы және жасанды интеллектіні біріктіреміз.",
        "clinical": "Клиникалық шолу",
        "participants": "Зерттеуге қатысушылар",
        "conditions": "Зерттеу жағдайлары",
        "engine": "Талдау жүйесі",
        "workspace": "Жұмыс кеңістігі",
        "upload": "CSV файлдарын жүктеу",
        "upload_help": "Жүріс параметрлері бар файлдарды таңдаңыз.",
        "uploaded": "Жүктелген деректер",
        "no_data": "Әзірге деректер жүктелмеген.",
        "coming": "Бұл бөлім әзірлену үстінде.",
        "analysis": "Талдау нәтижелері",
        "condition": "Зерттеу жағдайы",
        "all": "Барлық жағдайлар",
        "metric": "Көрсеткіш",
        "compare": "Жағдайларды салыстыру",
        "summary": "Жалпы статистика",
        "missing": "Жетіспейтін мәндер",
        "rows": "Жолдар саны",
        "columns": "Бағандар саны",
        "numeric": "Сандық көрсеткіштер",
        "download": "Есепті жүктеу",
        "valid": "Деректер сәтті тексерілді",
        "disclaimer": "NeuroKinetics — зерттеу және оңалтуға арналған қолдау платформасы. Ол диагноз қоймайды және медицина мамандарының шешімдерін алмастырмайды.",
        "individual": "Қатысушының жеке талдауы",
        "participant": "Қатысушыны таңдаңыз",
        "side": "Зерттеу жағы",
        "left": "Сол жақ (LEFT)",
        "right": "Оң жақ (RIGHT)",
        "individual_empty": "Таңдалған қатысушы үшін деректер жоқ.",
        "individual_missing": "Жеке талдау үшін Participant_ID және Study_Side бағандары қажет.",
        "baseline_change": "Baseline көрсеткішінен өзгеріс (%)",
        "asymmetry": "Жүріс асимметриясын талдау",
        "side_comparison": "Сол және оң жақты салыстыру",
        "asymmetry_percent": "Асимметрия (%)",
        "asymmetry_missing": "Салыстыру үшін LEFT және RIGHT деректері қажет.",
        "asymmetry_note": "Пайыздық айырмашылық сипаттамалық көрсеткіш болып табылады және өздігінен диагноз қоймайды.",
        "no_numeric": "Жүктелген кестелерде сандық көрсеткіштер жоқ.",
        "pdf_report": "Қатысушының PDF есебі",
        "download_pdf": "PDF есебін жүктеу"
    },

    "English": {
        "portal": "Select portal",
        "doctor": "Doctor",
        "family": "Patient / Parent",
        "navigation": "Navigation",
        "overview": "Overview",
        "gait": "Gait Analysis",
        "patients": "Study Participants",
        "weekly": "Weekly Monitoring",
        "ai": "AI Assistant",
        "experts": "Expert Voices",
        "dashboard": "My Dashboard",
        "progress": "My Progress",
        "exercises": "My Exercises",
        "welcome": "Intelligent Movement Analysis",
        "subtitle": "Connecting neuroscience, biomechanics and artificial intelligence.",
        "clinical": "Clinical Overview",
        "participants": "Research Participants",
        "conditions": "Study Conditions",
        "engine": "Analysis System",
        "workspace": "Workspace",
        "upload": "Upload CSV files",
        "upload_help": "Select files containing gait measurements.",
        "uploaded": "Uploaded Data",
        "no_data": "No data has been uploaded yet.",
        "coming": "This section is under development.",
        "analysis": "Analysis Results",
        "condition": "Study Condition",
        "all": "All conditions",
        "metric": "Measurement",
        "compare": "Condition Comparison",
        "summary": "Data Summary",
        "missing": "Missing values",
        "rows": "Rows",
        "columns": "Columns",
        "numeric": "Numeric measurements",
        "download": "Download summary report",
        "valid": "Data validated successfully",
        "disclaimer": "NeuroKinetics is a research and rehabilitation support platform. It does not diagnose conditions or replace clinical decisions.",
        "individual": "Individual participant analysis",
        "participant": "Select participant",
        "side": "Study side",
        "left": "Left (LEFT)",
        "right": "Right (RIGHT)",
        "individual_empty": "No data for the selected participant.",
        "individual_missing": "Individual analysis requires Participant_ID and Study_Side columns.",
        "baseline_change": "Change relative to Baseline (%)",
        "asymmetry": "Gait Asymmetry Analysis",
        "side_comparison": "Left and right side comparison",
        "asymmetry_percent": "Asymmetry (%)",
        "asymmetry_missing": "LEFT and RIGHT data are required for comparison.",
        "asymmetry_note": "Percentage difference is a descriptive measure and does not independently establish a gait disorder or diagnosis.",
        "no_numeric": "No numeric measurements found in uploaded tables.",
        "pdf_report": "Participant PDF report",
        "download_pdf": "Download PDF report"
    }
}


# ==================================================
# DESIGN
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

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
    color: white !important;
}

.hero {
    background: linear-gradient(120deg, #123B2B, #26764E);
    padding: 38px;
    border-radius: 22px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 38px;
}

.hero p {
    color: #D5EBD9;
}

.metric-card {
    background: white;
    border: 1px solid #E2EBE1;
    border-radius: 18px;
    padding: 22px;
    min-height: 120px;
}

.metric-label {
    color: #718276;
    font-size: 14px;
}

.metric-value {
    color: #123B2B;
    font-size: 30px;
    font-weight: 700;
    margin-top: 8px;
}

div.stButton > button {
    background: #26764E;
    color: white;
    border-radius: 10px;
    border: none;
}

[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #E2EBE1;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("# 🧠 NeuroKinetics")
    st.caption("AI NEUROREHABILITATION")
    st.divider()

    language = st.selectbox(
        "🌐 Language",
        ["Русский", "Қазақша", "English"]
    )

    tr = T[language]

    st.divider()

    role = st.radio(
        tr["portal"],
        [tr["doctor"], tr["family"]]
    )

    st.divider()

    if role == tr["doctor"]:

        pages = [
            tr["overview"],
            tr["gait"],
            tr["patients"],
            tr["weekly"],
            tr["ai"],
            tr["experts"]
        ]

    else:

        pages = [
            tr["dashboard"],
            tr["progress"],
            tr["exercises"],
            tr["ai"],
            tr["experts"]
        ]

    page = st.radio(tr["navigation"], pages)

    st.divider()
    st.caption("NeuroKinetics v2.1")


# ==================================================
# HEADER
# ==================================================

st.markdown(f"""
<div class="hero">
    <h1>🧠 NeuroKinetics</h1>
    <h3>{tr["welcome"]}</h3>
    <p>{tr["subtitle"]}</p>
</div>
""", unsafe_allow_html=True)


# ==================================================
# SESSION DATA
# ==================================================

if "gait_data" not in st.session_state:
    st.session_state.gait_data = {}


# ==================================================
# CONDITION DETECTION
# ==================================================

def detect_condition(filename):

    name = filename.lower()

    if "baseline" in name:
        return "Baseline"

    if "verbal" in name:
        return "Verbal"

    if "vr" in name:
        return "VR"

    return "Unknown"


# ==================================================
# DOCTOR PORTAL
# ==================================================

if role == tr["doctor"]:

    # ----------------------------------------------
    # OVERVIEW
    # ----------------------------------------------

    if page == tr["overview"]:

        st.header(tr["clinical"])

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{tr["participants"]}</div>
                <div class="metric-value">29</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{tr["conditions"]}</div>
                <div class="metric-value">03</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{tr["engine"]}</div>
                <div class="metric-value">AI</div>
            </div>
            """, unsafe_allow_html=True)

        st.subheader(tr["workspace"])

        st.info("Baseline / Verbal / VR")


    # ----------------------------------------------
    # GAIT ANALYSIS
    # ----------------------------------------------

    elif page == tr["gait"]:

        st.header(tr["gait"])
        st.write(tr["upload_help"])

        files = st.file_uploader(
            tr["upload"],
            type=["csv"],
            accept_multiple_files=True,
            key="gait_upload"
        )

        if files:

            for file in files:

                condition = detect_condition(file.name)

                try:

                    df = load_gait_csv(file)

                    valid, message = validate_gait_data(df)

                    if not valid:
                        st.error(f"{file.name}: {message}")
                        continue

                    st.session_state.gait_data[file.name] = {
                        "condition": condition,
                        "data": df
                    }

                    st.success(
                        f"{file.name}: {tr['valid']}"
                    )

                    summary = get_data_summary(df)

                    st.subheader(file.name)

                    m1, m2, m3 = st.columns(3)

                    m1.metric(tr["rows"], summary["rows"])
                    m2.metric(tr["columns"], summary["columns"])
                    m3.metric(tr["missing"], summary["missing_values"])

                    st.caption(
                        f"{tr['condition']}: {condition}"
                    )

                    with st.expander(tr["uploaded"]):

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

                        st.write(
                            tr["numeric"],
                            summary["numeric_columns"]
                        )

                except Exception as error:

                    st.error(f"{file.name}: {error}")

        else:

            st.info(tr["no_data"])


        # ------------------------------------------
        # COMPARISON
        # ------------------------------------------

        if st.session_state.gait_data:

            st.divider()
            st.header(tr["analysis"])

            condition_options = [
                "Baseline",
                "Verbal",
                "VR"
            ]

            available = list(dict.fromkeys(
                item["condition"]
                for item in st.session_state.gait_data.values()
                if item["condition"] in condition_options
            ))

            if available:

                selected_condition = st.selectbox(
                    tr["condition"],
                    [tr["all"]] + available
                )

                frames = []

                for filename, item in st.session_state.gait_data.items():

                    if (
                        selected_condition != tr["all"]
                        and item["condition"] != selected_condition
                    ):
                        continue

                    current = item["data"].copy()
                    current["Condition"] = item["condition"]
                    current["Source file"] = filename

                    frames.append(current)

                if frames:

                    combined = pd.concat(
                        frames,
                        ignore_index=True,
                        sort=False
                    )

                    numeric_columns = combined.select_dtypes(
                        include="number"
                    ).columns.tolist()

                    if numeric_columns:

                        selected_metric = st.selectbox(
                            tr["metric"],
                            numeric_columns
                        )

                        comparison = (
                            combined.groupby("Condition")[selected_metric]
                            .agg(["mean", "median", "std", "count"])
                            .reset_index()
                        )

                        st.subheader(tr["compare"])

                        st.dataframe(
                            comparison,
                            use_container_width=True
                        )

                        fig = px.bar(
                            comparison,
                            x="Condition",
                            y="mean",
                            error_y="std",
                            color="Condition",
                            title=selected_metric,
                            color_discrete_sequence=[
                                "#123B2B",
                                "#26764E",
                                "#8ABF9B"
                            ]
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                        st.caption(
                            "Средние значения описывают загруженные данные. "
                            "Они не являются клиническим заключением."
                        )


                        # ----------------------------------
                        # INDIVIDUAL PARTICIPANT ANALYSIS
                        # ----------------------------------

                        st.divider()
                        st.subheader(tr["individual"])

                        individual_frames = []

                        for uploaded_item in st.session_state.gait_data.values():

                            if uploaded_item["condition"] in condition_options:

                                participant_data = uploaded_item["data"].copy()
                                participant_data["Condition"] = uploaded_item["condition"]

                                individual_frames.append(participant_data)

                        if individual_frames:

                            individual_all = pd.concat(
                                individual_frames,
                                ignore_index=True,
                                sort=False
                            )

                            required_columns = {
                                "Participant_ID",
                                "Study_Side"
                            }

                            if required_columns.issubset(individual_all.columns):

                                participant_ids = sorted(
                                    individual_all["Participant_ID"]
                                    .dropna()
                                    .astype(str)
                                    .unique()
                                )

                                if participant_ids:

                                    # Defaults for PDF report
                                    individual_table = pd.DataFrame(
                                        columns=["Condition", "Value"]
                                    )

                                    report_asymmetry = pd.DataFrame(
                                        columns=[
                                            "Condition",
                                            "LEFT",
                                            "RIGHT",
                                            "Asymmetry (%)"
                                        ]
                                    )

                                    participant_col, side_col = st.columns(2)

                                    with participant_col:

                                        chosen_participant = st.selectbox(
                                            tr["participant"],
                                            participant_ids,
                                            key="individual_participant"
                                        )

                                    with side_col:

                                        chosen_side_label = st.selectbox(
                                            tr["side"],
                                            [tr["left"], tr["right"]],
                                            key="individual_side"
                                        )

                                    chosen_side = (
                                        "LEFT"
                                        if chosen_side_label == tr["left"]
                                        else "RIGHT"
                                    )

                                    individual_rows = individual_all[
                                        (
                                            individual_all["Participant_ID"].astype(str)
                                            == chosen_participant
                                        )
                                        & (
                                            individual_all["Study_Side"]
                                            .astype(str)
                                            .str.upper()
                                            == chosen_side
                                        )
                                    ].copy()

                                    condition_order = [
                                        "Baseline",
                                        "Verbal",
                                        "VR"
                                    ]

                                    individual_summary = (
                                        individual_rows
                                        .groupby("Condition")[selected_metric]
                                        .mean()
                                        .reindex(condition_order)
                                        .dropna()
                                    )

                                    if not individual_summary.empty:

                                        individual_table = (
                                            individual_summary
                                            .rename("Value")
                                            .rename_axis("Condition")
                                            .reset_index()
                                        )

                                        st.markdown(
                                            f"**{chosen_participant} · {chosen_side}**"
                                        )

                                        st.dataframe(
                                            individual_table,
                                            use_container_width=True,
                                            hide_index=True
                                        )

                                        individual_chart = px.bar(
                                            individual_table,
                                            x="Condition",
                                            y="Value",
                                            color="Condition",
                                            title=selected_metric,
                                            color_discrete_sequence=[
                                                "#123B2B",
                                                "#26764E",
                                                "#8ABF9B"
                                            ]
                                        )

                                        st.plotly_chart(
                                            individual_chart,
                                            use_container_width=True
                                        )

                                        if "Baseline" in individual_summary.index:

                                            baseline_value = float(
                                                individual_summary.loc["Baseline"]
                                            )

                                            if baseline_value != 0:

                                                percent_change = (
                                                    (
                                                        individual_summary
                                                        - baseline_value
                                                    )
                                                    / abs(baseline_value)
                                                ) * 100

                                                change_table = (
                                                    percent_change
                                                    .rename("Change (%)")
                                                    .rename_axis("Condition")
                                                    .reset_index()
                                                )

                                                st.markdown(
                                                    f"**{tr['baseline_change']}**"
                                                )

                                                st.dataframe(
                                                    change_table,
                                                    use_container_width=True,
                                                    hide_index=True
                                                )

                                    else:

                                        st.info(tr["individual_empty"])


                                    # ----------------------------------
                                    # GAIT ASYMMETRY ANALYSIS
                                    # ----------------------------------

                                    st.divider()
                                    st.subheader(tr["asymmetry"])

                                    asymmetry_data = individual_all[
                                        individual_all["Participant_ID"].astype(str)
                                        == chosen_participant
                                    ].copy()

                                    asymmetry_data["Study_Side"] = (
                                        asymmetry_data["Study_Side"]
                                        .astype(str)
                                        .str.upper()
                                    )

                                    side_comparison = (
                                        asymmetry_data[
                                            asymmetry_data["Study_Side"].isin(
                                                ["LEFT", "RIGHT"]
                                            )
                                        ]
                                        .groupby(
                                            ["Condition", "Study_Side"]
                                        )[selected_metric]
                                        .mean()
                                        .unstack()
                                    )

                                    if {"LEFT", "RIGHT"}.issubset(
                                        side_comparison.columns
                                    ):

                                        side_comparison = side_comparison.dropna(
                                            subset=["LEFT", "RIGHT"]
                                        )

                                        side_comparison["Difference"] = (
                                            side_comparison["LEFT"]
                                            - side_comparison["RIGHT"]
                                        )

                                        side_comparison["Absolute difference"] = (
                                            side_comparison["Difference"].abs()
                                        )

                                        denominator = (
                                            (
                                                side_comparison["LEFT"]
                                                + side_comparison["RIGHT"]
                                            ) / 2
                                        ).abs()

                                        side_comparison["Asymmetry (%)"] = (
                                            side_comparison["Absolute difference"]
                                            .div(denominator.where(denominator != 0))
                                            * 100
                                        )

                                        report_asymmetry = side_comparison.reset_index()[
                                            [
                                                "Condition",
                                                "LEFT",
                                                "RIGHT",
                                                "Asymmetry (%)"
                                            ]
                                        ].copy()

                                        st.markdown(
                                            f"**{tr['side_comparison']}**"
                                        )

                                        st.dataframe(
                                            side_comparison.reset_index(),
                                            use_container_width=True,
                                            hide_index=True
                                        )

                                        chart_data = (
                                            side_comparison[
                                                ["LEFT", "RIGHT"]
                                            ]
                                            .reset_index()
                                            .melt(
                                                id_vars="Condition",
                                                var_name="Side",
                                                value_name="Value"
                                            )
                                        )

                                        asymmetry_chart = px.bar(
                                            chart_data,
                                            x="Condition",
                                            y="Value",
                                            color="Side",
                                            barmode="group",
                                            title=selected_metric,
                                            color_discrete_sequence=[
                                                "#26764E",
                                                "#8ABF9B"
                                            ]
                                        )

                                        st.plotly_chart(
                                            asymmetry_chart,
                                            use_container_width=True
                                        )

                                        st.caption(
                                            tr["asymmetry_note"]
                                        )

                                    else:

                                        st.info(tr["asymmetry_missing"])


                                    # ----------------------------------
                                    # PDF REPORT
                                    # ----------------------------------

                                    st.divider()
                                    st.subheader(tr["pdf_report"])

                                    try:

                                        pdf_report = generate_medical_report(
                                            participant_id=chosen_participant,
                                            metric=selected_metric,
                                            individual_data=individual_table,
                                            asymmetry_data=report_asymmetry
                                        )

                                        st.download_button(
                                            label=tr["download_pdf"],
                                            data=pdf_report.getvalue(),
                                            file_name=(
                                                f"NeuroKinetics_"
                                                f"{chosen_participant}_report.pdf"
                                            ),
                                            mime="application/pdf",
                                            key="download_individual_pdf"
                                        )

                                    except Exception as error:

                                        st.error(
                                            f"Не удалось создать PDF: {error}"
                                        )

                                else:

                                    st.info(tr["individual_empty"])

                            else:

                                st.warning(tr["individual_missing"])


                        # ----------------------------------
                        # DOWNLOAD SUMMARY
                        # ----------------------------------

                        report = comparison.to_csv(
                            index=False
                        ).encode("utf-8-sig")

                        st.download_button(
                            tr["download"],
                            data=report,
                            file_name="neurokinetics_summary.csv",
                            mime="text/csv"
                        )

                    else:

                        st.warning(tr["no_numeric"])


    # ----------------------------------------------
    # OTHER DOCTOR PAGES
    # ----------------------------------------------

    else:

        st.header(page)
        st.info(tr["coming"])


# ==================================================
# PATIENT / PARENT PORTAL
# ==================================================

else:

    if page == tr["dashboard"]:

        st.header(tr["dashboard"])

        st.info(
            "Здесь будут отображаться данные, "
            "одобренные медицинским специалистом."
        )

    elif page == tr["progress"]:

        st.header(tr["progress"])
        st.info(tr["coming"])

    elif page == tr["exercises"]:

        st.header(tr["exercises"])
        st.info(tr["coming"])

    else:

        st.header(page)
        st.info(tr["coming"])


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(tr["disclaimer"])