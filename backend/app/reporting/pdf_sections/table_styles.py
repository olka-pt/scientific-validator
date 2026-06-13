from reportlab.lib import colors
from reportlab.platypus import TableStyle


class TableStylesMixin:

    def _apply_table_style(
        self,
        table,
        *rules
    ):

        table.setStyle(
            self._table_style(
                *rules
            )
        )

        return table


    def _table_style(
        self,
        *rules
    ) -> TableStyle:

        return TableStyle(
            list(rules)
        )


    def _card_table_style(
        self,
        accent
    ):

        return self._table_style(

            (
                "FONT",
                (0, 0),
                (-1, -1),
                "Arial",
            ),

            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                accent
            ),

            (
                "ROUNDEDCORNERS",
                [12]
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
        )


    def _header_table_style(
        self,
        accent,
    ):

        return TableStyle([

            (
                "FONT",
                (0, 0),
                (-1, -1),
                "Arial",
            ),

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                accent,
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white,
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                self.BRAND["border"],
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                11,
            ),

            (
                "LEADING",
                (0, 0),
                (-1, -1),
                14,
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
                6,
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6,
            ),
        ])