# -*- coding: utf-8 -*-

# Copyright (c) 2014, Le Tuan Anh <tuananh.ke@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import logging
from collections import namedtuple
from collections import defaultdict as dd
from collections import OrderedDict
from chirptext import FileHelper

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

OPEN_TAG = "<wnsk>"
CLOSE_TAG = "</wnsk>"

TokenInfo = namedtuple("TokenInfo", ['text', 'sk'])


class TagInfo(object):

    GOLD = 'gold'
    ISF = 'isf'
    MFS = 'mfs'
    LELESK = 'lelesk'
    OTHER = 'other'
    NTUMC = 'ntumc'
    MECAB = 'mecab'
    NLTK = 'nltk'
    DEFAULT = 'n/a'

    def __init__(self, cfrom=-1, cto=-1, label='', source=DEFAULT, tagtype=''):
        self.cfrom = cfrom
        self.cto = cto
        self.label = label
        self.source = source
        self.tagtype = tagtype  # tag type

    def __repr__(self):
        if not self.tagtype:
            return '`{}`'.format(self.label)
        else:
            return '`{}:{}`'.format(self.tagtype, self.label)

    def __str__(self):
        return "`{l}`<{f}:{t}>{v}".format(l=self.label, f=self.cfrom, t=self.cto, v=self.tagtype)


class TaggedSentence(object):

    def __init__(self, text, tags=None, tokens=None, ID=None):
        self.text = text
        self.tags = tags if tags else []
        self._tokens = tokens if tokens else []
        self.concept_map = OrderedDict()  # concept.cid to concept object
        self.ID = ID

    def __str__(self):
        # return format_tag(self)
        if self.ID:
            return "#{id}: {txt}".format(id=self.ID, txt=self.text)
        else:
            return self.text

    def __getitem__(self, idx):
        return self._tokens[idx]

    def __len__(self):
        return len(self._tokens)

    @property
    def tokens(self):
        return self._tokens

    @property
    def concepts(self):
        return tuple(self.concept_map.values())

    @property
    def wclinks(self):
        ''' Return word-concepts map '''
        wcm = dd(list)
        for concept in self.concept_map.values():
            for w in concept.words:
                wcm[w].append(concept)
        return wcm

    @property
    def mwe(self):
        ''' Get all multi-word expressions '''
        mwe = []
        for c in self.concept_map.values():
            if len(c.words) > 1:
                mwe.append(c)
        return mwe

    @property
    def msw(self):
        ''' Get words that were tagged with multiple senses '''
        return [w for w, c in self.wclinks.items() if len(c) > 1]

    def add_token(self, label, cfrom=-1, cto=-1, source=TagInfo.DEFAULT):
        tk = Token(cfrom, cto, label, self)
        self._tokens.append(tk)

    def import_tokens(self, tokens, import_hook=None, ignorecase=True):
        text = self.text.lower() if ignorecase else self.text
        has_hooker = import_hook and callable(import_hook)
        cfrom = 0
        for token in tokens:
            if has_hooker:
                import_hook(token)
            start = text.find(token.lower() if ignorecase else token, cfrom)
            if start == -1:
                raise LookupError('Cannot find token `{t}` in sent `{s}`({l}) from {i} ({p})'.format(t=token, s=self.text, l=len(self.text), i=cfrom, p=self.text[cfrom:cfrom + 20]))
            cfrom = start
            cto = cfrom + len(token)
            self.add_token(token, cfrom, cto)
            cfrom = cto - 1

    def add_concept(self, cid, clemma, tag, words=None):
        ''' Add a new concept object '''
        c = Concept(cid, clemma, tag, self, words)
        self.concept_map[cid] = c

    def tag(self, clemma, tag, *word_ids):
        cid = 0
        while cid in self.concept_map:
            cid += 1
        self.add_concept(cid, clemma, tag, [self[x] for x in word_ids])

    def concept(self, cid):
        ''' Get a concept by concept ID '''
        return self.concept_map[cid]

    def to_json(self):
        return {'text': self.text,
                'tokens': [t.to_json() for t in self.tokens],
                'concepts': [c.to_json() for c in self.concepts]}


class Token(object):

    LEMMA = 'lemma'
    POS = 'pos'
    COMMENT = 'comment'

    def __init__(self, cfrom, cto, label, sent=None, tags=None, source=TagInfo.DEFAULT):
        ''' A token (e.g. a word in a sentence) '''
        self.cfrom = cfrom
        self.cto = cto
        self._tags = tags if tags else []
        self.sent = sent
        self.label = label

    def __getitem__(self, idx):
        return self._tags[idx]

    def __len__(self):
        return len(self._tags)

    @property
    def surface(self):
        if self.sent and self.sent.text:
            return self.sent.text[self.cfrom:self.cto]
        else:
            return ''

    @property
    def pos(self):
        tm = self.tag_map
        if self.POS in tm:
            return tm[self.POS][0].label
        else:
            return ''

    @property
    def lemma(self):
        tm = self.tag_map
        if self.LEMMA in tm:
            return tm[self.LEMMA][0].label
        else:
            return ''

    @property
    def comment(self):
        tm = self.tag_map
        if Token.COMMENT in tm:
            return tm[self.COMMENT][0].label
        else:
            return ''

    def __repr__(self):
        return "`{l}`<{f}:{t}>".format(l=self.label, f=self.cfrom, t=self.cto)

    @property
    def tag_map(self):
        tm = dd(list)
        for tag in self._tags:
            tm[tag.tagtype].append(tag)
        return tm

    @property
    def tags(self):
        return self._tags

    def __str__(self):
        return "`{l}`<{f}:{t}>{tgs}".format(l=self.label, f=self.cfrom, t=self.cto, tgs=self._tags if self._tags else '')

    def tag(self, label, cfrom=None, cto=None, tagtype=None, source=TagInfo.DEFAULT):
        if not cfrom:
            cfrom = self.cfrom
        if not cto:
            cto = self.cto
        tag = TagInfo(label=label, cfrom=cfrom, cto=cto, tagtype=tagtype)
        self._tags.append(tag)

    def to_json(self):
        tagdict = dd(list)
        token_json = {'cfrom': self.cfrom,
                      'cto': self.cto,
                      'label': self.label}
        for k, tags in self.tag_map.items():
            if k == Token.LEMMA:
                token_json[Token.LEMMA] = ', '.join([t.label for t in tags])
                pass
            elif k == Token.POS:
                token_json[Token.POS] = ', '.join([t.label for t in tags])
            elif k == Token.COMMENT:
                token_json[Token.COMMENT] = '\n'.join([t.label for t in tags])
            else:
                tagdict[k if k else 'unsorted'].extend([t.label for t in tags])
        if tagdict:
            token_json['tags'] = dict(tagdict)
        return token_json


class TaggedDoc(object):

    def __init__(self, doc_path, doc_name):
        self.path = FileHelper.abspath(doc_path)
        self.name = doc_name
        self.sents = []
        self.sent_map = {}

    def __len__(self):
        return len(self.sents)

    def __getitem__(self, idx):
        return self.sents[idx]

    @property
    def sent_path(self):
        return os.path.join(self.path, '{}_sents.txt'.format(self.name))

    @property
    def word_path(self):
        return os.path.join(self.path, '{}_words.txt'.format(self.name))

    @property
    def concept_path(self):
        return os.path.join(self.path, '{}_concepts.txt'.format(self.name))

    @property
    def link_path(self):
        return os.path.join(self.path, '{}_links.txt'.format(self.name))

    def add_sent(self, text, ID):
        sent = TaggedSentence(text, ID=ID)
        self.sents.append(sent)
        self.sent_map[ID] = sent
        return sent

    def read(self):
        with open(self.sent_path) as sentfile:
            for line in sentfile:
                if not line.strip():
                    continue
                sid, text = line.split('\t', maxsplit=1)
                self.add_sent(text.strip(), ID=sid)
        # read words
        sent_words_map = dd(list)
        with open(self.word_path) as wordfile:
            for line in wordfile:
                sid, wid, word, lemma, pos = line.split('\t')
                sent_words_map[sid].append((word, lemma, pos.strip(), wid))
                # TODO: verify wid?
        # import words
        for sent in self.sents:
            sent_words = sent_words_map[sent.ID]
            sent.import_tokens([x[0] for x in sent_words])
            for ((word, lemma, pos, wid), token) in zip(sent_words, sent.tokens):
                token.tag(tagtype='pos', label=pos)
                token.tag(tagtype='lemma', label=lemma)
                token.tag(tagtype='wid', label=wid)
        # read concepts
        with open(self.concept_path) as concept_file:
            for line in concept_file:
                sid, cid, clemma, tag = line.split('\t')
                self.sent_map[sid].add_concept(cid, clemma, tag.strip())
        # read concept links
        with open(self.link_path) as link_file:
            for line in link_file:
                sid, cid, wid = line.split('\t')
                sent = self.sent_map[sid]
                wid = int(wid.strip())
                sent.concept_map[cid].words.append(sent[wid])
        # tag words
        # for sent in self.sents:
        #     sent_concepts = sent_concepts_map[sent.ID]
        #     for cid, clemma, tag in sent_concepts:
        #         wids = concept_links_map[(sent.ID, cid)]
        #         for wid in wids:
        #             logging.debug("wid {} of {} ({})".format(wid, len(sent), sent))
        #             sent[int(wid)].tag(label='clemma', value=clemma)
        #             sent[int(wid)].tag(tag)
        return self


class Concept(object):

    def __init__(self, cid, clemma, tag, sent, words=None):
        self.cid = cid
        self.clemma = clemma
        self.tag = tag
        self.sent = sent
        self.comment = ''
        if words:
            if type(words) == list:
                self.words = words
            else:
                self.words = list(words)
        else:
            self.words = []

    def add_word(self, word):
        self.words.append(word)

    def __repr__(self):
        return '<{t}:"{l}">'.format(l=self.clemma, t=self.tag)

    def __str__(self):
        return '<{t}:"{l}">({ws})'.format(l=self.clemma, t=self.tag, ws=self.words)

    def to_json(self):
        if self.sent:
            # get word idx from sent
            words = [self.sent.tokens.index(w) for w in self.words]
        else:
            words = [w.label for w in self.words]
        cdict = {
            'clemma': self.clemma,
            'tag': self.tag,
            'words': words
        }
        if self.comment:
            cdict['comment'] = self.comment
        return cdict


class StringBuffer:
    def __init__(self, text=None):
        self.buff = []
        self.__length = 0
        self.append(text)
        self.write = self.append

    def clear(self):
        del self.buff[:]

    def append(self, text):
        if text:
            self.buff.append(text)
            self.__length += len(text)
        return self

    def writeline(self, text):
        return self.append(text).newline()

    def newline(self):
        return self.append('\n')

    def size(self):
        return self.__length

    def __len__(self):
        return self.__length

    def __str__(self):
        return ''.join(self.buff)


if __name__ == "__main__":
    print("This is a library, not an application.")
