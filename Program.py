import itertools     # It is a library for performing permutations on a given iterable
import copy          # This library is used for making a deep copy of a list in the program
leftovers = {}       # This list is used for tagging the unused elements when moving to sucessive elements
isunique = False     # This variable is used for determining if all the implicants are unique or not ,
                     # thereby aiding us in finding the final table
def converttobinary(a,n):  # This function is used to convert the given number to binary. It returns
                           # a list of ones and zeroes.
    retlist=[]             # This is the list to be returned
    while(a>0):      # This loop is used to find the binary equivalents by sucessive division by 2
        retlist+=[a%2]
        a = int(a/2)
    for i in range(n-len(retlist)):#This loop is used to fill the extra cells with zeroes.
        retlist+=[0]
    retlist.reverse()
    return retlist
def checknumberofones(list): # This function returns the number of 1s and -1s from the given list.
    c = 0                    # Counter variable for 1s and -1s.
    for i in list:
        if i==1 or i==-1:
            c+=1
    return c
def givenexttable(table,n):
   table2 = {}         # This is the table to be returned .
   arr={}              # This is used for marking up the unused implicants which are appended to leftovers later.
   count =0            # This is a counter for checking inequalities in the lists.
   global isunique
   for i in table.keys(): # All values of arr are set to zero initially.
       arr[i] = 0

   for i,j in itertools.combinations(table.keys(),2): # All unique combinations of implicants are
        count = 0                                     # referenced for comparison.

        if abs(checknumberofones(table[i])-checknumberofones(table[j]))==1 :
# The difference number of 1s and -1s are checked . If difference  is 1 , they are compared.
               for l in range(n):
                   if not table[i][l] == table[j][l] :
                       count+=1
# The number of inequalities in the table is checked . If not one , The comparison is not done
               if count==1:

                   for l in range(n): # The unequal numbers are changed to -1 and the required keys
                                      # and values are put in table2
                      if not table[i][l] == table[j][l]:
                          temp = copy.copy(table[i])# This is to make a true copy of the list 'table[i]'
                          temp[l]=-1
                          table2[i+j] = copy.copy(temp)
                          arr[i]+=1   # The values of arr corresponding to i and j are incremented.
                          arr[j]+=1


   if not table2 == {}: # This is a check for non comparison , i.e. to check if this is the final table.
       isunique = False
   if isunique == True:
       return table

   for i in arr.keys(): # The keys having zero value of  arr are added to leftovers .
       if arr[i] == 0:  # Since they are not referenced at all.
           global leftovers
           leftovers[i] = table[i]

   table2 = removeredundancy(table2) # Redundancy removed .
   return table2
def removeredundancy(diction): # This function is used to remove redundant implicants from the
                               # table i.e. the implicants having the same binary lists.
                               # This loop checks for redundancy by using diction2 as a container.
                               # The next implicant's binary lists are checked
                               # with all the lists in diction2 . If found duplicate , it is not added.
   diction2 = {}        # The table in the form of a dictionary to be returned .
   for i in diction.keys():
       if diction[i] not in diction2.values():
           diction2[i]=diction[i]
   return diction2
def giveanswer(bin): # This function gives us the alphabetical equivalents of the given list.
    str = ""         #This is the string to be returned.
    letter = 97      # This is ascii value of 'a', the first letter.
    for i in bin:
        if i == 1 :
            str = str + chr(letter) # 'letter' is getting typecasted to Character and appended to the.
        elif i == 0 :               # return string.
            str = str + chr(letter) + "'"
        letter+=1                   # The value of 'letter' is incremented at each iteration
    return str                      # to give the next letter in the series.
def main():
    global isunique            # Comparison variable.
    orilist = []               # The original list containing all the minterms.
    table = {}                 # This is the initial table which is , as of yet , uninitialised
    primeimplicant = {}        # This is a counter dictionary for prime implicants.
    finalanswer = set()        # This would contain the final answer of the problem.
    epi = []                   # This list would contain all the essential prime implicants
    covered_elements = []      # This list would contain covered minterms
    uncovered_elements = set() # This list would contain uncovered minterms
    pi = []                    # This contains all the nonessential prime implicants.
    answerstring = ""          # This is the final answer string.
    n = int(input("Enter the number of variables:  ")) # n is number of variables.
    orilist1 = input("Enter the minterm numbers separated by a space. Press Enter when done::  ").split()
    dont_care = input("Enter the don't care terms as described above. Press Enter if no terms ").split()
    # All the minterms and dont care terms are taken as input.
    orilist = orilist1 + dont_care # A final list is created by joining orilist and dont care
    for i in orilist:              # All elements in primeimplicant are set to zero initially.
        primeimplicant[i] = 0
    for i in orilist:              # Initial table is initialized.
        table[i+"."] = converttobinary(int(i),n) # The '.' is added for separation.

    while isunique == False:   # The tables are analysed repeatedly till all the elements are unique.
        isunique = True
        table = givenexttable(table,n)

    table.update(leftovers)   # This table is appended to the leftovers ie the uncovered minterms.

    table = removeredundancy(table)
                              # Redundancy is removed to create the final table.


    for j in orilist:
        for i in table.keys():

            if j in i.split("."):
               primeimplicant[j]= primeimplicant[j] + 1
    # The above loop is for incrementation of elements in the primeimplicant[] list.
    # When element "j" is spotted in any key of the table , primeimplicant[j] is incremented.
    # Thus it serves as a counter so as to find the number of occurences(Remember the "stars" in
    # the quine mcclusky method ?) .
    for i in orilist1:
            for j in table.keys():

                if primeimplicant[i]== 1 :
                     if i in j.split(".") :
                         finalanswer.add(giveanswer(table[j]))
                         epi+=[j]
                         covered_elements += j.split(".")
    # All the essential prime implicants (Which occur only once) are put in "epi" list.
    # The elements which are referenced thorugh this process are put in covered elements list
    # In the above loop , all the minterms "i" whose primeimplicant[i] is one, their corresponding
    # binary lists are added to the "finalanswer" set

    epi = list(set(epi))
    # This is used to remove duplicate elements from a list.
    covered_elements = list(set(covered_elements))
    # This is similar to the above

    for i in epi:
         table.pop(i)
    # The essential prime implicants are removed from table to form the reduced pi table.
    for i in orilist1:
        if i not in covered_elements:
            uncovered_elements.add(i)
    # The elements not in covered elements are put in uncovered elements set.
    reduced_pi_numbers = list(uncovered_elements)
    # The set is converted to a list and stored as reduced pi numbers.


    for groupcount in range(1,len(table.keys())+1):# This is number of elements in the combinations at a time
        for i in itertools.combinations(table.keys() , groupcount):
            k = ''.join(i)# The keys are converted to a string.
            for num in reduced_pi_numbers:
                if num not in k.split("."): # Checking if numbers are present or not
                    pi = [] # If number is not present , pi is left empty.
                    break
                pi = list(i)# The tuple "i" is converted to a list
            if not pi == []:
                break
        if not pi == []:
            break
    # The above part (Line 152 - Line 163) is used to remove redundancy . This needs some explanation.
    # In the loop above , we take up unique combinations of keys in the table .
    # The number of keys in each combination is incremented each time .
    # WE check if the combination includes all the uncovered keys or not .
    # If it does , the corresponding binary lists are added to finalanswer set and the loop is broken.
    # At the end of the loop , all the nonessential but required prime implicants are contained in pi[]
    for i in pi:
        finalanswer.add(giveanswer(table[i]))
    # Elements of pi are added to finalanswer set.

    for i in finalanswer:
        answerstring = answerstring + i + " + "# The final answer string is created.
    answerstring = answerstring[:-3] # The last " + " is discarded.
    print(answerstring) # The answer string is printed.
    print("\n\n Press any key to exit")
    input()
main()                  # main() is called to initiate the program.
