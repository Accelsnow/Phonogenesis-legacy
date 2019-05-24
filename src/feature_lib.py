from __future__ import annotations
import csv
from sound import Sound

from typing import List, Tuple, Dict


class Particle:
    _features: List[str]

    def __init__(self, features_: List[str]) -> None:
        self._features = features_

    def __eq__(self, other: Particle) -> bool:
        for i in range(0, len(self._features)):
            if not self._features[i] == other._features[i]:
                return False

        return True

    def __hash__(self):
        return 0


def import_default_features() -> Tuple[
        List[str], List[Sound], Dict[str, List[str]], Dict[str, List[Sound]], Dict[Particle, Sound]]:
    return _fetch_feature_csv("defaultipa.csv")


def _fetch_feature_csv(filename: str) -> Tuple[
        List[str], List[Sound], Dict[str, List[str]], Dict[str, List[Sound]], Dict[Particle, Sound]]:
    features = []  # type: List[str]
    type_to_features = {}  # type: Dict[str, List[str]]
    feature_to_sounds = {}  # type: Dict[str, List[Sound]]
    features_to_sound = {}  # type: Dict[Particle, Sound]
    sounds = []  # type: List[Sound]

    feature_types = []

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

                for type_ in feature_types:
                    type_to_features[type_] = []

                header_solved = True
                continue

            if not header_solved:
                raise ImportError("File does not start with header line begins with [TL]")

            features_ = line[1:line.index('', 1)]

            if len(features_) != len(feature_types):
                raise ImportError("Feature line \'%s\' does not align with types" % str(features_))

            _sound = Sound(line[0], features_)

            if Particle(features_) in features_to_sound.keys():
                raise ImportError(
                    "Sound %s has the same property as sound %s" % (str(_sound), features_to_sound[features_]))

            features_to_sound[Particle(features_)] = _sound
            sounds.append(_sound)

            for i in range(0, len(features_)):
                feature_ = features_[i]
                type_ = feature_types[i]

                if feature_ not in features:
                    features.append(feature_)

                if feature_ not in type_to_features[type_]:
                    type_to_features[type_].append(feature_)

                if feature_ not in feature_to_sounds.keys():
                    feature_to_sounds[feature_] = []

                feature_to_sounds[feature_].append(_sound)

    return features, sounds, type_to_features, feature_to_sounds, features_to_sound
