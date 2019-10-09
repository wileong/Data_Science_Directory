
from mrjob.job import MRJob

class RatingsCount(MRJob):

    def mapper(self, _, line):
        # YOUR CODE HERE
        cols_3 = line.split('::')
        movie_id = cols_3[1]
        #rating = cols_3[2]
        
       
        
        #yield (movie_id), cols_3.count(cols_3[2]) # This line most works except if I get a case like:
        #[userid = 3, .. ,... ... , rating = 3, ....... ]. .count() would get number of instances of that rating
        
        yield (movie_id), 1 #yield 1 because each row yields just ONE RATING.

    def reducer(self, key, values):
        # YOUR CODE HERE
        num_ratings = 0
        
        for x in values:
            
            num_ratings+=x
            
        yield key, num_ratings

if __name__ == '__main__':
    RatingsCount.run()