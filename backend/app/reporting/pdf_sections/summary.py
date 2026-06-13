from collections import Counter

from reportlab.platypus import (
    Paragraph,
    Table,
    PageBreak,
)


class SummaryMixin:

    def _style_summary_card(
        self,
        card,
        accent,
    ):

        self._apply_table_style(

            card,

            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                accent,
            ),

            (
                "ROUNDEDCORNERS",
                [16],
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                self.LAYOUT[
                    "card_padding"
                ],
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                self.LAYOUT[
                    "card_padding"
                ],
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8,
            ),
        )

        return card


    def _create_card(
        self,
        title,
        value,
        accent,
    ):

        content = Paragraph(

            (
                "<para align='center'>"
                f"<b>{title}</b>"
                "<br/><br/>"
                f"<font size='20'>{value}</font>"
                "</para>"
            ),

            self.styles[
                "Card"
            ]
        )

        card = Table(

            [[content]],

            colWidths=[

                self.LAYOUT[
                    "card_width"
                ]
            ],

            rowHeights=[

                self.LAYOUT[
                    "card_height"
                ]
            ],
        )

        return self._style_summary_card(

            card,

            accent,
        )


    def _build_card_row(
        self,
        cards,
        accent,
    ):

        return [

            self._create_card(

                title,

                value,

                accent,
            )

            for title, value in cards
        ]


    def _create_card_table(
        self,
        row,
    ):

        return Table(

            [row],

            colWidths=[

                self.LAYOUT[
                    "card_table_width"
                ]

            ] * len(row)
        )


    def _build_summary_cards(
        self,
        elements,
        cards,
        accent,
    ):

        row = self._build_card_row(

            cards,

            accent,
        )

        elements.append(

            self._create_card_table(
                row
            )
        )


    def _build_executive_summary(
        self,
        elements,
    ):

        score = round(

            self.result.score,

            1,
        )

        categories = Counter(

            error.category

            for error in self.result.errors
        )

        top_problem = (

            self.text.get(

                max(

                    categories,

                    key=categories.get,
                ),

                self.text[
                    "no_errors"
                ],
            )

            if categories

            else self.text[
                "no_errors"
            ]
        )

        if score >= 90:

            status = self.text[
                "passed"
            ]

            accent = self.BRAND[
                "success"
            ]

        elif score >= 70:

            status = self.text[
                "warning_status"
            ]

            accent = self.BRAND[
                "warning"
            ]

        else:

            status = self.text[
                "failed"
            ]

            accent = self.BRAND[
                "danger"
            ]

            self.LAYOUT[
                "space_medium"
            ],
            

        cards = [

            (
                self.text[
                    "validation_score"
                ],

                f"{score:.1f}%"
            ),

            (
                self.text[
                    "total_errors"
                ],

                str(
                    self.result.total_errors
                )
            ),

            (
                self.text[
                    "total_checks"
                ],

                str(
                    self.result.total_checks
                )
            ),

            (
                self.text[
                    "top_issue"
                ],

                top_problem
            ),
        ]

        self._append(

            elements,

            self._build_heading(

                title=self.text[
                    "executive_summary"
                ],

                style_name="Heading1",

                number="1",
            ),

            self.LAYOUT[
                "space_medium"
            ],
        )

        self._build_summary_cards(

            elements,

            cards,

            accent,
        )

        elements.append(

            self._gap(

                self.LAYOUT[
                    "space_large"
                ]
            )
        )

#        self._build_score_gauge(
#
#           elements,
#
#            score,
#
#            status,
#
#            accent,
#        )

        elements.append(

            self._gap(20)
        )

        self._build_summary_table(
            elements
        )

        elements.append(
            PageBreak()
        )


    def _build_summary_table(
        self,
        elements,
    ):

        rows = [
            [
                self.text["metric"],
                self.text["value"],
            ],

            [
                self.text["validation_score"],
                f"{self.result.score:.1f}%"
            ],

            [
                self.text["total_errors"],
                str(self.result.total_errors)
            ],

            [
                self.text["total_checks"],
                str(self.result.total_checks)
            ],
        ]

        table = Table(
            rows,
            colWidths=[260, 180],
        )

        table.setStyle(

            self._header_table_style(

                self.BRAND[
                    "primary"
                ]
            )
        )

        elements.append(
            table
        )