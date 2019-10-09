
from mrjob.job import MRJob

class BabiesCount(MRJob):

    def mapper(self, _, line):
        
        col_info4 = line.split(',')
        
        
        names_first_letter = col_info4[0][0]
        
        yield names_first_letter, int(col_info4[2])
        
        

    def reducer(self, key, values):
        
        yield key, sum(values)
        
        

if __name__ == '__main__':
    BabiesCount.run()