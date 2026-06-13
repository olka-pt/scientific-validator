from reportlab.platypus import (
    Paragraph,
    PageBreak,
)

from reportlab.platypus.tableofcontents import (
    TableOfContents,
)

from reportlab.lib.styles import (
    ParagraphStyle,
)


class TOCMixin:

    def _build_table_of_contents(
        self,
        elements,
    ):

        elements.append(

            Paragraph(

                self.text.get(
                    "contents",
                    "Содержание",
                ),

                self.styles[
                    "Title"
                ],
            )
        )

        elements.append(

            self._gap(
                30
            )
        )

        toc = TableOfContents()

        toc.levelStyles = [

            ParagraphStyle(

                "TOC",

                parent=self.styles[
                    "BodyText"
                ],

                fontName="Arial",

                fontSize=14,

                leading=14,

                textColor=self.BRAND[
                    "muted"
                ],

                leftIndent=0,

                firstLineIndent=0,

                rightIndent=0,

                spaceBefore=2,

                spaceAfter=0,

                endDots=".",

                allowWidows=1,
                
                bulletFontName="Arial-Bold",
            )
        ]

        toc.dotsMinLevel = 1

        elements.append(
            toc
        )

        elements.append(
            PageBreak()
        )

        self.toc = toc