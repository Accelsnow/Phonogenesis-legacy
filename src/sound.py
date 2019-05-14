from __future__ import annotations
from typing import List, Dict
from features import *


class Sound:
    _features: Dict[FeatureTypes, Features]
    _symbol: str

    def __init__(self, symbol: str, features: List[Features]) -> None:
        self._features = {}
        self._symbol = symbol

        for feature in features:
            feature_type = get_type_from_feature(feature)

            if feature_type in self._features.keys():
                raise AttributeError

            self._features[feature_type] = feature

    def get_feature(self, type_: FeatureTypes) -> Features:
        return self._features[type_]

    def get_symbol(self) -> str:
        return self._symbol
