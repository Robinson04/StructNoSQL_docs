import os
import re
from mdscript import Runner
from mdscript.base_transformer import BaseTransformer
from typing import Optional


class FileTemplateTransformer(BaseTransformer):
    def __init__(self, runner: Runner, source_filepath: str, attribute: Optional[str]):
        super().__init__(runner=runner, source_filepath=source_filepath, attribute=attribute)
        if not isinstance(self.evaluated_attribute, dict):
            raise Exception("File template attribute must be of dict type")

        attributes_filepath: Optional[str] = self.evaluated_attribute.get('filepath', None)
        if attributes_filepath is None:
            raise Exception("Filepath must be defined")
        self.attributes_filepath: str = attributes_filepath

    @property
    def evaluated_attribute(self) -> dict:
        return super().evaluated_attribute

    def transform(self) -> str:
        if not os.path.isfile(self.attributes_filepath):
            raise Exception(f"File not found at {self.attribute}")

        self.runner.files_dependencies.add_dependency(
            parent_filepath=self.source_filepath,
            dependency_path=self.attributes_filepath
        )
        with open(self.attributes_filepath, 'r') as file:
            altered_file_content: str = file.read()
            for attribute_key, attribute_value in self.evaluated_attribute.items():
                regex_pattern: str = "{{" + attribute_key + "}}"
                altered_file_content = re.sub(regex_pattern, attribute_value, altered_file_content)
            return altered_file_content
