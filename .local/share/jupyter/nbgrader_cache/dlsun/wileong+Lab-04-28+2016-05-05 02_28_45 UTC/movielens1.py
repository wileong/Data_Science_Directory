
from mrjob.job import MRJob

class MovieCount(MRJob):

    def mapper(self, _, line):
        
        
        col_info2 = line.split('::') #returns a list of of strings that rep indices?, movie title and genre combos
        #print(col_info2)
        
        for str in col_info2:
            
            col_info2 = str.split('|') #returns a list of genres, seperated
            
            
            
        for genre in col_info2:
            
            yield(genre, 1)

    def reducer(self, key, values):
        
        num_movies = 0
        
        for x in values:
            
            num_movies+=x
            
        yield key, num_movies
           
        

if __name__ == '__main__':
    MovieCount.run()