from __future__ import annotations

import random
from typing import List, Dict, Optional

from word import Word

from feature_lib import Particle
from sound import Sound


class Template:
    _size: int
    _components: List[Particle]

    def __init__(self, components: List[Particle]) -> None:
        self._components = components
        self._size = len(components)

    def generate_word_list(self, phonemes: Optional[List[Sound], None], size_limit: Optional[int, None],
                           feature_to_sounds: Dict[str, List[Sound]]) -> List[Word]:
        word_len = len(self._components)
        part_sounds = []
        word_list = set([])

        if word_len == 0:
            return []

        for particle in self._components:
            part_sound = particle.get_matching_sounds(phonemes, feature_to_sounds)
            part_sounds.append(part_sound)

        if size_limit is None:
            result = self._recur_full_word_list(part_sounds, 0, [''])

            return [Word(r) for r in result]
        else:
            word_count = 0
            while word_count < size_limit:
                curr_word = ''

                for i in range(word_len):
                    curr_word += str(random.choice(part_sounds[i]))

                word_list.add(curr_word)
                word_count += 1

            result = list(word_list)
            return [Word(r) for r in result]

    def _recur_full_word_list(self, comb_sound: List[List[Sound]], index: int, words: List[str]) -> List[str]:
        if index >= len(comb_sound):
            return words
        else:
            new_words = []  # type: List[str]

            for sound in comb_sound[index]:
                for word in words:
                    new_words.append(word + str(sound))

            return self._recur_full_word_list(comb_sound, index + 1, new_words)

    def get_word_list_size(self, phonemes: Optional[List[Sound], None],
                           feature_to_sounds: Dict[str, List[Sound]]) -> int:
        size = 1
        for particle in self._components:
            size *= len(particle.get_matching_sounds(phonemes, feature_to_sounds))

        return size

    def get_components(self) -> List[Particle]:
        return [block for block in self._components]

    def __str__(self) -> str:
        return "-".join([str(p) for p in self._components])


def import_default_templates(feature_pool: List[str]) -> List[Template]:
    return _fetch_templates("defaulttemplate.txt", feature_pool)


def _fetch_templates(filename: str, feature_pool: List[str]) -> List[Template]:
    templates = []  # type: List[Template]

    with open(filename, encoding='utf-8') as data_file:
        lines = [l.rstrip('\n') for l in data_file.readlines()]

        for line in lines:
            line = line.replace('ɡ', 'g')
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

