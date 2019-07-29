from __future__ import annotations

import sys
from typing import List, Dict, Tuple

from feature_lib import Particle, import_default_features
from generator import Generator
import random
from rules import Rule, RuleFamily, import_default_rules
from sound import Sound
from glossgroup import GlossGroup, GlossFamily, import_default_gloss
from templates import Template, import_default_templates, import_default_phonemes

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

    rule_data = import_default_rules(features)  # type: Tuple[List[RuleFamily], List[Rule]]
    rule_families = rule_data[0]  # type: List[RuleFamily]
    rules = rule_data[1]  # type: List[Rule]

    print("\nfull rule families:")
    fi = 1
    for family in rule_families:
        print(fi, family)
        fi += 1

    print("\nfull rules: ")
    ri = 1
    for rule in rules:
        print(ri, rule)
        ri += 1

    phonemes = import_default_phonemes()

    print("\nfull phonemes: ", [str(p) for p in phonemes])

    gloss_data = import_default_gloss()
    gloss_families = gloss_data[0]
    gloss_groups = gloss_data[1]

    print("\nfull gloss families: ", [str(f) + "\n" for f in gloss_families])
    print("\nfull gloss groups: ", [str(g) + "\n" for g in gloss_groups])

    print("\n==================================================\n")

    manual_rule_select = 46

    # while True:
    #     # word = input("\nWord to check: ")
    #     word = "fab"
    #     print(rules[manual_rule_select].classify(word, phonemes, feature_to_type, feature_to_sounds))
    #     break

    if len(sys.argv) > 1:
        use_templates = [templates[int(s) - 1] for s in sys.argv[1].split(",")]
        use_rule = rules[int(sys.argv[2]) - 1]
        amount = int(sys.argv[3])
    else:
        use_templates = templates
        use_rule = rules[manual_rule_select]
        amount = 20

    print("USING TEMPLATES: ")
    ti = 1
    for template in use_templates:
        print(ti, template)
        ti += 1

    print("\nUSING RULE: ", use_rule)
    print("\nGENERATION AMOUNT:", amount, '\n')

    gen = Generator(phonemes, use_templates, use_rule, 5, feature_to_type, feature_to_sounds)

    result = gen.generate(amount, feature_to_type, feature_to_sounds, gloss_groups)

    print("=============INTEREST===============")
    interest = rules[manual_rule_select].get_interest_phones(phonemes, feature_to_type, feature_to_sounds)
    print(interest[0])
    print(interest[1])

    print("\n=============RESULTS================")
    print("UR: ", [str(s) for s in result[0]])
    print("SR: ", [str(s) for s in result[1]])
    print("RULE: ", result[2])
    print("TEMPLATES: ")
    for t in [str(s) for s in result[3]]:
        print(t)

    # sample template gen
    # print(templates[0].generate_word_list(feature_to_sounds))
    #
    # print(rules[0].apply("aba", phonemes, feature_to_type, feature_to_sounds))


def random_select(families: List[RuleFamily], rules_: List[Rule], family_num: int, rule_num: int) -> List[Rule]:
    if family_num > rule_num:
        raise AttributeError("family num larger than rule num")

    if len(families) < family_num:
        raise AttributeError("num greater than family size")

    if len(rules_) < rule_num:
        raise AttributeError("num greater than rule size")

    chosen_family = random.choices(families, k=family_num)  # type: List[RuleFamily]
    rules_pool = [family_.get_rules() for family_ in chosen_family]
    random_result = []

    while rule_num > 0:
        for pool in rules_pool:
            if rule_num <= 0:
                break

            if len(pool) == 0:
                continue

            chosen = random.choice(pool)  # type: Rule
            pool.remove(chosen)
            random_result.append(chosen)
            rule_num -= 1

    return random_result
