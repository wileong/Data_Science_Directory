
#hint:

#yield(industry,gender)(1,1)
#yield(industry,gender)(0,1)

#hint 2: 

#don't keep track of col names because rows will be split amongst different machines, theoretically

#hint 3:

#num_funded = 0
# num_total = 0
#values =[(1,1),(0,1),(0,1),(1,1),(0,1)]

# for x,y in values (over a generator):
#     num_funded += x
#     num_total += y

#yield key, (num_funded,num_total)

#hint 4:

#industry = ...
#gender = ...
#yield industry + gender
    

from mrjob.job import MRJob
import csv

class CompanyCount(MRJob):

    def mapper(self, _, line):

        col = list(csv.reader([line])) #return a list with one list...
        #print(col)
        #col = line.split(',')
        # take a line of entries and split by comma and return a list
        industry = col[0][4]
        gender = col[0][5]
        deal = col[0][3]
        yield (industry, gender),(deal == 'Yes', 1)
                
            

    def reducer(self, key, values):
        
        num_funded = 0
        num_total = 0
        
        for x,y in values:
            
            num_funded += x
            num_total += y
        
        
        yield key, (num_funded,num_total)
        

if __name__ == '__main__':
    CompanyCount.run()