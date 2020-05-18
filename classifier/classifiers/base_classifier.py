from typing import List
from classifier.domain import ClassifierPrediction, Article


class CategoryClassifier:
    """
    Base class of arXiv category classifiers.
    """
    def classify(self, article: Article, top_k: int = 5) -> List[ClassifierPrediction]:
        """
        Classify an article.

        Parameters
        ----------
        article
            Article object to predict category for.
        top_k
            Number of the best predictions to return.

        Returns
        -------
        list
            List of :class:`ClassifierPrediction` objects.
        """
        pass
