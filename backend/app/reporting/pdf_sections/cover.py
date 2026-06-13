from datetime import datetime

from reportlab.lib import colors

from reportlab.platypus import (
    Table,
    Image,
    Paragraph,
    PageBreak,
     NextPageTemplate,
)


class CoverMixin:

    def _load_logo(
        self
    ):

        try:

            logo = Image(

                "backend/assets/logo.png",

                width=120,

                height=86,
            )

            logo.hAlign = (
                "CENTER"
            )

            return logo

        except Exception:

            return None


    def _build_logo_block(
        self,
        elements,
    ):

        elements.append(

            self._gap(

                self.LAYOUT[
                    "space_large"
                ]
            )
        )

        logo = (
            self._load_logo()
        )

        if logo:

            elements.append(
                logo
            )

        elements.append(

            self._gap(2)
        )


    def _create_cover_data(
        self
    ):

        return [

            [

                self.text[
                    "checks"
                ],

                str(
                    self.result.total_checks
                ),
            ],

            [

                self.text[
                    "errors"
                ],

                str(
                    self.result.total_errors
                ),
            ],

            [

                self.text[
                    "score"
                ],

                f"{self.result.score:.1f}%"
            ],

            [

                self.text[
                    "generated"
                ],

                datetime.now().strftime(
                    "%d.%m.%Y %H:%M"
                ),
            ],
        ]


    def _build_cover_table(
        self,
        elements,
    ):

        data = (
            self._create_cover_data()
        )

        inner_table = Table(

            data,

            colWidths=[

                240,

                240,
            ]
        )
        
        inner_table.hAlign = "CENTER"

        inner_table.spaceBefore = 0
        inner_table.spaceAfter = 0

        self._apply_table_style(

            inner_table,

            (
                "BACKGROUND",

                (0, 0),

                (-1, -1),

                colors.HexColor("#5E6678")
            ),

            (
                "BOX",

                (0, 0),

                (-1, -1),

                1.5,

                colors.Color(
                    0.72,
                    1.0,
                    0.98,
                    alpha=0.30,
                ),
            ),

            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                10,
            ),

            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                10,
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                3,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                3,
            ),

            (
                "TEXTCOLOR",

                (0, 0),

                (-1, -1),

                colors.white
            ),

            (
                "FONTNAME",

                (0, 0),

                (0, -1),

                "Arial-Bold",
            ),

            (
                "FONTNAME",

                (1, 0),

                (1, -1),

                "Arial",
            ),

            (
                "FONTSIZE",

                (0, 0),

                (-1, -1),

                11,
            ),

            (
                "LINEAFTER",
                (0, 0),
                (0, -1),
                1,
                colors.HexColor("#334155"),
            ),

            (
                "ROUNDEDCORNERS",

                [18],
            ),

            (
                "VALIGN",

                (0, 0),

                (-1, -1),

                "MIDDLE",
            ),
        )


        # TOP LIGHT REFLECTION


        self._apply_table_style(

            inner_table,

            (
                "BACKGROUND",

                (0, 0),

                (0, -1),

                colors.Color(
                    0.18,
                    0.55,
                    0.72,
                    alpha=0.18,
                )
            ),
        )

        inner_table.hAlign = "CENTER"

        elements.append(
            inner_table
        )


    def _build_footer(
        self,
        elements,
    ):

        elements.append(

            self._gap(

                self.LAYOUT[
                    "space_footer"
                ]
            )
        )

        elements.append(

            Paragraph(

                self.text[
                    "footer"
                ],

                self.styles[
                    "Footer"
                ]
            )
        )

        elements.append(
            PageBreak()
        )


    def _build_status_block(
        self,
        elements,
    ):


        score = self.result.score


        if score >= 95:

            status = self.text[
                "pass"
            ]

            color = self.BRAND[
                "primary"
            ]


        elif score >= 70:

            status = self.text[
                "warning_status"
            ]

            color = self.BRAND[
                "warning"
            ]


        else:

            status = self.text[
                "fail"
            ]

            color = self.BRAND[
                "danger"
            ]

        style = (

            self.styles[
                "Status"
            ].clone(
                "DynamicStatus"
            )
        )

        style.textColor = (
            color
        )

        # elements.append(

        #     Paragraph(

        #         (
        #             "<para align='center' leading='26'>"

        #             f"<font size='14' color='{color}'>"
        #             f"<b>{status}</b>"
        #             "</font>"

        #             "<br/><br/>"

        #             "<font size='18' color='#67E8F9'>"
        #             "● ● ●"
        #             "</font>"

        #             "<br/><br/>"

        #             f"<font size='42' color='#F8FFFF'>"
        #             f"<b>{self.result.score:.1f}</b>"
        #             "</font>"

        #             "<font size='18' color='#67E8F9'>"
        #             "%"
        #             "</font>"

        #             "<br/><br/>"

        #             "<font size='10' color='#475569'>"
        #             "A I   V A L I D A T I O N   S C O R E"
        #             "</font>"

        #             "</para>"
        #         ),

        #         style,
        #     )
        # )        

        # elements.append(

        #     self._gap(4)
        # )

        # elements.append(

        #     Paragraph(

        #         (
        #             "<para align='center'>"
        #             "<font size='15' color='#E2E8F0'>"
        #             "<b>scientific_article.docx</b>"
        #             "</font>"
        #             "</para>"
        #         ),

        #         self.styles["BodyText"]
        #     )
        # )

        # elements.append(

        #     self._gap(4)
        # )

        # elements.append(

        #     Paragraph(

        #         (
        #             "<para align='center'>"
        #             "<font size='10' color='#475569'>"
        #             "Авторы: Иванов И.И., Петров П.П."
        #             "</font>"
        #             "</para>"
        #         ),

        #         self.styles["BodyText"]
        #     )
        # )

        # elements.append(

        #     self._gap(2)
        # )

        # # self._build_cover_table(
        # #     elements
        # # )

        elements.append(
            self._gap(20)
        )

       

    def _build_cover_section(
        self,
        elements,
    ):

        elements.append(
            NextPageTemplate(
                "default"
            )
        )

        elements.append(
            PageBreak()
        )
