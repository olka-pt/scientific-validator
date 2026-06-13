import logging
from reportlab.lib.units import mm

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
)

from reportlab.platypus.tableofcontents import (
    TableOfContents,
)

from reportlab.platypus import (
    HRFlowable
)

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from reportlab.lib.enums import TA_LEFT

logger = logging.getLogger(__name__)


class TOCDocument(
    BaseDocTemplate
):

    SECTION_CONFIG = {

        "Краткий отчёт": (
            "1",
            0,
        ),

        "Распределение ошибок": (
            "2",
            0,
        ),

        "Самые частые ошибки": (
            "2.1",
            1,
        ),

        "Ошибки проверки": (
            "2.2",
            1,
        ),

        "Рекомендации": (
            "3",
            0,
        ),
    }

    def afterFlowable(
        self,
        flowable
    ):

        if not isinstance(
            flowable,
            Paragraph
        ):
            return

        style = getattr(
            flowable,
            "style",
            None
        )

        if (
            style is None
            or  style.name not in [

                "Heading1",

                "Heading2",
            ]
        ):
            return

        original_title = (
            flowable.getPlainText()
            .strip()
        )
        
        number, level = self.SECTION_CONFIG.get(

            original_title,

            (
                None,
                0,
            )
        )

        toc_title = original_title

        bookmark = (

            getattr(

                flowable,

                "_bookmarkName",

                None
            )

            or

            toc_title
            .lower()
            .replace(
                " ",
                "_"
            )
        )

        self.canv.bookmarkPage(
            bookmark
        )

        try:

            self.canv.addOutlineEntry(

                toc_title,

                bookmark,

                level=level,

                closed=False,
            )

        except Exception:

            pass

        self.notify(

            "TOCEntry",

            (

                level,

                toc_title,

                max(
                    1,
                    self.page - 1
                ),

                bookmark,
            )
        )

class DocumentMixin:

    # --------------------
    # вспомогательные функции
    # --------------------

    def _get_generated_at(self):
        from datetime import datetime
        current_time = datetime.now()
        if not hasattr(self, "_generated_at"):
            self._generated_at = datetime.now()
        return self._generated_at

    def _get_report_number(
        self
    ):

        value = getattr(
            self,
            "report_number",
            None
        )

        if value:
            return str(value)

        generated_at = self._get_generated_at()

        return (
            "№ AI-"
            + generated_at.strftime(
                "%Y%m%d-%H%M"
            )
        )    

    def _get_report_status(self):
        score = self.result.score
        if score >= 95:
            return "Пройден"
        elif score >= 85:
            return "Требует внимания"
        else:
            return "Не пройден"

    def _get_report_status_short(self):
        score = self.result.score
        if score >= 95:
            return "ПРОЙДЕНО"
        elif score >= 85:
            return "ВНИМАНИЕ"
        else:
            return "НЕ ПРОЙДЕНО"

    def _get_status_color(
        self
    ):

        score = self.result.score

        if score >= 95:
            return "#10B981"

        if score >= 85:
            return "#F59E0B"

        return "#EF4444"    

    def _get_document_title(
        self
    ):

        return getattr(
            self,
            "document_title",
            "Научная статья"
        )

    def _get_document_authors(
        self
    ):

        return getattr(
            self,
            "document_authors",
            "Не указаны"
        )

    def _get_check_type_label(
        self
    ):

        check_type = getattr(
            self,
            "check_type",
            "csm_conference",
        )

        labels = {
            "csm_conference": "Конференция ЦСМ",
            "other_conference": "Другая конференция",
            "vkr": "ВКР",
        }

        return labels.get(
            check_type,
            "Конференция ЦСМ",
        )    

    def draw_header(
        self,
        canvas,
    ):

        from datetime import datetime

        page_width, page_height = A4

        # Логотип слева

        try:

            canvas.drawImage(

                "backend/assets/logo.png",

                45,
                page_height - 100,

                width=120,
                height=82,

                preserveAspectRatio=True,
                mask="auto",
            )

        except Exception:

            pass

        # Правая часть

        canvas.setFillColor(
            colors.HexColor("#64748B")
        )

        canvas.setFont(
            "Helvetica",
            9,
        )

        canvas.drawRightString(

            page_width - 45,

            page_height - 45,

            self._get_generated_at().strftime(
                "%d.%m.%Y"
            )
        )

        canvas.drawRightString(

            page_width - 45,

            page_height - 62,

            self._get_report_number()
        )

        # Линия-разделитель

        canvas.setStrokeColor(
            colors.HexColor("#E2E8F0")
        )

        canvas.setLineWidth(1)

        canvas.line(

            40,

            page_height - 110,

            page_width - 40,

            page_height - 110,
        )


    def draw_hero_section(
        self,
        canvas,
    ):

        page_width, page_height = A4

        left_x = 52
        title_y = page_height - 220

        canvas.setFillColor(
            colors.HexColor("#0F172A")
        )

        try:
            canvas.setFont("Arial-Bold", 46)
        except Exception:
            canvas.setFont("Helvetica-Bold", 46)

        canvas.drawString(
            left_x,
            title_y,
            "ОТЧЕТ"
        )

        try:
            canvas.setFont("Arial-Bold", 22)
        except Exception:
            canvas.setFont("Helvetica-Bold", 25)

        canvas.drawString(
            left_x,
            title_y - 36,
            "О ПРОВЕРКЕ ДОКУМЕНТА"
        )

        canvas.setStrokeColor(
            colors.HexColor("#1E90FF")
        )

        canvas.setLineWidth(2)

        canvas.line(
            left_x,
            title_y - 88,
            left_x + 48,
            title_y - 88,
        )

        canvas.setFillColor(
            colors.HexColor("#64748B")
        )

        try:
            canvas.setFont("Arial", 11)
        except Exception:
            canvas.setFont("Helvetica", 11)

        canvas.drawString(
            left_x,
            title_y - 120,
            "Документ успешно прошел проверку"
        )

        canvas.drawString(
            left_x,
            title_y - 140,
            "на соответствие установленным требованиям"
        )


    def draw_score_ring(
        self,
        canvas,
    ):

        score_percentage = max(0, min(100, self.result.score))  # Ограничиваем 0-100%

        orb_x = 480
        orb_y = 590

        outer_radius = 108
        ring_radius = 82

        score = self.result.score

        if score >= 95:
            ring_color_dark = "#10B981"
            ring_color_light = "#34D399"
            status_text = "ПРОЙДЕНО"

        elif score >= 85:
            ring_color_dark = "#F59E0B"
            ring_color_light = "#FBBF24"
            status_text = "ВНИМАНИЕ"

        else:
            ring_color_dark = "#EF4444"
            ring_color_light = "#F87171"
            status_text = "НЕ ПРОЙДЕНО"

        canvas.setFillColor(
            colors.Color(
                0.12,
                0.56,
                1.0,
                alpha=0.035,
            )
        )

        canvas.circle(
            orb_x,
            orb_y,
            outer_radius,
            fill=1,
            stroke=0,
        )

        canvas.setStrokeColor(
            colors.Color(
                0.12,
                0.56,
                1.0,
                alpha=0.16,
            )
        )

        canvas.setLineWidth(1)

        canvas.circle(
            orb_x,
            orb_y,
            outer_radius - 10,
            fill=0,
            stroke=1,
        )

        canvas.setStrokeColor(
            colors.HexColor("#E2E8F0")
        )

        canvas.setLineWidth(12)

        canvas.circle(
            orb_x,
            orb_y,
            ring_radius,
            fill=0,
            stroke=1,
        )

        canvas.setStrokeColor(
            colors.HexColor(ring_color_dark)
        )

        canvas.setLineWidth(12)

        canvas.arc(
            orb_x - ring_radius,
            orb_y - ring_radius,
            orb_x + ring_radius,
            orb_y + ring_radius,
            95,
            220,
        )

        canvas.setStrokeColor(
            colors.HexColor(ring_color_light)
        )

        canvas.arc(
            orb_x - ring_radius,
            orb_y - ring_radius,
            orb_x + ring_radius,
            orb_y + ring_radius,
            -45,
            210,
        )

        canvas.setFillColor(
            colors.HexColor("#0F172A")
        )

        try:
            canvas.setFont("Arial", 10)
        except Exception:
            canvas.setFont("Helvetica", 10)

        canvas.drawCentredString(
            orb_x,
            orb_y + 38,
            "ИТОГОВАЯ ОЦЕНКА",
        )

        try:
            canvas.setFont("Arial-Bold", 36)
        except Exception:
            canvas.setFont("Helvetica-Bold", 38)

        canvas.drawCentredString(
            orb_x,
            orb_y + 2,
            f"{score:.1f}%",
        )

        canvas.setFillColor(
            colors.HexColor(ring_color_light)
        )

        canvas.circle(
            orb_x - 40,
            orb_y - 16,
            11,
            fill=1,
            stroke=0,
        )

        canvas.setStrokeColor(
            colors.white
        )

        canvas.setLineWidth(2)

        canvas.line(
            orb_x - 45,
            orb_y - 17,
            orb_x - 41,
            orb_y - 22,
        )

        canvas.line(
            orb_x - 41,
            orb_y - 22,
            orb_x - 34,
            orb_y - 11,
        )

        canvas.setFillColor(
            colors.HexColor(ring_color_dark)
        )

        if status_text == "НЕ ПРОЙДЕНО":
            status_font_size = 9
            status_x = orb_x - 26
            status_y = orb_y - 21
        elif status_text == "ВНИМАНИЕ":
            status_font_size = 11
            status_x = orb_x - 24
            status_y = orb_y - 21
        else:
            status_font_size = 13
            status_x = orb_x - 22
            status_y = orb_y - 21

        try:
            canvas.setFont(
                "Arial-Bold",
                status_font_size,
            )
        except Exception:
            canvas.setFont(
                "Helvetica-Bold",
                status_font_size,
            )

        canvas.drawString(
            status_x,
            status_y,
            status_text,
        )


    def draw_kpi_cards(
        self,
        canvas,
    ):

        page_width, page_height = A4

        card_y = 330
        card_width = 112
        card_height = 122
        gap = 14
        start_x = 45

        cards = [
            ("ПРОВЕРКИ", str(self.result.total_checks), "#1E90FF", "backend/assets/icons/file-text.png"),
            ("ОШИБКИ", str(self.result.total_errors), "#EF4444", "backend/assets/icons/alert-triangle.png"),
            ("ОЦЕНКА", f"{self.result.score:.1f}%", "#38BDF8", "backend/assets/icons/chart-line.png"),
            ("СТАТУС", self._get_report_status_short(), "#22C55E", "backend/assets/icons/clipboard-check.png"),
        ]

        for index, card in enumerate(cards):

            title, value, accent, icon_path = card

            x = start_x + index * (card_width + gap)

            canvas.setFillColor(
                colors.Color(0, 0, 0, alpha=0.06)
            )

            canvas.roundRect(
                x,
                card_y - 4,
                card_width,
                card_height,
                14,
                fill=1,
                stroke=0,
            )

            canvas.setFillColor(
                colors.white
            )

            canvas.roundRect(
                x,
                card_y,
                card_width,
                card_height,
                14,
                fill=1,
                stroke=0,
            )

            canvas.setStrokeColor(
                colors.HexColor("#E2E8F0")
            )

            canvas.setLineWidth(0.8)

            canvas.roundRect(
                x,
                card_y,
                card_width,
                card_height,
                14,
                fill=0,
                stroke=1,
            )

            try:
                canvas.drawImage(
                    icon_path,
                    x + 40,
                    card_y + card_height - 42,
                    width=32,
                    height=32,
                    preserveAspectRatio=True,
                    mask="auto",
                )

            except Exception:
                canvas.setFillColor(
                    colors.HexColor(accent)
                )

                canvas.circle(
                    x + 22,
                    card_y + card_height - 22,
                    7,
                    fill=1,
                    stroke=0,
                )

            canvas.setFillColor(
                colors.HexColor("#0F172A")
            )

            try:
                if title == "СТАТУС":
                    canvas.setFont("Arial-Bold", 16)
                else:
                    canvas.setFont("Arial-Bold", 22)
            except Exception:
                if title == "СТАТУС":
                    canvas.setFont("Helvetica-Bold", 16)
                else:
                    canvas.setFont("Helvetica-Bold", 22)

            canvas.drawCentredString(
                x + card_width / 2,
                card_y + 48,
                value,
            )

            canvas.setFillColor(
                colors.HexColor("#64748B")
            )

            try:
                canvas.setFont("Arial", 8)
            except Exception:
                canvas.setFont("Helvetica", 8)

            canvas.drawCentredString(
                x + card_width / 2,
                card_y + 22,
                title,
            )


    def draw_document_card(
        self,
        canvas,
    ):



        card_x = 50
        card_y = 60
        card_width = 490
        card_height = 240
        radius = 18

        icon_x = card_x + 24
        label_x = card_x + 50
        value_x = card_x + 180

        value_width = (
            card_x
            + card_width
            - value_x
            - 30
        )

        def wrap_text(
            text,
            font_name,
            font_size,
            max_width,
        ):

            words = (
                str(text)
                .replace(
                    "\n",
                    " "
                )
                .split()
            )

            lines = []
            current_line = ""

            for word in words:

                candidate = (
                    f"{current_line} {word}"
                    if current_line
                    else word
                )

                if (
                    canvas.stringWidth(
                        candidate,
                        font_name,
                        font_size,
                    )
                    <= max_width
                ):
                    current_line = candidate

                else:
                    if current_line:
                        lines.append(
                            current_line
                        )

                    current_line = word

            if current_line:
                lines.append(
                    current_line
                )

            return lines

        rows = [
            {
                "label": "НАЗВАНИЕ РАБОТЫ",
                "value": self._get_document_title(),
                "icon": "backend/assets/icons/file-text.png",
                "height": 65,
                "font_size": 8.2,
                "line_height": 10,
            },
            {
                "label": "АВТОР",
                "value": self._get_document_authors(),
                "icon": "backend/assets/icons/user.png",
                "height": 30,
                "font_size": 8.8,
                "line_height": 10.5,
            },
            {
                "label": "ЦЕЛЬ ПРОВЕРКИ",
                "value": self._get_check_type_label(),
                "icon": "backend/assets/icons/target.png",
                "height": 24,
                "font_size": 9,
                "line_height": 10.5,
            },
            {
                "label": "ДАТА ПРОВЕРКИ",
                "value": self._get_generated_at().strftime(
                    "%d.%m.%Y %H:%M"
                ),
                "icon": "backend/assets/icons/calendar.png",
                "height": 24,
                "font_size": 9,
                "line_height": 10.5,
            },
            {
                "label": "ВЕРСИЯ",
                "value": "1.0",
                "icon": "backend/assets/icons/tag.png",
                "height": 24,
                "font_size": 9,
                "line_height": 10.5,
            },
            {
                "label": "СТАТУС",
                "value": self._get_report_status(),
                "icon": "backend/assets/icons/clipboard-check.png",
                "height": 24,
                "font_size": 9,
                "line_height": 10.5,
            },
        ]

        canvas.setFillColor(
            colors.Color(
                0,
                0,
                0,
                alpha=0.035,
            )
        )

        canvas.roundRect(
            card_x,
            card_y - 5,
            card_width,
            card_height,
            radius,
            fill=1,
            stroke=0,
        )

        canvas.setFillColor(
            colors.white
        )

        canvas.roundRect(
            card_x,
            card_y,
            card_width,
            card_height,
            radius,
            fill=1,
            stroke=0,
        )

        canvas.setStrokeColor(
            colors.HexColor("#E2E8F0")
        )

        canvas.setLineWidth(0.8)

        canvas.roundRect(
            card_x,
            card_y,
            card_width,
            card_height,
            radius,
            fill=0,
            stroke=1,
        )

        row_y = (
            card_y
            + card_height
            - 48
        )

        for index, row in enumerate(rows):

            label = row["label"]
            value = row["value"]
            icon_path = row["icon"]
            row_height = row["height"]
            font_size = row["font_size"]
            line_height = row["line_height"]

            canvas.setFillColor(
                colors.HexColor("#EFF6FF")
            )

            canvas.circle(
                icon_x,
                row_y + 1,
                9,
                fill=1,
                stroke=0,
            )

            try:
                canvas.drawImage(
                    icon_path,
                    icon_x - 5,
                    row_y - 4,
                    width=10,
                    height=10,
                    preserveAspectRatio=True,
                    mask="auto",
                )

            except Exception:
                canvas.setFillColor(
                    colors.HexColor("#1E90FF")
                )

                canvas.circle(
                    icon_x,
                    row_y + 2,
                    3,
                    fill=1,
                    stroke=0,
                )

            canvas.setFillColor(
                colors.HexColor("#64748B")
            )

            try:
                canvas.setFont(
                    "Arial",
                    8.5,
                )
            except Exception:
                canvas.setFont(
                    "Helvetica",
                    8.5,
                )

            canvas.drawString(
                label_x,
                row_y,
                label,
            )

            try:
                value_font = "Arial-Bold"

                canvas.setFont(
                    value_font,
                    font_size,
                )

            except Exception:
                value_font = "Helvetica-Bold"

                canvas.setFont(
                    value_font,
                    font_size,
                )

            value_lines = wrap_text(
                value,
                value_font,
                font_size,
                value_width,
            )

            if label == "СТАТУС":
                # Цвет бейджа
                badge_color = colors.HexColor(self._get_status_color())

                # Ширина текста в пикселях
                text_width = canvas.stringWidth(value, "Arial-Bold", 10) + 16  # 8px padding слева и справа

                # Позиция бейджа
                badge_x = value_x
                badge_y = row_y - 4  # немного ниже верхней линии строки

                badge_height = 14  # высота бейджа

                # Нарисовать закругленный прямоугольник
                canvas.setFillColor(badge_color)
                canvas.roundRect(badge_x, badge_y, text_width, badge_height, radius=6, fill=1, stroke=0)

                # Нарисовать белый текст поверх бейджа
                canvas.setFillColor(colors.white)
                try:
                    canvas.setFont("Arial-Bold", 10)
                except Exception:
                    canvas.setFont("Helvetica-Bold", 10)
                text_y = badge_y + 4  # выравниваем текст по центру по вертикали
                canvas.drawString(badge_x + 8, text_y, value)  # 8px отступ слева
            else:
                canvas.setFillColor(colors.HexColor("#0F172A"))
                line_y = row_y
                for line in value_lines:
                    canvas.drawString(value_x, line_y, line)
                    line_y -= line_height

            if index < len(rows) - 1:

                canvas.setStrokeColor(
                    colors.HexColor("#E2E8F0")
                )

                canvas.setLineWidth(0.6)

                line_position_y = (
                    row_y
                    - row_height
                    + 12
                )

                canvas.line(
                    label_x,
                    line_position_y,
                    card_x + card_width - 28,
                    line_position_y,
                )

            row_y -= row_height

    def draw_footer_cover(
        self,
        canvas,
    ):

        page_width, page_height = A4

        footer_y = 30

        canvas.setStrokeColor(
            colors.HexColor("#1E90FF")
        )

        canvas.setLineWidth(0.7)

        canvas.line(
            60,
            footer_y + 22,
            page_width - 60,
            footer_y + 22,
        )

        try:
            canvas.setFont("Arial", 8)
        except Exception:
            canvas.setFont("Helvetica", 8)

        canvas.setFillColor(
            colors.HexColor("#64748B")
        )

        canvas.drawString(
            60,
            footer_y,
            "Отчет сформирован автоматически системой ФорматУМ",
        )

        canvas.drawRightString(
            page_width - 60,
            footer_y,
            "© 2026 ФорматУМ",
        )

    def _build_heading(
        self,
        title,
        style_name,
        number,
    ):

        heading = Paragraph(

            f"{number}. {title.upper()}",

            self.styles[
                style_name
            ]
        )

        heading._bookmarkName = (

            title
            .lower()
            .replace(
                " ",
                "_"
            )
        )

        return heading

    def _draw_cover_page(
        self,
        canvas,
        document
    ):

        canvas.saveState()

        canvas.setFillColor(
            colors.HexColor("#F5F8FB")
        )

        canvas.rect(
            0,
            0,
            A4[0],
            A4[1],
            fill=1,
            stroke=0,
        )

        canvas.setFillColor(
            colors.Color(
                0.22,
                0.74,
                0.97,
                alpha=0.018,
            )
        )

        canvas.circle(
            220,
            760,
            130,
            fill=1,
            stroke=0,
        )

        self.draw_score_ring(
            canvas
        )

        self.draw_header(
            canvas
        )

        self.draw_hero_section(
            canvas
        )

        self.draw_kpi_cards(
            canvas
        )

        self.draw_document_card(
            canvas
        )

        self.draw_footer_cover(
            canvas
        )

        canvas.restoreState()

    def _draw_default_page(
        self,
        canvas,
        document
    ):

        real_page = (
            canvas.getPageNumber()
        )

        canvas.saveState()

        canvas.setFillColor(

            self.BRAND["background"]
        )

        canvas.rect(

            0,
            0,

            A4[0],
            A4[1],

            fill=1,
            stroke=0,
        )

        footer_y = 14

        canvas.setStrokeColor(

            self.BRAND[
                "border"
            ]
        )

        canvas.line(

            50,

            footer_y + 16,

            A4[0] - 50,

            footer_y + 16,
        )

        try:

            canvas.setFont(
                "Arial",
                9
            )

        except Exception:

            canvas.setFont(
                "Helvetica",
                9
            )

        canvas.setFillColor(

            self.BRAND[
                "muted"
            ]
        )

        canvas.drawString(

            50,

            footer_y,

            self.text[
                "footer"
            ]
        )

        if real_page > 1:

            visible = (
                real_page - 1
            )

            canvas.drawRightString(

                A4[0] - 50,

                footer_y,

                (
                    f"{self.text['page']} "
                    f"{visible}"
                )
            )

        canvas.restoreState()

    def _create_document(
        self
    ):

        document = TOCDocument(

            self.output_path,

            pagesize=A4,

            rightMargin=self.LAYOUT[
                "page_margin"
            ],

            leftMargin=self.LAYOUT[
                "page_margin"
            ],

            topMargin=self.LAYOUT[
                "page_margin"
            ],

            bottomMargin=self.LAYOUT[
                "page_margin"
            ],
        )

        frame = Frame(

            document.leftMargin,

            document.bottomMargin,

            document.width,

            document.height,

            id="main",
        )

        cover_template = PageTemplate(

            id="cover",

            frames=[frame],

            onPage=self._draw_cover_page,
        )

        default_template = PageTemplate(

            id="default",

            frames=[frame],

            onPage=self._draw_default_page,
        )

        document.addPageTemplates(

            [
                cover_template,
                default_template,
            ]
        )

        self.styles["Heading2"].fontName = (
            "Arial-Bold"
        )

        self.styles["Heading2"].fontSize = 11

        self.styles["Heading2"].leading = 18

        self.styles["Heading2"].leftIndent = 18

        self.styles["Heading2"].spaceBefore = 10

        self.styles["Heading2"].spaceAfter = 6

        self.styles["Heading2"].textColor = (
            "#666666"
        )

        self.styles["Heading2"].alignment = (
            TA_LEFT
        )

        return document

    def _build_table_of_contents(
        self,
        elements
    ):

        from reportlab.lib.enums import (
            TA_CENTER,
        )

        from reportlab.lib.styles import (
            ParagraphStyle,
        )

        from reportlab.platypus import (
            HRFlowable,
            Spacer,
        )

        elements.append(

            Paragraph(

                self.text.get(

                    "contents",

                    "Содержание"
                ),

                ParagraphStyle(

                    "TOCTitle",

                    parent=self.styles[
                        "Title"
                    ],

                    alignment=TA_CENTER,

                    fontName="Arial-Bold",

                    fontSize=20,

                    leading=24,

                    textColor=self.BRAND[
                        "text"
                    ],

                    spaceAfter=18,
                )
            )
        )

        elements.append(

            HRFlowable(

                width="100%",

                thickness=1,

                color=self.BRAND[
                    "border"
                ],

                spaceBefore=0,

                spaceAfter=14,
            )
        )

        toc = TableOfContents()

        toc.dotsMinLevel = 1

        toc.levelStyles = [

            ParagraphStyle(

                name="TOCLevel0",

                fontName="Arial-Bold",

                fontSize=16,

                leading=34,

                leftIndent=0,

                firstLineIndent=0,

                spaceBefore=34,

                spaceAfter=20,

                textColor="#222222",
            ),

            ParagraphStyle(

                name="TOCLevel1",

                fontName="Arial",

                fontSize=10,

                leading=14,

                leftIndent=36,

                firstLineIndent=0,

                spaceBefore=0,

                spaceAfter=2,

                textColor="#777777",
            ),
        ]

        elements.append(
            toc
        )

        elements.append(

            Spacer(
                1,
                18
            )
        )

        elements.append(

            HRFlowable(

                width="100%",

                thickness=0.8,

                color=self.BRAND[
                    "border"
                ],

                spaceBefore=0,

                spaceAfter=0,
            )
        )

        elements.append(
            self._page_break()
        )

    def _build_document(
        self
    ):

        document = (
            self._create_document()
        )

        elements = []

        self._build_sections(
            elements
        )

        try:

            logger.info(
                "Building PDF"
            )

            document.multiBuild(
                elements
            )

            logger.info(
                "PDF completed"
            )

        except Exception:

            logger.exception(
                "PDF failed"
            )

            raise

    def _build_sections(
        self,
        elements
    ):

        self._build_cover_section(
            elements
        )

        self._build_table_of_contents(
            elements
        )

        sections = [

            (
                self._build_executive_summary,
                "Heading1",
            ),

            (
                self._build_error_distribution,
                "Heading1",
            ),

            (
                self._build_top_errors,
                "Heading2",
            ),

            (
                self._build_validation_errors,
                "Heading2",
            ),

            (
                self._build_recommendations,
                "Heading1",
            ),
        ]

        for builder, heading_style in sections:

            self.current_heading_style = (
                heading_style
            )

            builder(
                elements
            )



    def generate(
        self
    ):

        logger.info(
            "Generating PDF"
        )

        self._build_document()

        logger.info(
            "Done"
        )