from __future__ import annotations

import random
from typing import List

from sound import Sound
from word import Word
from random import random, sample


def import_default_phonemes() -> List[Word]:
    return _fetch_preset_phonemes("defaultrandomizedphoneme.txt")


def _fetch_randomized_phonemes(filename: str) -> List[Word]:
    phoneme_list = []
    phoneme_str = []

    with open(filename, encoding='utf-8') as data_file:
        lines = [l.rstrip('\n') for l in data_file.readlines()]

        for line in lines:
            line = line.replace('ɡ', 'g')
            data = line.split(" ")
            phoneme_str.extend(data)
            phoneme_list.append(data)

    #   filter 1
    rf = []
    if random() < 0.5:
        rf.extend(["ʔ"])

    #   filter 2
    if random() < 0.5:
        rf.extend(["h"])

    #   filter 3
    if random() < 0.5:
        rf.extend(["t͡ʃ", "d͡ʒ"])

    #   filter 4
    r4 = random()
    if r4 < 0.25:
        rf.extend(["v", "ð", "z", "ʒ"])
    elif r4 < 0.5:
        rf.extend(["v", "ð", "z", "ʒ", "b", "d", "ɡ", "d͡ʒ"])

    #   filter 5
    if random() < 0.15:
        rf.extend(["f", "v"])

    #   filter 6
    if random() < 0.15:
        rf.extend(["θ", "ð"])

    #   filter 7
    if random() < 0.15:
        rf.extend(["ʃ", "ʒ"])

    #   filter 8
    if random() < 0.15:
        rf.extend(["m"])

    #   filter 9
    if random() < 0.25:
        rf.extend(["ŋ"])

    #   filter 10
    r10 = random()
    if r10 < 0.25:
        rf.extend(sample(["r", "l", "w", "j"], 1))
    elif r10 < 0.5:
        rf.extend(sample(["r", "l", "w", "j"], 2))
    elif r10 < 0.75:
        rf.extend(sample(["r", "l", "w", "j"], 3))

    #   filter 11
    if random() < 0.75:
        rf.extend(["æ", "ɑ"])
    else:
        rf.extend(["a"])

    #   filter 12
    if random() < 0.5:
        rf.extend(["ə"])

    #   filter 13
    r13 = random()
    if r13 < 0.2:
        rf.extend(["ɪ", "ʊ", "e", "ɛ", "ɔ", "o"])
    elif r13 < 0.4:
        rf.extend(["ɪ", "ʊ"])
        rf.extend(sample(["e", "ɛ", "ɔ", "o"], 3))
    elif r13 < 0.5:
        rf.extend(["ɪ", "ʊ"])
        rf.extend(sample(["e", "ɛ", "ɔ", "o"], 2))
    elif r13 < 0.6:
        rf.extend(["ɪ", "ʊ", "u"])
        rf.extend(sample(["e", "ɛ", "ɔ", "o"], 2))
    elif r13 < 0.7:
        rf.extend(["ɪ", "ʊ"])
        rf.extend(sample(["e", "ɛ", "ɔ", "o"], 1))
    elif r13 < 0.75:
        rf.extend(["ɪ", "ʊ", "u"])
        rf.extend(sample(["e", "ɛ", "ɔ", "o"], 1))
    elif r13 < 0.8:
        rf.extend(sample(["e", "ɛ", "ɔ", "o"], 1))
    elif r13 < 0.9:
        rf.extend(["ɪ", "ʊ"])
    elif r13 < 0.95:
        rf.extend(["ɪ", "ʊ", "u"])

    phoneme_randomized = [s for s in phoneme_str if s not in rf]
    phonemes = [Word([Sound(-1, '', [])[str(s)]]) for s in phoneme_randomized]

    return phonemes


def _fetch_preset_phonemes(filename: str) -> List[Word]:
    phonemes = []

    with open(filename, encoding='utf-8') as data_file:
        lines = [l.rstrip('\n') for l in data_file.readlines()]

        for line in lines:
            line = line.replace('ɡ', 'g')
            data = line.split(" ")

            for sound_str in data:
                phonemes.append(Word([Sound(-1, '', [])[str(sound_str)]]))

    return phonemes
