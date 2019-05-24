from __future__ import annotations
from typing import List, Dict
import warnings
import feature_lib


class Template:
    _size: int
    _components: List[str]

    def __init__(self, components: List[str]) -> None:
        self._components = components
        self._size = len(components)

    def is_match(self, word: str, dict_: Dict) -> bool:
        if len(word) != self._size:
            return False

        for i in range(0, self._size):
            char = word[i]
            type_ = self._components[i]

            if char not in dict_[type_]:
                return False

        return True

    def get_components(self) -> List[str]:
        return [block for block in self._components]

    def __str__(self):
        return " ".join(self._components)


def import_default_templates(feature_pool: List[str]) -> List[Template]:
    return _fetch_template_csv("defaulttemplate.txt", feature_pool)


def _fetch_template_csv(filename: str, feature_pool: List[str]) -> List[Template]:
    templates = []  # type: List[Template]

    with open(filename, encoding='utf-8') as data_file:
        lines = [l.rstrip('\n') for l in data_file.readlines()]

        for line in lines:
            components = line.split(" ")

            for comp in components:
                if comp not in feature_pool:
                    raise ImportError("Template %s does not conform to the given features." % str(template))

            template = Template(components)
            templates.append(template)

    return templates
