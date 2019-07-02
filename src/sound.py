from __future__ import annotations

from typing import List, Dict, Any, Optional

_SYMBOL = {}  # type: Dict[str, Sound]


class Sound:
    _num: int
    _features: List[str]
    _symbol: str

    def __init__(self, num: int, symbol: str, features: List[str]) -> None:
        self._num = num
        self._features = features
        self._symbol = symbol

        if symbol in _SYMBOL.keys():
            raise ValueError("Duplicated symbol not allowed!")

        if num >= 1 and symbol != '':
            _SYMBOL[symbol] = self

    def get_features(self) -> List[str]:
        return [f for f in self._features]

    def get_symbol(self) -> str:
        return self._symbol

    def get_transformed_sound(self, target_particle: Any, feature_to_type: Dict[str, str],
                              feature_to_sounds: Dict[str, List[Sound]]) -> Optional[Sound, None]:
        from feature_lib import Particle

        if not isinstance(target_particle, Particle):
            raise AttributeError("target particle must be a Particle")

        types = [feature_to_type[f] for f in target_particle.get_features()]

        for sound in target_particle.get_matching_sounds(None, feature_to_sounds):
            target_features = sound.get_features()
            passed = True

            for i in range(0, len(self._features)):
                target_feature = target_features[i]
                this_feature = self._features[i]

                if feature_to_type[target_feature] not in types and target_feature != this_feature:
                    passed = False
                    break

            if passed:
                return sound

        return None

    def get_num(self) -> int:
        return self._num

    def __hash__(self) -> int:
        return self._num

    def __getitem__(self, item: str) -> Sound:
        return _SYMBOL[item]

    def __str__(self) -> str:
        return self._symbol

    def __eq__(self, other: Sound) -> bool:
        return self._num == other.get_num()

    def __ne__(self, other: Sound) -> bool:
        return self._num != other.get_num()

    def __lt__(self, other: Sound) -> bool:
        return self._num < other.get_num()

    def __le__(self, other: Sound) -> bool:
        return self._num <= other.get_num()

    def __gt__(self, other: Sound) -> bool:
        return self._num > other.get_num()

    def __ge__(self, other: Sound) -> bool:
        return self._num >= other.get_num()
