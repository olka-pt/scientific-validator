from reportlab.platypus import Spacer


class HelpersMixin:
    
    def _gap(
        self,
        height
    ):

        return Spacer(
            1,
            height
        )


    def _append(
        self,
        elements,
        item,
        gap=None
    ):

        elements.append(
            item
        )

        if gap is not None:

            elements.append(

                self._gap(
                    gap
                )
            )