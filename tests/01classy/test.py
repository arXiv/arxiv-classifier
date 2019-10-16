import os
import unittest
import json

from classifier.services.classifier.naivebayes import ArticleClassifier

test_path = os.path.dirname(os.path.realpath(__file__))


class Test_ClassifierBasics(unittest.TestCase):
    def test_basic_training(self):
        with open(test_path + '/metadata.json') as mdjson:
            mdata = json.load(mdjson)
            for item in mdata:
                item["filename"]=test_path + '/' + item["filename"]

            aclz = ArticleClassifier()
            self.assertIsNotNone(mdata)
            self.assertGreater(len(mdata), 0)
            fn = aclz.create_input_file(mdata)
            aclz.train(fn)
            self.assertTrue(aclz.trained)
            aclz.save()
            self.assertTrue(False)
