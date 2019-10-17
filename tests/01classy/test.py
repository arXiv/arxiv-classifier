import os
import unittest
import json

from classifier.services.classifier.naivebayes import ArticleClassifier

test_path_prfx = os.path.dirname(os.path.realpath(__file__)) + '/'


class Test_ClassifierBasics(unittest.TestCase):
    def test_basic_training(self):
        mdate = []
        with open(test_path_prfx + 'metadata.json') as mdjson:
            mdata = json.load(mdjson)
            for item in mdata:
                item["filename"] = test_path_prfx + item["filename"]

        aclz = ArticleClassifier()
        self.assertIsNotNone(mdata)
        self.assertGreater(len(mdata), 0)
        fn = aclz.create_input_file(mdata)
        aclz.train(fn)
        self.assertTrue(aclz.trained)
        aclz.save()

        tdat = []
        with open(test_path_prfx + 'testdata1.json') as mdjson:
            tdat = json.load(mdjson)
            for item in tdat:
                item["filename"] = test_path_prfx + item["filename"]

        cats = aclz.classify(aclz.create_input_file(tdat))
        self.assertIsNotNone(cats)
        self.assertEqual(cats, "JUNK")
