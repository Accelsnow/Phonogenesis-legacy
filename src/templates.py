from __future__ import annotations
from typing import List, Dict, Optional
from sound import Sound
from feature_lib import Particle


class Template:
    _size: int
    _components: List[Particle]

    def __init__(self, components: List[Particle]) -> None:
        self._components = components
        self._size = len(components)

    def generate_word_list(self, phonemes: Optional[List[Sound], None], size_limit: Optional[int, None],
                           feature_to_sounds: Dict[str, List[Sound]]) -> List[str]:
        comb_sounds = []  # type: List[List[Sound]]
        curr_size = 0  # type: int

        for particle in self._components:
            comb_sounds.append(particle.get_matching_sounds(phonemes, feature_to_sounds))

        return self._recur_word(comb_sounds, 0, [''])

    def get_word_list_size(self, phonemes: Optional[List[Sound], None],
                           feature_to_sounds: Dict[str, List[Sound]]) -> int:
        size = 1
        for particle in self._components:
            size *= len(particle.get_matching_sounds(phonemes, feature_to_sounds))

        return size

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


def import_default_phonemes() -> List[Sound]:
    return _fetch_phoneme('defaultphoneme.txt')


def _fetch_phoneme(filename: str) -> List[Sound]:
    phonemes = []

    with open(filename, encoding='utf-8') as data_file:
        lines = [l.rstrip('\n') for l in data_file.readlines()]

        for line in lines:
            data = line.split(" ")

            for sound_str in data:
                phonemes.append(Sound('', [])[sound_str])

    return phonemes
