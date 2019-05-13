import unittest
from features import *


class TestFeatures(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(Features.dorsal in FEATURE_LIB[FeatureTypes.primary_POA])
        self.assertTrue(Features.dorsal in FEATURE_LIB[FeatureTypes.secondary_POA])
        self.assertTrue(Features.dorsal in FEATURE_LIB[FeatureTypes.tertiary_POA])
        self.assertTrue(Features.not_constricted in FEATURE_LIB[FeatureTypes.vocal_fold_constricted])

    def test_str(self):
        self.assertEqual(str(Features.bilabial), "bilabial")
        self.assertEqual(str(Features.unaspirated_voiceless), "unaspirated voiceless")

        self.assertEqual(str(FeatureTypes.phonation), "phonation")
        self.assertEqual(str(FeatureTypes.vocal_fold_constricted), "vocal fold constricted")
