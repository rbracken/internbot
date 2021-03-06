import random

""" Credits for this code go to Shabda Raaj, pulled from the article
    'Generating pseudo-random text with Markov chains using Python',
    which can be found at:
    http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/ """

class Markov(object):

    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database()


    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.lower().split()
        return words


    def triples(self):
        """ Generates triples from the given data string. So if our string were
                "What a lovely day", we'd generate (What, a, lovely) and then
                (a, lovely, day).
        """

        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i+1], self.words[i+2])

    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def generate_markov_text(self, size=25):
        seed = random.randint(0, self.word_size-3)
        seed_word, next_word = self.words[seed], self.words[seed+1]
        w1, w2 = seed_word, next_word
        gen_words = []
        for i in xrange(size):
            gen_words.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
        gen_words.append(w2)
        return ' '.join(gen_words)

    def generate_markov_response(self, seed_word=None, next_word=None, size=25):
        w1, w2 = seed_word, next_word
        gen_words = []
        try:
            for i in xrange(size):
                gen_words.append(w1)
                w1, w2 = w2, random.choice(self.cache[(w1, w2)])
            gen_words.append(w2)
        except:
            seed = self.words.index(next_word)
            seed_word = self.words[seed-1]
            w1, w2 = seed_word, next_word
            for i in xrange(size):
                gen_words.append(w1)
                w1, w2 = w2, random.choice(self.cache[(w1, w2)])
            gen_words.append(w2)
        return ' '.join(gen_words)

