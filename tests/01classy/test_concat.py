import os
import unittest

from classifier.services.classifier.naivebayes import ArticleClassifier

test_path_prfx = os.path.dirname(os.path.realpath(__file__)) + '/'

concat_out_target = 'test_concat_texts_outuput.txt'


class Test_Concat(unittest.TestCase):
    def setUp(self):
        self.addCleanup(os.remove, concat_out_target)

    def test_concat_texts(self):
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
