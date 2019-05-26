from __future__ import annotations
from typing import List, Optional, Dict, Tuple
from feature_lib import Particle
from templates import Template
from sound import Sound

EDGE_SYMBOL = '#'
NULL_SYMBOL = ''


class Rule:
    """
    A>B/C_D
    """
    _A: List[Particle]
    _B: Optional[Particle, str]
    _C: Optional[List[Particle], str]
    _D: Optional[List[Particle], str]

    def __init__(self, a: List[Particle], b: Optional[Particle, str], c: List[Particle],
                 d: List[Particle]) -> None:
        self._A = a
        self._B = b
        self._C = c
        self._D = d

    def apply(self, word: str, feature_to_type: Dict[str, str], feature_to_sounds: Dict[str, List[Sound]]) -> str:
        c_index = None
        c_fixed = False
        c_matcher = None

        if isinstance(self._C, str):
            if self._C == NULL_SYMBOL:
                c_index = None
            elif self._C == EDGE_SYMBOL:
                c_index = 0
            else:
                raise AttributeError("unknown string for C: %s" % self._C)

            c_fixed = True
        else:
            c_matcher = Template(self._C).generate_word_list(feature_to_sounds)

        d_index = None
        d_fixed = False
        d_matcher = None

        if isinstance(self._D, str):
            if self._D == NULL_SYMBOL:
                d_index = None
            elif self._D == EDGE_SYMBOL:
                d_index = len(word)
            else:
                raise AttributeError("unknown string for D: %s" % self._D)

            d_fixed = True
        else:
            d_matcher = Template(self._D).generate_word_list(feature_to_sounds)

        if c_fixed and d_fixed:
            return self._perform_transformation(word, c_index, d_index, feature_to_type, feature_to_sounds)
        elif not c_fixed and d_fixed:
            c_size = len(c_matcher[0])
            for pattern in c_matcher:
                try:
                    c_loc = word.index(pattern) + c_size
                except ValueError:
                    continue

                return self._perform_transformation(word, c_loc, d_index, feature_to_type, feature_to_sounds)

        elif c_fixed and not d_fixed:
            for pattern in d_matcher:
                try:
                    d_loc = word.index(pattern)
                except ValueError:
                    continue

                return self._perform_transformation(word, c_index, d_loc, feature_to_type, feature_to_sounds)
        else:
            c_size = len(c_matcher[0])
            for c_pattern in c_matcher:
                try:
                    c_loc = word.index(c_pattern) + c_size
                except ValueError:
                    continue

                for d_pattern in d_matcher:
                    try:
                        d_loc = word.index(d_pattern, c_loc + 1)
                    except ValueError:
                        continue

                    if d_loc > c_loc:
                        return self._perform_transformation(word, c_loc, d_loc, feature_to_type, feature_to_sounds)

        return word

    def _perform_transformation(self, word: str, begin_index: Optional[int, None], end_index: Optional[int, None],
                                feature_to_type: Dict[str, str], feature_to_sounds: Dict[str, List[Sound]]) -> str:
        targets_a = Template(self._A).generate_word_list(feature_to_sounds)
        target_size = len(targets_a[0])

        if begin_index is not None and end_index is None:
            end_index = begin_index + target_size
        elif begin_index is None and end_index is not None:
            begin_index = end_index - target_size

        for target in targets_a:

            if begin_index is None and end_index is None:
                try:
                    begin_index = word.index(target)
                    end_index = begin_index - target_size
                except ValueError:
                    continue

            return self._do_replace(word, target, begin_index, end_index, feature_to_type, feature_to_sounds)

    def _do_replace(self, word: str, target: str, begin_index: int, end_index: int, feature_to_type: Dict[str, str],
                    feature_to_sounds: Dict[str, List[Sound]]) -> str:

        if isinstance(self._B, str):
            print("not implemented yet")
        else:
            dest_sound = Sound('', [])[target].get_transformed_sound(self._B, feature_to_type, feature_to_sounds)
            return word[:begin_index] + str(dest_sound) + word[end_index:]

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
                bsec = Particle([bsec.lstrip("[").rstrip("]")])

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
