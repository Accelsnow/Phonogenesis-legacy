from __future__ import annotations

from feature_lib import Particle, import_default_features
from sound import Sound
from rules import Rule, import_default_rules
from templates import Template, import_default_templates, import_default_phonemes
from generator import Generator
import sys

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
    ti = 1
    for template in templates:
        print(ti, template)
        ti += 1

    rules = import_default_rules(features)  # type: List[Rule]

    print("\nfull rules: ")
    ri = 1
    for rule in rules:
        print(ri, rule)
        ri += 1

    phonemes = import_default_phonemes()

    print("\nfull phonemes: ", [str(p) for p in phonemes])

    print("\n==================================================\n")

    # while True:
    # word = input("\nWord to check: ")
    # print(rules[1].classify("susu", phonemes, feature_to_type, feature_to_sounds))

    if len(sys.argv) > 1:
        use_templates = [templates[int(s) - 1] for s in sys.argv[1].split(",")]
        use_rule = rules[int(sys.argv[2]) - 1]
        amount = int(sys.argv[3])
    else:
        use_templates = templates
        use_rule = rules[0]
        amount = 20

    print("USING TEMPLATES: ")
    ti = 1
    for template in use_templates:
        print(ti, template)
        ti += 1

    print("\nUSING RULE: ", use_rule)
    print("\nGENERATION AMOUNT:", amount, '\n')

    gen = Generator(phonemes, use_templates, use_rule, 5, feature_to_type, feature_to_sounds)

    result = gen.generate(amount, feature_to_type, feature_to_sounds)

    print("=============RESULTS================")
    print("SR: ", [str(s) for s in result[0]])
    print("UR: ", [str(s) for s in result[1]])
    print("RULE: ", result[2])
    print("TEMPLATES: ")
    for t in [str(s) for s in result[3]]:
        print(t)

    #
    # print(sounds[0].get_transformed_sound(Particle(["voiced"]), feature_to_type, feature_to_sounds))
    #
    # # sample template gen
    # # print(templates[0].generate_word_list(feature_to_sounds))
    # #
    # print(rules[0].apply("aba", feature_to_type, feature_to_sounds))
