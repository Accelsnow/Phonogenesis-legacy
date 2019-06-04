from __future__ import annotations

from feature_lib import Particle, import_default_features
from sound import Sound
from rules import Rule, import_default_rules
from templates import Template, import_default_templates, import_default_phonemes
from generator import Generator

from typing import List, Tuple, Dict, Any

if __name__ == '__main__':
    tup = import_default_features()

    features = tup[0]  # type: List[str]
    sounds = tup[1]  # type: List[Sound]
    type_to_features = tup[2]  # type: Dict[str, List[str]]
    feature_to_type = tup[3]  # type: Dict[str, str]
    feature_to_sounds = tup[4]  # type: Dict[str, List[Sound]]
    features_to_sound = tup[5]  # type: Dict[Particle, Sound]

    templates = import_default_templates(features)  # type: List[Template]

    print("full templates: ")
    for template in templates:
        print(template)

    rules = import_default_rules(features)  # type: List[Rule]

    print("\nfull rules: ")
    for rule in rules:
        print(rule)

    phonemes = import_default_phonemes()

    print("\nfull phonemes: ", [str(p) for p in phonemes])

    # while True:
    # word = input("\nWord to check: ")
    # print(rules[1].classify("susu", phonemes, feature_to_type, feature_to_sounds))

    gen = Generator(phonemes, templates, rules[1], 5, feature_to_type, feature_to_sounds)
    result = gen.generate(20, feature_to_type, feature_to_sounds)
    print("=====RESULTS=====")
    print("SR: ", [str(s) for s in result[0]])
    print("UR: ", [str(s) for s in result[1]])
    print("RULE: ", result[2])
    print("TEMPLATES: ", [str(s) for s in result[3]])


    #
    # print(sounds[0].get_transformed_sound(Particle(["voiced"]), feature_to_type, feature_to_sounds))
    #
    # # sample template gen
    # # print(templates[0].generate_word_list(feature_to_sounds))
    # #
    # print(rules[0].apply("aba", feature_to_type, feature_to_sounds))
