from __future__ import annotations

from enum import Enum
from typing import List, Optional, Dict, Tuple

from feature_lib import Particle
from sound import Sound
from templates import Template

import csv

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
    _A_matchers: Dict[int, List[str]]
    _B: Optional[Particle, str, None]
    _Cs: List[Optional[List[Particle], None]]
    _C_matchers: Dict[int, List[str]]
    _Ds: List[Optional[List[Particle], None]]
    _D_matchers: Dict[int, List[str]]

    _CADT_lib: Dict[str, List[Tuple[int, int]]]
    _Cs_edge: List[bool]
    _Ds_edge: List[bool]
    _name: str
    _family: RuleFamily
    _environments: List[
        Tuple[Optional[List[Particle], None], Optional[List[Sound], None], Optional[int, None], Dict[str, List[Sound]]]]

    def __init__(self, name: str, family: RuleFamily, a: Optional[List[Particle], None],
                 b: Optional[Particle, str, None], c: List[Optional[List[Particle], None]], c_edge: List[bool],
                 d: List[Optional[List[Particle], None]], d_edge: List[bool]) -> None:
        self._name = name
        self._family = family
        self._A = a
        self._A_matchers = {}
        self._B = b

        if len(c) != len(d):
            raise AttributeError("C and D list can not have different length %s _ %s" % (c, d))

        self._Cs = c
        self._C_matchers = {}
        self._Ds = d
        self._D_matchers = {}
        self._Cs_edge = c_edge
        self._Ds_edge = d_edge

        self._environments = []

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
                        c_matcher = self._get_c_matcher(c_instance, phonemes, None, feature_to_sounds)
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
                        d_matcher = self._get_d_matcher(d_instance, phonemes, None, feature_to_sounds)
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

    def _get_c_matcher(self, c_instance: Optional[List[Particle], None], phonemes: Optional[List[Sound], None],
                       size_limit: Optional[int, None], feature_to_sounds: Dict[str, List[Sound]]) -> List[str]:
        dest_env = (c_instance, phonemes, size_limit, feature_to_sounds)
        match_loc = self._locate_in_env(dest_env, self._C_matchers)

        if match_loc == -1:
            self._environments.append(dest_env)
            match_loc = len(self._environments) - 1
            self._C_matchers[match_loc] = Template(c_instance).generate_word_list(phonemes,
                                                                                  size_limit,
                                                                                  feature_to_sounds)

        return self._C_matchers[match_loc]

    def _get_d_matcher(self, d_instance: Optional[List[Particle], None], phonemes: Optional[List[Sound], None],
                       size_limit: Optional[int, None], feature_to_sounds: Dict[str, List[Sound]]) -> List[str]:
        dest_env = (d_instance, phonemes, size_limit, feature_to_sounds)
        match_loc = self._locate_in_env(dest_env, self._D_matchers)

        if match_loc == -1:
            self._environments.append(dest_env)
            match_loc = len(self._environments) - 1
            self._D_matchers[match_loc] = Template(d_instance).generate_word_list(phonemes,
                                                                                  size_limit,
                                                                                  feature_to_sounds)

        return self._D_matchers[match_loc]

    def _locate_in_env(self, dest_env: Tuple[
        Optional[List[Particle], None], Optional[List[Sound], None], Optional[int, None], Dict[str, List[Sound]]],
                       target_matchers: Dict[int, List[str]]):
        match_loc = -1

        for key in target_matchers.keys():
            env = self._environments[key]

            if len(env) != len(dest_env):
                raise ValueError(
                    "environment tuples should have the same size. ENV %s --- DEST_ENV %s" % (env, dest_env))

            is_match = True
            for i in range(0, len(env)):
                if env[i] != dest_env[i]:
                    is_match = False
                    break

            if is_match:
                match_loc = key
                break

        return match_loc

    def get_interest_phones(self, phonemes: List[Sound], feature_to_type: Dict[str, str],
                            feature_to_sounds: Dict[str, List[Sound]]) -> Tuple[Dict[str, str], List[str]]:
        a_matcher = self._get_a_matcher(phonemes, None, feature_to_sounds)
        result = {}
        all_phones = set([])

        if len(a_matcher) == 0:
            raise ValueError("No matching A found in the phonemes!")

        for a_str in a_matcher:
            if len(a_str) != 1:
                raise NotImplementedError("Currently only support A of size 1")

            b_str = self._do_replace(a_str, 0, 1, feature_to_type, feature_to_sounds)
            all_phones.add(a_str)
            all_phones.add(b_str)
            result[a_str] = b_str

        all_phones = list(all_phones)
        all_phones.sort(key=lambda x: Sound(-1, '', [])[x].get_num())
        return result, all_phones

    def locations_a(self, word: str, phonemes: List[Sound], feature_to_sounds: Dict[str, List[Sound]]) -> Dict[
        int, str]:
        if self._A is None:
            dict_ = {}

            for i in range(0, len(word)):
                dict_[i] = word[i]
            return dict_

        a_matcher = self._get_a_matcher(phonemes, None, feature_to_sounds)  # type:List[str]
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

    def _get_a_matcher(self, phonemes: List[Sound], size_limit: Optional[int, None],
                       feature_to_sounds: Dict[str, List[Sound]]) -> List[str]:
        dest_env = (self._A, phonemes, size_limit, feature_to_sounds)
        match_loc = self._locate_in_env(dest_env, self._D_matchers)

        if match_loc == -1:
            self._environments.append(dest_env)
            match_loc = len(self._environments) - 1
            matcher = Template(self._A).generate_word_list(phonemes, size_limit, feature_to_sounds)

            self._A_matchers[match_loc] = matcher

        return self._A_matchers[match_loc]

    def _do_replace(self, word: str, begin_index: int, end_index: int, feature_to_type: Dict[str, str],
                    feature_to_sounds: Dict[str, List[Sound]]) -> str:
        target = word[begin_index:end_index]

        if isinstance(self._B, str):
            raise NotImplementedError
        else:
            if self._B is None:
                dest_sound = ''
            else:
                dest_sound = Sound(-1, '', [])[target].get_transformed_sound(self._B, feature_to_type,
                                                                             feature_to_sounds)

            if dest_sound is not None:
                return word[:begin_index] + str(dest_sound) + word[end_index:]
            else:
                return word

    def get_name(self) -> str:
        return self._name

    def get_family(self) -> RuleFamily:
        return self._family

    def get_content_str(self) -> str:
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

    def __str__(self) -> str:
        return "%s ===== %s" % (self._name, self.get_content_str())


class PredefinedRule(Rule):
    def __init__(self, name: str, family: RuleFamily, a_to_b: Dict[str, str],
                 c: List[Optional[List[Particle], None]], c_edge: List[bool], d: List[Optional[List[Particle], None]],
                 d_edge: List[bool]) -> None:
        Rule.__init__(self, name, family, [], '', c, c_edge, d, d_edge)

        self._AtoB = a_to_b

    def _do_replace(self, word: str, begin_index: int, end_index: int, feature_to_type: Dict[str, str],
                    feature_to_sounds: Dict[str, List[Sound]]) -> str:
        return word[:begin_index] + self._AtoB[word[begin_index:end_index]] + word[end_index:]

    def _get_a_matcher(self, phonemes: List[Sound], size_limit: Optional[int, None],
                       feature_to_sounds: Dict[str, List[Sound]]) -> List[str]:
        return list(self._AtoB.keys())

    def get_content_str(self) -> str:
        ab_str = ''

        for key in self._AtoB.keys():
            ab_str += "%s > %s, " % (key, self._AtoB[key])

        ab_str = ab_str.rstrip(', ')
        parent_str = Rule.get_content_str(self)

        return "<Predefined> {%s} %s" % (ab_str, parent_str[parent_str.index('/'):])


class RuleFamily:
    _rules: List[Rule]
    _name: str

    def __init__(self, name: str, default: List[Rule]) -> None:
        self._rules = default
        self._name = name

    def add_rule(self, rule: Rule) -> bool:
        if rule not in self._rules:
            self._rules.append(rule)
            return True
        else:
            return False

    def get_rules(self) -> List[Rule]:
        return [r for r in self._rules]

    def get_name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return "%s : %s" % (self._name, str([r.get_name() for r in self._rules]))


def import_default_rules(feature_pool: List[str]) -> Tuple[List[RuleFamily], List[Rule]]:
    return _fetch_rule_and_family_csv(feature_pool, "defaultrules.csv")


def _fetch_rule_and_family_csv(feature_pool: List[str], filename: str) -> Tuple[List[RuleFamily], List[Rule]]:
    import ast
    rules = []  # type: List[Rule]
    families = {}  # type: Dict[str, RuleFamily]

    with open(filename, encoding='utf-8', newline='') as data_file:
        lines = csv.reader(data_file)

        for line in lines:
            if len(line) == 0 or len(line[0]) == 0 or line[0] == '' or line[0] == '\ufeff':
                continue

            family_name = line[2]

            if family_name not in families.keys():
                families[family_name] = RuleFamily(family_name, [])

            rule_family = families[family_name]
            rule_name = line[1]
            rule_content = str(line[0]).strip().strip('\n').strip('\ufeff').replace('g', 'ɡ')

            if rule_content.startswith('<<PREDEFINED>>'):
                predifined = True
            else:
                predifined = False

            rule_content = rule_content.lstrip('<<PREDEFINED>>')

            mid_break = rule_content.split("/")

            cd_info = _interpret_cd(mid_break[1], feature_pool)

            if predifined:
                rule = PredefinedRule(rule_name, rule_family, ast.literal_eval(mid_break[0]), cd_info[0], cd_info[1],
                                      cd_info[2], cd_info[3])
            else:
                action_break = mid_break[0].split(">")

                if len(action_break) != 2:
                    raise ImportError("Invalid rule format: %s" % rule_content)

                asec = action_break[0]
                bsec = action_break[1]

                if len(bsec) == 0:
                    bsec = None
                elif bsec[0] == '[' and bsec[-1] == ']':
                    bsec = Particle(bsec.lstrip("[").rstrip("]").split(","))

                if len(mid_break) != 2:
                    raise ImportError("Invalid rule format: %s" % rule_content)

                rule = Rule(rule_name, rule_family, _sec_to_particles(feature_pool, asec), bsec, cd_info[0], cd_info[1],
                            cd_info[2], cd_info[3])

            rule_family.add_rule(rule)
            rules.append(rule)

    return list(families.values()), rules


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
