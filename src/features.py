from __future__ import annotations
import csv
from sound import *

from typing import List, Tuple, Dict


def import_default() -> Tuple[Dict[str, str], List[Sound], Dict]:
    return _fetch_from_csv("defaultipa.csv")


def _fetch_from_csv(filename: str) -> Tuple[Dict, List[Sound], Dict]:
    feature_types = []
    sounds = []
    type_to_features = {}
    feature_to_sounds = {}

    with open(filename, encoding='utf-8') as data_file:
        lines = csv.reader(data_file)
        header_solved = False

        for line in lines:
            if len(line) == 0 or len(line[0]) == 0 or line[0] == '' or line[0] == '\ufeff':
                continue

            if line[0] == "[TL]":
                if header_solved:
                    raise ImportError("Duplicate [TL] header found")

                feature_types = line[1:line.index('', 1)]

                for _type in feature_types:
                    type_to_features[_type] = []

                header_solved = True
                continue

            if not header_solved:
                raise ImportError("File does not start with header line begins with [TL]")

            features = line[1:line.index('', 1)]

            if len(features) != len(feature_types):
                raise ImportError("Feature line \'%s\' does not align with types" % str(features))

            _sound = Sound(line[0], features, feature_types)
            sounds.append(_sound)

            for i in range(0, len(features)):
                _feature = features[i]
                _type = feature_types[i]

                if _feature not in type_to_features[_type]:
                    type_to_features[_type].append(_feature)

                if _feature not in feature_to_sounds.keys():
                    feature_to_sounds[_feature] = []

                feature_to_sounds[_feature].append(_sound)

    return type_to_features, sounds, feature_to_sounds


if __name__ == '__main__':
    d = import_default()[2]
    for f in d:
        print("%s - %s" % (f, [str(item) for item in d[f]]))
