
import ast
from pathlib import Path
from datetime import datetime

import streamlit as st
import pandas as pd


def render_rehab(language="Русский"):

    def L(ru, kz, en):
        return {
            "Русский": ru,
            "Қазақша": kz,
            "English": en
        }.get(language, ru)

    st.caption("NEUROKINETICS / NEUROREHAB")

    st.title(
        L(
            "Маленькие шаги. Значимые цели.",
            "Кішкентай қадамдар. Маңызды мақсаттар.",
            "Small steps. Meaningful goals."
        )
    )

    st.write(
        L(
            "Образовательная библиотека для семей "
            "и специалистов по реабилитации.",
            "Отбасылар мен мамандарға арналған "
            "оңалту кітапханасы.",
            "An educational rehabilitation library "
            "for families and professionals."
        )
    )

    st.warning(
        L(
            "Не начинайте новые лечебные упражнения "
            "без согласования со специалистом.",
            "Жаңа емдік жаттығуларды маманмен "
            "келісусіз бастамаңыз.",
            "Consult a qualified professional "
            "before starting new therapeutic exercises."
        )
    )

    library, goals, journal = st.tabs([
        L(
            "Видеобиблиотека",
            "Бейне кітапхана",
            "Video library"
        ),
        L(
            "Цели реабилитации",
            "Оңалту мақсаттары",
            "Rehabilitation goals"
        ),
        L(
            "Дневник",
            "Күнделік",
            "Journal"
        )
    ])

    # =====================================
    # EXPERT VIDEO LIBRARY
    # =====================================

    resources = [

        {
            "country": L(
                "Казахстан", "Қазақстан", "Kazakhstan"
            ),

            "flag": "🇰🇿",

            "institution": L(
                "Национальный центр детской реабилитации",
                "Ұлттық балаларды оңалту орталығы",
                "National Center for Children's Rehabilitation"
            ),

            "title": L(
                "Как проходит реабилитация",
                "Оңалту қалай өтеді",
                "Understanding rehabilitation"
            ),

            "description": L(
                "Интервью со специалистом о комплексной "
                "реабилитации и сотрудничестве с семьёй.",
                "Кешенді оңалту және отбасымен "
                "бірлескен жұмыс туралы сұхбат.",
                "An expert interview about multidisciplinary "
                "rehabilitation and family collaboration."
            ),

            "url": "https://www.youtube.com/watch?v=IEf01sELcB8",

            "video": True,

            "language": "Русский"
        },

        {
            "country": L(
                "Россия", "Ресей", "Russia"
            ),

            "flag": "🇷🇺",

            "institution": L(
                "Фонд «Обнажённые сердца»",
                "«Жалаңаш жүректер» қоры",
                "Naked Heart Foundation"
            ),

            "title": L(
                "Роль семьи в реабилитации",
                "Оңалтудағы отбасының рөлі",
                "Family-centered rehabilitation"
            ),

            "description": L(
                "Обсуждение подходов к поддержке "
                "детей с церебральным параличом.",
                "Церебралды сал ауруы бар балаларды "
                "қолдау тәсілдері.",
                "A discussion of approaches to "
                "supporting children with cerebral palsy."
            ),

            "url": "https://www.youtube.com/watch?v=BifnWt9bNco",

            "video": True,

            "language": "Русский"
        },

        {
            "country": L(
                "Индия", "Үндістан", "India"
            ),

            "flag": "🇮🇳",

            "institution": "CanChild / Kasturba Medical College",

            "title": L(
                "Движение и повседневная жизнь",
                "Қозғалыс және күнделікті өмір",
                "Movement and everyday life"
            ),

            "description": L(
                "Образовательные материалы с участием "
                "профессора физиотерапии Амитеша Нараяна.",
                "Физиотерапия профессоры Амитеш "
                "Нараян қатысқан оқу материалдары.",
                "Educational resources involving "
                "physiotherapy professor Amitesh Narayan."
            ),

            "url": "https://canchild.ca/the-icf-for-parents-p-icf/",

            "video": False,

            "language": "English"
        },

        {
            "country": L(
                "Австралия", "Аустралия", "Australia"
            ),

            "flag": "🇦🇺",

            "institution": "Cerebral Palsy Alliance",

            "title": L(
                "Библиотека занятий cpThrive",
                "cpThrive жаттығулар кітапханасы",
                "cpThrive activity library"
            ),

            "description": L(
                "Видеоматериалы о движении, занятиях "
                "и участии в повседневной жизни.",
                "Қозғалыс пен күнделікті "
                "белсенділік туралы бейнематериалдар.",
                "Video resources about movement "
                "and everyday participation."
            ),

            "url": (
                "https://cerebralpalsy.org.au/"
                "news-stories/"
                "cpthrive-cerebral-palsy-treatment-app/"
            ),

            "video": False,

            "language": "English"
        },

        {
            "country": L(
                "Великобритания",
                "Ұлыбритания",
                "United Kingdom"
            ),

            "flag": "🇬🇧",

            "institution": "NHS",

            "title": L(
                "Что такое физическая терапия?",
                "Физикалық терапия дегеніміз не?",
                "Understanding physiotherapy"
            ),

            "description": L(
                "Объяснение основных направлений "
                "помощи людям с церебральным параличом.",
                "Церебралды сал ауруы бар адамдарға "
                "көмек көрсету бағыттары.",
                "An overview of treatment and "
                "rehabilitation approaches."
            ),

            "url": (
                "https://www.nhs.uk/"
                "conditions/cerebral-palsy/treatment/"
            ),

            "video": False,

            "language": "English"
        }
    ]

    with library:

        st.subheader(
            L(
                "Материалы специалистов",
                "Мамандар материалдары",
                "Expert resources"
            )
        )

        all_countries = L(
            "Все страны",
            "Барлық елдер",
            "All countries"
        )

        countries = [all_countries] + [
            item["country"] for item in resources
        ]

        country = st.selectbox(
            L(
                "Выберите страну",
                "Елді таңдаңыз",
                "Select country"
            ),
            countries,
            key="rehab_country"
        )

        filtered = [
            item for item in resources

            if country == all_countries
            or item["country"] == country
        ]

        for i, item in enumerate(filtered):

            with st.container(border=True):

                st.caption(
                    item["flag"] + " " + item["country"]
                )

                st.subheader(item["title"])

                st.markdown(
                    "**" + item["institution"] + "**"
                )

                st.write(item["description"])

                st.caption(
                    L(
                        "Язык оригинала: ",
                        "Түпнұсқа тілі: ",
                        "Original language: "
                    ) + item["language"]
                )

                if item["video"]:

                    if st.checkbox(
                        L(
                            "Показать видео",
                            "Бейнені көрсету",
                            "Show video"
                        ),
                        key=f"rehab_video_{i}_{country}"
                    ):

                        st.video(item["url"])

                st.link_button(
                    L(
                        "Открыть оригинальный материал",
                        "Түпнұсқа материалды ашу",
                        "Open original resource"
                    ),
                    item["url"]
                )

        st.caption(
            L(
                "Материалы принадлежат их авторам. "
                "Они не являются индивидуальной "
                "программой лечения.",
                "Материалдар авторларына тиесілі. "
                "Бұл жеке емдеу бағдарламасы емес.",
                "Resources belong to their authors. "
                "They are not individual treatment plans."
            )
        )

    # =====================================
    # REHABILITATION GOALS
    # =====================================

    with goals:

        st.header(
            L(
                "Что важно для вас?",
                "Сіз үшін не маңызды?",
                "What matters to you?"
            )
        )

        st.write(
            L(
                "Выберите темы, которые хотите "
                "обсудить с физиотерапевтом.",
                "Маманмен талқылайтын "
                "тақырыптарды таңдаңыз.",
                "Choose topics to discuss "
                "with your physiotherapist."
            )
        )

        topics = [

            L(
                "Ходьба и мобильность",
                "Жүру және қозғалыс",
                "Walking and mobility"
            ),

            L(
                "Равновесие и координация",
                "Тепе-теңдік пен үйлесімділік",
                "Balance and coordination"
            ),

            L(
                "Движения рук и мелкая моторика",
                "Қол қозғалысы және ұсақ моторика",
                "Hand movement and fine motor skills"
            ),

            L(
                "Самостоятельность в быту",
                "Күнделікті дербестік",
                "Daily independence"
            ),

            L(
                "Участие в играх и занятиях",
                "Ойындар мен іс-шараларға қатысу",
                "Participation in play and activities"
            )
        ]

        selected = []

        for i, topic in enumerate(topics):

            with st.container(border=True):

                if st.checkbox(
                    topic,
                    key=f"rehab_goal_{i}"
                ):
                    selected.append(topic)

        st.metric(
            L(
                "Выбрано тем",
                "Таңдалған тақырыптар",
                "Selected topics"
            ),
            len(selected)
        )

        if selected:

            text = "\n".join(
                f"{i + 1}. {topic}"
                for i, topic in enumerate(selected)
            )

            st.download_button(
                L(
                    "Скачать список для врача",
                    "Дәрігерге арналған тізімді жүктеу",
                    "Download discussion list"
                ),
                text.encode("utf-8-sig"),
                file_name="rehabilitation_goals.txt",
                mime="text/plain"
            )

        st.info(
            L(
                "Специалист поможет определить "
                "подходящие упражнения и нагрузку.",
                "Маман қолайлы жаттығулар мен "
                "жүктемені анықтауға көмектеседі.",
                "A professional can help select "
                "appropriate exercises and activity levels."
            )
        )

    # =====================================
    # OBSERVATION JOURNAL
    # =====================================

    with journal:

        st.header(
            L(
                "Дневник занятий",
                "Жаттығу күнделігі",
                "Activity journal"
            )
        )

        st.write(
            L(
                "Отмечайте занятия, которые уже "
                "были согласованы со специалистом.",
                "Маманмен келісілген "
                "жаттығуларды белгілеңіз.",
                "Record activities already "
                "agreed with your professional."
            )
        )

        if "rehab_records" not in st.session_state:
            st.session_state.rehab_records = []

        with st.form("rehab_record_form"):

            day = st.date_input(
                L("Дата", "Күні", "Date")
            )

            activity = st.text_input(
                L(
                    "Название согласованного занятия",
                    "Келісілген жаттығу атауы",
                    "Name of agreed activity"
                )
            )

            status = st.radio(
                L(
                    "Как прошло занятие?",
                    "Жаттығу қалай өтті?",
                    "How did the activity go?"
                ),
                [
                    L("Выполнено", "Орындалды", "Completed"),
                    L("Частично", "Жартылай", "Partially"),
                    L("Пропущено", "Өткізілді", "Skipped")
                ]
            )

            submitted = st.form_submit_button(
                L(
                    "Сохранить запись",
                    "Жазбаны сақтау",
                    "Save entry"
                )
            )

            if submitted and activity.strip():

                st.session_state.rehab_records.append({
                    "Date": str(day),
                    "Activity": activity.strip(),
                    "Status": status
                })

                st.success(
                    L(
                        "Запись сохранена.",
                        "Жазба сақталды.",
                        "Entry saved."
                    )
                )

        records = st.session_state.rehab_records

        if records:

            st.metric(
                L(
                    "Записей в дневнике",
                    "Күнделік жазбалары",
                    "Journal entries"
                ),
                len(records)
            )

            table = pd.DataFrame(records)

            st.dataframe(
                table,
                width="stretch",
                hide_index=True
            )

            st.download_button(
                L(
                    "Скачать дневник",
                    "Күнделікті жүктеу",
                    "Download journal"
                ),
                table.to_csv(
                    index=False
                ).encode("utf-8-sig"),
                file_name="neurorehab_journal.csv",
                mime="text/csv"
            )

        st.caption(
            L(
                "Записи хранятся в текущей сессии. "
                "Не вводите личные медицинские данные. "
                "Количество занятий не является "
                "показателем клинического улучшения.",
                "Жазбалар ағымдағы сессияда сақталады. "
                "Жеке медициналық деректерді енгізбеңіз.",
                "Records are stored in the current session. "
                "Do not enter private medical information. "
                "Activity counts do not measure clinical improvement."
            )
        )

    st.divider()

    st.subheader(
        L(
            "Научная основа",
            "Ғылыми негіз",
            "Scientific evidence"
        )
    )

    st.write(
        L(
            "Международные рекомендации подчёркивают "
            "важность индивидуальных целей и "
            "сотрудничества семьи со специалистами.",
            "Халықаралық ұсыныстар жеке мақсаттар "
            "мен мамандармен ынтымақтастықты қолдайды.",
            "International guidelines emphasize "
            "individual goals and family collaboration."
        )
    )

    st.link_button(
        L(
            "Международные клинические рекомендации",
            "Халықаралық клиникалық ұсыныстар",
            "International clinical practice guideline"
        ),
        "https://doi.org/10.1111/dmcn.15055"
    )


# =========================================
# AUTOMATIC WEBSITE INTEGRATION
# =========================================

def install():

    app = Path(__file__).resolve().parent / "app.py"

    if not app.exists():
        raise SystemExit("Файл app.py не найден.")

    source = app.read_text(encoding="utf-8")

    if "# NEUROREHAB_INSTALLED" in source:
        print("NeuroRehab уже подключён.")
        return

    tree = ast.parse(source)

    lines = source.splitlines(keepends=True)

    edits = []

    pages_dictionary = next(
        (
            node for node in tree.body

            if isinstance(node, ast.Assign)

            and any(
                isinstance(target, ast.Name)
                and target.id == "PAGES"

                for target in node.targets
            )
        ),
        None
    )

    if pages_dictionary is None:
        raise SystemExit(
            "Версия app.py отличается. "
            "Исходный файл не изменён."
        )

    edits.append((
        pages_dictionary.end_lineno,

        '\n# NEUROREHAB_INSTALLED\n'
        'PAGES["rehab"] = L('
        '"Занятия и реабилитация", '
        '"Жаттығулар және оңалту", '
        '"Activities and Rehabilitation")\n'
    ))

    menus = 0

    for node in ast.walk(tree):

        if not isinstance(node, ast.Assign):
            continue

        if not isinstance(node.value, ast.List):
            continue

        if not any(
            isinstance(t, ast.Name)
            and t.id == "pages"

            for t in node.targets
        ):
            continue

        values = [
            item.value
            for item in node.value.elts

            if isinstance(item, ast.Constant)
        ]

        if "guide" not in values:
            continue

        indent = " " * node.col_offset

        edits.append((
            node.end_lineno,
            indent + 'pages.append("rehab")\n'
        ))

        menus += 1

    if menus != 2:
        raise SystemExit(
            "Не удалось определить оба кабинета. "
            "Файл app.py не изменён."
        )

    position = next(
        (
            i for i, line in enumerate(lines)

            if line.strip() == 'elif page == "guide":'
            and not line.startswith((" ", "\t"))
        ),
        None
    )

    if position is None:
        raise SystemExit(
            "Навигация не найдена. "
            "Файл app.py не изменён."
        )

    edits.append((
        position,

        'elif page == "rehab":\n'
        '    from neurorehab import render_rehab\n'
        '    render_rehab(language)\n\n'
    ))

    for position, text in sorted(
        edits,
        key=lambda item: item[0],
        reverse=True
    ):
        lines.insert(position, text)

    updated = "".join(lines)

    compile(updated, str(app), "exec")

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup = app.with_name(
        f"app_backup_rehab_{timestamp}.py"
    )

    backup.write_text(
        source,
        encoding="utf-8"
    )

    app.write_text(
        updated,
        encoding="utf-8"
    )

    print("NeuroRehab успешно подключён!")
    print("Добавлен в оба кабинета.")
    print("Резервная копия создана.")
    print("Остальные разделы сохранены.")


if __name__ == "__main__":
    install()
