#jupyter magic
#writes to filename specified
#wrote code below to file.py
# see new file!

#use pass to do nothing

from mrjob.job import MRJob

# get the length of the longest word in a document
class MaxLength(MRJob):

    def mapper(self, _, line): # FOCUS ON
        #underscore means we will not be using this arg at all
        #go line by line in text
        
        words = line.split()
        
#         for word in words:
#             yield None, len(word) #we're not looking for key!
#             #YIELD EVERY WORD in line

        lengths = [len(w) for w in words] #
        
        if len(lengths) > 0:
            yield None,max(lengths)
        
        
        #yield creates a 'generator', we're making generators to not store stuff in memory

    def reducer(self, key, values ): #finds max of max of each line
        
        #Every key would be called none
        yield None, max(values)


if __name__ == '__main__':
    MaxLength.run()