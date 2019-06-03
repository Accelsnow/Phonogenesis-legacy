from __future__ import annotations
from typing import List, Tuple, Dict

from sound import Sound
from templates import Template
from rules import Rule, ExampleType
import random
import warnings


class Generator:
    _difficulty: int  # 0- 10
    _difficulty_to_percent: Dict[int, Tuple[float, float, float, float, float, float]]
    _templates: List[Template]
    _rule: Rule
    _CADT: List[str]
    _CADNT: List[str]
    _CAND: List[str]
    _NCAD: List[str]
    _NCAND: List[str]
    _IRR: List[str]
    _phonemes: List[Sound]

    def __init__(self, phonemes: List[Sound], templates: List[Template], rule: Rule, difficulty: int,
                 feature_to_type: Dict[str, str], feature_to_sounds: Dict[str, List[Sound]]) -> None:
        self._templates = templates
        self._rule = rule
        self._CADT = []
        self._CADNT = []
        self._CAND = []
        self._NCAD = []
        self._NCAND = []
        self._IRR = []
        self._phonemes = phonemes

        self._difficulty_to_percent = {
            5: (0.32, 0.08, 0.175, 0.175, 0.05, 0.2)
        }

        self._difficulty = difficulty
        self._initialize_templates(feature_to_type, feature_to_sounds)

    def _initialize_templates(self, feature_to_type: Dict[str, str], feature_to_sounds: Dict[str, List[Sound]]) -> None:
        for template in self._templates:
            word_list = template.generate_word_list(self._phonemes, feature_to_sounds)

            for word in word_list:
                example_type = self._rule.classify(word, self._phonemes, feature_to_type, feature_to_sounds)

                if ExampleType.CADT in example_type:
                    self._CADT.append(word)
                if ExampleType.CADNT in example_type:
                    self._CADNT.append(word)
                if ExampleType.CAND in example_type:
                    self._CAND.append(word)
                if ExampleType.NCAD in example_type:
                    self._NCAD.append(word)
                if ExampleType.NCAND in example_type:
                    self._NCAND.append(word)
                if ExampleType.IRR in example_type:
                    self._IRR.append(word)

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

        print(cadt, cadnt, cand, ncad, ncand, irr)
        return cadt, cadnt, cand, ncad, ncand, irr

    def generate(self, amount: int, feature_to_type: Dict[str, str], feature_to_sounds: Dict[str, List[Sound]]) -> \
            Tuple[List[str], List[str], Rule, List[Template]]:
        underlying_rep = []  # type: List[str]
        surface_rep = []  # type: List[str]

        num_cadt, num_cadnt, num_cand, num_ncad, num_ncand, num_irr = self._get_num(amount)

        if len(self._CADT) >= num_cadt:
            underlying_rep.extend(random.sample(self._CADT, num_cadt))
        else:
            warnings.warn("Insufficient amount of CADT type.(%d required, %d found)" % (num_cadt, len(self._CADT)))
            underlying_rep.extend(self._CADT)

        if len(self._CADNT) >= num_cadnt:
            underlying_rep.extend(random.sample(self._CADNT, num_cadnt))
        else:
            warnings.warn("Insufficient amount of CADNT type.(%d required, %d found)" % (num_cadnt, len(self._CADNT)))
            underlying_rep.extend(self._CADNT)

        if len(self._CAND) >= num_cand:
            underlying_rep.extend(random.sample(self._CAND, num_cand))
        else:
            warnings.warn("Insufficient amount of CAND cases.(%d required, %d found)" % (num_cand, len(self._CAND)))
            underlying_rep.extend(self._CAND)

        if len(self._NCAD) >= num_ncad:
            underlying_rep.extend(random.sample(self._NCAD, num_ncad))
        else:
            warnings.warn("Insufficient amount of NCAD cases.(%d required, %d found)" % (num_ncad, len(self._NCAD)))
            underlying_rep.extend(self._NCAD)

        if len(self._NCAND) >= num_ncand:
            underlying_rep.extend(random.sample(self._NCAND, num_ncand))
        else:
            warnings.warn("Insufficient amount of NCAND cases.(%d required, %d found)" % (num_ncand, len(self._NCAND)))
            underlying_rep.extend(self._NCAND)

        if len(self._IRR) >= num_irr:
            underlying_rep.extend(random.sample(self._IRR, num_irr))
        else:
            warnings.warn("Insufficient amount of IRR cases.(%d required, %d found)" % (num_irr, len(self._IRR)))
            underlying_rep.extend(self._IRR)

        # random.shuffle(underlying_rep)

        for word in underlying_rep:
            surface_rep.append(self._rule.apply(word, self._phonemes, feature_to_type, feature_to_sounds))

        return surface_rep, underlying_rep, self._rule, self._templates
