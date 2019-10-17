import os
import unittest
import json

from classifier.services.classifier.naivebayes import ArticleClassifier

test_path_prfx = os.path.dirname(os.path.realpath(__file__)) + '/'


class Test_ClassifierBasics(unittest.TestCase):

    def test_concat_texts(self):
        concat_out_target = 'test_concat_texts_outuput.txt'
        articles = [test_path_prfx + 'f1.txt',
                    test_path_prfx + 'g1.txt']
        ac = ArticleClassifier()
        concat_out = ac._concatenate_texts(articles, concat_out_target)
        self.assertEqual(concat_out, concat_out_target)
        with open(concat_out) as cfn:
            first = cfn.readline()
            self.assertIn("new york", first)
            self.assertNotIn("yorkwhen", first)
            self.assertNotIn("gilgamesh", first)
            second = cfn.readline()
            self.assertNotIn("new york", second)
            self.assertIn("gilgamesh", second)

    def test_basic_training(self):
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

        tdat = [{"id": "Federalist No. 20",
                 "categories": [],
                 "filename": test_path_prfx + "f20_unseen.txt"}]
        cats = aclz.classify(aclz.create_input_file(tdat))
        self.assertIsNotNone(cats)
        self.assertEqual(cats, ['federalist'])

        tdat = [{"id": "TABLET X",
                 "categories": [],
                 "filename": test_path_prfx + "g10_unseen.txt"}]
        cats = aclz.classify(aclz.create_input_file(tdat))
        self.assertIsNotNone(cats)
        self.assertEqual(cats, ['gilgamesh'])
