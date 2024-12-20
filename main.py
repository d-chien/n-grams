from nGrams import MarkovChain

mc = MarkovChain()

with open('BBC_news.txt','r') as f:
    raw_news = f.read()
#print(raw_news)

my_markov = MarkovChain(sequence_length = 2, seeded = True)
my_markov.add_document(raw_news)

random_news = my_markov.generate_text(max_length = 20)
print(random_news)


my_markov = MarkovChain(sequence_length = 3, seeded = True)
my_markov.add_document(raw_news)
random_news = my_markov.generate_text(max_length = 50)
print(random_news)