from abc import ABC
from abc import abstractmethod

from backend.app.models.document import (
    DocumentModel
)

from backend.app.models.validation import (
    ValidationError
)


class BaseRule(ABC):

    @abstractmethod
    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        pass