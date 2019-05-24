from __future__ import annotations
from typing import List, Dict, Any


class Sound:
    _features: List[str]
    _symbol: str

    def __init__(self, symbol: str, features: List[str]) -> None:
        self._features = features
        self._symbol = symbol

    def get_features(self) -> List[str]:
        return [f for f in self._features]

    def get_symbol(self) -> str:
        return self._symbol

    def get_transformed_sound(self, target_feature: str, type_to_features: Dict[str, List[str]],
                              features_to_sound: Dict[Any, Sound]) -> Sound:
        from feature_lib import Particle

        for type_, features in type_to_features.items():
            if target_feature in features:
                for i in range(0, len(self._features)):
                    if self._features[i] in type_to_features[type_]:
                        target_feature_arr = [s for s in self._features]
                        target_feature_arr[i] = target_feature

                        if Particle(target_feature_arr) not in features_to_sound.keys():
                            raise RuntimeError(
                                "Post transformation features \'%s\'does not represent an existing sound" % str(
                                    target_feature_arr))

                        return features_to_sound[Particle(target_feature_arr)]

        raise AttributeError("Transformation failed. Target feature invalid.")

    def __str__(self) -> str:
        return self._symbol
