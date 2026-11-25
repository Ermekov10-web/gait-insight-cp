
import streamlit as st
import sqlite3
import uuid

from pathlib import Path
from datetime import datetime
from urllib.parse import quote


CENTERS = [
    {
        "name": "Национальный центр детской реабилитации",
        "kz": "Ұлттық балаларды оңалту орталығы",
        "city": "Астана",
        "gis_city": "astana",
        "address": "Проспект Туран, 36",
        "description": (
            "Комплексная детская нейрореабилитация, "
            "физическая медицина, эрготерапия, "
            "роботизированная кинезотерапия."
        ),
        "description_kz": (
            "Балалардың кешенді нейрооңалтуы, "
            "физикалық медицина және эрготерапия."
        ),
        "website": "https://www.nccr.kz/index.php/ru/",
        "doctors_url": (
            "https://www.nccr.kz/index.php/ru/"
            "o-nas/about-ru/spetsialisty"
        ),
        "contacts": (
            "https://www.nccr.kz/index.php/ru/contact-us"
        ),
        "doctors": [
            (
                "Дарибаев Жолтай Рахимбекович",
                "Невролог, реабилитолог, кандидат медицинских наук",
                "Невролог, оңалту дәрігері"
            ),
            (
                "Агланбекова Меруерт Болатовна",
                "Невролог, реабилитолог",
                "Невролог, оңалту дәрігері"
            ),
            (
                "Искулова Асыл Ергазиевна",
                "Врач физической медицины и реабилитации",
                "Физикалық медицина және оңалту дәрігері"
            )
        ]
    },
    {
        "name": "Детский реабилитационный центр Балбулак",
        "kz": "Балбұлақ балаларды оңалту орталығы",
        "city": "Алматы",
        "gis_city": "almaty",
        "address": "Керей Жанибек хандар, 440",
        "description": (
            "Реабилитация детей с ДЦП и другими "
            "неврологическими нарушениями. "
            "Центр работает с 1996 года."
        ),
        "description_kz": (
            "БЦС және басқа неврологиялық бұзылыстары "
            "бар балаларды оңалту. "
            "Орталық 1996 жылдан бері жұмыс істейді."
        ),
        "phone": "+7 (727) 271-62-24",
        "website": "https://balbulak.kz/ru/",
        "doctors_url": "https://balbulak.kz/?page_id=11348",
        "contacts": "https://balbulak.kz/ru/",
        "support": "https://balbulak.kz/ru/?page_id=2419",
        "doctors": [
            (
                "Мухамбетова Гульнар Амерзаевна",
                "Консультант, кандидат медицинских наук",
                "Кеңесші, медицина ғылымдарының кандидаты"
            ),
            (
                "Варзина Татьяна Владимировна",
                "Невропатолог высшей категории",
                "Жоғары санатты невропатолог"
            ),
            (
                "Мирзахметова Сабина Ержановна",
                "Врач-невролог",
                "Невролог дәрігер"
            )
        ]
    },
    {
        "name": "Детский реабилитационный центр Тоқтамыс",
        "kz": "Тоқтамыс балаларды оңалту орталығы",
        "city": "Семей",
        "gis_city": "semey",
        "address": "Улица Гоголя, 95",
        "description": (
            "Детская медицинская реабилитация, "
            "неврологические консультации "
            "и восстановительная медицина."
        ),
        "description_kz": (
            "Балаларды медициналық оңалту, "
            "неврологиялық кеңес және қалпына келтіру."
        ),
        "website": "https://toqtamys.kz/ru/",
        "doctors_url": "https://toqtamys.kz/ru/struktura-2/",
        "contacts": "https://toqtamys.kz/ru/",
        "doctors": [
            (
                "Рахметова Анар Сайлаугалиевна",
                "Врач-невропатолог",
                "Невропатолог дәрігер"
            ),
            (
                "Алибекова Бакытжан Алибековна",
                "Детский невролог",
                "Балалар неврологі"
            ),
            (
                "Даулетжарова Жайық Калымовна",
                "Врач-реабилитолог",
                "Оңалту дәрігері"
            )
        ]
    }
]


def gis_url(center):

    query = (
        center["name"] + " " + center["address"]
    )

    return (
        "https://2gis.kz/"
        + center["gis_city"]
        + "/search/"
        + quote(query)
    )


def render_centers(language="Русский"):

    kz = language == "Қазақша"

    def L(ru, kk):
        return kk if kz else ru

    st.caption("NEUROKINETICS · CARE NETWORK")

    st.title(L(
        "Центры реабилитации и специалисты",
        "Оңалту орталықтары және мамандар"
    ))

    st.write(L(
        "Найдите профильный центр, познакомьтесь "
        "со специалистами и уточните условия приёма.",
        "Оңалту орталығын тауып, мамандармен "
        "танысып, қабылдау шарттарын анықтаңыз."
    ))

    a, b, c = st.columns(3)

    a.metric(L("Центры", "Орталықтар"), len(CENTERS))
    b.metric(L("Города", "Қалалар"), 3)
    c.metric(L("Специалисты", "Мамандар"), 9)

    directory, support = st.tabs([
        L("Каталог центров", "Орталықтар каталогы"),
        L("Служба поддержки", "Қолдау қызметі")
    ])

    with directory:

        cities = [L("Все города", "Барлық қалалар")]

        cities += sorted({
            center["city"] for center in CENTERS
        })

        city = st.selectbox(
            L("Выберите город", "Қаланы таңдаңыз"),
            cities,
            key="nk_center_city"
        )

        search = st.text_input(
            L(
                "Поиск центра или специалиста",
                "Орталықты немесе маманды іздеу"
            ),
            key="nk_center_search"
        ).lower().strip()

        count = 0

        for center in CENTERS:

            if city != cities[0] and city != center["city"]:
                continue

            searchable = (
                center["name"]
                + center["kz"]
                + center["city"]
                + " ".join(d[0] for d in center["doctors"])
            ).lower()

            if search and search not in searchable:
                continue

            count += 1

            with st.container(border=True):

                st.caption(
                    "📍 " + center["city"]
                )

                st.header(
                    center["kz"] if kz else center["name"]
                )

                st.write(center["address"])

                st.write(
                    center["description_kz"]
                    if kz else center["description"]
                )

                if center.get("phone"):
                    st.write("☎ " + center["phone"])

                col1, col2, col3 = st.columns(3)

                col1.link_button(
                    "📍 2ГИС",
                    gis_url(center)
                )

                col2.link_button(
                    L("Официальный сайт", "Ресми сайт"),
                    center["website"]
                )

                col3.link_button(
                    L("Контакты и запись", "Байланыс"),
                    center["contacts"]
                )

                st.caption(L(
                    "Актуальные отзывы, оценки и маршрут "
                    "доступны в 2ГИС.",
                    "Пікірлер, бағалар және бағыт "
                    "2ГИС жүйесінде қолжетімді."
                ))

                st.divider()

                st.subheader(L(
                    "Специалисты центра",
                    "Орталық мамандары"
                ))

                for name, role_ru, role_kz in center["doctors"]:

                    with st.container(border=True):

                        icon, info = st.columns([1, 7])

                        icon.title("🩺")

                        with info:

                            st.markdown("**" + name + "**")

                            st.write(
                                role_kz if kz else role_ru
                            )

                st.link_button(
                    L(
                        "Официальный список специалистов",
                        "Мамандардың ресми тізімі"
                    ),
                    center["doctors_url"]
                )

                if center.get("support"):

                    st.link_button(
                        L(
                            "Служба поддержки пациентов",
                            "Пациенттерді қолдау қызметі"
                        ),
                        center["support"]
                    )

        if count == 0:
            st.info(L(
                "Ничего не найдено",
                "Ештеңе табылмады"
            ))

        st.divider()

        st.link_button(
            L(
                "Найти другие центры в 2ГИС",
                "2ГИС арқылы басқа орталықтарды іздеу"
            ),
            "https://2gis.kz/"
        )

        st.caption(L(
            "Справочный каталог, а не медицинский рейтинг. "
            "Уточняйте расписание и условия госпитализации. "
            "Отзывы не гарантируют результат лечения.",
            "Бұл медициналық рейтинг емес. "
            "Қабылдау кестесін орталықтан нақтылаңыз."
        ))

    with support:
        render_support(language)


# ==========================================
# TECHNICAL SUPPORT
# ==========================================

DB = (
    Path.home()
    / ".neurokinetics"
    / "support.sqlite3"
)

DB.parent.mkdir(
    parents=True,
    exist_ok=True
)


def render_support(language="Русский"):

    kz = language == "Қазақша"

    def L(ru, kk):
        return kk if kz else ru

    st.header("🎧 NeuroSupport")

    st.write(L(
        "Техническая помощь пользователям",
        "Пайдаланушыларға техникалық көмек"
    ))

    st.info(L(
        "Демонстрационная служба поддержки. "
        "Обращения сохраняются локально, "
        "но пока не отправляются сотрудникам.",
        "Демонстрациялық қолдау қызметі. "
        "Өтініштер жергілікті сақталады, "
        "қызметкерлерге жіберілмейді."
    ))

    with sqlite3.connect(DB) as con:

        con.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id TEXT PRIMARY KEY,
                topic TEXT,
                created TEXT
            )
        """)

    with st.form("nk_support_form"):

        topic = st.selectbox(
            L("Тема обращения", "Өтініш тақырыбы"),
            [
                L("Ошибка приложения", "Қолданба қатесі"),
                L("Проблема с 3D", "3D мәселесі"),
                L("Проблема с ИИ", "ЖИ мәселесі"),
                L("Уведомления", "Хабарландырулар"),
                L("Другой вопрос", "Басқа сұрақ")
            ]
        )

        submit = st.form_submit_button(
            L(
                "Создать обращение",
                "Өтініш жасау"
            )
        )

    if submit:

        ticket = "NK-" + uuid.uuid4().hex[:8].upper()

        with sqlite3.connect(DB) as con:

            con.execute(
                "INSERT INTO tickets VALUES (?,?,?)",
                (
                    ticket,
                    topic,
                    datetime.now().strftime(
                        "%d.%m.%Y %H:%M"
                    )
                )
            )

        st.success(
            L("Обращение сохранено: ", "Өтініш сақталды: ")
            + ticket
        )

    st.subheader(L(
        "Мои обращения",
        "Менің өтініштерім"
    ))

    with sqlite3.connect(DB) as con:

        rows = con.execute(
            "SELECT * FROM tickets ORDER BY rowid DESC"
        ).fetchall()

    for ticket, topic, created in rows:

        with st.container(border=True):

            st.markdown("**" + ticket + "**")

            st.write(topic)

            st.caption(created)

            st.caption(L(
                "Сохранено локально · не отправлено",
                "Жергілікті сақталды"
            ))

    st.subheader(L(
        "Частые вопросы",
        "Жиі қойылатын сұрақтар"
    ))

    faq = [
        (
            "Почему не работает ИИ?",
            "Проверьте подключение Ollama."
        ),
        (
            "Почему не открывается 3D?",
            "Проверьте интернет и поддержку WebGL."
        ),
        (
            "Как получать уведомления?",
            "Импортируйте файл напоминаний из календаря."
        ),
        (
            "Как записаться к врачу?",
            "Используйте официальные контакты центра."
        ),
        (
            "Можно ли получить медицинский диагноз?",
            "Нет. NeuroKinetics — исследовательский прототип."
        )
    ]

    for question, answer in faq:

        with st.expander(question):
            st.write(answer)

    st.caption(
        "Не вводите личные и медицинские данные."
    )
