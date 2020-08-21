#!/usr/bin/env python
# coding: utf-8
import os

import nltk
import collections
import fasttext as ft
import pandas as pd
from tqdm import tqdm




def ngram_cont_punct(ngram: tuple, puncts):
    for el in ngram:
        if el in puncts:
            return True
    return False


def tokens_enough_long(tokens:tuple):
    n=len(tokens)
    m=sum([len(token) for token in tokens])
    for token in tokens:
        if len(token)<2:
            return False
    return m/n>2


class Seed_Generator:

    def __init__(self, gsw_text, args):
        self.lang = args.language
        self.text = gsw_text
        self.n_seeds = args.n_seeds
        self.ngram = list(range(args.ngram[0], args.ngram[1]+1))
        self.min_proba = args.min_proba
        self.model_filename = args.model
        self.existing_seeds=args.existing_seeds
        self.output_fn=args.output_fn

        self.puncts = ['.', ',', '?', '!', ':', ';', '-', '``','(',')','...',"''","'",'--','%','。','，','？','！']

        self.seeds_df_list = []

    def generate_ngram_frq(self, ngram):
        """
        ngram: int
        Example: if n=3, generate 3-grams
        """
        if self.lang in ['cmn','yue','wuu']:
            import jieba
            tokens=list(jieba.cut(self.text))
        elif  self.lang in ['jpn']:
            # import MeCab
            # from fugashi import Tagger
            # tokens = nltk.word_tokenize(self.text)
            phrases = nltk.word_tokenize(self.text)
            # phrases=[self.text]
            # mecab_tagger = MeCab.Tagger("-Owakati")
            tokens=[]
            # print(len(phrases))
            for phrase in tqdm(phrases):

                tokens+=[phrase[n:n+2] for n in range(len(phrase)-5)]
                tokens+=[phrase[n:n+3] for n in range(len(phrase)-5)]
            # tagger = Tagger('-Owakati')
            # tokens=tagger.parse(self.text).split()  
        elif self.lang in ['tha']:
            import pythainlp as thai
            tokens=thai.tokenize.word_tokenize(self.text)
        else:
            tokens = nltk.word_tokenize(self.text)
        self.ngrams = nltk.ngrams(tokens, ngram)
        self.ngrams = [
            ngram for ngram in self.ngrams if not ngram_cont_punct(ngram, self.puncts)]

        # Build ngram frequency list and sort in descending order
        self.fdist = nltk.FreqDist(self.ngrams)
        self.ngram_freq = {k: v for k, v in sorted(
            self.fdist.items(), reverse=True, key=lambda item: item[1])}

        # Build a pandas DataFrame to do furthur processing
        self.ngrams_df = pd.DataFrame(
            {'ngram': list(self.ngram_freq.keys()), 'freq': list(self.ngram_freq.values())})

        # only keep the most frequent ngrams for furthur processing. empirically, to produce self.n_seeds in the end
        # 3 times seeds as candidates in this step should be enough
        self.candidates_proportion=4

        self.ngrams_df = self.ngrams_df.head(self.n_seeds*self.candidates_proportion//len(self.ngram))



    def remove_existing_seeds(self):

        exsting_seeds_path=self.existing_seeds

        with open(exsting_seeds_path, 'r') as file:
            exsting_seeds_list=file.read().splitlines()

        tqdm.pandas(desc="remove seeds already generated before")

        self.ngrams_df['not_generated_before'] = self.ngrams_df['text'].progress_apply(
            lambda x: x not in exsting_seeds_list)

        self.ngrams_df = self.ngrams_df[self.ngrams_df['not_generated_before']]

    def remove_too_short_ngrams(self):


        self.ngrams_df = self.ngrams_df[self.ngrams_df['ngram'].apply(tokens_enough_long)]

    def load_lid(self):
        path = os.path.join("seeding/src", self.model_filename)
        self.lid = ft.load_model(path)

    def apply_lang_detector(self):
        self.ngrams_df['text'] = self.ngrams_df['ngram'].apply(
            lambda ngram: ' '.join(list(ngram)))

        self.ngrams_df['pred'] = self.ngrams_df['text'].apply(
            lambda x: self.lid.predict(x)[0][0])

        self.ngrams_df['proba'] = self.ngrams_df['text'].apply(
            lambda x: self.lid.predict(x)[1][0])

        # Only keep ngrams which are predicted as the given language and have a proba higher than the threshold given
        threshold = self.min_proba
        self.ngrams_df = self.ngrams_df[(self.ngrams_df['pred'] == '__label__{}'.format(self.lang))
                                        & (self.ngrams_df['proba'] > threshold)]
    def save_seedings(self):
        if len(self.ngrams_df) < self.n_seeds:
            print('''number of seeds produced is less than number of seeds requested. Please consider increase the 
                self.candidates_proportion parameter in self.generate_ngram_frq''')
        seeds_list = self.ngrams_df.head(self.n_seeds)['text'].to_list()
        seeds_list_ = [el+'\n' for el in seeds_list]

        if not self.output_fn.endswith('.txt'):
            self.output_fn+='.txt'
        
        with open('seeding/72seeds/{}'.format(self.output_fn), 'w') as file:
            file.writelines(seeds_list_)

        print('seeds genereated with success!')

    def generate_ngrams(self):

        for n in self.ngram:
            print('start generating {}-gram seeds'.format(n))
            self.generate_ngram_frq(n)
            self.apply_lang_detector()
            if self.lang not in ['cmn','yue','wuu','jpn']:
                self.remove_too_short_ngrams()
            if self.existing_seeds:
                self.remove_existing_seeds()
            # n_sub is the number of seeds we keep for each n(gram). It's equally distributed for each value of n.
            # except the last value of ngram will get some mores seeds due to the effect of euclidien divison
            n_sub = self.n_seeds//len(self.ngram)
            if n != self.ngram[-1]:
                self.seeds_df_list.append(
                    self.ngrams_df.head(n_sub))
            else:
                self.seeds_df_list.append(
                    self.ngrams_df.head(self.n_seeds-n_sub*(len(self.ngram)-1)))

        self.ngrams_df=pd.concat(self.seeds_df_list)


if __name__ == '__main__':
    import argparse
    import sys

    parser=argparse.ArgumentParser()
    parser.add_argument('output_fn', help='extra info to name the saved file')
    parser.add_argument('-l', '--language',
                        default='eng')
    parser.add_argument('-c', '--corpus-filename',
                        default='corpus.txt')
    parser.add_argument('-n', '--n-seeds', default=10,
                        type=int, help='Number of seeds to generate.')
    parser.add_argument('-e', '--existing-seeds', default=None,
                        help='seeds files already existing')      
    parser.add_argument('-g', '--ngram', nargs=2, type=int, default=(3, 3),
                        help='Number of words per seed.')
    parser.add_argument('-m', '--model', default="langdetect72.ftz",
                        help='Pretrained model of language detector')
    parser.add_argument('-p', '--min-proba', default=0.95,
                        help='Min. probability for a seed to be accepted.')
    parser.add_argument('--verboisty', action='store_true', help='verbose')

    args=parser.parse_args()

    corpus_path=os.path.join('seeding', args.corpus_filename)


    with open(corpus_path, 'r') as file:
        sent_list=file.read().splitlines()
    gsw_text=''.join(sent_list)

    seed_generator=Seed_Generator(gsw_text, args)

    seed_generator.load_lid()

    seed_generator.generate_ngrams()

    seed_generator.save_seedings()
