from reportlab.lib import colors

from reportlab.lib.enums import (
    TA_CENTER,
    TA_LEFT,
)

from reportlab.lib.styles import (
    ParagraphStyle,
)


class StylesMixin:

    def _configure_styles(
        self
    ):

        for style in (

            self.styles.byName.values()

        ):

            style.fontName = (
                "Arial"
            )

        self.styles["Title"].fontName = (
            "Arial-Bold"
        )

        self.styles["Title"].fontSize = 24

        self.styles["Title"].leading = 30

        self.styles["Title"].alignment = (
            TA_CENTER
        )

        self.styles["Heading1"].fontName = (
            "Arial-Bold"
        )

        self.styles["Heading1"].fontSize = 18

        self.styles["Heading1"].leading = 24

        self.styles["Heading2"].fontName = (
            "Arial-Bold"
        )

        self.styles["Heading2"].fontSize = 15

        self.styles["Heading2"].leading = 20

        self.styles["BodyText"].fontName = (
            "Arial"
        )

        self.styles["BodyText"].fontSize = 11

        self.styles["BodyText"].leading = 18

        self.styles["BodyText"].textColor = (
            self.BRAND["text"]
        )

        self.styles["Normal"].fontName = (
            "Arial"
        )

        self.styles["Normal"].fontSize = 10

        self.styles["Normal"].leading = 15

        self._build_custom_styles()


    def _build_custom_styles(
        self
    ):

        self.styles.add(

            ParagraphStyle(

                "Summary",

                parent=self.styles[
                    "BodyText"
                ],

                fontName="Arial-Bold",

                fontSize=18,

                leading=24,

                alignment=TA_CENTER,

                textColor=self.BRAND[
                    "primary"
                ],
            )
        )

        self.styles.add(

            ParagraphStyle(

                "Status",

                parent=self.styles[
                    "Heading1"
                ],

                fontName="Arial-Bold",

                fontSize=28,

                leading=34,

                alignment=TA_CENTER,

                textColor=self.BRAND[
                    "primary"
                ],
            )
        )

        self.styles.add(

            ParagraphStyle(

                "Card",

                parent=self.styles[
                    "BodyText"
                ],

                fontName="Arial",

                fontSize=11,

                leading=18,

                alignment=TA_CENTER,

                textColor=self.BRAND["text"],

                spaceAfter=0,
            )
        )

        self.styles.add(

            ParagraphStyle(

                "CardValue",

                parent=self.styles[
                    "BodyText"
                ],

                fontName="Arial-Bold",

                fontSize=22,

                leading=26,

                alignment=TA_CENTER,

                textColor=colors.white,
            )
        )

        self.styles.add(

            ParagraphStyle(

                "CardLabel",

                parent=self.styles[
                    "BodyText"
                ],

                fontName="Arial",

                fontSize=10,

                leading=14,

                alignment=TA_CENTER,

                textColor=colors.white,
            )
        )

        self.styles.add(

            ParagraphStyle(

                "Recommendation",

                parent=self.styles[
                    "BodyText"
                ],

                fontName="Arial",

                fontSize=11,

                leading=20,

                alignment=TA_LEFT,

                textColor=self.BRAND["text"],

            )
        )

        self.styles.add(

            ParagraphStyle(

                "Footer",

                parent=self.styles[
                    "BodyText"
                ],

                fontName="Arial",

                fontSize=9,

                leading=12,

                alignment=TA_CENTER,

                textColor=colors.grey,
            )
        )