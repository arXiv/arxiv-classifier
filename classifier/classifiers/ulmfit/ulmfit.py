"""
ULMFiT based arXiv category classifier with SentencePiece tokenization. 


Currently ignores article's authors and fulltext when predicting.
"""
from classifier.classifiers import CategoryClassifier
from typing import List, Union, Tuple
from classifier.domain import ClassifierPrediction, Article
from arxiv.taxonomy import Category, CATEGORIES
from fastai.text import load_learner, SPProcessor
from pathlib import Path

# These are older categories that should new papers
# should not be classified into.
NEVER_CLASSIFY = tuple(key for key in CATEGORIES.keys()
                       if not CATEGORIES[key]['is_active'])

DEFAULT_PRECISION = 2


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
        self.never_classify = NEVER_CLASSIFY
        self.digits = DEFAULT_PRECISION

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

    def _format(self, cat: ClassifierPrediction) -> ClassifierPrediction:
        cat.probability = float(f"%.{self.digits}f" % cat.probability)
        return cat

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
        minimum = 1 / 10 ** self.digits 
        predictions = [
            ClassifierPrediction(
                Category(category),
                float(probability)
            )
            for category, probability
            in self._predict(article)
        ]

        predictions = sorted(predictions, key=lambda p: p.probability, reverse=True)
        filtered = [self._format(cat)
                    for cat in predictions
                    if cat.category not in self.never_classify
                    and cat.probability >= minimum]
        top = filtered[:top_k]
        
        if article.primary:
            primary_pred_in_top = next((pred for pred in top if
                                        pred.category == article.primary), None)
            if not primary_pred_in_top:
                primary_pred = next((pred for pred in predictions if
                                     pred.category == article.primary), None)
                if primary_pred:
                    top.append(self._format(primary_pred))

        return top
