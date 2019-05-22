from __future__ import annotations
from typing import List, Dict


class Sound:
    _features: Dict[str, str]
    _symbol: str

    def __init__(self, symbol: str, features: List[str], feature_types: List[str]) -> None:
        self._features = {}
        self._symbol = symbol

        for i in range(0, len(features)):
            _type = feature_types[i]
            _feature = features[i]

            self._features[_type] = _feature

    def get_feature(self, type_: str) -> str:
        if type_ not in self._features.keys():
            raise AttributeError("type %s not found. Available types: %s" % (type_, self._features.keys()))
        return self._features[type_]

    def get_symbol(self) -> str:
        return self._symbol

    def __str__(self) -> str:
        return self._symbol

