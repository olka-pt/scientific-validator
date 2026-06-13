# backend/app/reporting/pdf_sections/errors.py

from xml.sax.saxutils import escape

from reportlab.platypus import (
    Paragraph,
    Table,
)


class ErrorsMixin:

    def _safe_text(
        self,
        value,
    ) -> str:
        return escape(
            str(value)
            if value is not None
            else ""
        )

    def _error_style(
        self,
        category,
    ):

        if category == "formatting":
            return (
                self.text["warning"],
                self.BRAND["warning_light"],
                self.BRAND["warning"],
            )

        if category in (
            "structure",
            "language",
        ):
            return (
                self.text["info"],
                self.BRAND["success_light"],
                self.BRAND["success"],
            )

        return (
            self.text["critical"],
            self.BRAND["danger_light"],
            self.BRAND["danger"],
        )

    def _build_error_card(
        self,
        error,
        background,
        accent,
    ):

        paragraph = (
            f"<font color='{accent}'>"
            f"<b>{self._safe_text(error['severity'])}</b>"
            f"</font>"
            "<br/><br/>"
            +
            (
                f"<b>{self.text['paragraph']}:</b> {self._safe_text(error['paragraph'])}"
                if (
                    error["paragraph"] is not None
                    and error["paragraph"] >= 0
                )
                else
                "<b>Общая ошибка</b>"
            )
            +
            "<br/>"
            +
            f"<b>{self.text['category']}:</b> "
            f"{self._safe_text(error['category'])}"
            "<br/><br/>"
            +
            self._safe_text(error["message"])
            +
            "<br/><br/>"
            +
            f"<b>{self.text['expected']}:</b> "
            f"{self._safe_text(error['expected'])}"
            "<br/>"
            +
            f"<b>{self.text['actual']}:</b> "
            f"{self._safe_text(error['actual'])}"
        )

        table = Table(
            [[
                Paragraph(
                    paragraph,
                    self.styles["Card"],
                )
            ]],
            colWidths=[
                self.LAYOUT["content_width"]
            ],
        )

        self._apply_table_style(
            table,
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                background,
            ),
            (
                "BOX",
                (0, 0),
                (-1, -1),
                1,
                self.BRAND["border"],
            ),
            (
                "ROUNDEDCORNERS",
                [18],
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                18,
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                18,
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                10,
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10,
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP",
            ),
        )

        return table

    def _build_validation_errors(
        self,
        elements,
    ):

        self._append(
            elements,
            self._build_heading(
                title=self.text["validation_errors"],
                style_name="Heading2",
                number="2.2",
            ),
            self.LAYOUT["space_medium"],
        )

        for error in self.result.errors:

            severity, background, accent = self._error_style(
                error.category
            )

            elements.append(
                self._build_error_card(
                    {
                        "severity": severity,
                        "paragraph": error.paragraph_index,
                        "category": self.text.get(
                            error.category,
                            error.category,
                        ),
                        "message": error.message,
                        "expected": error.expected,
                        "actual": error.actual,
                    },
                    background,
                    accent,
                )
            )

            elements.append(
                self._gap(12)
            )