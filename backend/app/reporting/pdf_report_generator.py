from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet,
)

from backend.app.models.validation import (
    ValidationResult
)

from backend.app.reporting.pdf_sections.translations import (
    TEXT
)

from backend.app.reporting.pdf_sections import (
    HelpersMixin,
    TableStylesMixin,
    StylesMixin,
    FontsMixin,
    CoverMixin,
    TOCMixin,
    SummaryMixin,
    DistributionMixin,
    GaugeMixin,
    ErrorsMixin,
    TopErrorsMixin,
    RecommendationsMixin,
    DocumentMixin,
)
    
    

class PDFValidationReport(
    HelpersMixin,
    TableStylesMixin,
    StylesMixin,
    FontsMixin,
    CoverMixin,
    TOCMixin,
    SummaryMixin,
    DistributionMixin,
    GaugeMixin,
    ErrorsMixin,
    TopErrorsMixin,
    RecommendationsMixin,
    DocumentMixin,
):
   
    BRAND = {

        # Основной цвет
        "primary": colors.HexColor(
            "#0F172A"
        ),

        # Акцент / заголовки таблиц
        "secondary": colors.HexColor(
            "#256EF1"
        ),

        # Карточки
        "card": colors.HexColor(
            "#FDFDFD"
        ),

        # Успех
        "success": colors.HexColor(
            "#22C55E"
        ),

        # Предупреждение
        "warning": colors.HexColor(
            "#F59E0B"
        ),

        # Ошибка
        "danger": colors.HexColor(
            "#EF4444"
        ),

        # Светлые фоны
        "success_light": colors.HexColor(
            "#DCFCE7"
        ),

        "warning_light": colors.HexColor(
            "#FDE68A"
        ),

        "danger_light": colors.HexColor(
            "#FECACA"
        ),

        # Поверхность
        "background": colors.HexColor(
            "#FFFFFF"
        ),

        # Границы
        "border": colors.HexColor(
            "#EDF2F7"
        ),

        # Текст
        "text": colors.HexColor(
            "#111827"
        ),

        "muted": colors.HexColor(
            "#64748B"
        ),
    }

    LAYOUT = {

        # ========= Page =========

        "page_margin": 40,

        "content_width": 500,


        # ========= Cards =========

        "card_width": 115,
        "card_height": 100,

        "card_table_width": 122,

        "card_padding": 16,


        # ========= Cover =========

        "cover_col_width": 180,

        "space_status": 40,

        "space_footer": 90,


        # ========= Spacing =========

        "space_small": 12,

        "space_medium": 20,

        "space_large": 36,

        "space_xlarge": 48,

        "space_error": 12,

        "space_summary": 28,

        # ========= Summary =========

        "summary_table_width": 240,

        "summary_value_width": 180,

        "summary_height": 90,


        # ========= Distribution =========

        "distribution_width": 520,

        "distribution_height": 260,

        "chart_width": 280,

        "chart_height": 100,

        "legend_col": 260,

        "legend_value": 100,

        # ========= Gauge =========

        "gauge_width": 520,
        "gauge_height": 260,

        "gauge_center_x": 260,
        "gauge_center_y": 110,

        "gauge_outer_radius": 150,
        "gauge_inner_radius": 108,

        "gauge_arrow_length": 130,

        # ========= Gauge Card =========

        "gauge_card_x": 40,
        "gauge_card_y": 10,

        "gauge_card_width": 440,
        "gauge_card_height": 250,

    }

    # Initialization


    def __init__(
        self,
        result: ValidationResult,
        output_path: str
    ):

        self.result = result

        self.output_path = (
            output_path
        )

        self.text = TEXT

        self._register_fonts()

        self.styles = (
            getSampleStyleSheet()
        )

        self._configure_styles()

    
    def _draw_footer(
        self,
        canvas,
        doc,
    ):

        canvas.saveState()

        width = doc.pagesize[0]

        footer_y = 18

        canvas.setFont(
            "Arial",
            9,
        )

        canvas.setFillColor(
            self.BRAND["muted"]
        )

        canvas.drawCentredString(

            width / 2,

            footer_y,

            self.text["footer"]
        )

        canvas.drawRightString(

            width - 40,

            footer_y,

            f"Стр. {canvas.getPageNumber()}"
        )

        canvas.restoreState()