from backend.app.reporting.recommendation_engine import (
    ValidationRecommendationEngine
)

from reportlab.lib import colors

from reportlab.platypus import (
    Paragraph,
    Table,
    PageBreak,
)


class RecommendationsMixin:


    def _recommendation_color(
        self,
        text,
    ):

        text = text.lower()

        if any(

            word in text

            for word in [

                "исправить",
                "ошибка",
                "несоответствие",
                "добавить",
                "отсутствует",
            ]
        ):

            return self.BRAND[
                "danger_light"
            ]

        if any(

            word in text

            for word in [

                "проверить",
                "рекомендуется",
                "желательно",
                "уточнить",
            ]
        ):

            return self.BRAND[
                "warning_light"
            ]

        if any(

            word in text

            for word in [

                "улучшить",
                "оптимизировать",
                "повысить",
            ]
        ):

            return self.BRAND[
                "success_light"
            ]

        return self.BRAND[
            "card"
        ]


    def _build_recommendation_card(
        self,
        index,
        text,
    ):

        content = Paragraph(

            (
                f"<font size=13><b>{index}.</b></font>"
                "<br/><br/>"
                f"{text}"
            ),

            self.styles[
                "Recommendation"
            ]
        )

        card = Table(

            [[content]],

            colWidths=[

                self.LAYOUT[
                    "content_width"
                ]
            ]
        )

        background = (

            self._recommendation_color(
                text
            )
        )

        self._apply_table_style(

            card,

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

                self.BRAND[
                    "border"
                ],
            ),

            (
                "ROUNDEDCORNERS",
                [18],
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP",
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
                16,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                16,
            ),
        )

        return card


    def _build_recommendations(
        self,
        elements,
    ):

        elements.append(
            PageBreak()
        )

        self._append(

            elements,

        self._build_heading(

            title=self.text[
                "recommendations"
            ],

            style_name="Heading1",

            number="3",
        ),

            self.LAYOUT[
                "space_medium"
            ],
        )

        engine = (

            ValidationRecommendationEngine(

                self.result
            )
        )

        recommendations = (

            engine.generate()
        )

        if not recommendations:

            elements.append(

                Paragraph(

                    self.text[
                        "no_recommendations"
                    ],

                    self.styles[
                        "BodyText"
                    ],
                )
            )

            return


        for index, recommendation in enumerate(

            recommendations,

            start=1,
        ):

            elements.append(

                self._build_recommendation_card(

                    index,

                    recommendation,
                )
            )

            elements.append(

                self._gap(

                    self.LAYOUT[
                        "space_small"
                    ]
                )
            )