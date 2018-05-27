from os import urandom
from math import log, ceil
from itertools import chain
from choose import Choose, count, get_choice
from words import get_words

words = get_words()

noun = Choose(words.nouns)
adjective = Choose(words.adjectives)
adverb = Choose(words.adverbs)
a_noun = Choose(words.a_nouns)
an_adjective = Choose(words.an_adjectives)
superlative = Choose(words.superlatives)

recipient = '{name}'
recipients = '{plural_name}'

def with_commas(semantics):
    return list(chain(*([word, ', '] for word in semantics)))[:-1]

superlatives = Choose(
    with_commas(superlative for _ in range(i))
    for i in range(1,3)
)

adjectives = Choose(
    with_commas(adjective for _ in range(i))
    for i in range(1,3)
)

preposition = Choose(
    ['in ', Choose(
        ['the ', Choose('entire '), Choose('universe','world')],
        [Choose('creation','existence','history','time immemorial')]
    )],
    ['on the ', Choose('entire '), Choose('planet','globe')],
    'ever',
    'of all'
)

alignments = [
    [recipient,' is ',a_noun],
    [recipient,' is ',adjective],
    [recipient,' is ',adjective,' and ',adjective],
    [recipient,' is ',adjectives,' and ',adjective],
    [recipient,' is ',adverb,' ',adjective],
    [recipient,' is ',an_adjective,' ',noun],
    [recipient,' is ',an_adjective,' ',noun],
    [recipient,' is the ',superlative,' ',noun],
    [recipient,' is the ',superlative,' ',noun],
    [recipient,' is the ',superlative,', ',adjective,' ',noun],
    [recipient,' is the ',superlative,', ',adjective,' ',noun,' ',preposition],
    [recipient,' is the ',superlative,' ',noun,' ',preposition],
    [recipient,' is always the ',superlatives,' ',noun],
    [adjective,' is one word that describes ',recipient],
    [adjective, ' and ', adjective, '! That\'s what ',recipient,' is'],
    [adverb,' ',adjective,' are two words that describe ',recipient]
]

compliment_count = len(Choose(alignments))

def plural_name(word):
    if word.endswith('s'):
        return "{}'s".format(word)
    else:
        return '{}s'.format(word)

# We need high quality, cryptographically secured, random numbers to
# ensure sure that ANY ONE of the potential BILLIONS of compliment 
# can be chosen, so we can't use random.randint
def randint(low, hi):
    num = hi-low
    bytes_needed = ceil(log(num)/log(2**8))
    while True:
        rand = int.from_bytes(urandom(bytes_needed), byteorder='little')
        if rand < num:
            return low + rand

def generate_compliment(name):
    chosen_semantics = alignments[randint(0, len(alignments))] # make each alignment have the same chance of being chosen
    chosen_phrase = get_choice(chosen_semantics, randint(0, count(chosen_semantics)))
    return chosen_phrase.format(
        name=name,
        plural_name=plural_name(recipient)
    )

