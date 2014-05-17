import re
import os
import sys
import codecs

allstags = {'a', 'r', 'v', 'n'}

class SWNReader:
    def __init__(self,filename):
        self.filename = filename
        self.swn_lines = []
        self.open_swn()
    
    def open_swn(self):
        self.swn_lines = codecs.open(self.filename, "r", "utf8").read().splitlines()
        self.swn_lines = filter((lambda x : not re.search(r"^\s*#", x)), self.swn_lines)

    def parse_line(self, line):
        fields = re.split(r"\t+", line)
        fields = map(unicode.strip, fields)
        return fields
    
    def senti_score(self, line, pos):
        fields = self.parse_line(line)
        try:            
            line_pos, offset, pos_score, neg_score, synset_terms, gloss = fields
        except:
            sys.stderr.write("Line %s formatted incorrectly: %s\n" % (i, line))
        if pos == line_pos:
            return pos_score, neg_score
        else:
            return 100, 100
    
    def no_pos_senti_synset(self, lemma):
        synset_term = unicode(lemma + '#')
        for line in self.swn_lines:
            if synset_term in line:
                for stag in allstags:
                    pos_score, neg_score = self.senti_score(line, stag)
                    if pos_score and neg_score:
                        return pos_score, neg_score
                        break
    

    def senti_synset(self, key):
        terms = key.split('.',3)
        lemma, pos, n = terms
        synset_term = unicode(lemma + '#' + n)
        for line in self.swn_lines:
            if synset_term in line:
                pos_score, neg_score = self.senti_score(line, pos)
                if pos_score !=100 and neg_score != 100:
                    return pos_score, neg_score
    
    def synset(self, lemma):
        lemma_set = []
        lemma = lemma + '#'
        for line in self.swn_lines:
            if lemma in line:
                fields = self.parse_line(line)
                line_pos, offset, pos_score, neg_score, synset_terms, gloss = fields
                temp = []
                temp = synset_terms.split(' ')
                for term in temp:
                    lemma_set.append(term + '#' + line_pos)
        if lemma_set != []:
            return lemma_set
        else:
            return None
    

    
