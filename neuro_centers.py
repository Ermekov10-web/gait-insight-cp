
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

    import sqlite3
    import uuid

    from datetime import datetime
    from urllib.parse import urlencode

    EMAIL = "neurokinetics.support@gmail.com"

    kz = language == "Қазақша"
    en = language == "English"

    def L(ru, kk, eng):
        return kk if kz else eng if en else ru

    st.caption("NEUROKINETICS · HELP CENTER")
    st.title("🎧 NeuroSupport")

    st.write(L(
        "Служба поддержки NeuroKinetics",
        "NeuroKinetics қолдау қызметі",
        "NeuroKinetics Support"
    ))

    st.markdown("""
    <div style="
        padding:25px;
        background:linear-gradient(135deg,#123b2b,#091e16);
        border:1px solid #377b56;
        border-radius:18px;
        color:#e0ffec;
    ">
        <small>NEUROSUPPORT</small>
        <h2>How can we help?</h2>
        <p>neurokinetics.support@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    a, b = st.columns(2)

    a.metric(
        L("Канал связи", "Байланыс арнасы", "Contact"),
        "Email"
    )

    b.metric(
        L("Стоимость", "Құны", "Cost"),
        L("Бесплатно", "Тегін", "Free")
    )

    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id TEXT PRIMARY KEY,
                topic TEXT,
                created TEXT
            )
        """)

    if "nk_support_history" not in st.session_state:
        st.session_state.nk_support_history = []

    create, history, faq = st.tabs([
        L("Новое обращение", "Жаңа өтініш", "New ticket"),
        L("Мои обращения", "Менің өтініштерім", "My tickets"),
        "FAQ"
    ])

    with create:

        st.info(L(
            "Не указывайте персональные данные, диагнозы "
            "или медицинские документы.",
            "Жеке және медициналық деректерді енгізбеңіз.",
            "Do not include personal or medical information."
        ))

        with st.form("neuro_support_email_form"):

            topic = st.selectbox(
                L("Тема", "Тақырып", "Subject"),
                [
                    L("Ошибка сайта", "Сайт қатесі", "Website error"),
                    L("Проблема с ИИ", "ЖИ мәселесі", "AI issue"),
                    L("Проблема с 3D", "3D мәселесі", "3D issue"),
                    L("Уведомления", "Хабарландырулар", "Notifications"),
                    L("Предложение", "Ұсыныс", "Suggestion"),
                    L("Другой вопрос", "Басқа сұрақ", "Other")
                ]
            )

            message = st.text_area(
                L(
                    "Опишите техническую проблему",
                    "Техникалық мәселені сипаттаңыз",
                    "Describe the technical problem"
                ),
                height=160,
                max_chars=1500
            )

            submit = st.form_submit_button(
                L(
                    "Подготовить обращение",
                    "Өтініш дайындау",
                    "Prepare ticket"
                ),
                type="primary"
            )

        if submit:

            if not message.strip():

                st.warning(L(
                    "Добавьте описание проблемы.",
                    "Мәселені сипаттаңыз.",
                    "Please describe the issue."
                ))

            else:

                ticket = "NK-" + uuid.uuid4().hex[:8].upper()

                created = datetime.now().strftime(
                    "%d.%m.%Y %H:%M"
                )

                body = (
                    f"NeuroKinetics Support\n\n"
                    f"Ticket: {ticket}\n"
                    f"Date: {created}\n"
                    f"Topic: {topic}\n\n"
                    f"{message.strip()}\n"
                )

                url = (
                    "https://mail.google.com/mail/?"
                    + urlencode({
                        "view": "cm",
                        "fs": "1",
                        "to": EMAIL,
                        "su": f"{ticket} | {topic}",
                        "body": body
                    })
                )

                with sqlite3.connect(DB) as con:

                    con.execute(
                        "INSERT INTO tickets "
                        "(id, topic, created) VALUES (?, ?, ?)",
                        (ticket, topic, created)
                    )

                st.session_state.nk_support_history.insert(
                    0,
                    {
                        "id": ticket,
                        "topic": topic,
                        "date": created,
                        "url": url,
                        "body": body
                    }
                )

        if st.session_state.nk_support_history:

            item = st.session_state.nk_support_history[0]

            st.success(
                L(
                    "Обращение подготовлено: ",
                    "Өтініш дайын: ",
                    "Ticket prepared: "
                ) + item["id"]
            )

            st.link_button(
                L(
                    "📨 Открыть Gmail и отправить",
                    "📨 Gmail арқылы жіберу",
                    "📨 Open Gmail and send"
                ),
                item["url"]
            )

            st.caption(L(
                "В Gmail нажмите «Отправить». "
                "Отправка пока не подтверждена.",
                "Gmail ішінде жіберу батырмасын басыңыз.",
                "Press Send in Gmail. Delivery is not confirmed."
            ))

            with st.expander(L(
                "Скопировать текст обращения",
                "Өтініш мәтінін көшіру",
                "Copy ticket text"
            )):
                st.code(item["body"], language="text")

    with history:

        if not st.session_state.nk_support_history:

            st.info(L(
                "В текущем сеансе обращений пока нет.",
                "Ағымдағы сеанста өтініштер жоқ.",
                "No tickets in this session."
            ))

        for item in st.session_state.nk_support_history:

            with st.container(border=True):

                st.markdown("### " + item["id"])
                st.write(item["topic"])
                st.caption(item["date"])

                st.caption(L(
                    "Подготовлено · отправка не подтверждена",
                    "Дайындалды · жіберу расталмаған",
                    "Prepared · delivery unconfirmed"
                ))

                st.link_button(
                    L("Открыть письмо", "Хатты ашу", "Open email"),
                    item["url"]
                )

    with faq:

        questions = [
            (
                "Почему не работает 3D-модель?",
                "Проверьте интернет и поддержку WebGL."
            ),
            (
                "Почему не отвечает NeuroCare AI?",
                "Проверьте доступность сервера ИИ."
            ),
            (
                "Как получать уведомления?",
                "Добавьте напоминания из календаря приложения."
            ),
            (
                "Как связаться с разработчиками?",
                EMAIL
            )
        ]

        for question, answer in questions:

            with st.expander(question):
                st.write(answer)

    st.divider()
    st.caption("NeuroKinetics © 2026 · Support Team")

