import re


def normalize_sentences(sentence):
    nl_replacer = str(object())
    sentence = sentence.replace('\n', nl_replacer)
    sentence = re.sub(r'([^A-Z\)])([\.\?!])\s+([A-Z])', r'\1\2  \3', sentence)
    sentence = sentence.replace('). ', ').  ').replace(nl_replacer, '\n')
    return sentence.replace('Dr.  ', 'Dr. ')
