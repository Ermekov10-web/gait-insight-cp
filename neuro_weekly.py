
import streamlit as st
import pandas as pd
import sqlite3
import uuid
import re

from pathlib import Path
from datetime import date, timedelta, datetime


DB = Path.home() / ".neurokinetics" / "weekly_demo.sqlite3"
DB.parent.mkdir(parents=True, exist_ok=True)


def db(sql, params=()):
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute(sql, params).fetchall()
        return [dict(row) for row in rows]


db("""CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    day TEXT,
    ru TEXT,
    kz TEXT,
    notes TEXT,
    status TEXT,
    feedback TEXT
)""")


db("""CREATE TABLE IF NOT EXISTS weekly (
    week TEXT PRIMARY KEY,
    comfort TEXT,
    difficulty TEXT,
    support TEXT,
    mood TEXT,
    saved TEXT
)""")


STATUS = {
    "pending": "Запланировано / Жоспарланған",
    "done": "Выполнено / Орындалды",
    "partial": "Частично / Жартылай",
    "missed": "Не выполнено / Орындалмады"
}

FEEDBACK = {
    "none": "Не указано / Көрсетілмеген",
    "good": "Без трудностей / Қиындықсыз",
    "help": "Нужна помощь / Көмек қажет",
    "pain": "Дискомфорт / Жайсыздық"
}

COMFORT = {
    "good": "Комфортно / Жайлы",
    "sometimes": "Иногда некомфортно / Кейде жайсыз",
    "pain": "Боль / Ауырсыну",
    "unknown": "Не могу оценить / Бағалай алмаймын"
}

DIFFICULTY = {
    "easy": "Легко / Оңай",
    "medium": "Средне / Орташа",
    "hard": "Сложно / Қиын",
    "unknown": "Не могу оценить / Бағалай алмаймын"
}

SUPPORT = {
    "none": "Нет / Жоқ",
    "some": "Иногда / Кейде",
    "often": "Часто / Жиі",
    "unknown": "Не могу оценить / Бағалай алмаймын"
}

MOOD = {
    "good": "Хорошее / Жақсы",
    "normal": "Спокойное / Қалыпты",
    "hard": "Тревожное / Мазасыз",
    "unknown": "Не могу оценить / Бағалай алмаймын"
}


def week_start(day=None):
    day = day or date.today()
    return day - timedelta(days=day.weekday())


def tasks():
    return db("SELECT * FROM tasks ORDER BY day, id")


def title(t):
    return " / ".join(
        x for x in [t["ru"], t["kz"]] if x
    )


def notice():
    st.caption(
        "Демонстрационный профиль. "
        "Не вводите данные реальных пациентов. "
        "/ Нақты пациенттердің деректерін енгізбеңіз."
    )


def sync_home():
    rows = tasks()

    st.session_state.nk51_tasks = [
        {
            "id": t["id"],
            "ru": t["ru"],
            "kz": t["kz"],
            "date": t["day"],
            "status": t["status"],
            "topic": "daily",
            "notes": t["notes"]
        }
        for t in rows
    ]

    st.session_state.nk_plan = [
        {
            "activity": title(t),
            "date": t["day"],
            "done": t["status"] == "done"
        }
        for t in rows
    ]


def show_notifications():
    today = str(date.today())
    week = str(week_start())

    pending = sum(
        t["day"] == today
        and t["status"] == "pending"
        for t in tasks()
    )

    survey = db(
        "SELECT week FROM weekly WHERE week=?",
        (week,)
    )

    with st.sidebar:
        st.divider()
        st.subheader("🔔 Напоминания / Еске салу")

        if pending:
            st.info(f"Сегодня занятий: {pending}")

        if not survey:
            st.warning(
                "Заполните опрос недели / "
                "Апталық сауалнаманы толтырыңыз"
            )
        else:
            st.success(
                "Опрос заполнен / Сауалнама толтырылды"
            )


# ==========================================
# ADD APPROVED ACTIVITIES
# ==========================================

def add_task(key):

    with st.form(key, clear_on_submit=True):

        ru = st.text_input("Название на русском")
        kz = st.text_input("Қазақша атауы")

        day = st.date_input("Дата / Күні")

        notes = st.text_area(
            "Согласованные указания специалиста / "
            "Маманның келісілген нұсқаулары"
        )

        approved = st.checkbox(
            "Занятие согласовано с врачом / "
            "Жаттығу дәрігермен келісілген"
        )

        save = st.form_submit_button(
            "Добавить занятие / Жаттығу қосу"
        )

    if save:

        if not (ru.strip() or kz.strip()) or not approved:
            st.warning(
                "Укажите название и подтвердите согласование."
            )
            return

        if re.search(r"[A-Za-z]", ru + kz + notes):
            st.warning("Используйте русский или казахский.")
            return

        db(
            "INSERT INTO tasks VALUES (?,?,?,?,?,?,?)",
            (
                uuid.uuid4().hex,
                str(day),
                ru.strip(),
                kz.strip(),
                notes.strip(),
                "pending",
                "none"
            )
        )

        st.rerun()


# ==========================================
# INTERACTIVE ACTIVITIES
# ==========================================

def show_tasks(rows, key, editable=True):

    if not rows:
        st.info(
            "Пока нет занятий. Добавьте согласованное "
            "со специалистом задание."
        )

    for t in rows:

        with st.container(border=True):

            st.subheader(title(t))
            st.caption("📅 " + t["day"])

            if t["notes"]:
                st.write(t["notes"])

            if editable:

                with st.form(key + t["id"]):

                    status = st.radio(
                        "Результат занятия / Жаттығу нәтижесі",
                        list(STATUS),
                        index=list(STATUS).index(t["status"]),
                        format_func=lambda x: STATUS[x]
                    )

                    feedback = st.selectbox(
                        "Самочувствие / Жағдайы",
                        list(FEEDBACK),
                        index=list(FEEDBACK).index(t["feedback"]),
                        format_func=lambda x: FEEDBACK[x]
                    )

                    save = st.form_submit_button(
                        "Сохранить результат / Нәтижені сақтау"
                    )

                if save:
                    db(
                        "UPDATE tasks SET status=?, feedback=? WHERE id=?",
                        (status, feedback, t["id"])
                    )
                    st.rerun()

                if t["feedback"] == "pain":
                    st.warning(
                        "Не продолжайте занятие, вызывающее боль. "
                        "Обсудите это со специалистом."
                    )

            else:

                st.write(STATUS[t["status"]])
                st.write(FEEDBACK[t["feedback"]])

                if st.button(
                    "Удалить / Жою",
                    key=key + t["id"]
                ):
                    db(
                        "DELETE FROM tasks WHERE id=?",
                        (t["id"],)
                    )
                    st.rerun()


# ==========================================
# WEEKLY QUESTIONS
# ==========================================

def questionnaire(key):

    st.subheader("Еженедельный опрос / Апталық сауалнама")

    week = str(week_start())

    st.caption(
        f"{week} — {week_start() + timedelta(days=6)}"
    )

    rows = db(
        "SELECT * FROM weekly WHERE week=?",
        (week,)
    )

    old = rows[0] if rows else {}

    if old:
        st.success(
            "Ответы сохранены. Их можно обновить. "
            "/ Жауаптар сақталды."
        )

    with st.form(key):

        def ask(label, options, field):

            keys = list(options)

            return st.radio(
                label,
                keys,
                index=keys.index(old.get(field, "unknown")),
                format_func=lambda x: options[x]
            )

        comfort = ask(
            "Как прошло занятие? / Өзіңізді қалай сезіндіңіз?",
            COMFORT,
            "comfort"
        )

        difficulty = ask(
            "Было ли сложно? / Қиын болды ма?",
            DIFFICULTY,
            "difficulty"
        )

        support = ask(
            "Требовалась ли помощь? / Көмек қажет болды ма?",
            SUPPORT,
            "support"
        )

        mood = ask(
            "Какое было настроение? / Көңіл-күйіңіз қандай болды?",
            MOOD,
            "mood"
        )

        save = st.form_submit_button(
            "Сохранить ответы / Жауаптарды сақтау"
        )

    if save:

        db(
            "INSERT OR REPLACE INTO weekly VALUES (?,?,?,?,?,?)",
            (
                week,
                comfort,
                difficulty,
                support,
                mood,
                datetime.now().isoformat()
            )
        )

        st.rerun()

    if old.get("comfort") == "pain":
        st.warning(
            "Обсудите боль со специалистом. "
            "Не продолжайте вызывающее боль занятие."
        )

    st.caption(
        "Опрос не является медицинской диагностикой."
    )


# ==========================================
# PROGRESS AND HISTORY
# ==========================================

def dashboard(key):

    rows = tasks()

    start = str(week_start())
    end = str(week_start() + timedelta(days=6))

    current = [
        t for t in rows
        if start <= t["day"] <= end
    ]

    total = len(current)

    done = sum(
        t["status"] == "done" for t in current
    )

    partial = sum(
        t["status"] == "partial" for t in current
    )

    a, b, c = st.columns(3)

    a.metric("Задания / Тапсырмалар", total)
    b.metric("Выполнено / Орындалды", done)
    c.metric("Частично / Жартылай", partial)

    percent = done / total if total else 0.0

    st.progress(percent)

    st.write(
        f"Выполнение плана: {percent * 100:.0f}%"
    )

    if rows:

        weeks = {}

        for t in rows:

            week = str(
                week_start(date.fromisoformat(t["day"]))
            )

            if week not in weeks:
                weeks[week] = {
                    "Все занятия": 0,
                    "Выполнено": 0
                }

            weeks[week]["Все занятия"] += 1
            weeks[week]["Выполнено"] += (
                t["status"] == "done"
            )

        st.bar_chart(
            pd.DataFrame.from_dict(weeks, orient="index")
            .sort_index()
        )

        table = pd.DataFrame([
            {
                "Дата / Күні": t["day"],
                "Занятие / Жаттығу": title(t),
                "Результат / Нәтиже": STATUS[t["status"]],
                "Самочувствие / Жағдайы": FEEDBACK[t["feedback"]]
            }
            for t in rows
        ])

        st.dataframe(table, hide_index=True)

        st.download_button(
            "Скачать историю / Тарихты жүктеу",
            table.to_csv(index=False).encode("utf-8-sig"),
            "activity_history.csv",
            key=key + "_history"
        )

    st.caption(
        "Процент выполнения не является показателем "
        "медицинского улучшения."
    )

    records = db(
        "SELECT * FROM weekly ORDER BY week DESC"
    )

    if records:

        st.subheader("История опросов / Сауалнамалар тарихы")

        table = pd.DataFrame([
            {
                "Неделя": r["week"],
                "Самочувствие": COMFORT[r["comfort"]],
                "Сложность": DIFFICULTY[r["difficulty"]],
                "Помощь": SUPPORT[r["support"]],
                "Настроение": MOOD[r["mood"]]
            }
            for r in records
        ])

        st.dataframe(table, hide_index=True)

        st.download_button(
            "Скачать мониторинг",
            table.to_csv(index=False).encode("utf-8-sig"),
            "weekly_monitoring.csv",
            key=key + "_weekly"
        )


# ==========================================
# EDUCATIONAL LIBRARY
# ==========================================

def library(key):
    try:
        from neurorehab_ru_kz import render_library
    except ImportError:
        st.link_button(
            "Материалы для родителей",
            "https://nakedheart.online/"
        )
        st.link_button(
            "Ұлттық балаларды оңалту орталығы",
            "https://www.nccr.kz/"
        )
    else:
        render_library(key)


# ==========================================
# CALENDAR REMINDER
# ==========================================

def reminder():

    first = datetime.combine(
        week_start() + timedelta(days=6),
        datetime.min.time()
    ).replace(hour=19)

    if first <= datetime.now():
        first += timedelta(days=7)

    content = "\r\n".join([
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//NeuroKinetics//Weekly//EN",
        "BEGIN:VEVENT",
        "UID:weekly@neurokinetics.local",
        "DTSTAMP:" + datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),
        "DTSTART:" + first.strftime("%Y%m%dT%H%M%S"),
        "RRULE:FREQ=WEEKLY;BYDAY=SU",
        "DURATION:PT10M",
        "SUMMARY:NeuroKinetics - Еженедельный опрос",
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        "TRIGGER:-PT15M",
        "DESCRIPTION:Заполните опрос",
        "END:VALARM",
        "END:VEVENT",
        "END:VCALENDAR",
        ""
    ])

    st.download_button(
        "🔔 Еженедельное напоминание / Еске салу",
        content.encode("utf-8"),
        "NeuroKinetics.ics",
        mime="text/calendar",
        key="weekly_reminder"
    )

    st.caption(
        "Откройте файл в календаре устройства. "
        "Напоминание: воскресенье, 19:00."
    )


# ==========================================
# FAMILY PAGES
# ==========================================

def render_progress():

    st.title("Мой прогресс / Менің жетістіктерім")
    notice()

    dashboard("progress")

    st.divider()
    st.header("Отметить выполнение / Орындалуын белгілеу")

    show_tasks(tasks(), "progress_task_")

    with st.expander("Добавить согласованное занятие"):
        add_task("progress_add")

    st.divider()
    pass

    st.divider()
    reminder()


def render_rehab():

    st.title("Мои занятия / Менің жаттығуларым")
    notice()

    tab1, tab2, tab3 = st.tabs([
        "Задания / Тапсырмалар",
        "Опрос / Сауалнама",
        "Библиотека / Кітапхана"
    ])

    with tab1:

        show_tasks(tasks(), "rehab_task_")

        with st.expander("Добавить согласованное занятие"):
            add_task("rehab_add")

    with tab2:
        questionnaire("rehab_survey")

    with tab3:
        library("rehab_library")


def render_calendar():

    st.title("Календарь / Күнтізбе")
    notice()

    day = st.date_input("Дата / Күні")

    show_tasks(
        [t for t in tasks() if t["day"] == str(day)],
        "calendar_task_"
    )

    reminder()


# ==========================================
# DOCTOR PAGES
# ==========================================

def render_plan():

    st.title("План занятий / Жаттығулар жоспары")
    notice()

    add_task("doctor_add")

    show_tasks(tasks(), "doctor_task_", editable=False)

    with st.expander("Библиотека / Кітапхана"):
        library("doctor_library")


def render_monitor():

    st.header("Еженедельный мониторинг")
    notice()

    dashboard("doctor_monitor")
    st.divider()

