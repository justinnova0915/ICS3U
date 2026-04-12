#IntroLoops.py

#Ex1
##x=0
##while x<5:
##    print(x)
##    x+1


#Ex2a
##name=""
##while name!="end":
##    name=input("Enter a name: <end to exit> ")
##    if name!="end":
##        print("Hello",name)

#Ex2b
##while True:
##    name=input("Enter a name: <end to exit> ")
##    if name=="end":
##        break #exits the loop immediately
##    print("Hello",name)


#Ex3 Enter marks until -1 is entered and display
#the average of all marks (2 decimals)
##count=0 #to count the number of marks entered
##total=0 #to calculate the sum of all marks
##
##while True:
##    mark=int(input("Enter a mark <-1 to stop>: "))
##    if mark==-1:
##        break
##    elif 0<=mark<=100:
##        count+=1
##        total+=mark
##    else:
##        print("error")
##
##print(f"You entered {count} marks")
##print(f"The total is {total}")
##avg=total/count
##print(f"The average is {avg:.2f}")

'''
TWO IMPORTANT CONCEPTS:
1. Counter
 - A counter is an INTEGER variable that we use to keep
 track of the number of times certain event has happened.
 The most common thing to count is the number
 of times "we went around the loop"

To use a counter follow these steps:
- give initial value BEFORE THE LOOP  (e.g. count=0)
- each time "an event happens", increas the
 counter by 1  (count+=1      or   count=count+1)
- typically we use this counter in calculations
 or we use it to exit the loop


2. Accumulator is similar to a counter. Instead
 of increasing the value by 1, we can increase it
 by any number

    (total+=num    or  total=total+num)



'''

#Ex4a
#Find the sum of all squares from 1 to 100

##total=0
##count=1
##
##while count<=100:
##    total=total+count**2
##    count+=1
##    
##print("the sum is",total)



####Counted loop    (FOR LOOP)

#            start stop  step
for i in range(4,   16,  2):
    print(i)

#Ex4b
#Use the for loop to ind the sum of all squares
#from 1 to 100
##tot=0
##for i in range(1,101):
##    tot=tot+i**2
##    
##print("total=",tot)

#Ex 5
#Exponential growth and decay
#If you invest $10 000 and 10% interest for 40 years

    
##money=10000
##for year in range(1,41):
##    money=money*1.10 #10% growth
##print(year,round(money,2))


#Ex6
#Using loops with strings
#Simple program that adds dots after each letter
#kate ---> k.a.t.e.

name=input("Enter a word: ")
newWord=""
for let in name:
    newWord=newWord+let+"."
print(newWord)

'''
This example points out 2 important things:
 1. Strings accumulate differently. Rather than
 starting from 0, they start from an empty string.
 When we add on letters they simply make
 the string LONGER
 2. The for loop allows us to have the
 "loop control variable" BECOME each letter
 of the string

'''






    
















    
















    









    


















    










    
