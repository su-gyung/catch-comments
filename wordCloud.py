from wordcloud import (WordCloud, get_single_color_func)
import matplotlib.pyplot as plt
from config import font_path
import time


class MyWordCloud:
    class SimpleGroupedColorFunc(object):
        """Create a color function object which assigns EXACT colors
           to certain words based on the color to words mapping

           Parameters
           ----------
           color_to_words : dict(str -> list(str))
             A dictionary that maps a color to the list of words.

           default_color : str
             Color that will be assigned to a word that's not a member
             of any value from color_to_words.
        """

        def __init__(self, color_to_words, default_color):
            self.word_to_color = {word: color
                                  for (color, words) in color_to_words.items()
                                  for word in words}

            self.default_color = default_color

        def __call__(self, word, **kwargs):
            return self.word_to_color.get(word, self.default_color)

    class GroupedColorFunc(object):
        """Create a color function object which assigns DIFFERENT SHADES of
           specified colors to certain words based on the color to words mapping.

           Uses wordcloud.get_single_color_func

           Parameters
           ----------
           color_to_words : dict(str -> list(str))
             A dictionary that maps a color to the list of words.

           default_color : str
             Color that will be assigned to a word that's not a member
             of any value from color_to_words.
        """

        def __init__(self, color_to_words, default_color):
            self.color_func_to_words = [
                (get_single_color_func(color), set(words))
                for (color, words) in color_to_words.items()]

            self.default_color_func = get_single_color_func(default_color)

        def get_color_func(self, word):
            """Returns a single_color_func associated with the word"""
            try:
                color_func = next(
                    color_func for (color_func, words) in self.color_func_to_words
                    if word in words)
            except StopIteration:
                color_func = self.default_color_func

            return color_func

        def __call__(self, word, **kwargs):
            return self.get_color_func(word)(word, **kwargs)

    def __init__(self, negative={}, positive={}, general={}):
        self.negative = negative
        self.positive = positive
        self.general = general

        keywords = {}
        keywords.update(negative)
        keywords.update(positive)
        keywords.update(general)

        self.keywords = keywords
        self.wc = WordCloud()

    def set_color(self):
        neg_list = [key for key in self.negative]
        pos_list = [key for key in self.positive]

        self.wc = WordCloud(font_path=font_path, width=1000, height=1000, background_color="white").generate_from_frequencies(
            self.keywords)

        color_to_words = {
            # words below will be colored with a green single color function
            '#00ff00': pos_list,
            # will be colored with a red single color function
            'red': neg_list
        }

        # Words that are not in any of the color_to_words values
        # will be colored with a grey single color function
        default_color = 'grey'

        # Create a color function with multiple tones
        grouped_color_func = self.GroupedColorFunc(color_to_words, default_color)

        # Apply our color function
        self.wc.recolor(color_func=grouped_color_func)

    def show(self):
        # Plot
        plt.figure()
        plt.imshow(self.wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    def save(self):
        num = str(time.time())
        plt.figure()
        plt.imshow(self.wc, interpolation="bilinear")
        plt.axis("off")
        plt.savefig("/Users/sugyung/Desktop/"+num+".png")
