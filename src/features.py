from __future__ import annotations

from enum import Enum, unique
from typing import List, Tuple, Dict


@unique
class FeatureTypes(Enum):
    NA = "NA"
    skeletal_tier = "skeletal tier"
    primary_POA = "primary POA"
    secondary_POA = "secondary POA"
    tertiary_POA = "tertiary POA"
    specific_consonant_POA = "specific consonant POA"
    rounding = "rounding"
    anteriority = "anteriority"
    apicality = "apicality"
    backness = "backness"
    height = "height"
    tenseness = "tenseness"
    manner = "manner"
    voicing = "voicing"
    major_class = "major class"
    aperture = "aperture"
    oral_airflow = "oral airflow"
    lateral = "lateral"
    nasality = "nasality"
    stridency = "stridency"
    vocal_fold_spread = "vocal fold spread"
    vocal_fold_constricted = "vocal fold constricted"
    phonation = "phonation"

    dummy1 = "dummy1"
    dummy2 = "dummy2"
    dummy3 = "dummy3"

    def __str__(self):
        return self.value


FEATURE_LIB = {}


@unique
class Features(Enum):
    NA = [FeatureTypes.NA], "NA"

    non_syllabic = [FeatureTypes.skeletal_tier], "non syllabic"
    syllabic = [FeatureTypes.skeletal_tier], "syllabic"

    labial = [FeatureTypes.primary_POA, FeatureTypes.secondary_POA, FeatureTypes.tertiary_POA], "labial"
    coronal = [FeatureTypes.primary_POA, FeatureTypes.secondary_POA, FeatureTypes.tertiary_POA], "coronal"
    dorsal = [FeatureTypes.primary_POA, FeatureTypes.secondary_POA, FeatureTypes.tertiary_POA], "dorsal"

    bilabial = [FeatureTypes.specific_consonant_POA], "bilabial"
    alveolar = [FeatureTypes.specific_consonant_POA], "alveolar"
    labiodental = [FeatureTypes.specific_consonant_POA], "labiodental"
    dental = [FeatureTypes.specific_consonant_POA], "dental"
    postalveolar = [FeatureTypes.specific_consonant_POA], "postalveolar"
    retroflex = [FeatureTypes.specific_consonant_POA], "retroflex"
    laryngal = [FeatureTypes.specific_consonant_POA], "laryngal"

    rounded = [FeatureTypes.rounding], "rounded"
    unrounded = [FeatureTypes.rounding], "unrounded"

    anterior = [FeatureTypes.anteriority], "anterior"
    posterior = [FeatureTypes.anteriority], "posterior"

    apical = [FeatureTypes.apicality], "apical"
    laminal = [FeatureTypes.apicality], "laminal"

    back = [FeatureTypes.backness], "back"
    front = [FeatureTypes.backness], "front"
    center = [FeatureTypes.backness], "center"  ################################## CONFLICTED CENTRAL

    high = [FeatureTypes.height], "high"
    middle = [FeatureTypes.height], "middle"
    low = [FeatureTypes.height], "low"

    tense = [FeatureTypes.tenseness], "tense"
    lax = [FeatureTypes.tenseness], "lax"

    oral_stop = [FeatureTypes.manner], "oral stop"
    fricative = [FeatureTypes.manner], "fricative"
    nasal_stop = [FeatureTypes.manner], "nasal stop"
    liquid = [FeatureTypes.manner], "liquid"
    glide = [FeatureTypes.manner], "glide"
    vowel = [FeatureTypes.manner], "vowel"

    voiced = [FeatureTypes.voicing], "voiced"
    voiceless = [FeatureTypes.voicing], "voiceless"

    obstruent = [FeatureTypes.major_class], "obstruent"
    sonorant = [FeatureTypes.major_class], "sonorant"

    contoid = [FeatureTypes.aperture], "contoid"
    vocoid = [FeatureTypes.aperture], "vocoid"

    occlusive = [FeatureTypes.oral_airflow], "occlusive"
    continuant = [FeatureTypes.oral_airflow], "continuant"

    central = [FeatureTypes.lateral], "central"  ################################## CONFLICTED CENTRAL
    lateral = [FeatureTypes.lateral], "lateral"

    oral = [FeatureTypes.nasality], "oral"
    nasal = [FeatureTypes.nasality], "nasal"

    strident = [FeatureTypes.stridency], "strident"
    not_strident = [FeatureTypes.stridency], "not strident"

    spread = [FeatureTypes.vocal_fold_spread], "spread"
    not_spread = [FeatureTypes.vocal_fold_spread], "not spread"

    constricted = [FeatureTypes.vocal_fold_constricted], "constricted"
    not_constricted = [FeatureTypes.vocal_fold_constricted], "not constricted"

    unaspirated_voiceless = [FeatureTypes.phonation], "unaspirated voiceless"
    modal_voiced = [FeatureTypes.phonation], "modal voiced"
    aspirated = [FeatureTypes.phonation], "aspirated"
    breathy = [FeatureTypes.phonation], "breathy"

    dummy1A = [FeatureTypes.dummy1], "dummy1A"
    dummy1B = [FeatureTypes.dummy1], "dummy1B"
    dummy1C = [FeatureTypes.dummy1], "dummy1C"

    dummy2A = [FeatureTypes.dummy2], "dummy2A"
    dummy2B = [FeatureTypes.dummy2], "dummy2B"
    dummy2C = [FeatureTypes.dummy2], "dummy2C"

    dummy3A = [FeatureTypes.dummy3], "dummy3A"
    dummy3B = [FeatureTypes.dummy3], "dummy3B"
    dummy3C = [FeatureTypes.dummy3], "dummy3C"

    def __init__(self, kind: List[FeatureTypes], name: str) -> None:
        if kind[0] == FeatureTypes.NA or name == "NA":
            return

        for featureType in kind:
            if featureType not in FEATURE_LIB.keys():
                FEATURE_LIB[featureType] = []

            FEATURE_LIB[featureType].append(self)

    def __str__(self) -> str:
        return self.value[1]

