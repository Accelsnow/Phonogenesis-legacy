from __future__ import annotations
from typing import List, Tuple, Dict

from sound import Sound
from templates import Template
from rules import Rule
import random
import warnings


class Generator:
    _difficulty: int  # 0- 10
    _difficulty_to_num: Dict[int, Tuple[int, int, int]]
    _templates: List[Template]
    _rule: Rule
    _matching: List[str]
    _confusing: List[str]
    _unrelated: List[str]
    _phonemes: List[Sound]

    def __init__(self, phonemes: List[Sound], templates: List[Template], rule: Rule, difficulty: int,
                 feature_to_type: Dict[str, str], feature_to_sounds: Dict[str, List[Sound]]) -> None:
        self._templates = templates
        self._rule = rule
        self._matching = []
        self._confusing = []
        self._unrelated = []
        self._phonemes = phonemes

        self._difficulty_to_num = {
            0: (4, 0, 0),
            1: (4, 1, 0),
            2: (4, 2, 0),
            3: (4, 3, 0),
            4: (4, 4, 0),
            5: (4, 4, 1),
            6: (4, 4, 2),
            7: (4, 4, 3),
            8: (4, 4, 4),
            9: (4, 4, 5),
            10: (4, 4, 6)
        }

        self._difficulty = difficulty
        self._initialize_templates(feature_to_type, feature_to_sounds)

    def _initialize_templates(self, feature_to_type: Dict[str, str],
                              feature_to_sounds: Dict[str, List[Sound]]) -> None:
        for template in self._templates:
            word_list = template.generate_word_list(self._phonemes, feature_to_sounds)

            for word in word_list:
                if self._rule.apply(word, self._phonemes, feature_to_type, feature_to_sounds) != word:
                    self._matching.append(word)
                    continue

                cd_loc = self._rule.locate_cd(word, self._phonemes, feature_to_sounds)

                if cd_loc is None:
                    if self._rule.confirm_position_validity(word, self._phonemes, None, None,
                                                            feature_to_sounds) is None:
                        self._unrelated.append(word)
                    # else:
                    #     self._confusing.append(word)
                else:
                    if self._rule.confirm_position_validity(word, self._phonemes, cd_loc[0], cd_loc[1],
                                                            feature_to_sounds) is None:
                        self._confusing.append(word)

    def get_difficulty(self) -> int:
        return self._difficulty

    def get_templates(self) -> List[Template]:
        return [t for t in self._templates]

    def get_rule(self) -> Rule:
        return self._rule

    def change_difficulty(self, target_difficulty: int) -> None:
        self._difficulty = target_difficulty

    def generate(self, feature_to_type: Dict[str, str], feature_to_sounds: Dict[str, List[Sound]]) -> Tuple[
        List[str], List[str], Rule, List[Template]]:
        underlying_rep = []  # type: List[str]
        surface_rep = []  # type: List[str]

        difficulty_data = self._difficulty_to_num[self._difficulty]
        num_matching = difficulty_data[0]  # type: int
        num_confusing = difficulty_data[1]  # type: int
        num_unrelated = difficulty_data[2]  # type: int

        if len(self._matching) >= num_matching:
            underlying_rep.extend(random.sample(self._matching, num_matching))
        else:
            warnings.warn(
                "Insufficient amount of matching cases.(%d required, %d found)" % (num_matching, len(self._matching)))
            underlying_rep.extend(self._matching)

        if len(self._confusing) >= num_confusing:
            underlying_rep.extend(random.sample(self._confusing, num_confusing))
        else:
            warnings.warn("Insufficient amount of confusing cases.(%d required, %d found)" % (
                num_confusing, len(self._confusing)))
            underlying_rep.extend(self._confusing)

        if len(self._unrelated) >= num_unrelated:
            underlying_rep.extend(random.sample(self._unrelated, num_unrelated))
        else:
            warnings.warn("Insufficient amount of unrelated cases.(%d required, %d found)" % (
                num_unrelated, len(self._unrelated)))
            underlying_rep.extend(self._unrelated)

        # random.shuffle(underlying_rep)

        for word in underlying_rep:
            surface_rep.append(self._rule.apply(word, self._phonemes, feature_to_type, feature_to_sounds))

        return surface_rep, underlying_rep, self._rule, self._templates
