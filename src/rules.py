from __future__ import annotations

from enum import Enum
from typing import List, Optional, Dict, Tuple

from feature_lib import Particle
from sound import Sound
from templates import Template

EDGE_SYMBOL = '#'


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
    _A: Optional[List[Particle], None]
    _B: Optional[Particle, str, None]
    _Cs: List[Optional[List[Particle], None]]
    _Ds: List[Optional[List[Particle], None]]
    _CADT_lib: Dict[str, List[Tuple[int, int]]]
    _Cs_edge: List[bool]
    _Ds_edge: List[bool]

    def __init__(self, a: Optional[List[Particle], None], b: Optional[Particle, str, None],
                 c: List[Optional[List[Particle], None]], c_edge: List[bool], d: List[Optional[List[Particle], None]],
                 d_edge: List[bool]) -> None:
        self._A = a
        self._B = b

        if len(c) != len(d):
            raise AttributeError("C and D list can not have different length %s _ %s" % (c, d))

        self._Cs = c
        self._Ds = d
        self._Cs_edge = c_edge
        self._Ds_edge = d_edge

        self._CADT_lib = {}

    def apply(self, word: str, phonemes: List[Sound], feature_to_type: Dict[str, str],
              feature_to_sounds: Dict[str, List[Sound]]) -> str:
        if word not in self._CADT_lib.keys():
            if ExampleType.CADT not in self.classify(word, phonemes, feature_to_type, feature_to_sounds, ):
                return word

        indexes = list(set(self._CADT_lib[word]))
        new_word = word
        prev_len = len(new_word)
        len_diff = 0

        for index in indexes:
            new_word = self._do_replace(new_word, index[0] + len_diff, index[1] + len_diff, feature_to_type,
                                        feature_to_sounds)
            new_len = len(new_word)
            len_diff = new_len - prev_len
            prev_len = new_len

        return new_word

    def classify(self, word: str, phonemes: List[Sound], feature_to_type: Dict[str, str],
                 feature_to_sounds: Dict[str, List[Sound]]) -> List[Dict[ExampleType, str]]:
        a_data = self.locations_a(word, phonemes, feature_to_sounds)
        a_locations = list(a_data.keys())  # type: List[int]

        if len(a_locations) == 0 or a_locations == []:
            return [{ExampleType.IRR: ''} for _ in range(0, len(self._Cs))]
        else:
            types_to_sounds = [{} for _ in range(0, len(self._Cs))]  # type: List[Dict[ExampleType, str]]

            for a_loc in a_locations:
                a_size = len(a_data[a_loc])

                for i in range(0, len(self._Cs)):
                    c_instance = self._Cs[i]
                    d_instance = self._Ds[i]
                    c_edge = self._Cs_edge[i]
                    d_edge = self._Ds_edge[i]

                    is_c = False

                    if c_edge and c_instance is None:
                        is_c = a_loc == 0
                    elif not c_edge and c_instance is None:
                        is_c = True
                    else:
                        c_matcher = Template(c_instance).generate_word_list(phonemes, None, feature_to_sounds)
                        c_size = len(c_matcher[0])

                        if not c_edge or a_loc - c_size == 0:

                            for c_pattern in c_matcher:
                                if a_loc - c_size >= 0 and word[a_loc - c_size:a_loc] == c_pattern:
                                    is_c = True
                                    break

                    is_d = False

                    if d_edge and d_instance is None:
                        is_d = a_loc + a_size == len(word)
                    elif not d_edge and d_instance is None:
                        is_d = True
                    else:
                        d_matcher = Template(d_instance).generate_word_list(phonemes, None, feature_to_sounds)
                        d_size = len(d_matcher[0])

                        if not d_edge or a_loc + a_size + d_size == len(word):

                            for d_pattern in d_matcher:
                                if a_loc + a_size < len(word) and word[
                                                                  a_loc + a_size:a_loc + a_size + d_size] == d_pattern:
                                    is_d = True
                                    break

                    a_str = word[a_loc]
                    if is_c and is_d:
                        if word != self._do_replace(word, a_loc, a_loc + a_size, feature_to_type, feature_to_sounds):
                            types_to_sounds[i] = {ExampleType.CADT: a_str}
                            location = (a_loc, a_loc + a_size)

                            # if True not in [location in val for val in self._CADT_lib.values()]:
                            if word in self._CADT_lib:
                                self._CADT_lib[word].append(location)
                            else:
                                self._CADT_lib[word] = [location]
                        elif ExampleType.CADT not in types_to_sounds[i]:
                            types_to_sounds[i] = {ExampleType.CADNT: a_str}

                    elif ExampleType.CADT not in types_to_sounds[i] and ExampleType.CADNT not in types_to_sounds[i]:
                        if is_c and not is_d:
                            types_to_sounds[i][ExampleType.CAND] = a_str
                        elif not is_c and is_d:
                            types_to_sounds[i][ExampleType.NCAD] = a_str
                        elif not is_c and not is_d:
                            types_to_sounds[i][ExampleType.NCAND] = a_str

            return types_to_sounds

    def locations_a(self, word: str, phonemes: List[Sound], feature_to_sounds: Dict[str, List[Sound]]) -> Dict[
        int, str]:
        if self._A is None:
            dict_ = {}

            for i in range(0, len(word)):
                dict_[i] = word[i]
            return dict_

        a_matcher = self._get_a_matcher(phonemes, feature_to_sounds)  # type:List[str]
        prev_index = 0  # type: int
        result = {}  # type: Dict[int, str]
        i = 0

        while i < len(a_matcher):
            a_pattern = a_matcher[i]

            try:
                a_index = word.index(a_pattern, prev_index)

                prev_index = a_index + 1
                result[a_index] = a_pattern
                i -= 1
            except ValueError:
                i += 1
                prev_index = 0
                continue

            i += 1

        return result

    def _get_a_matcher(self, phonemes: List[Sound], feature_to_sounds: Dict[str, List[Sound]]) -> List[str]:
        return Template(self._A).generate_word_list(phonemes, None, feature_to_sounds)

    def _do_replace(self, word: str, begin_index: int, end_index: int, feature_to_type: Dict[str, str],
                    feature_to_sounds: Dict[str, List[Sound]]) -> str:
        target = word[begin_index:end_index]

        if isinstance(self._B, str):
            raise NotImplementedError
        else:
            if self._B is None:
                dest_sound = ''
            else:
                dest_sound = Sound('', [])[target].get_transformed_sound(self._B, feature_to_type, feature_to_sounds)

            if dest_sound is not None:
                return word[:begin_index] + str(dest_sound) + word[end_index:]
            else:
                return word

    def __str__(self) -> str:
        cd_str = ''

        for i in range(0, len(self._Cs)):
            if len(cd_str) > 0:
                cd_str += ' or '

            c_block = self._Cs[i]
            d_block = self._Ds[i]
            c_edge = self._Cs_edge[i]
            d_edge = self._Ds_edge[i]

            c_part = ''
            if c_edge:
                c_part += '#'
            if c_block is not None:
                c_part += "".join([str(s) for s in c_block])

            d_part = ''
            if d_block is not None:
                d_part += "".join([str(s) for s in d_block])
            if d_edge:
                d_part += '#'

            part = "%s _ %s" % (c_part, d_part)

            cd_str += part

        return "%s -> %s / %s" % (
            "".join([str(s) for s in self._A]), str(self._B), cd_str)


class PredefinedRule(Rule):
    def __init__(self, a_to_b: Dict[str, str],
                 c: List[Optional[List[Particle], None]], c_edge: List[bool], d: List[Optional[List[Particle], None]],
                 d_edge: List[bool]) -> None:
        Rule.__init__(self, [], '', c, c_edge, d, d_edge)

        self._AtoB = a_to_b

    def _do_replace(self, word: str, begin_index: int, end_index: int, feature_to_type: Dict[str, str],
                    feature_to_sounds: Dict[str, List[Sound]]) -> str:
        return word[:begin_index] + self._AtoB[word[begin_index:end_index]] + word[end_index:]

    def _get_a_matcher(self, phonemes: List[Sound], feature_to_sounds: Dict[str, List[Sound]]) -> List[str]:
        return list(self._AtoB.keys())

    def __str__(self) -> str:
        ab_str = ''

        for key in self._AtoB.keys():
            ab_str += "%s > %s, " % (key, self._AtoB[key])

        ab_str = ab_str.rstrip(', ')
        parent_str = Rule.__str__(self)

        return "<Predefined> {%s} %s" % (ab_str, parent_str[parent_str.index('/'):])


def import_default_rules(feature_pool: List[str]) -> List[Rule]:
    return _fetch_rule_csv(feature_pool, "defaultrule.txt")


def _fetch_rule_csv(feature_pool: List[str], filename: str) -> List[Rule]:
    import ast
    rules = []  # type: List[Rule]

    with open(filename, encoding='utf-8') as data_file:
        lines = [l.rstrip('\n') for l in data_file.readlines()]

        for line in lines:
            if line.startswith('<<PREDEFINED>>'):
                predifined = True
            else:
                predifined = False

            line = line.lstrip('<<PREDEFINED>>')

            mid_break = line.split("/")

            cd_info = _interpret_cd(mid_break[1], feature_pool)

            if predifined:
                rules.append(
                    PredefinedRule(ast.literal_eval(mid_break[0]), cd_info[0], cd_info[1], cd_info[2], cd_info[3]))

            else:
                action_break = mid_break[0].split(">")

                if len(action_break) != 2:
                    raise ImportError("Invalid rule format: %s" % line)

                asec = action_break[0]
                bsec = action_break[1]

                if len(bsec) == 0:
                    bsec = None
                elif bsec[0] == '[' and bsec[-1] == ']':
                    bsec = Particle(bsec.lstrip("[").rstrip("]").split(","))

                if len(mid_break) != 2:
                    raise ImportError("Invalid rule format: %s" % line)

                rules.append(
                    Rule(_sec_to_particles(feature_pool, asec), bsec, cd_info[0], cd_info[1], cd_info[2], cd_info[3]))

    return rules


def _interpret_cd(cd_str: str, feature_pool: List[str]) -> Tuple[
    List[Optional[List[Particle], None]], List[bool], List[Optional[List[Particle], None]], List[bool]]:
    conditions = cd_str.split("&")
    c_list = []  # type: List[Optional[List[Particle], None]]
    d_list = []  # type: List[Optional[List[Particle], None]]
    c_edge = []  # type: List[bool]
    d_edge = []  # type: List[bool]

    for cond_sec in conditions:
        condition_break = cond_sec.split("_")

        if len(condition_break) != 2:
            raise ImportError("Invalid rule format: %s" % cond_sec)

        c_part = condition_break[0]
        d_part = condition_break[1]

        if len(c_part) > 0 and c_part[0] == EDGE_SYMBOL:
            c_part = c_part[1:]
            c_edge.append(True)
        else:
            c_edge.append(False)

        if len(d_part) > 0 and d_part[-1] == EDGE_SYMBOL:
            d_part = d_part[:len(d_part) - 1]
            d_edge.append(True)
        else:
            d_edge.append(False)

        c_list.append(_sec_to_particles(feature_pool, c_part))
        d_list.append(_sec_to_particles(feature_pool, d_part))

    return c_list, c_edge, d_list, d_edge


def _sec_to_particles(feature_pool: List[str], sec: str) -> Optional[List[Particle], None]:
    particles = []  # type: List[Particle]

    parts = sec.lstrip('[').rstrip(']').split("][")

    if len(parts) == 1 and len(parts[0]) == 0:
        return None

    for part in parts:
        features = part.split(",")

        for feature in features:
            if feature not in feature_pool:
                raise ImportError("Rule sector %s does not conform to the given features." % sec)

        particles.append(Particle(features))

    return particles
