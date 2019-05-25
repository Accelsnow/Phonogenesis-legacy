from __future__ import annotations
from typing import List, Dict
from sound import Sound
from feature_lib import Particle


class Template:
    _size: int
    _components: List[Particle]

    def __init__(self, components: List[Particle]) -> None:
        self._components = components
        self._size = len(components)

    def generate_word_list(self, feature_to_sounds: Dict[str, List[Sound]]) -> List[str]:
        comb_sounds = []  # type: List[List[Sound]]

        for particle in self._components:
            comb_sounds.append(particle.get_matching_sounds(feature_to_sounds))

        return self._recur_word(comb_sounds, 0, [''])

    def _recur_word(self, comb_sound: List[List[Sound]], index: int, words: List[str]) -> List[str]:
        if index >= len(comb_sound):
            return words
        else:
            new_words = []  # type: List[str]

            for sound in comb_sound[index]:
                for word in words:
                    new_words.append(word + str(sound))

            return self._recur_word(comb_sound, index + 1, new_words)

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
