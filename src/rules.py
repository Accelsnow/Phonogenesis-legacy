from __future__ import annotations
from typing import List, Dict, Optional
import csv
import warnings
from feature_lib import Particle


class Rule:
    """
    A>B/C_D
    """
    _A: List[Particle]
    _B: Optional[List[Particle], str]
    _C: List[Particle]
    _D: List[Particle]

    def __init__(self, a: List[Particle], b: Optional[List[Particle], str], c: List[Particle],
                 d: List[Particle]) -> None:
        self._A = a
        self._B = b
        self._C = c
        self._D = d

    def __str__(self) -> str:
        return "%s -> %s / %s _ %s" % (
            "+".join([str(s) for s in self._A]), "+".join([str(s) for s in self._B]),
            "+".join([str(s) for s in self._C]),
            "+".join([str(s) for s in self._D]))


def import_default_rules() -> List[Rule]:
    return _fetch_rule_csv("defaultrule.txt")


def _fetch_rule_csv(filename: str) -> List[Rule]:
    rules = []  # type: List[Rule]

    with open(filename, encoding='utf-8') as data_file:
        lines = [l.rstrip('\n') for l in data_file.readlines()]

        for line in lines:
            mid_break = line.split("/")

            if len(mid_break) != 2:
                raise ImportError("Invalid rule format: %s" % line)

            action_break = mid_break[0].split("-")
            condition_break = mid_break[1].split("_")

            if len(action_break) != 2 or len(condition_break) != 2:
                raise ImportError("Invalid rule format: %s" % line)

            asec = action_break[0]
            bsec = action_break[1]
            csec = condition_break[0]
            dsec = condition_break[1]

            rules.append(Rule(_sec_to_particles(asec), _sec_to_particles(bsec), _sec_to_particles(csec),
                              _sec_to_particles(dsec)))
    return rules


def _sec_to_particles(sec: str) -> List[Particle]:
    particles = []  # type: List[Particle]

    parts = sec.split("+")

    for part in parts:
        particles.append(Particle(part.split(",")))

    return particles
