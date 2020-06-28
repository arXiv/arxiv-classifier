"""
ULMFiT based arXiv category classifier with SentencePiece tokenization. Currently ignores article's authors and
fulltext when predicting.
"""
from classifier.classifiers import CategoryClassifier
from typing import List, Union, Tuple
from classifier.domain import ClassifierPrediction, Article
from arxiv.taxonomy import Category
from fastai.text import load_learner, SPProcessor
from pathlib import Path


class ULMFiTClassifier(CategoryClassifier):
    def __init__(self, path: Union[str, Path]):
        """
        Parameters
        ----------
        path
            path to the model file. SentencePiece model and vocabulary files should reside in the same directory
            and be called spm.model and spm.vocab respectively.
        """
        self.path = Path(path)
        self._load_model()

    def _load_model(self) -> None:
        """
        Loads model from file.
        """
        model_path = self.path.parent
        model_file = self.path.name
        self.learner = load_learner(model_path, model_file)
        self._fix_sp_processor(model_path, 'spm.model', 'spm.vocab')
        self.learner.predict("")  # force loading of SentencePiece files

    def _fix_sp_processor(self, sp_path: Path, sp_model: str, sp_vocab: str) -> None:
        """
        Fixes SentencePiece paths serialized into the model.
        Parameters
        ----------
        sp_path
            path to  the directory containing the SentencePiece model and vocabulary files.
        sp_model
            SentencePiece model filename.
        sp_vocab
            SentencePiece vocabulary filename.
        """
        for processor in self.learner.data.processor:
            if isinstance(processor, SPProcessor):
                processor.sp_model = sp_path / sp_model
                processor.sp_vocab = sp_path / sp_vocab

    def _predict(self, article: Article) -> List[Tuple[str, float]]:
        """
        Predict probabilities of all categories.
        Parameters
        ----------
        article
            Article object to predict category for. Only the title and abstract are taken into consideration.

        Returns
        -------
        list
            list of (category, probability) pairs
        """

        inputs = [
            article.title or '',
            article.abstract or ''
        ]
        probabilities = self.learner.predict(inputs)[2].numpy()
        return list(zip(self.learner.data.classes, probabilities))

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
        predictions = [
            ClassifierPrediction(
                Category(category),
                float(probability)
            )
            for category, probability
            in self._predict(article)
        ]

        predictions = sorted(predictions, key=lambda p: p.probability, reverse=True)
        return predictions[:top_k]
