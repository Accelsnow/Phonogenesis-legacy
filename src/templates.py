from __future__ import annotations
from typing import List
from feature_lib import Particle


class Template:
    _size: int
    _components: List[Particle]

    def __init__(self, components: List[Particle]) -> None:
        self._components = components
        self._size = len(components)

    def generate_word_list(self):
        pass

    def get_components(self) -> List[Particle]:
        return [block for block in self._components]

    def __str__(self) -> str:
        return "-".join([str(p) for p in self._components])


def import_default_templates(feature_pool: List[str]) -> List[Template]:
    return _fetch_template_csv("defaulttemplate.txt", feature_pool)


def _fetch_template_csv(filename: str, feature_pool: List[str]) -> List[Template]:
    templates = []  # type: List[Template]

    with open(filename, encoding='utf-8') as data_file:
        lines = [l.rstrip('\n') for l in data_file.readlines()]

        for line in lines:
            particle_list = line.split("-")
            particles = []

            for particle_data in particle_list:
                particle_data = particle_data.rstrip(']').lstrip('[')
                feature_list = particle_data.split(",")

                for feature in feature_list:
                    if feature not in feature_pool:
                        raise ImportError("Template line %s does not conform to the given features." % line)

                particles.append(Particle(feature_list))

            template = Template(particles)
            templates.append(template)

    return templates
