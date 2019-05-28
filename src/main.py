from __future__ import annotations

from feature_lib import Particle, import_default_features
from sound import Sound
from rules import Rule, import_default_rules
from templates import Template, import_default_templates
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

    print([str(s) for s in sounds])

    templates = import_default_templates(features)  # type: List[Template]

    print([str(t) for t in templates])

    rules = import_default_rules(features)  # type: List[Rule]

    print([str(r) for r in rules])

    gen = Generator(templates, rules[0], 10, feature_to_type, feature_to_sounds)
    result = gen.generate(feature_to_type, feature_to_sounds)
    print("RESULTS")
    for r in result:
        if isinstance(r, list):
            print([str(d) for d in r])
        else:
            print(r)

    #
    # print(sounds[0].get_transformed_sound(Particle(["voiced"]), feature_to_type, feature_to_sounds))
    #
    # # sample template gen
    # # print(templates[0].generate_word_list(feature_to_sounds))
    # #
    # print(rules[0].apply("aba", feature_to_type, feature_to_sounds))
