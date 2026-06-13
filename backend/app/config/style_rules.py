EXPECTED_FONT_SIZES = {

    "udc": 12,

    "title_ru": 14,
    "title_en": 14,

    "author": 12,
    "affiliation": 12,
    "email": 12,

    "abstract_ru": 12,
    "abstract_en": 12,

    "keywords_ru": 12,
    "keywords_en": 12,

    "introduction": 14,
    "body": 14,
    "conclusion": 14,

    "caption": 12,
    "table_caption": 14,
    "equation": 14,

    "references_header": 14,
    "reference_item": 14,
}


EXPECTED_ALIGNMENTS = {

    "title_ru": "center",
    "title_en": "center",

    "introduction": "justify",
    "body": "justify",
    "conclusion": "justify",

    "abstract_ru": "justify",
    "abstract_en": "justify",

    "keywords_ru": "justify",
    "keywords_en": "justify",

    "equation": "center",
}


EXPECTED_BOLD = {

    "title_ru": True,
    "title_en": True,

    "introduction": False,
    "body": False,
    "conclusion": False,

    "abstract_ru": False,
    "abstract_en": False,

    "keywords_ru": True,
    "keywords_en": True,

    "author": False,
    "affiliation": False,
}

EXPECTED_ITALIC = {

    "title_ru": False,
    "title_en": False,

    "introduction": False,
    "body": False,
    "conclusion": False,

    "abstract_ru": False,
    "abstract_en": False,

    "keywords_ru": False,
    "keywords_en": False,

    "author": False,
    "affiliation": False,
    "email": False,

    "caption": False,
    "table_caption": False,

    "reference_item": False,
    "references_header": False,
}

EXPECTED_LINE_SPACING = {

    "title_ru": 18,
    "title_en": 18,

    "introduction": 18,
    "body": 18,
    "conclusion": 18,

    "abstract_ru": 18,
    "abstract_en": 18,

    "keywords_ru": 18,
    "keywords_en": 18,

    "author": 18,
    "affiliation": 18,
    "email": 18,

    "caption": 18,
    "table_caption": 18,

    "reference_item": 18,
    "references_header": 18,
}

EXPECTED_FIRST_LINE_INDENT = {

    "title_ru": 0,
    "title_en": 0,

    "author": 0,
    "affiliation": 0,
    "email": 0,

    "abstract_ru": 1.25,
    "abstract_en": 1.25,

    "keywords_ru": 1.25,
    "keywords_en": 1.25,

    "introduction": 1.25,
    "body": 1.25,
    "conclusion": 1.25,

    "caption": 0,
    "table_caption": 0,

    "references_header": 0,
    "reference_item": 1.25,
}

EXPECTED_SPACE_BEFORE = {

    "title_ru": 0,
    "title_en": 0,

    "author": 0,
    "affiliation": 0,
    "email": 0,

    "abstract_ru": 0,
    "abstract_en": 0,

    "keywords_ru": 0,
    "keywords_en": 0,

    "body": 0,

    "caption": 0,
    "table_caption": 0,

    "references_header": 0,
    "reference_item": 0,
}

EXPECTED_SPACE_AFTER = {

    "title_ru": 0,
    "title_en": 0,

    "author": 0,
    "affiliation": 0,
    "email": 0,

    "abstract_ru": 0,
    "abstract_en": 0,

    "keywords_ru": 0,
    "keywords_en": 0,

    "body": 0,

    "caption": 0,
    "table_caption": 0,

    "references_header": 0,
    "reference_item": 0,
    
}

EXPECTED_MARGINS = {

    "top": 20.0,
    "bottom": 20.0,

    "left": 20.0,
    "right": 20.0
}

EXPECTED_CSM_MARGINS = {
    "top": 20.0,
    "bottom": 20.0,
    "left": 20.0,
    "right": 20.0,
}

EXPECTED_VKR_MARGINS = {
    "top": 20.0,
    "bottom": 20.0,
    "left": 30.0,
    "right": 15.0,
}

EXPECTED_PAGE_WIDTH = 210.0
EXPECTED_PAGE_HEIGHT = 297.0


EXPECTED_FONT_SIZES["subsection_header"] = 14
# EXPECTED_ALIGNMENTS["subsection_header"] = "justify"
EXPECTED_BOLD["subsection_header"] = True
EXPECTED_ITALIC["subsection_header"] = False
# EXPECTED_LINE_SPACING["subsection_header"] = 18
EXPECTED_FIRST_LINE_INDENT["subsection_header"] = 1.25
# EXPECTED_SPACE_BEFORE["subsection_header"] = 0
# EXPECTED_SPACE_AFTER["subsection_header"] = 0


EXPECTED_FONT_SIZES["table_note"] = 12
EXPECTED_ITALIC["table_note"] = True
EXPECTED_BOLD["table_note"] = False
EXPECTED_FIRST_LINE_INDENT["table_note"] = 0

EXPECTED_FONT_SIZES["section_header"] = 14
EXPECTED_ALIGNMENTS["section_header"] = "center"
EXPECTED_BOLD["section_header"] = True
EXPECTED_ITALIC["section_header"] = False
EXPECTED_LINE_SPACING["section_header"] = 1.0
EXPECTED_FIRST_LINE_INDENT["section_header"] = 0
EXPECTED_SPACE_BEFORE["section_header"] = 0
EXPECTED_SPACE_AFTER["section_header"] = 0