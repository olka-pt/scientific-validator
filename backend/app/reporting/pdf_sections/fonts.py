import logging
from pathlib import Path

from reportlab.platypus import (
    Spacer,
)

from reportlab.pdfbase import (
    pdfmetrics,
)

from reportlab.pdfbase.ttfonts import (
    TTFont,
)

logger = logging.getLogger(__name__)

class FontsMixin:

    # ==========================
    # Fonts
    # ==========================

    def _register_fonts(
        self
    ):

        font_dir = (
            Path(__file__)
            .parents[3]
            / "assets"
            / "fonts"
        )

        fonts = {

            "Arial": "Arial.ttf",

            "Arial-Bold": "Arial-Bold.ttf",

            "Arial-Italic": "Arial-Italic.ttf",

            "Arial-BoldItalic": "Arial-BoldItalic.ttf",
        }

        for name, file_name in fonts.items():

            font_path = (
                font_dir
                / file_name
            )

            if not font_path.exists():

                logger.warning(
                    "Font not found: %s",
                    font_path
                )

                continue

            pdfmetrics.registerFont(

                TTFont(
                    name,
                    str(font_path)
                )
            )

            logger.info(
                "REGISTERED: %s",
                name
            )
