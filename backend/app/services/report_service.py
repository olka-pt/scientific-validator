# backend/app/services/report_service.py

import re
from datetime import datetime
from pathlib import Path

from backend.app.classification.section_classifier import SectionClassifier
from backend.app.config.style_rules import (
    EXPECTED_ALIGNMENTS,
    EXPECTED_BOLD,
    EXPECTED_FIRST_LINE_INDENT,
    EXPECTED_FONT_SIZES,
    EXPECTED_ITALIC,
    EXPECTED_LINE_SPACING,
    EXPECTED_MARGINS,
    EXPECTED_PAGE_HEIGHT,
    EXPECTED_PAGE_WIDTH,
    EXPECTED_SPACE_AFTER,
    EXPECTED_SPACE_BEFORE,
)
from backend.app.rules.content.vkr_structure_rule import (
    VkrStructureRule,
)
from backend.app.normalizer.normalizer import DocumentNormalizer
from backend.app.parser.docx_parser import DocxParser
from backend.app.reporting.pdf_report_generator import PDFValidationReport
from backend.app.rules.content.abstract_length_rule import AbstractLengthRule
from backend.app.rules.content.affiliation_rule import AffiliationRule
from backend.app.rules.content.article_page_count_rule import ArticlePageCountRule
from backend.app.rules.content.author_affiliation_match_rule import AuthorAffiliationMatchRule
from backend.app.rules.content.author_email_match_rule import AuthorEmailMatchRule
from backend.app.rules.content.author_count_rule import AuthorCountRule
from backend.app.rules.content.citation_rule import CitationRule
from backend.app.rules.content.duplicate_reference_rule import DuplicateReferenceRule
from backend.app.rules.content.email_format_rule import EmailFormatRule
from backend.app.rules.content.empty_section_rule import EmptySectionRule
from backend.app.rules.content.equation_layout_rule import EquationLayoutRule
from backend.app.rules.content.equation_number_sequence_rule import EquationNumberSequenceRule
from backend.app.rules.content.equation_reference_rule import EquationReferenceRule
from backend.app.rules.content.equation_rule import EquationRule
from backend.app.rules.content.equation_explanation_rule import EquationExplanationRule
from backend.app.rules.content.figure_rule import FigureRule
from backend.app.rules.content.heading_detection_rule import HeadingDetectionRule
from backend.app.rules.content.keyword_count_rule import KeywordCountRule
from backend.app.rules.content.language_consistency_rule import LanguageConsistencyRule
from backend.app.rules.content.page_numbering_rule import PageNumberingRule
from backend.app.rules.content.reference_format_rule import ReferenceFormatRule
from backend.app.rules.content.reference_year_rule import ReferenceYearRule
from backend.app.rules.content.reference_identifier_rule import ReferenceIdentifierRule
from backend.app.rules.content.foreign_reference_rule import ForeignReferenceRule
from backend.app.rules.content.required_section_rule import RequiredSectionRule
from backend.app.rules.content.section_hierarchy_rule import SectionHierarchyRule
from backend.app.rules.content.section_order_rule import SectionOrderRule
from backend.app.rules.content.sequential_numbering_rule import SequentialNumberingRule
from backend.app.rules.content.table_font_rule import TableFontRule
from backend.app.rules.content.table_rule import TableRule
from backend.app.rules.engine import RuleEngine
from backend.app.rules.formatting.alignment_rule import AlignmentRule
from backend.app.rules.formatting.bold_rule import BoldRule
from backend.app.rules.formatting.first_line_indent_rule import FirstLineIndentRule
from backend.app.rules.formatting.font_size_rule import FontSizeRule
from backend.app.rules.formatting.italic_rule import ItalicRule
from backend.app.rules.formatting.line_spacing_rule import LineSpacingRule
from backend.app.rules.formatting.margins_rule import MarginsRule
from backend.app.rules.formatting.page_size_rule import PageSizeRule
from backend.app.rules.formatting.space_after_rule import SpaceAfterRule
from backend.app.rules.formatting.space_before_rule import SpaceBeforeRule
from backend.app.rules.content.vkr_chapter_new_page_rule import VkrChapterNewPageRule


REPORT_DIR = Path("backend/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def build_formatting_rules(
    check_type: str = "csm_conference",
) -> list:

    font_sizes = EXPECTED_FONT_SIZES.copy()
    alignments = EXPECTED_ALIGNMENTS.copy()
    bold = EXPECTED_BOLD.copy()
    italic = EXPECTED_ITALIC.copy()
    line_spacing = EXPECTED_LINE_SPACING.copy()
    first_line_indent = EXPECTED_FIRST_LINE_INDENT.copy()
    space_before = EXPECTED_SPACE_BEFORE.copy()
    space_after = EXPECTED_SPACE_AFTER.copy()

    if check_type == "vkr":
        font_sizes.update(
            {
                "abstract_ru": 14,
                "abstract_en": 14,
            }
        )

        excluded_vkr_sections = (
            "title_page",
            "assignment",
            "contents",
            "appendix",
        )

        for section in excluded_vkr_sections:
            font_sizes.pop(section, None)
            alignments.pop(section, None)
            bold.pop(section, None)
            italic.pop(section, None)
            line_spacing.pop(section, None)
            first_line_indent.pop(section, None)
            space_before.pop(section, None)
            space_after.pop(section, None)

    if check_type == "vkr":
        line_spacing.update(
            {
                "abstract_ru": 1.5,
                "abstract_en": 1.5,
                "introduction": 1.5,
                "body": 1.5,
                "conclusion": 1.5,
                "subsection_header": 1.0,
                "caption": 1.0,
                "table_caption": 1.0,
                "table_note": 1.0,
                "reference_item": 1.0,
                "references_header": 1.0,
            }
        )
    return [
        FontSizeRule(expected_values=font_sizes),
        AlignmentRule(expected_values=alignments),
        BoldRule(expected_values=bold),
        ItalicRule(expected_values=italic),
        LineSpacingRule(expected_values=line_spacing),
        FirstLineIndentRule(expected_values=first_line_indent),
        SpaceBeforeRule(expected_values=space_before),
        SpaceAfterRule(expected_values=space_after),
        MarginsRule(expected_margins=EXPECTED_MARGINS),
        PageSizeRule(
            expected_width=EXPECTED_PAGE_WIDTH,
            expected_height=EXPECTED_PAGE_HEIGHT,
        ),
    ]


def build_common_content_rules() -> list:
    return [
        ReferenceFormatRule(),
        CitationRule(),
        FigureRule(
            reference_severity="warning",
            numbering_severity="critical",
        ),
        TableRule(
            reference_severity="warning",
            numbering_severity="critical",
        ),
        TableFontRule(),
        EquationRule(font_family="Cambria Math", font_size=14),
        EquationReferenceRule(),
        EquationLayoutRule(),
        EquationNumberSequenceRule(
            severity="critical",
        ),
        EquationExplanationRule(
            severity="warning",
        ),
        SequentialNumberingRule(),
        DuplicateReferenceRule(),
        EmptySectionRule(),
        LanguageConsistencyRule(),
        HeadingDetectionRule(),
        SectionHierarchyRule(),
        ReferenceYearRule(),
    ]


def build_csm_conference_rule_engine() -> RuleEngine:
    return RuleEngine(
        rules=[
            *build_formatting_rules("csm_conference"),
            *build_common_content_rules(),
            KeywordCountRule(
                min_keywords=5,
                max_keywords=10,
            ),
            AbstractLengthRule(
                min_words=75,
                max_words=300,
            ),
            ArticlePageCountRule(
                min_pages=3,
                max_pages=5,
                severity="warning",
            ),
            EmailFormatRule(),
            AffiliationRule(),
            AuthorAffiliationMatchRule(),
            AuthorEmailMatchRule(),
            AuthorCountRule(
                max_authors=3,
                severity="warning",
            ),
            ReferenceIdentifierRule(
                severity="critical",
            ),
            SectionOrderRule(
                section_groups=[
                    {"udc"},
                    {
                        "title_ru",
                        "author",
                        "affiliation",
                        "email",
                        "abstract_ru",
                        "keywords_ru",
                    },
                    {
                        "title_en",
                        "abstract_en",
                        "keywords_en",
                    },
                    {"body"},
                    {"references"},
                ],
                severity="critical",
            ),
            RequiredSectionRule(
                required_sections=[
                    "udc",
                    "title_ru",
                    "author",
                    "affiliation",
                    "email",
                    "abstract_ru",
                    "keywords_ru",
                    "title_en",
                    "abstract_en",
                    "keywords_en",
                    "body",
                    "references",
                ],
                severity="critical",
            ),
        ]
    )


def build_other_conference_rule_engine() -> RuleEngine:
    return RuleEngine(
        rules=[
            *build_formatting_rules("other_conference"),
            *build_common_content_rules(),
            KeywordCountRule(
                min_keywords=3,
                max_keywords=12,
            ),
            AbstractLengthRule(
                min_words=50,
                max_words=350,
            ),
            EmailFormatRule(),
            AffiliationRule(),
            AuthorEmailMatchRule(),
            RequiredSectionRule(
                required_sections=[
                    "udc",
                    "title_ru",
                    "author",
                    "affiliation",
                    "email",
                    "abstract_ru",
                    "keywords_ru",
                    "title_en",
                    "abstract_en",
                    "keywords_en",
                    "body",
                    "references",
                ],
                severity="critical",
            ),
        ]
    )


def build_vkr_rule_engine() -> RuleEngine:
    return RuleEngine(
        rules=[
            *build_formatting_rules("vkr"),
            ReferenceFormatRule(),
            CitationRule(),
            FigureRule(
                reference_severity="critical",
                numbering_severity="critical",
            ),
            TableRule(
                reference_severity="critical",
                numbering_severity="critical",
            ),
            TableFontRule(),
            EquationRule(font_family="Cambria Math", font_size=14),
            EquationReferenceRule(),
            EquationLayoutRule(),
            EquationNumberSequenceRule(
                severity="critical",
            ),
            EquationExplanationRule(
                severity="critical",
            ),
            SequentialNumberingRule(),
            DuplicateReferenceRule(),
            EmptySectionRule(),
            LanguageConsistencyRule(),
            HeadingDetectionRule(),
            SectionHierarchyRule(),
            ReferenceYearRule(),
            ForeignReferenceRule(
                min_foreign_references=2,
                severity="critical",
            ),
            PageNumberingRule(
                severity="critical",
            ),
            VkrChapterNewPageRule(
                severity="critical",
            ),
            VkrStructureRule(),
            RequiredSectionRule(
                required_sections=[
                    "title_page",
                    "assignment",
                    "abstract_ru",
                    "abstract_en",
                    "contents",
                    "introduction",
                    "analytical_section",
                    "special_section",
                    "life_safety_section",
                    "economic_efficiency_section",
                    "conclusion",
                    "references",
                ],
                severity="critical",
            ),
            SectionOrderRule(
                section_groups=[
                    {"title_page"},
                    {"assignment"},
                    {
                        "abstract_ru",
                        "abstract_en",
                    },
                    {"contents"},
                    {"terms"},
                    {"abbreviations"},
                    {"introduction"},
                    {"analytical_section"},
                    {"special_section"},
                    {"life_safety_section"},
                    {"economic_efficiency_section"},
                    {"conclusion"},
                    {"student_publications"},
                    {"references"},
                ],
                severity="critical",
            ),
        ]
    )


def build_rule_engine(
    check_type: str,
) -> RuleEngine:

    if check_type == "vkr":
        return build_vkr_rule_engine()

    if check_type == "other_conference":
        return build_other_conference_rule_engine()

    return build_csm_conference_rule_engine()


def get_document_title(document) -> str:
    try:
        return document.paragraphs[1].text.replace("\n", " ").strip()
    except Exception:
        return "Научная статья"


def get_document_authors(document) -> str:
    try:
        return document.paragraphs[2].text.replace("\n", " ").strip()
    except Exception:
        return "Не указаны"


def make_safe_report_filename(original_filename: str) -> str:
    name_without_ext = Path(original_filename).stem

    translit_map = {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
        "е": "e", "ё": "e", "ж": "zh", "з": "z", "и": "i",
        "й": "i", "к": "k", "л": "l", "м": "m", "н": "n",
        "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
        "у": "u", "ф": "f", "х": "h", "ц": "c", "ч": "ch",
        "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "",
        "э": "e", "ю": "yu", "я": "ya",
    }

    normalized_title = name_without_ext.lower()

    transliterated = "".join(
        translit_map.get(char, char)
        for char in normalized_title
    )

    safe_name = re.sub(
        r"[^a-z0-9]+",
        "_",
        transliterated,
    ).strip("_")

    words = safe_name.split("_")[:6]

    short_name = (
        "_".join(words)
        if words
        else "document"
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    return f"{short_name}_{timestamp}.pdf"


def build_error_category_stats(
    result,
) -> list[dict]:
    category_labels = {
        "authors": "Авторы",
        "formatting": "Форматирование",
        "references": "Список литературы",
        "citations": "Цитирования",
        "tables": "Таблицы",
        "figures": "Рисунки",
        "equations": "Формулы",
        "sections": "Разделы",
        "language": "Язык",
        "keywords": "Ключевые слова",
        "abstract": "Аннотация",
        "affiliations": "Аффилиации",
        "content": "Содержание",
        "other": "Другое",
    }

    category_counts = {}

    for error in result.errors:
        category = getattr(
            error,
            "category",
            "other",
        )

        category_counts[category] = (
            category_counts.get(category, 0)
            + 1
        )

    stats = []

    for category, count in category_counts.items():
        stats.append(
            {
                "category": category,
                "label": category_labels.get(
                    category,
                    category,
                ),
                "count": count,
            }
        )

    stats.sort(
        key=lambda item: item["count"],
        reverse=True,
    )

    return stats


def generate_pdf_report_from_docx(
    docx_path: Path,
    original_filename: str | None = None,
    check_type: str = "csm_conference",
) -> dict:
    document = DocxParser.parse(
        str(docx_path)
    )

    normalized_document = DocumentNormalizer.normalize(
        document
    )

    classified_document = SectionClassifier.classify(
        normalized_document,
        check_type=check_type,
    )

    print("\n=== DEBUG SEMANTIC TYPES ===")

    for paragraph in classified_document.paragraphs[:120]:
        print(
            paragraph.paragraph_index,
            "|",
            paragraph.semantic_type,
            "|",
            paragraph.font_size,
            "|",
            paragraph.text[:120],
        )

    print("=== END DEBUG ===\n")   

    debug_ranges = (
        (650, 700),
        (920, 980),
    )

    print("\n=== DEBUG PROBLEM PARAGRAPHS ===")

    for start, end in debug_ranges:
        print(f"\n--- {start}-{end} ---")

        for paragraph in classified_document.paragraphs:
            if start <= paragraph.paragraph_index <= end:
                print(
                    paragraph.paragraph_index,
                    "|",
                    paragraph.semantic_type,
                    "|",
                    paragraph.font_size,
                    "|",
                    paragraph.text[:140],
                )

    print("=== END DEBUG PROBLEM PARAGRAPHS ===\n")   

    if paragraph.paragraph_index in (
        192,
        197,
        233,
        239,
    ):
        print(
            paragraph.paragraph_index,
            paragraph.semantic_type,
            paragraph.line_spacing,
            paragraph.text[:80],
        )

    engine = build_rule_engine(
        check_type
    )

    result = engine.validate(
        classified_document
    )

    document_title = get_document_title(
        document
    )

    document_authors = get_document_authors(
        document
    )

    source_filename = (
        original_filename
        if original_filename
        else docx_path.name
    )

    report_filename = make_safe_report_filename(
        source_filename
    )

    report_path = REPORT_DIR / report_filename

    pdf_report = PDFValidationReport(
        result=result,
        output_path=str(report_path),
    )

    pdf_report.document_title = document_title
    pdf_report.document_authors = document_authors
    pdf_report.check_type = check_type

    pdf_report.generate()

    return {
        "report_filename": report_filename,
        "report_path": str(report_path),
        "score": result.score,
        "total_checks": result.total_checks,
        "total_errors": result.total_errors,
        "check_type": check_type,
        "error_categories": build_error_category_stats(
            result
        ),
        "critical_errors_count": result.critical_errors_count,
        "regular_errors_count": result.regular_errors_count,
        "warnings_count": result.warnings_count,
        "recommendations_count": result.recommendations_count,
        "weighted_penalty": result.weighted_penalty,
        "has_critical_errors": result.has_critical_errors,
        "status": result.status,
    }