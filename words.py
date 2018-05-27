import re
import configuration
from nltk.corpus import wordnet
from itertools import chain
from collections import namedtuple

Words = namedtuple('Words', ('nouns','adjectives','verbs','adverbs','a_nouns','an_adjectives','superlatives'))

def has_pos(pos):
    return lambda x: x.pos() == pos

def has_lexname(lexname):
    return lambda x: x.lexname() == lexname

def synonyms(words, kind, lexname=None):
    syns = chain(*(wordnet.synsets(word,kind) for word in words))
    more_syns = chain(*([syn]+syn.hyponyms() for syn in syns))
    if lexname:
        more_syns = filter(has_lexname(lexname), more_syns)
    more_syns = filter(has_pos(kind), more_syns)
    return chain(*(syn.lemmas() for syn in more_syns))

def derived_lemmas(lemmas, kind):
    forms = chain(*(lemma.derivationally_related_forms() for lemma in lemmas))
    syns = (form.synset() for form in forms)
    more_syns = chain(*([syn]+syn.hyponyms() for syn in syns))
    filtered_syns = filter(has_pos(kind), more_syns)
    return chain(*(syn.lemmas() for syn in more_syns))

def a(words):
    return (
        'an {}'.format(word) if word[0] in 'aeiou' else 'a {}'.format(word)
        for word in words
    )

def to_superlative(adjective):
    if len(re.findall(r'[aeiouy]+',adjective)) < 2:
        if re.match(r'^.*[aeiou][tp]$', adjective):
          adjective += adjective[-1]
        return '{}est'.format(adjective)
    elif adjective.endswith('y'):
        return '{}iest'.format(adjective[:-1])
    else:
        return 'most {}'.format(adjective)

def get_words():
    noun_lemmas = set(synonyms(configuration.noun_list,'n'))

    derived_adjective_lemmas = derived_lemmas(noun_lemmas,'s')

    added_adjective_lemmas = synonyms(configuration.adjective_list,'s')
    adjective_lemmas = set(chain(derived_adjective_lemmas, added_adjective_lemmas))

    derived_adverbs = chain(derived_lemmas(adjective_lemmas,'r'), derived_lemmas(noun_lemmas,'r'))
    added_adverbs = synonyms(configuration.adverb_list,'r')
    adverb_lemmas = set(chain(derived_adverbs, added_adverbs))

    nouns = set(lemma.name().replace('_','-') for lemma in noun_lemmas)
    adjectives = set(lemma.name().replace('_','-') for lemma in adjective_lemmas)
    adverbs = set(lemma.name().replace('_','-') for lemma in adverb_lemmas)

    a_nouns = set(a(nouns))
    an_adjectives = set(a(adjectives))

    superlatives = set(to_superlative(adj) for adj in adjectives)
    return Words(nouns=nouns,verbs=set(),adjectives=adjectives,adverbs=adverbs,a_nouns=a_nouns,an_adjectives=an_adjectives,superlatives=superlatives)

