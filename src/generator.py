from __future__ import annotations
from typing import List, Tuple, Dict, Any

from feature_lib import Particle
from sound import Sound
from templates import Template
from rules import Rule


class Generator:
    _difficulty: int  # 0- 10
    _difficulty_to_num: Dict[int, Tuple[int, int, int]]
    _templates: List[Template]
    _rule: Rule
    _matching: List[Template]
    _confusing: List[Template]
    _unrelated: List[Template]

    def __init__(self, templates: List[Template], rule: Rule, difficulty: int) -> None:
        self._templates = templates
        self._rule = rule

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
        self._initialize_templates()

    def _initialize_templates(self) -> None:
        info = self._rule.get_info()
        a = info[0]
        b = info[1]
        c = info[2]
        d = info[3]

    def get_difficulty(self) -> int:
        return self._difficulty

    def get_templates(self) -> List[Template]:
        return [t for t in self._templates]

    def get_rule(self) -> Rule:
        return self._rule

    def change_difficulty(self, target_difficulty: int) -> None:
        self._difficulty = target_difficulty

    def generate(self) -> Tuple[List[str], List[str], Rule, List[Template]]:
        difficulty_data = self._difficulty_to_num[self._difficulty]
        num_matching = difficulty_data[0]  # type: int
        num_confusing = difficulty_data[1]  # type: int
        num_unrelated = difficulty_data[2]  # type: int
