from collections import Counter

from reportlab.platypus import (
    Paragraph,
    Table,
    PageBreak,
)


class TopErrorsMixin:

    def _build_top_error_card(
        self,
        position,
        category,
        count,
    ):

        content = Paragraph(

            (
                f"<b>#{position}</b>"
                "<br/><br/>"
                f"{category}"
                "<br/><br/>"
                f"<font size='34'><b>{count}</b></font>"
            ),

            self.styles["Card"]
        )

        table = Table(

            [[content]],

            colWidths=[
                230
            ],

            rowHeights=[
                100
            ]
        )

        self._apply_table_style(

            table,

            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                self.BRAND["card"],
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
                18,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                18,
            ),

            (
                "LINEBEFORE",
                (0, 0),
                (0, -1),
                6,
                self.BRAND["primary"],
            ),
        )

        return table

    def _build_top_errors(
        self,
        elements
    ):

        self._append(

            elements,

            self._build_heading(

                title=self.text[
                    "top_error_categories"
                ],

                style_name="Heading2",

                number="2.1",
                
            ),

            self.LAYOUT[
                "space_medium"
            ]
        )

        categories = [

            error.category

            for error in (
                self.result.errors
            )
        ]

        if not categories:

            elements.append(

                Paragraph(

                    self.text[
                        "no_errors",
                    ],

                    self.styles[
                        "BodyText"
                    ]
                )
            )

            elements.append(
                PageBreak()
            )

            return

        counter = Counter(
            categories
        )

        cards = []

        for position, (category, count) in enumerate(

            counter.most_common(5),

            start=1
        ):

            cards.append(

                self._build_top_error_card(

                    position,

                    self.text.get(
                        category,
                        category
                    ),

                    count
                )
            )


        for i in range(

            0,

            len(cards),

            2
        ):

            row = cards[i:i + 2]

            if len(row) == 1:

                row.append("")

            elements.append(

                Table(

                    [row],

                    colWidths=[250, 250]
                )
            )

            elements.append(

                self._gap(
                    14
                )
            )

        elements.append(
            PageBreak()
        )