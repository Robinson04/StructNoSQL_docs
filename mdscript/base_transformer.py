import ast
import logging

from mdscript.runner import Runner
from abc import abstractmethod
from typing import Optional, Any


class BaseTransformer:
    def __init__(self, runner: Runner, source_filepath: str, attribute: Optional[str]):
        self.runner = runner
        self.source_filepath = source_filepath
        self._attribute = attribute
        self._evaluated_attribute: Optional[Any] = None

    @property
    def attribute(self) -> Optional[Any]:
        return self._attribute

    @property
    def evaluated_attribute(self) -> Optional[Any]:
        if self._evaluated_attribute is None:
            try:
                self._evaluated_attribute = ast.literal_eval(self._attribute) if self._attribute is not None else None
            except SyntaxError as e:
                logging.warning(e)
                self._evaluated_attribute = None
        return self._evaluated_attribute

    @abstractmethod
    def transform(self) -> str:
        raise Exception(f"transform function must be implemented")

    def test(self) -> bool:
        # The implementation of the test function is optional, hence the missing @abstractmethod.
        # If the test function is not implemented, we return True so that it will be considered as passed.
        return True
