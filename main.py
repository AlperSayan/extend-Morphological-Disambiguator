from MorphologicalAnalysis.FsmMorphologicalAnalyzer import FsmMorphologicalAnalyzer

from MorphologicalDisambiguation.DisambiguatedWord import DisambiguatedWord
from MorphologicalDisambiguation.DisambiguationCorpus import DisambiguationCorpus

from MorphologicalDisambiguation.MyDisambiguation import MyDisambiguation
from MorphologicalDisambiguation.My_algo_combined import My_algo_combined

import os


#   I wrote 2 interfaces for morphological disambigation interface first one is myDisambiguation.py which does:
#   If the length of the sentence is more than 3 words it looks into the beginning word and end word of the sentence
#   In addition with their igs to get the correct parse
#   the other one is my_algo_combined.py which combines all the written disambugation algorithms and returns the most
#   frequent parse for each word.


def main():


    my_corpus_path = r'disambigation_dataset.txt'

    if not os.path.isfile(my_corpus_path):
        print('parsing turkish-phrase')
        loader()

    fsm = FsmMorphologicalAnalyzer("turkish_dictionary.txt", "turkish_misspellings.txt",
                                  "turkish_finite_state_machine.xml")

    # load corpus from turkish_phrases
    my_corpus = DisambiguationCorpus('disambigation_dataset.txt')

    # load given corpus
    corpus = DisambiguationCorpus("penntreebank.txt")
    my_algo = MyDisambiguation()
    my_algo_combined = My_algo_combined()

    my_algo.train(corpus)
    my_algo_combined.train(corpus)



    correctParse = 0
    correctRoot = 0

    # test solo performance of myAlgorithm.py on penntreebank.txt

    for i in range(corpus.sentenceCount()):

        sentenceAnalyses = fsm.robustMorphologicalAnalysis(corpus.getSentence(i))

        fsmParses = my_algo.disambiguate(sentenceAnalyses)


        for j in range(corpus.getSentence(i).wordCount()):
            word = corpus.getSentence(i).getWord(j)

            if isinstance(word, DisambiguatedWord):
                if fsmParses[j].transitionList() == word.getParse().__str__():
                    correctParse = correctParse + 1
                if fsmParses[j].getWord() == word.getParse().getWord():
                    correctRoot = correctRoot + 1





    print('Performance of myAlgorithm.py correct Root from penntreebank.txt:\n' + str((correctRoot + 0.0) / corpus.numberOfWords()))
    print('Performance of myAlgorithm.py correct Parse from penntreebank.txt:\n' + str((correctParse + 0.0) / corpus.numberOfWords()))
    print()


    correctParse = 0
    correctRoot = 0


    # test performance of my_algo_combined.py on penntreebank.txt

    for i in range(corpus.sentenceCount()):

        sentenceAnalyses = fsm.robustMorphologicalAnalysis(corpus.getSentence(i))

        fsmParses = my_algo_combined.disambiguate(sentenceAnalyses)


        for j in range(corpus.getSentence(i).wordCount()):
            word = corpus.getSentence(i).getWord(j)

            if isinstance(word, DisambiguatedWord):
                if fsmParses[j].transitionList() == word.getParse().__str__():
                    correctParse = correctParse + 1
                if fsmParses[j].getWord() == word.getParse().getWord():
                    correctRoot = correctRoot + 1

    print('Performance of my_algo_combined.py correct Root from penntreebank.txt:\n ' + str((correctRoot + 0.0) / corpus.numberOfWords()))
    print('Performance of my_algo_combined.py correct Parse from penntreebank.txt:\n ' + str((correctParse + 0.0) / corpus.numberOfWords()))
    print()

    correctParse = 0
    correctRoot = 0

    my_algo = MyDisambiguation()
    my_algo_combined = My_algo_combined()

    my_algo.train(my_corpus)
    my_algo_combined.train(my_corpus)


    # test solo performance of myAlgorithm.py on disambigation_dataset.txt

    for i in range(my_corpus.sentenceCount()):

        sentenceAnalyses = fsm.robustMorphologicalAnalysis(my_corpus.getSentence(i))

        fsmParses = my_algo.disambiguate(sentenceAnalyses)


        for j in range(my_corpus.getSentence(i).wordCount()):
            word = my_corpus.getSentence(i).getWord(j)

            if isinstance(word, DisambiguatedWord):
                if fsmParses[j].transitionList() == word.getParse().__str__():
                    correctParse = correctParse + 1
                if fsmParses[j].getWord() == word.getParse().getWord():
                    correctRoot = correctRoot + 1





    print('Performance of myAlgorithm.py correct Root from disambigation_dataset.txt:\n' + str((correctRoot + 0.0) / my_corpus.numberOfWords()))
    print('Performance of myAlgorithm.py correct Parse from disambigation_dataset.txt:\n' + str((correctParse + 0.0) / my_corpus.numberOfWords()))
    print()

    # test performance of my_algo_combined.py on disambigation_dataset.txt

    correctParse = 0
    correctRoot = 0

    for i in range(my_corpus.sentenceCount()):

        sentenceAnalyses = fsm.robustMorphologicalAnalysis(my_corpus.getSentence(i))

        fsmParses = my_algo_combined.disambiguate(sentenceAnalyses)

        for j in range(my_corpus.getSentence(i).wordCount()):
            word = my_corpus.getSentence(i).getWord(j)

            if isinstance(word, DisambiguatedWord):
                if fsmParses[j].transitionList() == word.getParse().__str__():
                    correctParse = correctParse + 1
                if fsmParses[j].getWord() == word.getParse().getWord():
                    correctRoot = correctRoot + 1

    print('Performance of my_algo_combined.py correct Root from disambigation_dataset.txt:\n ' + str(
        (correctRoot + 0.0) / my_corpus.numberOfWords()))
    print('Performance of my_algo_combined.py correct Parse from disambigation_dataset.txt:\n ' + str(
        (correctParse + 0.0) / my_corpus.numberOfWords()))
    print()




# method to write Turkish-phrase as text file
def loader():

    folderpath = r"Turkish-Phrase"
    filepaths = [os.path.join(folderpath, name) for name in os.listdir(folderpath)]

    str_ = '<DOC>\t<DOC>+BDTAG\n'

    for path in filepaths:

        with open(path, 'r', encoding='utf-8') as f:

            file = f.readlines()
            if '{' not in file[0]:
                pass
            else:

                str_ += '<S>\t<S>+BSTAG\n'
                line = file[0]
                line_split = line.split()
                for split in line_split:
                    split_2 = split[1:-1].split("}{")
                    for split_3 in split_2:
                        split_4 = split_3.split('=')
                        if split_4[0] == 'turkish':
                            full_word = str(split_4[1])
                        elif split_4[0] == 'morphologicalAnalysis':
                            morphologicalAnalysis = str(split_4[1])
                        else:
                            pass
                    str_ += full_word + '\t' + morphologicalAnalysis + '\n'
                str_ += '</S>\t</S>+ESTAG\n'

    str_ += '</DOC>\t</DOC>+EDTAG\n'

    with open("disambigation_dataset.txt", "w", encoding='utf8') as text_file:
        text_file.write(str_)


if __name__ == '__main__':
    main()
