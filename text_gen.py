import nltk
import re
from HTMLParser import HTMLParser

class BigramText(nltk.Text):
    def generate(self, length=100):
        """
        Print random text, generated using a bigram language model.

        :param length: The length of text to generate (default=100)
        :type length: int
        :seealso: NgramModel
        """
        if '_bigram_model' not in self.__dict__:
            # print("Building ngram index...")
            estimator = lambda fdist, bins: nltk.LidstoneProbDist(fdist, 0.2)
            self._bigram_model = nltk.NgramModel(2, self, estimator=estimator)
        text = self._bigram_model.generate(length)
        return text
        # print(nltk.tokenwrap(text))


def gen(tokens):
    print 'generating'
    words = [word for word in tokens if word]
    text = BigramText(words)
    # text = nltk.Text(words)
    result = ' '.join(text.generate())
    r = HTMLParser()
    result = r.unescape(result)
    for punct in '.:"!,':
        #could be more efficient!
        result = result.replace(' %s'%punct, punct)

    return result


