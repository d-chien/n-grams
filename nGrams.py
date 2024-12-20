import nltk, re, random
from nltk.tokenize import word_tokenize
from collections import defaultdict, deque, Counter
import itertools

class MarkovChain:
    def __init__(self, sequence_length = 3, seeded = False):
        self.lookup_dict = defaultdict(list)   # a dictionary that each value of keys would default as a list
        self.most_common = list()
        self.seq_len = sequence_length
        self._seeded = seeded
        self.__seed_me()
    
    def __seed_me(self, rand_seed = None):
        if self._seeded is not True:
            try:
                if rand_seed is not None:
                    random.seed(rand_seed)
                else:
                    random.seed()
                    self._seeded = True
            except NotImplementedError:
                self._seeded = False

    def add_document(self, str):
        '''
        str: string of raw text data
        '''
        preprocessed_list = self._preprocess(str)
        self.most_common = Counter(preprocessed_list).most_common(50)   # save top 50 sequences
        pairs = self.__generate_tuple_keys(preprocessed_list)   # set pairs as a generator that create wordpair from data
        for pair in pairs:
            self.lookup_dict[pair[0]].append(pair[1])   # add every next word to first word to show relations between first and next word and freq

    def _preprocess(self, str):
        cleaned = re.sub(r'\W+',' ',str).lower()
        tokenized = word_tokenize(cleaned)
        return tokenized
    
    def __generate_tuple_keys(self, data):
        '''
        if len(data)<seq_len, return None, else return wordpair
        eg. seq_len=3>>data='i look happy'>>'i look','look happy'
        '''
        if len(data) < self.seq_len:
            return
        for i in range(len(data)-1):
            yield [data[i],data[i+1]]

    def generate_text(self, max_length = 15):
        context = deque()   # deque is a better-efficiency replacement of list, which only operate the left/right one object, with time perplexity of O(1)
        output = list()
        if len(self.lookup_dict) > 0:
            self.__seed_me(rand_seed = len(self.lookup_dict))   # to put the first word in the text the first place of predictive text
            chain_head = [list(self.lookup_dict)[0]]
            context.extend(chain_head)
        if self.seq_len>1:
            while len(output) < (max_length - 1):
                next_choices = self.lookup_dict[context[-1]]

                if len(next_choices) > 0:
                    next_word = random.choice(next_choices)

                    context.append(next_word)
                    output.append(context.popleft())
                else:
                    break
            output.extend(list(context))
        else:
            while len(output)<(max_length - 1):
                next_choices = [word[0] for word in self.most_common]
                next_word = random.choice(next_choices)
                output.append(next_word)
        print(f'context: {context}')
        return ' '.join(output)

    def get_most_common_ngrams(self, n = 5):
        print(f'The most common {n} {self.seq_len}-grams: {self.most_common[:n]}')

    def get_lookup_dict(self, n = 10):
        print(f'Lookup dict: (showing the former {n} pairs only)\n{dict(itertools.islice(self.lookup_dict.items(),n))}')

if __name__=='__main__':
    pass