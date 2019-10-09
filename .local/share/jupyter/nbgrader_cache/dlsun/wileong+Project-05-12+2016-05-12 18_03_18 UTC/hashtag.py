
from mrjob.job import MRJob

class HashtagCount(MRJob):
  
    
    def mapper(self, _, line):
        
        fields_byspace = line.split(" ")
        
        
        for word in fields_byspace:
            
            if (len(word) > 0) and (word[0] == '#'):
                
                for i in range(1,len(word[1:])):
                    
                    if not word[i].isalnum() or word[i:i + 4] == "http":
                        
                        yield word[:i], 1
                
    
    def reducer(self, key, values):
        
    
        yield key, sum(values)

if __name__ == '__main__':
    HashtagCount.run()