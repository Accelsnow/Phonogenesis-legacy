from __future__ import annotations

from enum import Enum
from typing import List


class PropertyTypes(Enum):
    MAIN = 0
    MANNER = 1
    VOICING = 2
    PLACE_OF_ARTICULATION = 3


class Properties(Enum):
    CONSONANT = "CONSONANT", [], [], PropertyTypes.MAIN
    VOWEL = "VOWEL", [], [], PropertyTypes.MAIN

    OBS = "OBS", [CONSONANT], [], PropertyTypes.MANNER
    STOP = "STOP", [OBS], [], PropertyTypes.MANNER
    FRICATIVE = "FRICATIVE", [OBS], [], PropertyTypes.MANNER

    SON = "SON", [CONSONANT], [], PropertyTypes.MANNER
    GLIDE = "GLIDE", [SON], [], PropertyTypes.MANNER
    LIQUID = "LIQUID", [SON], [], PropertyTypes.MANNER
    NASAL = "NASAL", [SON], [], PropertyTypes.MANNER

    VOICED = "VOICED", [CONSONANT], [], PropertyTypes.VOICING
    MODAL = "MODAL", [VOICED], [], PropertyTypes.VOICING
    BREATHY = "BREATHY", [VOICED], [], PropertyTypes.VOICING

    VOICELESS = "VOICELESS", [CONSONANT], [], PropertyTypes.VOICING
    ASP = "ASP", [VOICELESS], [], PropertyTypes.VOICING
    UNASP = "UNSAP", [VOICELESS], [], PropertyTypes.VOICING

    COR = "COR", [CONSONANT], [], PropertyTypes.PLACE_OF_ARTICULATION
    DENT = "DENT", [COR], [], PropertyTypes.PLACE_OF_ARTICULATION
    ALV = "ALV", [COR], [], PropertyTypes.PLACE_OF_ARTICULATION
    POSTALV = "POSTALV", [COR], [], PropertyTypes.PLACE_OF_ARTICULATION

    DOR = "DOR", [CONSONANT], [], PropertyTypes.PLACE_OF_ARTICULATION
    VEL = "VEL", [DOR], [], PropertyTypes.PLACE_OF_ARTICULATION
    NVU = "NVU", [DOR], [], PropertyTypes.PLACE_OF_ARTICULATION

    PAL = "PAL", [COR, DOR], [], PropertyTypes.PLACE_OF_ARTICULATION

    LAB = "LAB", [CONSONANT], [], PropertyTypes.PLACE_OF_ARTICULATION
    BILAB = "BILAB", [LAB], [], PropertyTypes.PLACE_OF_ARTICULATION
    LABIODENT = "LABIODENT", [LAB], [], PropertyTypes.PLACE_OF_ARTICULATION

    def __init__(self, name: str, parents: List[Properties], children: List[Properties], property_type: PropertyTypes):
        """
        Register all children properties to their parents

        >>> p1 = Properties.CONSONANT
        >>> Properties.OBS in p1.children
        True
        >>> p2 = Properties.COR
        >>> Properties.CONSONANT in p2.parents
        True
        >>> Properties.PAL in p2.children
        True
        >>> p3 = Properties.GLIDE
        >>> Properties.SON in p3.parents
        True
        >>> Properties.CONSONANT not in p3.parents
        True
        >>> p4 = Properties.PAL
        >>> Properties.COR in p4.parents
        True
        >>> Properties.DOR in p4.parents
        True
        """
        # add children to parents' children list
        for parent in parents:
            parent[2].append(self)

        self._parents = parents
        self._children = children
        self._str_name = name
        self._property_type = property_type

    @property
    def parents(self):
        # converting parents list from values to enums
        while len(self._parents) > 0 and not isinstance(self._parents[0], Properties):
            info = self._parents[0][0], self._parents[0][1], self._parents[0][2], self._parents[0][3]
            self._parents.append(Properties(info))
            self._parents.pop(0)

        return self._parents

    @property
    def children(self):
        return self._children

    @property
    def str_name(self):
        return self._str_name

    @property
    def property_type(self):
        return self._property_type


if __name__ == '__main__':
    for p in Properties:
        print(p.value[0], p.value[2])
