import random

announcedNumbers = []

def randNumGen(start,end):
	while(len(announcedNumbers) <= 90):
		num = random.randint(start,end)
		if num not in announcedNumbers:
			raw_input("PRESS TO CONTINUE....")		
			print ("ANNOUNCED NUMBER is \t %d"%(num))
			announcedNumbers.append(num)
			
begin = 1
stop = 90
randNumGen(begin,stop)
