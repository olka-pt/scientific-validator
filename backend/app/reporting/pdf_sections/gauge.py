from math import (
    radians,
    cos,
    sin,
)

from reportlab.lib import colors

from reportlab.graphics.shapes import (
    Drawing,
    Rect,
    Circle,
    String,
    Line,
    Wedge,
)


class GaugeMixin:


    def _build_gauge_background(
        self,
        gauge
    ):

        center_x = self.LAYOUT[
            "gauge_center_x"
        ]

        center_y = self.LAYOUT[
            "gauge_center_y"
        ]

        outer = self.LAYOUT[
            "gauge_outer_radius"
        ]

        inner = self.LAYOUT[
            "gauge_inner_radius"
        ]

        gauge.add(

            Rect(

                self.LAYOUT[
                    "gauge_card_x"
                ],
                self.LAYOUT[
                    "gauge_card_y"
                ],

                self.LAYOUT[
                        "gauge_card_width"
                    ],
                self.LAYOUT[
                    "gauge_card_height"
                ],

                rx=24,
                ry=24,

                fillColor=colors.white,

                strokeColor=self.BRAND[
                    "border"
                ]
            )
        )

        zones = self._gauge_zones()

        for start, end, color in zones:

            gauge.add(

                Wedge(

                    center_x,

                    center_y,

                    outer,

                    start,

                    end,

                    fillColor=color,

                    strokeColor=None
                )
            )

        gauge.add(

            Circle(

                center_x,

                center_y,

                inner,

                fillColor=colors.white,

                strokeColor=None
            )
        )

        return gauge

    def _gauge_zones(
        self
    ):

        return [

            (
                108,
                180,
                self.BRAND["danger"]
            ),

            (
                54,
                108,
                self.BRAND["warning"]
            ),

            (
                0,
                54,
                self.BRAND["success"]
            ),
        ]

    def _build_gauge_indicator(
        self,
        gauge,
        score,
        status,
        accent
    ):

        center_x = self.LAYOUT[
            "gauge_center_x"
        ]

        center_y = self.LAYOUT[
            "gauge_center_y"
        ]

        arrow = self.LAYOUT[
            "gauge_arrow_length"
        ]

        score = max(
            0,
            min(score, 100)
        )

        angle = radians(
            180 - score * 1.8
        )

        gauge.add(

            Line(

                center_x,

                center_y,

                center_x + arrow * cos(angle),

                center_y + arrow * sin(angle),

                strokeWidth=6,

                strokeColor=colors.black
            )
        )

        gauge.add(

            Circle(

                center_x,

                center_y,

                10,

                fillColor=accent,

                strokeColor=None
            )
        )

        gauge.add(

            String(

                center_x,

                center_y + 10,

                f"{score:.1f}%",

                fontName="Arial-Bold",

                fontSize=36,

                fillColor=self.BRAND[
                    "primary"
                ],

                textAnchor="middle"
            )
        )

        gauge.add(

            String(

                center_x,

                center_y - 25,

                str(
                    status
                ),

                fontName="Arial",

                fontSize=14,

                fillColor=accent,

                textAnchor="middle"
            )
        )

        return gauge

    def _build_score_gauge(
        self,
        elements,
        score,
        status,
        accent
    ):

        gauge = Drawing(

            self.LAYOUT["gauge_width"],

            self.LAYOUT["gauge_height"]
        )

        self._build_gauge_background(
            gauge
        )

        self._build_gauge_indicator(

            gauge,

            score,

            status,

            accent
        )

        elements.append(
            gauge
        )