from __future__ import annotations
import csv
from sound import *

from typing import List, Tuple, Dict


def import_default() -> Tuple[Dict[str, str], List[Sound]]:
    return _fetch_from_csv("defaultipa.csv")


def _fetch_from_csv(filename: str) -> Tuple[Dict, List[Sound]]:
    feature_types = []
    sounds = []
    feature_lib = {}

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
                    feature_lib[_type] = []

                header_solved = True
                continue

            if not header_solved:
                raise ImportError("File does not start with header line begins with [TL]")

            features = line[1:line.index('', 1)]

            if len(features) != len(feature_types):
                raise ImportError("Feature line \'%s\' does not align with types" % str(features))

            for i in range(0, len(features)):
                _feature = features[i]
                _type = feature_types[i]

                if _feature not in feature_lib[_type]:
                    feature_lib[_type].append(_feature)

            sounds.append(Sound(line[0], features, feature_types))

    return feature_lib, sounds


if __name__ == '__main__':
    for sound in import_default()[1]:
        print(str(sound))