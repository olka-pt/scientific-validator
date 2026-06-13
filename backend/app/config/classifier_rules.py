# backend/app/config/classifier_rules.py

import re


UDC_PREFIXES = (
    "удк",
)

REFERENCES_HEADERS = (
    "источники",
    "литература",
    "references",
    "список использованных источников",
    "библиографический список",
)

REFERENCES_CONTAINS = (
    "список литературы",
    "список использованных источников",
)

KEYWORDS_RU_PREFIXES = (
    "ключевые слова",
)

KEYWORDS_EN_PREFIXES = (
    "keywords",
)

AFFILIATION_KEYWORDS = (
    "университет",
    "институт",
    "academy",
    "kazan",
    "россия",
    "russia",
    "кгэу",
    "kgэу",
)

FIGURE_CAPTION_PATTERN = re.compile(
    r"^рис(?:\.|унок)?\s*\d+(?:\.\d+)*\s*[–—-]?",
    re.IGNORECASE,
)

TABLE_CAPTION_PATTERN = re.compile(
    r"^таблица\s*\d+(?:\.\d+)*\s*[–—-]?",
    re.IGNORECASE,
)

AUTHOR_PATTERN = re.compile(
    r"[А-ЯA-Z]\."
)

CYRILLIC_PATTERN = re.compile(
    r"[а-яА-ЯёЁ]"
)

TITLE_MIN_FONT_SIZE = 14

AUTHORS_FONT_SIZE = 12

INTRODUCTION_HEADERS = (
    "введение",
    "introduction",
)

CONCLUSION_HEADERS = (
    "заключение",
    "выводы",
    "conclusion",
    "conclusions",
)

TITLE_PAGE_HEADERS = (
    "титульный лист",
)

ASSIGNMENT_HEADERS = (
    "задание",
    "задание на выполнение вкр",
    "задание на выполнение выпускной квалификационной работы",
)

CONTENTS_HEADERS = (
    "содержание",
    "оглавление",
)

TERMS_HEADERS = (
    "термины и определения",
)

ABBREVIATIONS_HEADERS = (
    "перечень сокращений и обозначений",
    "сокращения и обозначения",
    "перечень сокращений",
)

ANALYTICAL_SECTION_HEADERS = (
    "аналитический раздел",
    "аналитическая часть",
)

ANALYTICAL_SECTION_PREFIXES = (
    "анализ деятельности ооо",
    "анализ предметной области",
)

SPECIAL_SECTION_HEADERS = (
    "специальный раздел",
    "проект информационной системы",
    "проектирование информационной системы",
    "разработка информационной системы",
    "разработка мобильного",
    "программная реализация",
)

LIFE_SAFETY_HEADERS = (
    "безопасность жизнедеятельности",
    "безопасность жизнедеятельности и охрана труда",
    "раздел безопасность жизнедеятельности",
)

ECONOMIC_EFFICIENCY_HEADERS = (
    "расчет экономической эффективности",
    "расчёт экономической эффективности",
    "экономическая эффективность",
    "оценка экономической эффективности",
    "оценка экономической и управленческой эффективности",
    "расчет показателей экономической эффективности",
    "расчёт показателей экономической эффективности",
)

STUDENT_PUBLICATIONS_HEADERS = (
    "список публикаций обучающегося",
    "публикации обучающегося",
)

APPENDIX_HEADERS = (
    "приложения",
    "приложение",
)

ABSTRACT_RU_HEADERS = (
    "аннотация",
)

ABSTRACT_EN_HEADERS = (
    "abstract",
    "annotation",
)

CHAPTER_CONCLUSION_HEADERS = (
    "выводы по главе",
)