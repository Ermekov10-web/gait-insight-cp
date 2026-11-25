
from pathlib import Path
from datetime import date
from io import BytesIO
import os
import json
import urllib.request

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from modules.gait_3d import show_gait_3d
from modules.gait_analysis import load_research_data
from modules.data_loader import load_gait_csv, validate_gait_data


# ==========================================
# NEUROKINETICS 5.0
# ==========================================

st.set_page_config(
    page_title="NeuroKinetics",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "research"

st.markdown("""
<style>
.stApp {
    background: radial-gradient(
        ellipse at top right,
        #174331,
        #081B14 40%,
        #030D09 85%
    );
    color: #E8FFF2;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #071C14;
    border-right: 1px solid #315B47;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stWidgetLabel"] p {
    color: #D7EDE1 !important;
}

h1,h2,h3,h4 {
    color: #EEFFF5 !important;
    letter-spacing: -.6px;
}

.stMarkdown p {
    color: #C8E0D3;
    line-height: 1.7;
}

[data-testid="stCaptionContainer"] p {
    color: #A5C7B5 !important;
}

[data-testid="stMetric"] {
    padding: 22px;
    background: #102D21;
    border: 1px solid #315E47;
    border-radius: 19px;
}

[data-testid="stMetricValue"] {
    color: #81FFC1 !important;
}

[data-testid="stChatMessage"] {
    background: #102C21;
    border: 1px solid #315B47;
    border-radius: 18px;
    padding: 20px;
}

.stButton > button,
.stDownloadButton > button {
    background: #1B4B34;
    color: #EEFFF5;
    border: 1px solid #3B7855;
    border-radius: 12px;
    min-height: 44px;
}

.stButton > button:hover {
    background: #296D48;
    color: white;
    border-color: #78FFB8;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #315B47;
    border-radius: 20px;
}

div[data-baseweb="select"] > div {
    background: #153326;
    border-color: #3B654D;
    color: #EEFFF5;
}

[data-testid="stFileUploaderDropzone"] {
    background: #153326;
    border-color: #3B654D;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1500px;
    padding-top: 2rem;
}

hr {
    border-color: #315B47;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# LANGUAGES
# ==========================================

with st.sidebar:

    st.title("◈ NeuroKinetics")

    language = st.selectbox(
        "🌐 Язык / Тіл / Language",
        ["Русский", "Қазақша", "English"],
        key="nk_language"
    )


def L(ru, kz, en):

    return {
        "Русский": ru,
        "Қазақша": kz,
        "English": en
    }[language]


# ==========================================
# SESSION
# ==========================================

defaults = {
    "nk_chat": [],
    "nk_plan": [],
    "nk_notes": [],
    "nk_measurements": []
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# SCIENTIFIC DATA
# ==========================================

research = load_research_data(str(DATA))

waveforms = research.get("waveforms", {})
discrete = research.get("discrete", {})

CONDITIONS = ["Baseline", "Verbal", "VR"]

CONDITION_NAMES = {
    "Baseline": L(
        "Обычная ходьба",
        "Қалыпты жүріс",
        "Baseline walking"
    ),
    "Verbal": L(
        "Голосовые подсказки",
        "Сөздік нұсқаулар",
        "Verbal feedback"
    ),
    "VR": L(
        "Виртуальные подсказки",
        "Виртуалды нұсқаулар",
        "Virtual feedback"
    )
}

participants = sorted({
    str(value)
    for df in waveforms.values()
    for value in df.get(
        "Participant_ID",
        pd.Series(dtype=str)
    ).dropna()
})

cycles = sum(len(df) for df in waveforms.values())

SOURCE = "https://doi.org/10.48804/JUNNWW"
GUIDELINE = "https://doi.org/10.1111/dmcn.15055"

METRICS = {
    "aSagP": L("Таз", "Жамбас", "Pelvis"),
    "aSagH": L(
        "Тазобедренный сустав",
        "Жамбас буыны",
        "Hip joint"
    ),
    "aSagK": L(
        "Коленный сустав",
        "Тізе буыны",
        "Knee joint"
    ),
    "aSagA": L(
        "Голеностопный сустав",
        "Тобық буыны",
        "Ankle joint"
    )
}


# ==========================================
# DIFFERENT WORKSPACES
# ==========================================

PAGES = {
    "home": L("Главная", "Басты бет", "Home"),
    "analysis": L(
        "Анализ движений",
        "Қозғалысты талдау",
        "Movement analysis"
    ),
    "participants": L(
        "Участники исследования",
        "Зерттеу қатысушылары",
        "Participants"
    ),
    "plan": L(
        "План реабилитации",
        "Оңалту жоспары",
        "Rehabilitation plan"
    ),
    "reports": L(
        "Научные отчёты",
        "Ғылыми есептер",
        "Research reports"
    ),
    "monitor": L(
        "Мониторинг",
        "Мониторинг",
        "Monitoring"
    ),
    "assistant": "NeuroCare AI",
    "experts": L(
        "Мировые специалисты",
        "Әлемдік мамандар",
        "Global experts"
    ),
    "rehab": L(
        "Занятия и упражнения",
        "Жаттығулар",
        "Activities"
    ),
    "calendar": L(
        "Календарь занятий",
        "Жаттығу күнтізбесі",
        "Activity calendar"
    ),
    "progress": L(
        "Мой прогресс",
        "Менің прогресім",
        "My progress"
    ),
    "journal": L(
        "Дневник наблюдений",
        "Бақылау күнделігі",
        "Observation journal"
    ),
    "guide": L(
        "Подготовка к врачу",
        "Дәрігерге дайындық",
        "Medical visit preparation"
    )
}

with st.sidebar:

    st.caption(
        L(
            "За каждым движением — человек.",
            "Әр қозғалыстың артында адам бар.",
            "Behind every movement is a person."
        )
    )

    st.divider()

    role = st.radio(
        L("Ваш кабинет", "Кабинет", "Workspace"),
        ["doctor", "family"],
        format_func=lambda x:
        L(
            "🩺 Специалист",
            "🩺 Маман",
            "🩺 Professional"
        ) if x == "doctor" else L(
            "🤍 Родитель",
            "🤍 Ата-ана",
            "🤍 Parent"
        )
    )

    if role == "doctor":

        pages = [
            "home",
            "analysis",
            "participants",
            "plan",
            "monitor",
            "reports",
            "assistant",
            "experts"
        ]

    else:

        pages = [
            "home",
            "rehab",
            "calendar",
            "progress",
            "journal",
            "assistant",
            "experts",
            "guide"
        ]

    page = st.radio(
        L("Навигация", "Навигация", "Navigation"),
        pages,
        format_func=lambda x: PAGES[x],
        key=f"nk_navigation_{role}"
    )

    st.divider()

    st.caption("NeuroKinetics 5.0")
    st.caption("Developed in Kazakhstan 🇰🇿")


# ==========================================
# HELPERS
# ==========================================

def card(title, description):

    with st.container(border=True):
        st.subheader(title)
        st.write(description)


def choose_participant(key):

    if not participants:
        st.warning(
            L(
                "Исследовательские данные не найдены.",
                "Зерттеу деректері табылмады.",
                "Research data not found."
            )
        )
        return None

    return st.selectbox(
        L(
            "Участник исследования",
            "Зерттеу қатысушысы",
            "Research participant"
        ),
        participants,
        key=key
    )


def gait_curve(df, metric, participant):

    selected = df[
        df["Participant_ID"].astype(str)
        == str(participant)
    ]

    columns = [
        c for c in selected.columns
        if c.startswith(metric + "_pct_GC_")
    ]

    columns.sort(
        key=lambda c: int(c.split("_")[-1])
    )

    if selected.empty or not columns:
        return None

    values = selected[columns].apply(
        pd.to_numeric,
        errors="coerce"
    ).mean()

    return pd.DataFrame({
        "Phase": [
            int(c.split("_")[-1]) / 10
            for c in columns
        ],
        "Angle": values.to_numpy()
    }).dropna()


def download_table(df, filename):

    st.download_button(
        L(
            "Скачать таблицу",
            "Кестені жүктеу",
            "Download table"
        ),
        df.to_csv(index=False).encode("utf-8-sig"),
        file_name=filename,
        mime="text/csv"
    )


def analysis_table(participant, metric):

    rows = []

    for condition in CONDITIONS:

        if condition not in waveforms:
            continue

        curve = gait_curve(
            waveforms[condition],
            metric,
            participant
        )

        if curve is None or curve.empty:
            continue

        low = float(curve["Angle"].min())
        high = float(curve["Angle"].max())

        rows.append({
            "Condition": condition,
            "Mean angle (deg)": round(
                curve["Angle"].mean(), 2
            ),
            "Minimum (deg)": round(low, 2),
            "Maximum (deg)": round(high, 2),
            "Range (deg)": round(high-low, 2)
        })

    result = pd.DataFrame(rows)

    if not result.empty:

        baseline = result[
            result["Condition"] == "Baseline"
        ]

        if not baseline.empty:

            reference = baseline[
                "Mean angle (deg)"
            ].iloc[0]

            result["Difference vs baseline (deg)"] = (
                result["Mean angle (deg)"] - reference
            ).round(2)

    return result


def team_footer():

    st.divider()

    st.caption("DESIGNED & DEVELOPED IN KAZAKHSTAN")

    st.subheader("NeuroKinetics Team")

    a, b, c = st.columns(3)

    with a:

        card(
            "Abdikakim Aibubi",
            L(
                "Lead Developer · Ведущий разработчик",
                "Lead Developer · Жетекші әзірлеуші",
                "Lead Developer"
            )
        )

    with b:

        card(
            "Ermekov Arystan",
            L(
                "Участник команды",
                "Команда мүшесі",
                "Team Member"
            )
        )

    with c:

        card(
            "Tolegen Barys",
            L(
                "Участник команды",
                "Команда мүшесі",
                "Team Member"
            )
        )


# ==========================================
# HOME
# ==========================================

from neuro_weekly import sync_home, show_notifications
sync_home()
show_notifications()

if page == "home":

    st.caption("NEUROKINETICS • HUMAN MOTION")

    st.title(
        L(
            "За каждым движением — человек.",
            "Әр қозғалыстың артында адам бар.",
            "Behind every movement is a person."
        )
    )

    if role == "doctor":

        st.write(
            L(
                "Исследуйте движения суставов, "
                "сравнивайте научные измерения "
                "и формируйте отчёты.",
                "Буын қозғалыстарын зерттеп, "
                "ғылыми деректерді салыстырыңыз.",
                "Explore joint movements, compare "
                "measurements and create reports."
            )
        )

        a, b, c = st.columns(3)

        a.metric(
            L("Участники", "Қатысушылар", "Participants"),
            len(participants)
        )

        b.metric(
            L("Циклы ходьбы", "Жүріс циклі", "Gait cycles"),
            cycles
        )

        c.metric(
            L("Условия", "Жағдайлар", "Conditions"),
            len(waveforms)
        )

    else:

        st.write(
            L(
                "Пространство для семей, которые хотят "
                "лучше понимать движение, общаться "
                "со специалистами и организовывать занятия.",
                "Қозғалысты түсінуге және мамандармен "
                "бірге жұмыс істеуге арналған кеңістік.",
                "A welcoming space to understand "
                "movement and organize agreed activities."
            )
        )

        a, b, c = st.columns(3)

        a.metric(
            L("Занятия", "Жаттығулар", "Activities"),
            len(st.session_state.nk_plan)
        )

        b.metric(
            L("Выполнено", "Орындалды", "Completed"),
            sum(
                x["done"]
                for x in st.session_state.nk_plan
            )
        )

        c.metric(
            L("Наблюдения", "Бақылаулар", "Observations"),
            len(st.session_state.nk_notes)
        )

        st.info(
            L(
                "Каждый человек развивается в своём "
                "темпе. Важны индивидуальные цели "
                "и поддержка специалистов.",
                "Әр адам өз қарқынымен дамиды.",
                "Everyone develops at their own pace."
            )
        )

    st.divider()

    # The 3D model exists only on this page.

    show_gait_3d()

    team_footer()


# ==========================================
# PROFESSIONAL GAIT ANALYSIS
# ==========================================

elif page == "analysis":

    st.title(PAGES["analysis"])

    participant = choose_participant("nk_analysis_person")

    if participant:

        metric = st.selectbox(
            L("Сустав", "Буын", "Joint"),
            list(METRICS),
            format_func=lambda x: METRICS[x]
        )

        fig = go.Figure()

        colors = ["#68FFB6", "#61D9FF", "#C3A0FF"]

        for condition, color in zip(CONDITIONS, colors):

            if condition not in waveforms:
                continue

            curve = gait_curve(
                waveforms[condition],
                metric,
                participant
            )

            if curve is None:
                continue

            fig.add_trace(go.Scatter(
                x=curve["Phase"],
                y=curve["Angle"],
                name=CONDITION_NAMES[condition],
                mode="lines",
                line=dict(color=color, width=3)
            ))

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#081B14",
            plot_bgcolor="#081B14",
            height=480,
            xaxis_title=L(
                "Цикл ходьбы (%)",
                "Жүріс циклі (%)",
                "Gait cycle (%)"
            ),
            yaxis_title=L(
                "Угол (°)",
                "Бұрыш (°)",
                "Angle (°)"
            )
        )

        st.plotly_chart(fig, width="stretch")

        result = analysis_table(participant, metric)

        st.subheader(
            L(
                "Автоматический анализ",
                "Автоматты талдау",
                "Automatic analysis"
            )
        )

        st.dataframe(
            result,
            hide_index=True,
            width="stretch"
        )

        if "Difference vs baseline (deg)" in result:

            for _, row in result.iterrows():

                if row["Condition"] == "Baseline":
                    continue

                difference = row[
                    "Difference vs baseline (deg)"
                ]

                st.write(
                    CONDITION_NAMES[row["Condition"]]
                    + f": Δ {difference:+.2f}°"
                )

        st.caption(
            L(
                "Различия между экспериментальными "
                "условиями не доказывают улучшение "
                "или ухудшение состояния пациента.",
                "Зерттеу жағдайларының айырмашылығы "
                "емнің нәтижесін дәлелдемейді.",
                "Differences between conditions do not "
                "establish clinical improvement."
            )
        )

        download_table(result, "gait_analysis.csv")

    st.divider()

    st.subheader(
        L(
            "Загрузка дополнительных данных",
            "Қосымша деректер",
            "Upload additional data"
        )
    )

    files = st.file_uploader(
        "CSV",
        type=["csv"],
        accept_multiple_files=True
    )

    for file in files:

        try:

            df = load_gait_csv(file)

            valid, message = validate_gait_data(df)

            if valid:

                st.success(file.name)

                st.dataframe(
                    df.head(50),
                    width="stretch"
                )

            else:
                st.warning(message)

        except Exception:

            st.error(
                L(
                    "Не удалось прочитать файл.",
                    "Файлды оқу мүмкін болмады.",
                    "Unable to read the file."
                )
            )


# ==========================================
# PARTICIPANT PROFILES
# ==========================================

elif page == "participants":

    st.title(PAGES["participants"])

    participant = choose_participant("nk_profile_person")

    if participant:

        rows = []

        for condition, df in waveforms.items():

            selected = df[
                df["Participant_ID"].astype(str)
                == participant
            ]

            if selected.empty:
                continue

            rows.append({
                "Condition": CONDITION_NAMES[condition],
                "Cycles": len(selected),
                "Study side": ", ".join(
                    selected["Study_Side"]
                    .astype(str).unique()
                )
            })

        profile = pd.DataFrame(rows)

        st.dataframe(
            profile,
            hide_index=True,
            width="stretch"
        )

        download_table(profile, "research_profile.csv")

        st.link_button("KU Leuven — Research", SOURCE)


# ==========================================
# REHABILITATION PLAN
# ==========================================

elif page == "plan":

    from neuro_weekly import render_plan
    render_plan()




# ==========================================
# FAMILY CALENDAR
# ==========================================

elif page == "calendar":

    from neuro_weekly import render_calendar
    render_calendar()



# ==========================================
# MONITORING
# ==========================================

elif page == "monitor":

    from neuro_weekly import render_monitor
    render_monitor()

    st.title(PAGES["monitor"])

    st.write(
        L(
            "Добавляйте обезличенные результаты "
            "повторных измерений одного показателя.",
            "Қайталама өлшеу нәтижелерін қосыңыз.",
            "Record anonymized repeated measurements."
        )
    )

    with st.form("nk_measurement_form"):

        person = st.text_input(
            L("Анонимный код", "Анонимді код", "Anonymous ID")
        )

        day = st.date_input(
            L("Дата измерения", "Өлшеу күні", "Measurement date")
        )

        metric = st.selectbox(
            L("Показатель", "Көрсеткіш", "Metric"),
            list(METRICS),
            format_func=lambda x: METRICS[x]
        )

        value = st.number_input(
            L(
                "Измеренное значение (°)",
                "Өлшенген мән (°)",
                "Measured value (°)"
            ),
            min_value=-180.0,
            max_value=180.0
        )

        submit = st.form_submit_button(
            L("Сохранить", "Сақтау", "Save")
        )

        if submit and person.strip():

            st.session_state.nk_measurements.append({
                "Participant": person.strip(),
                "Date": str(day),
                "Metric": metric,
                "Value": value
            })

    if st.session_state.nk_measurements:

        table = pd.DataFrame(
            st.session_state.nk_measurements
        )

        st.dataframe(table, width="stretch")

        download_table(table, "followup_measurements.csv")


# ==========================================
# FAMILY PROGRESS
# ==========================================

elif page == "progress":

    from neuro_weekly import render_progress
    render_progress()



# ==========================================
# JOURNAL
# ==========================================

elif page == "journal":

    st.title(PAGES["journal"])

    with st.form("nk_journal_form"):

        day = st.date_input(
            L("Дата", "Күні", "Date")
        )

        note = st.text_area(
            L(
                "Что хотите обсудить со специалистом?",
                "Маманмен нені талқылағыңыз келеді?",
                "What would you like to discuss?"
            )
        )

        if st.form_submit_button(
            L("Сохранить", "Сақтау", "Save")
        ) and note.strip():

            st.session_state.nk_notes.append({
                "Date": str(day),
                "Note": note.strip()
            })

    if st.session_state.nk_notes:

        table = pd.DataFrame(
            st.session_state.nk_notes
        )

        st.dataframe(table, width="stretch")

        download_table(table, "family_journal.csv")


# ==========================================
# REHABILITATION LIBRARY
# ==========================================

elif page == "rehab":

    from neuro_weekly import render_rehab
    render_rehab()




# ==========================================
# GLOBAL EXPERTS
# ==========================================

elif page == "experts":

    if role == 'family':
        from neuro_centers import render_centers
        render_centers(language)
    else:
        st.title(PAGES["experts"])

        experts = [
            (
                "🇰🇿",
                L("Казахстан", "Қазақстан", "Kazakhstan"),
                L(
                    "Айгуль Алтынбекова",
                    "Айгүл Алтынбекова",
                    "Aigul Altynbekova"
                ),
                L(
                    "Детская медицинская реабилитация.",
                    "Балаларды медициналық оңалту.",
                    "Pediatric medical rehabilitation."
                ),
                "https://www.nccr.kz/"
            ),
            (
                "🇷🇺",
                L("Россия", "Ресей", "Russia"),
                L(
                    "Фонд «Обнажённые сердца»",
                    "«Жалаңаш жүректер» қоры",
                    "Naked Heart Foundation"
                ),
                L(
                    "Образовательные материалы для семей.",
                    "Отбасыларға арналған материалдар.",
                    "Educational family resources."
                ),
                "https://nakedheart.online/"
            ),
            (
                "🇯🇵",
                L("Япония", "Жапония", "Japan"),
                "National Center for Child Health and Development",
                L(
                    "Междисциплинарная детская реабилитация.",
                    "Балаларды кешенді оңалту.",
                    "Multidisciplinary pediatric rehabilitation."
                ),
                "https://www.ncchd.go.jp/en/hospital/about/section/surgical_specialties/rihabiri.html"
            ),
            (
                "🇰🇷",
                L("Южная Корея", "Оңтүстік Корея", "South Korea"),
                "Jeong Yi Kwon",
                L(
                    "Профессор восстановительной медицины.",
                    "Оңалту медицинасының профессоры.",
                    "Professor of rehabilitation medicine."
                ),
                "https://www.samsunghospital.com/en/find-doctor/jeong-yi-kwon-487.do"
            ),
            (
                "🇮🇳",
                L("Индия", "Үндістан", "India"),
                "CanChild / Amitesh Narayan",
                L(
                    "Образовательная поддержка семей.",
                    "Отбасыларды ақпараттық қолдау.",
                    "Family education."
                ),
                "https://canchild.ca/the-icf-for-parents-p-icf/"
            ),
            (
                "🇦🇺",
                L("Австралия", "Аустралия", "Australia"),
                "Iona Novak",
                L(
                    "Исследователь церебрального паралича, "
                    "соавтор международных рекомендаций.",
                    "Церебралды сал ауруын зерттеуші.",
                    "Cerebral palsy researcher and guideline co-author."
                ),
                GUIDELINE
            ),
            (
                "🇬🇧",
                L("Великобритания", "Ұлыбритания", "United Kingdom"),
                "NHS",
                L(
                    "Информация о медицинской помощи.",
                    "Медициналық ақпарат.",
                    "Public healthcare information."
                ),
                "https://www.nhs.uk/conditions/cerebral-palsy/"
            ),
            (
                "🇺🇸",
                L("США", "АҚШ", "United States"),
                "CDC",
                L(
                    "Информация о церебральном параличе.",
                    "Церебралды сал ауруы туралы ақпарат.",
                    "Cerebral palsy education."
                ),
                "https://www.cdc.gov/cerebral-palsy/treatment/index.html"
            )
        ]

        countries = [x[1] for x in experts]

        all_countries = L(
            "Все страны", "Барлық елдер", "All countries"
        )

        selected = st.selectbox(
            L("Страна", "Ел", "Country"),
            [all_countries] + countries
        )

        for flag, country, name, description, url in experts:

            if selected not in [all_countries, country]:
                continue

            with st.container(border=True):

                st.caption(flag + " " + country)

                st.subheader(name)

                st.write(description)

                st.link_button(
                    L(
                        "Оригинальный источник",
                        "Түпнұсқа дереккөз",
                        "Original source"
                    ),
                    url
                )

        st.caption(
            L(
                "Это образовательная подборка, не рейтинг "
                "врачей и не список партнёров проекта.",
                "Бұл білім беру жинағы, рейтинг емес.",
                "Educational selection, not endorsements."
            )
        )


# ==========================================
# NEUROCARE GENERATIVE AI
# ==========================================

elif page == "assistant":

    from neurocare_local import show_local_ai
    show_local_ai(language)



# ==========================================
# PDF RESEARCH REPORTS
# ==========================================

elif page == "reports":

    st.title(PAGES["reports"])

    participant = choose_participant("nk_report_person")

    if participant:

        metric = st.selectbox(
            L("Сустав", "Буын", "Joint"),
            list(METRICS),
            format_func=lambda x: METRICS[x],
            key="nk_report_metric"
        )

        result = analysis_table(participant, metric)

        st.dataframe(result, width="stretch")

        download_table(result, "research_report.csv")

        try:

            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas

            buffer = BytesIO()

            pdf = canvas.Canvas(buffer, pagesize=A4)

            pdf.setFillColorRGB(.04, .20, .13)
            pdf.rect(0, 730, 595, 112, fill=1, stroke=0)

            pdf.setFillColorRGB(1, 1, 1)
            pdf.setFont("Helvetica-Bold", 26)
            pdf.drawString(42, 785, "NeuroKinetics")

            pdf.setFont("Helvetica", 12)
            pdf.drawString(42, 757, "Scientific Research Report")

            pdf.setFillColorRGB(.08, .15, .12)
            pdf.setFont("Helvetica", 11)

            pdf.drawString(
                42, 700,
                f"Participant: {participant}"
            )

            pdf.drawString(
                42, 680,
                f"Research metric: {metric}"
            )

            pdf.drawString(
                42, 660,
                f"Date: {date.today()}"
            )

            y = 620

            for _, row in result.iterrows():

                pdf.setFont("Helvetica-Bold", 12)

                pdf.drawString(
                    42, y, str(row["Condition"])
                )

                y -= 20

                pdf.setFont("Helvetica", 11)

                for key, value in row.items():

                    if key != "Condition":

                        pdf.drawString(
                            52, y,
                            f"{key}: {value}"
                        )

                        y -= 17

                y -= 20

            pdf.setFont("Helvetica", 9)

            pdf.drawString(
                42, 90,
                "Research prototype. Not a clinical diagnosis."
            )

            pdf.drawString(
                42, 73,
                "Source: KU Leuven RDR. DOI: 10.48804/JUNNWW"
            )

            pdf.drawString(
                42, 56,
                "CC BY-NC-SA 4.0"
            )

            pdf.save()

            st.download_button(
                "PDF ↓",
                buffer.getvalue(),
                file_name="NeuroKinetics_Report.pdf",
                mime="application/pdf"
            )

        except ImportError:

            st.info(
                L(
                    "Для PDF установите библиотеку reportlab.",
                    "PDF үшін reportlab қажет.",
                    "Install reportlab to enable PDF export."
                )
            )


# ==========================================
# PREPARE FOR A MEDICAL VISIT
# ==========================================

elif page == "guide":

    from neuro_visit import render_visit_guide
    render_visit_guide(language)



# ==========================================
# GLOBAL FOOTER
# ==========================================

st.divider()

st.caption(
    L(
        "Исследовательский прототип. Кабинеты "
        "демонстрационные, без защищённой авторизации. "
        "Записи хранятся только в текущей сессии. "
        "Не вводите персональные медицинские данные. "
        "Не заменяет квалифицированного врача.",
        "Зерттеу прототипі. Жеке медициналық "
        "деректерді енгізбеңіз. Дәрігерді алмастырмайды.",
        "Research prototype. Demo workspaces, "
        "session-only storage. Do not enter private "
        "medical data. Not a substitute for medical care."
    )
)

st.caption("© 2026 NeuroKinetics Team · Kazakhstan")

st.markdown(
    "[KU Leuven — Scientific Dataset]"
    "(https://doi.org/10.48804/JUNNWW)"
)
