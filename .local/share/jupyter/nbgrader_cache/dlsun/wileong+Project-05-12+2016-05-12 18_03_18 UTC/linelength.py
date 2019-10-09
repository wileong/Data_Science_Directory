
from mrjob.job import MRJob

class LineLength(MRJob):
    
    def mapper(self, _, line):
        
        
        if '@' in line:
            #print(len(line.split(' ')))
            
            yield '@', len(line.split(" "))
            
        else:
           
            yield 'not @',  len(line.split(" "))
       
    
    def reducer(self, key, values):
        
        
        total = 0
        length = 0
        for i in values:
            total += i
            length += 1
        yield key, total / length
        

if __name__ == '__main__':
    LineLength.run()