from __future__ import annotations
from typing import Dict
from features import *
import csv


class Sound:
    _features: Dict[FeatureTypes, Features]
    _symbol: str

    def __init__(self, symbol: str, features: List[Features], feature_types: List[FeatureTypes]) -> None:
        self._features = {}
        self._symbol = symbol

        for i in range(0, len(features)):
            self._features[feature_types[i]] = features[i]

    def get_feature(self, type_: FeatureTypes) -> Features:
        return self._features[type_]

    def get_symbol(self) -> str:
        return self._symbol

    def __str__(self) -> str:
        return self._symbol


def import_sounds(filename: str) -> List[Sound]:
    sounds = []
    ext_types = None

    with open(filename, encoding='utf-8') as data_file:
        lines = csv.reader(data_file)

        for line in lines:
            if len(line) == 0 or len(line[0]) == 0 or line[0] == '':
                continue

            if line[0] == "[TL]":
                ext_types = _feature_types_check(line)
                continue

            if ext_types is not None:
                sounds.append(Sound(line[0], line[1:line.index('')], ext_types))

    return sounds


def _feature_types_check(org_types: List[str]) -> List[FeatureTypes]:
    ext_types = [FeatureTypes[item.replace(' ', '_')] for item in org_types[1:org_types.index('', 1)]]
    defined_types = [item for item in FeatureTypes]
    defined_types.remove(FeatureTypes.NA)

    for t in defined_types:
        if t not in ext_types:
            raise ModuleNotFoundError("%s is a necessary feature but not included in the data" % str(t))

    for t in ext_types:
        if t not in defined_types:
            raise ModuleNotFoundError("Feature %s is undefined" % str(t))

    return ext_types


if __name__ == "__main__":
    for sound in import_sounds("ipafeatures.csv"):
        print(sound)
