#jupyter magic
#wrote code below to file.py
# see new file!

from mrjob.job import MRJob


class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line): # FOCUS ON
        #underscore means we will not be using this arg at all
        #go line by line in text
        yield "chars", len(line)
        yield "words", len(line.split()) #take a line and split by whitespace
        yield "lines", 1
        #yield creates a 'generator', we're making generators to not store stuff in memory

    def reducer(self, key, values ): #FOCUS ON 
        yield key, sum(values)
                #values is a list of number of words


if __name__ == '__main__':
    MRWordFrequencyCount.run()