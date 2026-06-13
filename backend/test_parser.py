from backend.app.normalizer.normalizer import (
    DocumentNormalizer
)

from backend.app.parser.docx_parser import (
    DocxParser
)

from backend.app.rules.engine import (
    RuleEngine
)

from backend.app.rules.formatting.font_size_rule import (
    FontSizeRule
)

from backend.app.rules.formatting.alignment_rule import (
    AlignmentRule
)

from backend.app.classification.section_classifier import (
    SectionClassifier
)

from backend.app.rules.formatting.italic_rule import (
    ItalicRule
)

from backend.app.rules.formatting.line_spacing_rule import (
    LineSpacingRule
)

from backend.app.rules.formatting.first_line_indent_rule import (
    FirstLineIndentRule
)

from backend.app.rules.formatting.space_before_rule import (
    SpaceBeforeRule
)

from backend.app.rules.formatting.space_after_rule import (
    SpaceAfterRule
)

from backend.app.rules.formatting.margins_rule import (
    MarginsRule
)

from backend.app.rules.formatting.page_size_rule import (
    PageSizeRule
)

from backend.app.rules.content.reference_format_rule import (
    ReferenceFormatRule
)

from backend.app.rules.content.citation_rule import (
    CitationRule
)

from backend.app.rules.content.figure_rule import (
    FigureRule
)

from backend.app.rules.content.table_rule import (
    TableRule
)

from backend.app.rules.content.table_font_rule import (
    TableFontRule
)

from backend.app.rules.content.equation_rule import (
    EquationRule
)

from backend.app.rules.content.equation_reference_rule import (
    EquationReferenceRule
)

from backend.app.rules.content.equation_layout_rule import (
    EquationLayoutRule
)

from backend.app.rules.content.equation_number_sequence_rule import (
    EquationNumberSequenceRule
)

from backend.app.rules.content.sequential_numbering_rule import (
    SequentialNumberingRule
)

from backend.app.rules.content.duplicate_reference_rule import (
    DuplicateReferenceRule
)

from backend.app.rules.content.empty_section_rule import (
    EmptySectionRule
)

from backend.app.rules.content.keyword_count_rule import (
    KeywordCountRule
)

from backend.app.rules.content.abstract_length_rule import (
    AbstractLengthRule
)

from backend.app.rules.content.language_consistency_rule import (
    LanguageConsistencyRule
)

from backend.app.rules.content.affiliation_rule import (
    AffiliationRule
)

from backend.app.rules.content.author_affiliation_match_rule import (
    AuthorAffiliationMatchRule
)

from backend.app.rules.content.email_format_rule import (
    EmailFormatRule
)

from backend.app.rules.content.author_email_match_rule import (
    AuthorEmailMatchRule
)

from backend.app.rules.content.institutional_email_rule import (
    InstitutionalEmailRule
)

from backend.app.rules.content.section_order_rule import (
    SectionOrderRule
)

from backend.app.rules.content.required_section_rule import (
    RequiredSectionRule
)

from backend.app.rules.content.heading_detection_rule import (
    HeadingDetectionRule
)

from backend.app.rules.content.section_hierarchy_rule import (
    SectionHierarchyRule
)

from backend.app.rules.content.reference_year_rule import (
    ReferenceYearRule
)


from backend.app.config.style_rules import (
    EXPECTED_FONT_SIZES,
    EXPECTED_ALIGNMENTS,
    EXPECTED_BOLD,
    EXPECTED_ITALIC,
    EXPECTED_LINE_SPACING,
    EXPECTED_FIRST_LINE_INDENT,
    EXPECTED_SPACE_BEFORE,
    EXPECTED_SPACE_AFTER,
    EXPECTED_MARGINS,
    EXPECTED_PAGE_WIDTH,
    EXPECTED_PAGE_HEIGHT,

)

from backend.app.rules.formatting.bold_rule import (
    BoldRule
)

document = DocxParser.parse(
    "backend/uploads/3ce13935-e4e6-4bc9-b5e8-60df12049c03.docx"
)

normalized_document = (
    DocumentNormalizer.normalize(
        document
    )
)

classified_document = (
    SectionClassifier.classify(
        normalized_document
    )
)

print("\n")
print("=" * 50)
print("ПОЛЯ")
print("=" * 50)

print(
    classified_document.margins
)

print("\n")
print("=" * 50)
print("РАЗМЕР СТРАНИЦЫ")
print("=" * 50)

print(
    classified_document.page_size
)

print("\n")
print("=" * 50)
print("КЛАССИФИЦИРОВАННЫЕ АБЗАЦЫ")
print("=" * 50)

for paragraph in (
    classified_document.paragraphs
):

    print("\n")

    print(
        f"Абзац: "
        f"{paragraph.paragraph_index}"
    )

    print(
        f"Текст: "
        f"{paragraph.text}"
    )

    print(
        f"Семантический тип: "
        f"{paragraph.semantic_type}"
    )

    if paragraph.semantic_type == "heading":

        print(">>> ОБНАРУЖЕН ЗАГОЛОВОК <<<")

    print(
        f"Размер шрифта: "
        f"{paragraph.font_size}"
    )

    print(
        f"Выравнивание: "
        f"{paragraph.alignment}"
    )

    print(
        f"Жирный: "
        f"{paragraph.bold}"
    )

    print(
        f"Курсив: "
        f"{paragraph.italic}"
    )

    print(
        f"Межстрочный интервал: "
        f"{paragraph.line_spacing}"
    )

    print(
        f"Отступ первой строки: "
        f"{paragraph.first_line_indent}"
    )


engine = RuleEngine(
    rules=[
        FontSizeRule(
            expected_values=EXPECTED_FONT_SIZES
        ),

        AlignmentRule(
            expected_values=EXPECTED_ALIGNMENTS
        ),

        BoldRule(
            expected_values=EXPECTED_BOLD
        ),

        ItalicRule(
            expected_values=EXPECTED_ITALIC
        ),

        LineSpacingRule(
            expected_values=(
                EXPECTED_LINE_SPACING
            )
        ),

        FirstLineIndentRule(
            expected_values=(
                EXPECTED_FIRST_LINE_INDENT
            )
        ),

        SpaceBeforeRule(
            expected_values=(
                 EXPECTED_SPACE_BEFORE
            )
        ),

        SpaceAfterRule(
            expected_values=(
                 EXPECTED_SPACE_AFTER
            )
        ),

        MarginsRule(
            expected_margins=EXPECTED_MARGINS
        ),

        PageSizeRule(
            expected_width=EXPECTED_PAGE_WIDTH,
            expected_height=EXPECTED_PAGE_HEIGHT
        ),

        ReferenceFormatRule(),
        CitationRule(),
        FigureRule(),
        TableRule(),
        TableFontRule(),
        EquationRule(font_family="Cambria Math", font_size=14),
        EquationReferenceRule(),
        EquationLayoutRule(),
        EquationNumberSequenceRule(),
        SequentialNumberingRule(),
        DuplicateReferenceRule(),
        EmptySectionRule(),

        KeywordCountRule(
            min_keywords=5,
            max_keywords=10
        ),

        AbstractLengthRule(
            min_words=75,
            max_words=300
        ),

        LanguageConsistencyRule(),
        EmailFormatRule(),
        AffiliationRule(),
        AuthorAffiliationMatchRule(),
        AuthorEmailMatchRule(),
#        InstitutionalEmailRule(),
        SectionOrderRule(),
        RequiredSectionRule(),
        HeadingDetectionRule(),
        SectionHierarchyRule(),
        ReferenceYearRule(),



    ]
)

result = engine.validate(
    classified_document
)

print("\n")
print("=" * 50)
print("РЕЗУЛЬТАТ ПРОВЕРКИ")
print("=" * 50)

print(
    f"Проверок: "
    f"{result.total_checks}"
)

print(
    f"Ошибок: "
    f"{result.total_errors}"
)

print(
    f"Оценка: "
    f"{result.score}%"
)

print("\n")
print("=" * 50)
print("ОШИБКИ")
print("=" * 50)

for error in result.errors:

    print("\n")

    print(
        f"Абзац: "
        f"{error.paragraph_index}"
    )

    print(
        f"Сообщение: "
        f"{error.message}"
    )

    print(
        f"Ожидалось: "
        f"{error.expected}"
    )

    print(
        f"Получено: "
        f"{error.actual}"
    )

    print(
        f"Категория: "
        f"{error.category}"
    )



from backend.app.reporting.pdf_report_generator import (
    PDFValidationReport
)

print("\n")
print("=" * 50)
print("ГЕНЕРАЦИЯ PDF-ОТЧЁТА")
print("=" * 50)

report_path = (
    "validation_report_v6.pdf"
)

document_title = (
    document.paragraphs[1].text
    .replace(
        "\n",
        " "
    )
    .strip()
)

document_authors = (
    document.paragraphs[2].text
    .replace(
        "\n",
        " "
    )
    .strip()
)

print("\n")
print("=" * 50)
print("ДАННЫЕ ДЛЯ PDF")
print("=" * 50)
print(
    f"Название: {document_title}"
)
print(
    f"Авторы: {document_authors}"
)

pdf_report = (
    PDFValidationReport(
        result=result,
        output_path=report_path
    )
)

pdf_report.document_title = (
    document_title
)

pdf_report.document_authors = (
    document_authors
)

pdf_report.generate()