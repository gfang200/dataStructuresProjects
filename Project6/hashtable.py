
#Hash Functions
def Hash1(k, n):
    return k % n

def Hash2(k, n):
    phi = 1.61803398875
    return int(n*(k*(phi - 1)-int(k*(phi -1)))) + 1
    
def Permute(k, i, n):
    prehash = hash(k)
    return (Hash1(prehash, n) + i*Hash2(prehash, n)) % n




class Hashtable:
    def __init__(self, dict):
        self.TableSize = max(2*len(dict), 2)
        self.Load = len(dict)
        self.Table = [None for i in range(self.TableSize)]
        #hash the table for each key in the dictionary
        for k in dict:
            i=0
            index = Permute(k, i, self.TableSize)
            while self.Table[index] != None:
                i += 1
                index = Permute(k, i, self.TableSize)
                
            self.Table[index] = (k, dict[k])
            
                

    def __getitem__(self, key):
        i = 0
        index = Permute(key, i, self.TableSize)

        #look through the table through the hash permutation until the key is found or an empty block is found
        while self.Table[index] != None and self.Table[index][0] != key:
            i += 1
            index = Permute(key, i, self.TableSize)

        #if the entry is empty, we haven't been here before and the key isn't in the table
        if self.Table[index] == None:
            print "Key not found. Cannot Get"
            return
        else:
            return self.Table[index][1]
        
        
    def __setitem__(self, k, value):
        #If the Load Factor is less then one, no need to Table Double
        if (float(self.Load) / self.TableSize) < .5:
            #look for the first open slot to put the key
            i=0
            index = Permute(k, i, self.TableSize)
            deleted_index = None
            while self.Table[index] != None and self.Table[index][0] != k:
                #If I reach a deleted node, hold my finger on it in case I need to return
                if self.Table[index] == "DELETED":
                    deleted_index = index
                i += 1
                index = Permute(k, i, self.TableSize)


            #if key not found and finger held on deleted node, replace deleted
            if self.Table[index] == None:
                if deleted_index:
                    index = deleted_index
                self.Load += 1

            
            self.Table[index] = (k, value)
            
        else:
            #if the Table is full, double the table
            newTable = [None for i in range(2*self.TableSize)]
            #move all the keys to the new table
            for pair in self.Table:
                #If there is actually something there, add it to the new table
                if pair:
                    key = pair[0]
                    i=0
                    index = Permute(key, i, 2*self.TableSize)
                    while newTable[index] != None:
                        i += 1
                        index = Permute(key, i, 2*self.TableSize)
                    
                    newTable[index] = pair
    
            #redirect pointer to new table
            self.Table = newTable
            self.TableSize = 2*self.TableSize
    
            #add new element
            self.__setitem__(k, value)
            
            
                


    def __delitem__(self, key):
        i = 0
        index = Permute(key, i, self.TableSize)
        while self.Table[index] != None and self.Table[index][0] != key:
            i += 1
            index = Permute(key, i, self.TableSize)

        #if the key isn't there, print error msg
        if self.Table[index] == None:
            print "Key not found. Cannot Delete"
            return
        
        self.Table[index] = "DELETED"
        self.Load -= 1        
        
        if float(self.Load) / self.TableSize < .25:
            
            newTable = [None for i in range(.5*self.TableSize)]
            #move all keys to new table
            for pair in self.Table:
                key = pair[0]
                i=0
                index = Permute(key, i, .5*self.TableSize)
                while self.Table[index] != None:
                    i += 1
                    index = Permute(key, i, .5*self.TableSize)
                
                newTable[index] = pair

            #redirect pointer
            self.Table = newTable
            self.TableSize = .5*self.TableSize



    def keys(self):
        ls = list()
        for pair in self.Table:
            ls.append(pair[0])

        return ls


