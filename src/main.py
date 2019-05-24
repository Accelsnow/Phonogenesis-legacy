from __future__ import annotations

import sound
import templates
from rules import Rule, import_default_rules
from feature_lib import Particle, import_default_features
from sound import Sound

from typing import List, Tuple, Dict, Any

if __name__ == '__main__':
    # tup = import_default_features()
    #
    # features = tup[0]  # type: List[str]
    # sounds = tup[1]  # type: List[Sound]
    # type_to_features = tup[2]  # type: Dict[str, List[str]]
    # feature_to_sounds = tup[3]  # type: Dict[str, List[Sound]]
    # features_to_sound = tup[4]  # type: Dict[Particle, Sound]
    #
    # t = sounds[0]
    # print(t)
    # print(t.get_transformed_sound("voiced", type_to_features, features_to_sound))

    r = import_default_rules()

    print([str(rl) for rl in r])
