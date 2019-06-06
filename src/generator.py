from __future__ import annotations

import random
import warnings
from typing import List, Tuple, Dict

from rules import Rule, ExampleType
from sound import Sound
from templates import Template

WORD_LIST_SIZE_LIMIT = 1000


class Generator:
    _difficulty: int  # 0- 10
    _difficulty_to_percent: Dict[int, Tuple[float, float, float, float, float, float]]
    _templates: List[Template]
    _rule: Rule
    _CADT: Dict[str, List[str]]
    _CADNT: Dict[str, List[str]]
    _CAND: Dict[str, List[str]]
    _NCAD: Dict[str, List[str]]
    _NCAND: Dict[str, List[str]]
    _IRR: Dict[str, List[str]]
    _phonemes: List[Sound]

    def __init__(self, phonemes: List[Sound], templates: List[Template], rule: Rule, difficulty: int,
                 feature_to_type: Dict[str, str], feature_to_sounds: Dict[str, List[Sound]]) -> None:
        self._templates = templates
        self._rule = rule
        self._CADT = {}
        self._CADNT = {}
        self._CAND = {}
        self._NCAD = {}
        self._NCAND = {}
        self._IRR = {}
        self._phonemes = phonemes

        self._difficulty_to_percent = {
            5: (0.32, 0.08, 0.175, 0.175, 0.05, 0.2)
        }

        self._difficulty = difficulty
        self._initialize_templates(feature_to_type, feature_to_sounds)

    def _initialize_templates(self, feature_to_type: Dict[str, str], feature_to_sounds: Dict[str, List[Sound]]) -> None:
        for template in self._templates:
            word_list = template.generate_word_list(self._phonemes, WORD_LIST_SIZE_LIMIT, feature_to_sounds)
            random.shuffle(word_list)

            for word in word_list:
                word_types = self._rule.classify(word, self._phonemes, feature_to_type, feature_to_sounds)
                has_exclusive_type = False

                if ExampleType.IRR in word_types:
                    self._dict_add(self._IRR, word_types[ExampleType.IRR], word)
                    has_exclusive_type = True
                else:
                    if ExampleType.CADT in word_types:
                        self._dict_add(self._CADT, word_types[ExampleType.CADT], word)
                        has_exclusive_type = True
                    if ExampleType.CADNT in word_types:
                        self._dict_add(self._CADNT, word_types[ExampleType.CADNT], word)
                        has_exclusive_type = True

                if not has_exclusive_type:
                    if ExampleType.CAND in word_types:
                        self._dict_add(self._CAND, word_types[ExampleType.CAND], word)
                    if ExampleType.NCAD in word_types:
                        self._dict_add(self._NCAD, word_types[ExampleType.NCAD], word)
                    if ExampleType.NCAND in word_types:
                        self._dict_add(self._NCAND, word_types[ExampleType.NCAND], word)

    @staticmethod
    def _dict_add(dic: Dict[str, List[str]], key: str, value: str) -> None:
        if key in dic:
            if value not in dic[key]:
                dic[key].append(value)
        else:
            dic[key] = [value]

    def get_difficulty(self) -> int:
        return self._difficulty

    def get_templates(self) -> List[Template]:
        return [t for t in self._templates]

    def get_rule(self) -> Rule:
        return self._rule

    def change_difficulty(self, target_difficulty: int) -> None:
        self._difficulty = target_difficulty

    def _get_num(self, amount: int) -> Tuple[int, int, int, int, int, int]:
        diff_data = self._difficulty_to_percent[self._difficulty]
        cadt = round(amount * diff_data[0])
        cadnt = round(amount * diff_data[1])
        cand = round(amount * diff_data[2])
        ncad = round(amount * diff_data[3])
        ncand = round(amount * diff_data[4])
        irr = round(amount * diff_data[5])

        if cadt + cadnt + cand + ncad + ncand + irr > amount:
            irr -= 1

        print("\nExpected Number:", "CADT", cadt, "CADNT", cadnt, "CAND", cand, "NCAD", ncad, "NCAND", ncand, "IRR",
              irr)
        return cadt, cadnt, cand, ncad, ncand, irr

    @staticmethod
    def _get_dist_values(dic: Dict[str, List[str]]) -> List[str]:
        existed = []

        for lst in dic.values():
            for item in lst:
                if item not in existed:
                    existed.append(item)

        return existed

    @staticmethod
    def _generate_words(amount: int, dic: Dict[str, List[str]]) -> List[str]:
        words = []
        rand_keys = list(dic)
        curr_index = 0
        continue_find = True

        for key in rand_keys:
            random.shuffle(dic[key])

        while continue_find:
            random.shuffle(rand_keys)

            for key in rand_keys:
                value_lst = dic[key]

                if curr_index < len(value_lst):
                    chosen = value_lst[curr_index]

                    if chosen not in words:
                        words.append(chosen)

                        if len(words) >= amount:
                            continue_find = False
                            break

            curr_index += 1

        return words

    def _generate_helper(self, dic: Dict[str, List[str]], amount: int, name: str) -> Tuple[List[str], List[str]]:
        vals = self._get_dist_values(dic)

        if len(vals) >= amount:
            words = self._generate_words(amount, dic)
            return words, [item for item in vals if item not in words]
        else:
            warnings.warn("Insufficient amount of %s type.(%d required, %d found)" % (name, amount, len(vals)))
            return vals, []

    def generate(self, amount: int, feature_to_type: Dict[str, str], feature_to_sounds: Dict[str, List[Sound]]) -> \
            Tuple[List[str], List[str], Rule, List[Template]]:
        underlying_rep = []  # type: List[str]
        surface_rep = []  # type: List[str]

        cadt_num, cadnt_num, cand_num, ncad_num, ncand_num, irr_num = self._get_num(amount)

        # START RANDOM PICK

        cadt_words, cadt_left = self._generate_helper(self._CADT, cadt_num, "CADT")
        cadnt_words, cadnt_left = self._generate_helper(self._CADNT, cadnt_num, "CADNT")
        cand_words, cand_left = self._generate_helper(self._CAND, cand_num, "CAND")
        ncad_words, ncad_left = self._generate_helper(self._NCAD, ncad_num, "NCAD")
        ncand_words, ncand_left = self._generate_helper(self._NCAND, ncand_num, "NCAND")
        irr_words, irr_left = self._generate_helper(self._IRR, irr_num, "IRR")

        # FINISH RANDOM PICK
        sum_num = len(cadt_words) + len(cadnt_words) + len(cand_words) + len(ncad_words) + len(ncand_words) + len(
            irr_words)

        if sum_num < amount:
            diff = amount - sum_num

            while len(cadt_left) > 0 and diff > 0:
                cadt_words.append(cadt_left.pop())
                diff -= 1

            while len(cadnt_left) > 0 and diff > 0:
                cadnt_words.append(cadnt_left.pop())
                diff -= 1

            while len(cand_left) > 0 and diff > 0:
                cand_words.append(cand_left.pop())
                diff -= 1

            while len(ncad_left) > 0 and diff > 0:
                ncad_words.append(ncad_left.pop())
                diff -= 1

            while len(ncand_left) > 0 and diff > 0:
                ncand_words.append(ncand_left.pop())
                diff -= 1

            while len(irr_left) > 0 and diff > 0:
                irr_words.append(irr_left.pop())
                diff -= 1

            if diff > 0:
                warnings.warn("CRITICAL WARNING: No available word left in any category. (%d missing)" % diff)

        print("\nActual Number:", "CADT", len(cadt_words), "CADNT", len(cadnt_words), "CAND", len(cand_words), "NCAD",
              len(ncad_words), "NCAND", len(ncand_words), "IRR", len(irr_words))
        # random.shuffle(underlying_rep)

        underlying_rep.extend(cadt_words)
        underlying_rep.extend(cadnt_words)
        underlying_rep.extend(cand_words)
        underlying_rep.extend(ncad_words)
        underlying_rep.extend(ncand_words)
        underlying_rep.extend(irr_words)

        for word in underlying_rep:
            surface_rep.append(self._rule.apply(word, self._phonemes, feature_to_type, feature_to_sounds))

        return underlying_rep, surface_rep, self._rule, self._templates
