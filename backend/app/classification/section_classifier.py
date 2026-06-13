# backend/app/classifiers/section_classifier.py

import re
from backend.app.models.document import (
    DocumentModel
)

from backend.app.config.semantic_types import (
    UDC,
    TITLE_RU,
    TITLE_EN,
    AUTHORS,
    AFFILIATION,
    EMAIL,
    ABSTRACT_RU,
    ABSTRACT_EN,
    KEYWORDS_RU,
    KEYWORDS_EN,
    BODY,
    INTRODUCTION,
    CONCLUSION,
    CAPTION,
    TABLE_CAPTION,
    TABLE_NOTE,
    REFERENCES_HEADER,
    REFERENCE_ITEM,
    EQUATION,
    TITLE_PAGE,
    ASSIGNMENT,
    CONTENTS,
    TERMS,
    ABBREVIATIONS,
    ANALYTICAL_SECTION,
    SPECIAL_SECTION,
    LIFE_SAFETY_SECTION,
    ECONOMIC_EFFICIENCY_SECTION,
    STUDENT_PUBLICATIONS,
    APPENDIX,
    SUBSECTION_HEADER, 
    SECTION_HEADER,
)

from backend.app.config.classifier_rules import (
    UDC_PREFIXES,
    REFERENCES_HEADERS,
    REFERENCES_CONTAINS,
    KEYWORDS_RU_PREFIXES,
    KEYWORDS_EN_PREFIXES,
    AFFILIATION_KEYWORDS,
    FIGURE_CAPTION_PATTERN,
    TABLE_CAPTION_PATTERN,
    AUTHOR_PATTERN,
    CYRILLIC_PATTERN,
    TITLE_MIN_FONT_SIZE,
    AUTHORS_FONT_SIZE,
    INTRODUCTION_HEADERS,
    CONCLUSION_HEADERS,
    CHAPTER_CONCLUSION_HEADERS,
    TITLE_PAGE_HEADERS,
    ASSIGNMENT_HEADERS,
    CONTENTS_HEADERS,
    TERMS_HEADERS,
    ABBREVIATIONS_HEADERS,
    ANALYTICAL_SECTION_HEADERS,
    SPECIAL_SECTION_HEADERS,
    ANALYTICAL_SECTION_PREFIXES,    
    LIFE_SAFETY_HEADERS,
    ECONOMIC_EFFICIENCY_HEADERS,
    STUDENT_PUBLICATIONS_HEADERS,
    APPENDIX_HEADERS,
    ABSTRACT_RU_HEADERS,
    ABSTRACT_EN_HEADERS,
)


class SectionClassifier:

    @staticmethod
    def _normalize_header(
        text: str,
    ) -> str:
        normalized_text = text.strip().lower()

        normalized_text = re.sub(
            r"^\d+(\.\d+)*\.?\s*",
            "",
            normalized_text,
        )

        normalized_text = re.sub(
            r"\s+",
            " ",
            normalized_text,
        )

        return normalized_text.strip()

    @staticmethod
    def _matches_header(
        text: str,
        headers: tuple[str, ...],
    ) -> bool:
        normalized_text = SectionClassifier._normalize_header(
            text
        )

        return any(
            normalized_text == header
            or normalized_text.startswith(f"{header} ")
            for header in headers
        )    

    @staticmethod
    def classify(
        document: DocumentModel,
        check_type: str = "csm_conference",
    ) -> DocumentModel:

        inside_references = False

        inside_ru_abstract = False
        inside_en_abstract = False

        inside_introduction = False
        inside_conclusion = False
        inside_contents = False
        main_part_started = False
        inside_title_page = check_type == "vkr"
        inside_assignment = False
        inside_appendix = False
    
        def reset_context():
            nonlocal inside_references
            nonlocal inside_ru_abstract
            nonlocal inside_en_abstract
            nonlocal inside_introduction
            nonlocal inside_conclusion
            nonlocal inside_contents
            nonlocal inside_title_page
            nonlocal inside_assignment        
            nonlocal inside_appendix    

            inside_references = False
            inside_ru_abstract = False
            inside_en_abstract = False
            inside_introduction = False
            inside_conclusion = False    
            inside_contents = False
            inside_title_page = False
            inside_assignment = False  
            inside_appendix = False          

        for paragraph in document.paragraphs:

            text = (
                paragraph.text.strip()
            )

            lower_text = (
                text.lower()
            )

            if not text:
                continue
            if (
                check_type == "vkr"
                and not main_part_started
            ):

                if SectionClassifier._is_assignment_heading(text):

                    paragraph.semantic_type = (
                        ASSIGNMENT
                    )

                    reset_context()

                    inside_assignment = True

                    continue

                if (
                    SectionClassifier._matches_header(
                        text,
                        ABSTRACT_RU_HEADERS,
                    )
                    or SectionClassifier._matches_header(
                        text,
                        ABSTRACT_EN_HEADERS,
                    )
                ):

                    reset_context()

                elif inside_assignment:

                    paragraph.semantic_type = (
                        ASSIGNMENT
                    )

                    continue

                elif inside_title_page:

                    paragraph.semantic_type = (
                        TITLE_PAGE
                    )

                    continue

            if (
                check_type == "vkr"
                and not main_part_started
                and SectionClassifier._looks_like_contents_line(text)
            ):

                paragraph.semantic_type = (
                    CONTENTS
                )

                continue            

            if (
                check_type == "vkr"
                and inside_contents
            ):

                if (
                    SectionClassifier._matches_header(
                        text,
                        INTRODUCTION_HEADERS,
                    )
                    or paragraph.font_size == 14
                ):

                    reset_context()

                else:

                    paragraph.semantic_type = (
                        CONTENTS
                    )

                    continue

            # UDC

            if lower_text.startswith(
                UDC_PREFIXES
            ):

                paragraph.semantic_type = (
                    UDC
                )

                continue

            # VKR title page

            if SectionClassifier._matches_header(text, TITLE_PAGE_HEADERS):

                paragraph.semantic_type = (
                    TITLE_PAGE
                )

                reset_context()

                continue

            # VKR assignment

            if SectionClassifier._matches_header(text, ASSIGNMENT_HEADERS):

                paragraph.semantic_type = (
                    ASSIGNMENT
                )

                reset_context()

                continue

            # VKR contents

            if (
                check_type == "vkr"
                and SectionClassifier._is_exact_header(
                    text,
                    CONTENTS_HEADERS,
                )
            ):

                paragraph.semantic_type = (
                    CONTENTS
                )

                reset_context()

                inside_contents = True

                continue

            # VKR terms

            if SectionClassifier._matches_header(text, TERMS_HEADERS):

                paragraph.semantic_type = (
                    TERMS
                )

                reset_context()

                continue

            # VKR abbreviations

            if SectionClassifier._matches_header(text, ABBREVIATIONS_HEADERS):

                paragraph.semantic_type = (
                    ABBREVIATIONS
                )

                reset_context()

                continue

            # VKR analytical section

            if (
                check_type != "vkr"
                or main_part_started
            ) and (
                SectionClassifier._is_vkr_section_header(
                    text,
                    ANALYTICAL_SECTION_HEADERS,
                )
                or any(
                    SectionClassifier._normalize_header(
                        text
                    ).startswith(prefix)
                    for prefix in ANALYTICAL_SECTION_PREFIXES
                )
            ):

                paragraph.semantic_type = (
                    ANALYTICAL_SECTION
                )

                reset_context()

                continue

            # VKR special section

            if (
                check_type != "vkr"
                or main_part_started
            ) and SectionClassifier._is_vkr_section_header(text, SPECIAL_SECTION_HEADERS):

                paragraph.semantic_type = (
                    SPECIAL_SECTION
                )

                reset_context()

                continue

            # VKR life safety section

            if (
                check_type != "vkr"
                or main_part_started
            ) and SectionClassifier._is_vkr_section_header(text, LIFE_SAFETY_HEADERS):

                paragraph.semantic_type = (
                    LIFE_SAFETY_SECTION
                )

                reset_context()

                continue

            # VKR economic efficiency section

            if (
                check_type != "vkr"
                or main_part_started
            ) and SectionClassifier._is_vkr_section_header(text, ECONOMIC_EFFICIENCY_HEADERS):

                paragraph.semantic_type = (
                    ECONOMIC_EFFICIENCY_SECTION
                )

                reset_context()

                continue

            # VKR student publications

            if (
                check_type != "vkr"
                or main_part_started
            ) and SectionClassifier._matches_header(text, STUDENT_PUBLICATIONS_HEADERS):

                paragraph.semantic_type = (
                    STUDENT_PUBLICATIONS
                )

                reset_context()

                continue

            # VKR appendix

            if (
                check_type != "vkr"
                or main_part_started
            ) and (SectionClassifier._matches_header(text, APPENDIX_HEADERS)
                or lower_text.startswith("приложение ")
            ):

                paragraph.semantic_type = (
                    APPENDIX
                )

                reset_context()

                inside_appendix = True

                continue

            # Abstract RU header

            if SectionClassifier._matches_header(text, ABSTRACT_RU_HEADERS):

                paragraph.semantic_type = (
                    SECTION_HEADER
                )

                reset_context()

                inside_ru_abstract = True

                continue

            # Abstract EN header

            if SectionClassifier._matches_header(text, ABSTRACT_EN_HEADERS):

                paragraph.semantic_type = (
                    SECTION_HEADER
                )

                reset_context()

                inside_en_abstract = True

                continue       

            # References

            if (
                (
                    check_type != "vkr"
                    or main_part_started
                ) 
                and  (
                    SectionClassifier._matches_header(
                        text, 
                        REFERENCES_HEADERS,
                    )
                    or any(
                        item in lower_text
                        for item in REFERENCES_CONTAINS
                    )
                )
            ):

                paragraph.semantic_type = (
                    REFERENCES_HEADER
                )

                reset_context()

                inside_references = True

                continue

            if inside_references:

                paragraph.semantic_type = (
                    REFERENCE_ITEM
                )

                continue

            if (
                inside_ru_abstract
                and SectionClassifier._matches_header(text, ABSTRACT_EN_HEADERS)
            ):

                inside_ru_abstract = False
                inside_en_abstract = True

                paragraph.semantic_type = (
                    ABSTRACT_EN
                )

                continue

            # Keywords RU

            if lower_text.startswith(
                KEYWORDS_RU_PREFIXES
            ):

                paragraph.semantic_type = (
                    KEYWORDS_RU
                )

                inside_ru_abstract = False

                continue

            # Keywords EN

            if lower_text.startswith(
                KEYWORDS_EN_PREFIXES
            ):

                paragraph.semantic_type = (
                    KEYWORDS_EN
                )

                inside_en_abstract = False

                continue

            # Introduction

            if SectionClassifier._matches_header(text, INTRODUCTION_HEADERS):

                paragraph.semantic_type = (
                    SECTION_HEADER
                )

                reset_context()
                
                inside_introduction = True
                main_part_started = True

                continue

            # Chapter conclusion

            if (
                check_type == "vkr"
                and SectionClassifier._matches_header(
                    text,
                    CHAPTER_CONCLUSION_HEADERS,
                )
            ):

                paragraph.semantic_type = (
                    SUBSECTION_HEADER
                )

                continue

            # Conclusion

            if SectionClassifier._matches_header(text, CONCLUSION_HEADERS):

                paragraph.semantic_type = (
                    CONCLUSION
                )

                reset_context()

                inside_conclusion = True

                continue

            # Figure caption

            if FIGURE_CAPTION_PATTERN.match(
                lower_text
            ):

                paragraph.semantic_type = (
                    CAPTION
                )

                continue

            # Table caption

            if TABLE_CAPTION_PATTERN.match(
                lower_text
            ):

                paragraph.semantic_type = (
                    TABLE_CAPTION
                )

                continue

            # Table continuation

            if (
                lower_text.startswith(
                    "продолжение таблицы"
                )
                or lower_text.startswith(
                    "окончание таблицы"
                )
            ):

                paragraph.semantic_type = (
                    TABLE_CAPTION
                )

                continue

            # Table note

            if (
                lower_text.startswith(
                    "примечание"
                )
                or text.startswith("*")
            ):

                paragraph.semantic_type = (
                    TABLE_NOTE
                )

                continue


            if (
                check_type == "vkr"
                and main_part_started
                and not inside_appendix
                and paragraph.bold
                and paragraph.alignment == "left"
                and paragraph.font_size == 14
                and len(text) < 150
            ):

                paragraph.semantic_type = (
                    SUBSECTION_HEADER
                )

                continue

            # Titles

            if (
                paragraph.alignment == "center"
                and paragraph.bold
                and paragraph.font_size
                and paragraph.font_size >= TITLE_MIN_FONT_SIZE
            ):

                has_cyrillic = bool(
                    CYRILLIC_PATTERN.search(
                        text
                    )
                )

                if has_cyrillic:

                    paragraph.semantic_type = (
                        TITLE_RU
                    )

                else:

                    paragraph.semantic_type = (
                        TITLE_EN
                    )

                continue

            # Emails

            if (
                check_type != "vkr"
                and "@" in text
            ):

                paragraph.semantic_type = (
                    EMAIL
                )

                continue

            # Authors

            if (
                paragraph.font_size
                == AUTHORS_FONT_SIZE
                and "," in text
                and AUTHOR_PATTERN.search(
                    text
                )
            ):

                paragraph.semantic_type = (
                    AUTHORS
                )

                continue

            # Affiliations

            if any(
                keyword in lower_text
                for keyword in AFFILIATION_KEYWORDS
            ):

                paragraph.semantic_type = (
                    AFFILIATION
                )

                continue

            # Abstract start detection for conference papers only

            if check_type != "vkr":

                previous_index = (
                    document.paragraphs.index(
                        paragraph
                    ) - 1
                )

                previous_paragraph = None

                if previous_index >= 0:

                    previous_paragraph = (
                        document.paragraphs[
                            previous_index
                        ]
                    )

                if (
                    previous_paragraph
                    and previous_paragraph.semantic_type
                    == EMAIL
                ):

                    has_cyrillic = bool(
                        CYRILLIC_PATTERN.search(
                            text
                        )
                    )

                    if has_cyrillic:

                        inside_ru_abstract = True
                        inside_en_abstract = False

                    else:

                        inside_en_abstract = True
                        inside_ru_abstract = False

            # Stop introduction section

            if (
                inside_introduction
                and paragraph.bold
                and paragraph.alignment == "center"
                and len(text) < 100
            ):

                inside_introduction = False            
            
            # Stop conclusion section

            if (
                inside_conclusion
                and (
                SectionClassifier._matches_header(text, REFERENCES_HEADERS)
                or any(
                    item in lower_text
                    for item in REFERENCES_CONTAINS
                    )
                )
            ):

                inside_conclusion = False


            # Body / Abstract / Introduction / Conclusion

            if inside_ru_abstract:

                paragraph.semantic_type = (
                    ABSTRACT_RU
                )

            elif inside_en_abstract:

                paragraph.semantic_type = (
                    ABSTRACT_EN
                )

            elif inside_introduction:

                paragraph.semantic_type = (
                    INTRODUCTION
                )

            elif inside_conclusion:

                paragraph.semantic_type = (
                    CONCLUSION
                )

            elif inside_appendix:

                paragraph.semantic_type = (
                    APPENDIX
                )    

            else:

                paragraph.semantic_type = (
                    BODY
                )

            # Equation
            if (
                "=" in paragraph.text 
                and paragraph.font_family == "Cambria Math"
                and paragraph.alignment == "center"
            ):
                paragraph.semantic_type = (
                    EQUATION
                )

        return document

    @staticmethod
    def _is_exact_header(
        text: str,
        headers: tuple[str, ...],
    ) -> bool:

        normalized_text = (
            SectionClassifier._normalize_header(
                text
            )
        )

        return normalized_text in headers

    @staticmethod
    def _looks_like_contents_line(
        text: str,
    ) -> bool:
        return bool(
            re.search(
                r"^.{5,}\s+\d+\s*$",
                text.strip(),
            )
        )

    @staticmethod
    def _is_vkr_section_header(
        text: str,
        headers: tuple[str, ...],
    ) -> bool:

        normalized_text = (
            SectionClassifier._normalize_header(
                text
            )
        )

        if any(
            normalized_text == header
            or normalized_text.startswith(
                f"{header} "
            )
            for header in headers
        ):
            return True

        if any(
            normalized_text.startswith(
                prefix
            )
            for prefix in ANALYTICAL_SECTION_PREFIXES
        ):
            return True

        return False

    @staticmethod
    def _is_assignment_heading(
        text: str,
    ) -> bool:

        normalized_text = (
            text
            .strip()
            .lower()
            .replace(" ", "")
        )

        return (
            normalized_text == "задание"
            or normalized_text.startswith("заданиена")
        )