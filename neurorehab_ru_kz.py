
import streamlit as st
import pandas as pd

TOPICS = [
    (
        "🚶 Ходьба и мобильность",
        "Жүру және қозғалыс",
        "Цель: поддержка навыков передвижения.",
        "Мақсаты: қозғалу дағдыларын қолдау."
    ),
    (
        "⚖️ Равновесие",
        "Тепе-теңдік",
        "Цель: развитие устойчивости тела.",
        "Мақсаты: дене тұрақтылығын дамыту."
    ),
    (
        "🤲 Мелкая моторика",
        "Ұсақ моторика",
        "Цель: развитие навыков использования рук.",
        "Мақсаты: қол қимылдарын дамыту."
    ),
    (
        "🧩 Координация",
        "Қимыл үйлесімділігі",
        "Цель: согласованность движений.",
        "Мақсаты: қозғалыстардың үйлесімділігі."
    ),
    (
        "🦿 Движения рук и ног",
        "Қол мен аяқ қозғалысы",
        "Цель: поддержка двигательных навыков.",
        "Мақсаты: қимыл-қозғалыс дағдыларын қолдау."
    ),
    (
        "🏡 Повседневные навыки",
        "Күнделікті дағдылар",
        "Цель: участие в повседневной жизни.",
        "Мақсаты: күнделікті өмірге қатысу."
    ),
    (
        "🌱 Самостоятельность",
        "Дербестік",
        "Цель: поддержка самостоятельности ребёнка.",
        "Мақсаты: баланың дербестігін қолдау."
    ),
    (
        "🤍 Поддержка семьи",
        "Отбасын қолдау",
        "Цель: сотрудничество семьи и специалистов.",
        "Мақсаты: отбасы мен мамандардың ынтымақтастығы."
    )
]

RESOURCES = [
    (
        "Русский",
        "🎬 Помощь детям с двигательными нарушениями",
        "Вебинар",
        "Фонд «Обнажённые сердца»",
        "Обзор современных подходов к поддержке детей.",
        "https://nakedheart.online/webinars/"
        "sovremennye-tehnologii-pomoschi-detyam-"
        "s-dvigatelnymi-narusheniyami"
    ),
    (
        "Русский",
        "🎧 Ходьба и мобильность",
        "Подкаст",
        "Фонд «Обнажённые сердца»",
        "Обсуждение двигательных навыков "
        "и средств реабилитации.",
        "https://nakedheart.online/podcasts/"
        "dtsp-hodba-mobilnost-i-tehnicheskie-"
        "sredstva-reabilitatsii"
    ),
    (
        "Русский",
        "📖 Развитие двигательных навыков",
        "Статья",
        "Фонд «Обнажённые сердца»",
        "Обзор научно изученных программ помощи.",
        "https://nakedheart.online/articles/"
        "programmy-vmeshatelstva-napravlennye-na-"
        "razvitie-dvizhenii-u-detei-s-tserebralnym-paralichom"
    ),
    (
        "Русский",
        "🎧 Семья и реабилитация",
        "Подкаст",
        "Фонд «Обнажённые сердца»",
        "Роль семьи и специалистов "
        "в процессе реабилитации.",
        "https://nakedheart.online/podcasts/"
        "dtsp-semeino-tsentrirovannyi-podhod-kak-"
        "osnova-uspeshnoi-reabilitatsii-detei-s-"
        "tserebralnym-paralichom"
    ),
    (
        "Қазақша",
        "🇰🇿 Үй жағдайындағы оңалту",
        "Мақала",
        "ҚР Еңбек және халықты әлеуметтік "
        "қорғау министрлігі",
        "Балалар мен ата-аналарға "
        "үй жағдайында қолдау көрсету.",
        "https://www.gov.kz/org/enbek/press/news/"
        "details/1271793?lang=kk"
    ),
    (
        "Қазақша",
        "🇰🇿 Қамқорлық оңалту орталығы",
        "Мақала",
        "Астана қаласының әкімдігі",
        "Балаларды оңалту және күнделікті "
        "дағдыларды дамыту туралы ақпарат.",
        "https://www.gov.kz/memleket/entities/"
        "astana/press/news/details/283414?lang=kk"
    )
]


def render_library(key="rehab"):

    st.subheader(
        "Направления реабилитации / Оңалту бағыттары"
    )

    st.caption(
        "Образовательные цели, а не индивидуальные назначения."
        " / Бұл жеке емдеу жоспары емес."
    )

    for start in range(0, len(TOPICS), 2):

        cols = st.columns(2)

        for col, topic in zip(
            cols, TOPICS[start:start + 2]
        ):

            with col:

                with st.container(border=True):

                    st.subheader(topic[0])
                    st.caption(topic[1])
                    st.write(topic[2])
                    st.write(topic[3])

                    with st.expander(
                        "Подробнее / Толығырақ"
                    ):

                        st.write(
                            "Конкретные занятия и нагрузку "
                            "определяет специалист после "
                            "индивидуальной оценки."
                        )

                        st.write(
                            "Жаттығуларды маман баланың "
                            "жеке ерекшеліктеріне қарай таңдайды."
                        )

    st.divider()

    st.subheader(
        "Материалы специалистов / Мамандар материалдары"
    )

    selected = st.radio(
        "Язык материалов / Материалдар тілі",
        ["Все / Барлығы", "Русский", "Қазақша"],
        horizontal=True,
        key=key + "_language"
    )

    for lang, title, kind, author, desc, url in RESOURCES:

        if selected not in ["Все / Барлығы", lang]:
            continue

        with st.container(border=True):

            st.caption(lang + " · " + kind)

            st.subheader(title)

            st.write(author)

            st.write(desc)

            st.link_button(
                "Открыть материал"
                if lang == "Русский"
                else "Материалды ашу",
                url
            )

    st.warning(
        "Лечебные упражнения выполняются только "
        "после согласования со специалистом."
        " / Емдік жаттығуларды маманмен келісу қажет."
    )


def render_rehab(language="Русский", add_form=None):

    st.caption("NEUROKINETICS · NEUROREHAB")

    st.title("Занятия и реабилитация")

    st.subheader("Жаттығулар және оңалту")

    st.write(
        "Поддержка ребёнка и семьи на каждом этапе."
        " / Бала мен отбасына әр кезеңде қолдау көрсету."
    )

    library, assigned = st.tabs([
        "Библиотека / Кітапхана",
        "Мои занятия / Менің жаттығуларым"
    ])

    with library:

        render_library("parent_rehab")

    with assigned:

        tasks = st.session_state.get(
            "nk51_tasks",
            st.session_state.get("nk_plan", [])
        )

        statuses = {
            "done": "Выполнено / Орындалды",
            "pending": "Запланировано / Жоспарланған",
            "partial": "Частично / Жартылай",
            "missed": "Не выполнено / Орындалмады"
        }

        if not tasks:

            st.info(
                "Согласованных занятий пока нет."
                " / Келісілген жаттығулар әзірге жоқ."
            )

        else:

            for task in tasks:

                with st.container(border=True):

                    title = " / ".join(
                        task.get(k, "")
                        for k in ["ru", "kz"]
                        if task.get(k)
                    )

                    title = title or task.get(
                        "activity", "Занятие / Жаттығу"
                    )

                    st.subheader(title)

                    st.caption(
                        "Дата / Күні: "
                        + str(task.get("date", "—"))
                    )

                    status = task.get(
                        "status",
                        "done" if task.get("done") else "pending"
                    )

                    st.write(
                        statuses.get(status, status)
                    )

                    if task.get("notes"):
                        st.write(task["notes"])

            st.info(
                "Отметить выполнение можно в календаре."
                " / Орындалуын күнтізбеде белгілеуге болады."
            )

        if callable(add_form):

            with st.expander(
                "Добавить согласованное занятие"
                " / Келісілген жаттығуды қосу"
            ):

                add_form("rehab_bilingual_form")

