#jupyter magic
#writes to filename specified
#wrote code below to file.py
# see new file!

#use pass to do nothing

from mrjob.job import MRJob

#count number of occurrences of ea distinct character in the text
class CharacterCount(MRJob):

    def mapper(self, _, line): # FOCUS ON
        #underscore means we will not be using this arg at all
        #go line by line in text
        for char in line:
            if char.isalnum():
                yield char.lower(), 1 #lowercase only
        
        #yield creates a 'generator', we're making generators to not store stuff in memory

    def reducer(self, key, values ):
        #what shoudl u do to vals to get total of letters?
        #what should we do with all those "1"'s for count of char...
        yield key, sum(values)


if __name__ == '__main__':
    CharacterCount.run()