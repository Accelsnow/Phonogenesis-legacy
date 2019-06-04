from __future__ import annotations
from typing import List, Optional, Dict, Tuple, Set
from feature_lib import Particle
from templates import Template
from sound import Sound
from enum import Enum

EDGE_SYMBOL = '#'
NULL_SYMBOL = ''


class ExampleType(Enum):
    CADT = 0,
    CADNT = 1,
    CAND = 2,
    NCAD = 3,
    NCAND = 4,
    IRR = 5

    def __str__(self) -> str:
        return self.name


class Rule:
    """
    A>B/C_D
    """
    _A: Optional[List[Particle], str]
    _B: Optional[Particle, str]
    _C: Optional[List[Particle], str]
    _D: Optional[List[Particle], str]
    _CADT_lib: Dict[str, Tuple[int, int]]

    def __init__(self, a: Optional[List[Particle], str], b: Optional[Particle, str], c: List[Particle],
                 d: List[Particle]) -> None:
        self._A = a
        self._B = b
        self._C = c
        self._D = d
        self._CADT_lib = {}

    def get_info(self) -> Tuple[
        List[Particle], Optional[Particle, str], Optional[List[Particle], str], Optional[List[Particle], str]]:
        return self._A, self._B, self._C, self._D

    def apply(self, word: str, phonemes: List[Sound], feature_to_type: Dict[str, str],
              feature_to_sounds: Dict[str, List[Sound]]) -> str:
        if word not in self._CADT_lib.keys():
            if self.classify(word, phonemes, feature_to_type, feature_to_sounds) != ExampleType.CADT:
                return word

        index = self._CADT_lib[word]
        return self._do_replace(word, index[0], index[1], feature_to_type, feature_to_sounds)

    def classify(self, word: str, phonemes: List[Sound], feature_to_type: Dict[str, str],
                 feature_to_sounds: Dict[str, List[Sound]]) -> Set[ExampleType]:
        a_data = self.locations_a(word, phonemes, feature_to_sounds)
        a_locations = a_data[0]
        a_size = a_data[1]

        if len(a_locations) == 0 or a_locations == []:
            return {ExampleType.IRR}
        else:
            types = set([])  # type: set

            for a_loc in a_locations:
                is_c = False

                if isinstance(self._C, str):
                    if self._C == NULL_SYMBOL:
                        is_c = True
                    elif self._C == EDGE_SYMBOL:
                        if a_loc == 0:
                            is_c = True
                    else:
                        raise AttributeError("unknown string for C: %s" % self._C)
                else:
                    c_matcher = Template(self._C).generate_word_list(phonemes, feature_to_sounds)
                    c_size = len(c_matcher[0])

                    for c_pattern in c_matcher:
                        if a_loc - c_size >= 0 and word[a_loc - c_size:a_loc] == c_pattern:
                            is_c = True
                            break

                is_d = False

                if isinstance(self._D, str):
                    if self._D == NULL_SYMBOL:
                        is_d = True
                    elif self._D == EDGE_SYMBOL:
                        if a_loc == len(word) - 1:
                            is_d = True
                    else:
                        raise AttributeError("unknown string for D: %s" % self._D)

                else:
                    d_matcher = Template(self._D).generate_word_list(phonemes, feature_to_sounds)
                    d_size = len(d_matcher[0])

                    for d_pattern in d_matcher:
                        if a_loc + a_size + d_size <= len(word) and \
                                word[a_loc + a_size:a_loc + a_size + d_size] == d_pattern:
                            is_d = True
                            break

                if is_c and is_d:
                    if word == self._do_replace(word, a_loc, a_loc + a_size, feature_to_type, feature_to_sounds):
                        types = {ExampleType.CADNT}
                    else:
                        types = {ExampleType.CADT}
                        self._CADT_lib[word] = a_loc, a_loc + a_size
                elif ExampleType.CADT not in types and ExampleType.CADNT not in types:
                    if is_c and not is_d:
                        types.add(ExampleType.CAND)
                    elif not is_c and is_d:
                        types.add(ExampleType.NCAD)
                    elif not is_c and not is_d:
                        types.add(ExampleType.NCAND)

            return types

    def locations_a(self, word: str, phonemes: List[Sound], feature_to_sounds: Dict[str, List[Sound]]) -> Tuple[
        List[int], int]:
        if isinstance(self._A, str):
            if self._A == NULL_SYMBOL:
                return [i for i in range(0, len(word))], 0
            else:
                raise AttributeError('A can only be Null or List of particles')

        a_matcher = Template(self._A).generate_word_list(phonemes, feature_to_sounds)
        prev_index = 0
        locations = []
        size = len(a_matcher[0])
        i = 0

        while i < len(a_matcher):
            a_pattern = a_matcher[i]

            try:
                a_index = word.index(a_pattern, prev_index)

                prev_index = a_index + 1
                locations.append(a_index)
                i -= 1
            except ValueError:
                i += 1
                continue

        return locations, size

    def _do_replace(self, word: str, begin_index: int, end_index: int, feature_to_type: Dict[str, str],
                    feature_to_sounds: Dict[str, List[Sound]]) -> str:
        target = word[begin_index:end_index]
        if isinstance(self._B, str):
            raise NotImplementedError
        else:
            dest_sound = Sound('', [])[target].get_transformed_sound(self._B, feature_to_type, feature_to_sounds)

            if dest_sound is not None:
                return word[:begin_index] + str(dest_sound) + word[end_index:]
            else:
                return word

    def __str__(self) -> str:
        return "%s -> %s / %s _ %s" % (
            "".join([str(s) for s in self._A]), str(self._B), "".join([str(s) for s in self._C]),
            "".join([str(s) for s in self._D]))


def import_default_rules(feature_pool: List[str]) -> List[Rule]:
    return _fetch_rule_csv(feature_pool, "defaultrule.txt")


def _fetch_rule_csv(feature_pool: List[str], filename: str) -> List[Rule]:
    rules = []  # type: List[Rule]

    with open(filename, encoding='utf-8') as data_file:
        lines = [l.rstrip('\n') for l in data_file.readlines()]

        for line in lines:
            mid_break = line.split("/")

            if len(mid_break) != 2:
                raise ImportError("Invalid rule format: %s" % line)

            action_break = mid_break[0].split(">")
            condition_break = mid_break[1].split("_")

            if len(action_break) != 2 or len(condition_break) != 2:
                raise ImportError("Invalid rule format: %s" % line)

            asec = action_break[0]
            bsec = action_break[1]
            csec = condition_break[0]
            dsec = condition_break[1]

            if bsec[0] == '[' and bsec[-1] == ']':
                bsec = Particle(bsec.lstrip("[").rstrip("]").split(","))

            rules.append(Rule(_sec_to_particles(feature_pool, asec), bsec,
                              _sec_to_particles(feature_pool, csec), _sec_to_particles(feature_pool, dsec)))
    return rules


def _sec_to_particles(feature_pool: List[str], sec: str) -> Optional[List[Particle], str]:
    particles = []  # type: List[Particle]

    parts = sec.lstrip('[').rstrip(']').split("][")

    if len(parts) == 1 and (parts[0] == EDGE_SYMBOL or parts[0] == NULL_SYMBOL):
        return parts[0]

    for part in parts:
        features = part.split(",")

        for feature in features:
            if feature not in feature_pool:
                raise ImportError("Rule sector %s does not conform to the given features." % sec)

        particles.append(Particle(features))

    return particles
