from __future__ import annotations
from typing import List, Dict


class Template:
    _size: int
    _components: List[str]

    def __init__(self, components: List[str]) -> None:
        self._components = components
        self._size = len(components)

    def is_match(self, word: str, _dict: Dict) -> bool:
        if len(word) != self._size:
            return False

        for i in range(0, self._size):
            char = word[i]
            _type = self._components[i]

            if char not in _dict[_type]:
                return False

        return True

    def get_components(self) -> List[str]:
        return [block for block in self._components]

    def __str__(self):
        return " ".join(self._components)


def import_default_template() -> List[Template]:
    templates = _fetch_template_csv("defaulttemplate.txt")

    return templates


def _fetch_template_csv(filename: str) -> List[Template]:
    templates = []

    with open(filename, encoding='utf-8') as data_file:
        lines = [l.rstrip('\n') for l in data_file.readlines()]

        for line in lines:
            components = line.split(" ")
            templates.append(Template(components))

    return templates


def template_fits_features(templates: List[Template], features: List[str]) -> bool:
    for template in templates:
        for comp_block in template.get_components():
            if comp_block not in features:
                return False

    return True


if __name__ == "__main__":
    tmp = import_default_template()

    # for t in tmp:
    #     print(t)

    print(template_fits_features(tmp, ["consonant", "vowel"]))
