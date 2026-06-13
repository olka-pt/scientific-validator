from copy import deepcopy

from backend.app.models.document import DocumentModel


DEFAULT_FONT_FAMILY = (
    "Times New Roman"
)

DEFAULT_FONT_SIZE = 14

DEFAULT_ALIGNMENT = (
    "justify"
)


class DocumentNormalizer:

    @staticmethod
    def normalize(
        document: DocumentModel
    ) -> DocumentModel:

        normalized_document = (
            deepcopy(document)
        )

        for paragraph in (
            normalized_document.paragraphs
        ):

            if (
                paragraph.font_family
                is None
            ):
                paragraph.font_family = (
                    DEFAULT_FONT_FAMILY
                )

            if (
                paragraph.font_size
                is None
            ):
                paragraph.font_size = (
                    DEFAULT_FONT_SIZE
                )

            if (
                paragraph.alignment
                is None
            ):
                paragraph.alignment = (
                    DEFAULT_ALIGNMENT
                )

        return normalized_document