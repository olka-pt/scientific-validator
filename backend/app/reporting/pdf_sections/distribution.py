from collections import Counter

from reportlab.lib import colors

from reportlab.platypus import (
    Paragraph,
    Table,
    PageBreak,
)

from reportlab.graphics.shapes import (
    Drawing,
)

from reportlab.graphics.charts.barcharts import (
    HorizontalBarChart,
)


class DistributionMixin:

    def _build_error_distribution(
        self,
        elements,
    ):

        self._append(
            elements,
            self._build_heading(
                title=self.text[
                    "distribution"
                ],
                style_name="Heading1",

                number="2",
            ),
            self.LAYOUT["space_medium"],
        )

        categories = [
            error.category
            for error in self.result.errors
        ]

        counter = Counter(
            categories
        )

        if not counter:

            elements.append(
                Paragraph(
                    self.text[
                        "no_errors"
                    ],
                    self.styles["BodyText"],
                )
            )

            elements.append(
                PageBreak()
            )

            return

        labels = [

            self.text.get(
                category,
                category
            )

            for category in (
                counter.keys()
            )
        ]

        values = list(
            counter.values()
        )

        drawing = Drawing(
            self.LAYOUT["distribution_width"],
            self.LAYOUT["distribution_height"],
        )

        chart = HorizontalBarChart()

        chart.x = 90
        chart.y = 50

        chart.width = (
            self.LAYOUT["distribution_width"]
            - 180
        )

        chart.height = (
            min(
                65 * len(values),
                260
            )
        )

        chart.data = [values]

        chart.categoryAxis.categoryNames = (
            labels
        )

        chart.categoryAxis.labels.fontName = (
            "Arial"
        )

        chart.categoryAxis.labels.fontSize = 11

        chart.categoryAxis.labels.fillColor = (
            self.BRAND["text"]
        )

        chart.valueAxis.labels.fontName = (
            "Arial"
        )

        chart.valueAxis.labels.fontSize = 10

        chart.categoryAxis.labels.boxAnchor = (
            "e"
        )

        chart.valueAxis.valueMin = 0

        chart.valueAxis.valueMax = (
            max(values) + 1
        )

        chart.valueAxis.valueStep = 1

        chart.valueAxis.visible = False

        chart.categoryAxis.visibleAxis = False

        chart.categoryAxis.visibleTicks = False

        chart.bars[0].fillColor = (
            self.BRAND["secondary"]
        )

        chart.bars[0].strokeColor = (
            self.BRAND["secondary"]
        )

        chart.barWidth = 14

        chart.barSpacing = 10

        chart.groupSpacing = 10

        drawing.add(
            chart
        )

        self._append(
            elements,
            drawing,
            self.LAYOUT["space_medium"],
        )

        rows = [
            [
                self.text["category"],
                self.text["count"],
                self.text["percent"],
            ]
        ]

        total = sum(values)

        for label, value in zip(
            labels,
            values,
        ):

            rows.append(
                [
                    self.text.get(
                        label,
                        label,
                    ),
                    str(value),
                    f"{value / total * 100:.1f}%",
                ]
            )

        table = Table(
            rows,
            colWidths=[
                self.LAYOUT["legend_col"],
                self.LAYOUT["legend_value"],
                self.LAYOUT["legend_value"],
            ],
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

        elements.append(
            PageBreak()
        )