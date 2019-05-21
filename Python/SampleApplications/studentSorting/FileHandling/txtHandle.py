
'''

	r,r+,w,w+,a,a+

'''

# ****** CREATING A FILE  ******

f = "textFile.txt"

# file = open(f,"w")

# file.write("Line from python program,\n")
# file.write("Another Line from python program")

# # More lines
# lines = ["from list line 1","from list line 2"]
# file.writelines(lines)

# file.close()

# **** TO APPEND TO A FILE ****

file = open(f,"a")
file.write("appended line")
file.close()



#  ****** READING A FILE ****** 

file = open(f,"r")

# print file.read() # read entire text file
# print file.read(5) # read only first 5 characters of text file
# print file.readline() # read the lines of the text file
# print file.readline(2) # read the 2 line of the text file
# print file.readlines() # It returns all the lines in the text as comma seperated in the list

#  ****** LOOPING OVER FILE OBJECT *****

for line in file:
	print line

# ****** USING WITH STATEMENT *****
# using with method files will be automatically closed when we are done using it.




with open(f,"r") as file:
	for line in file:
		print line	
	# ---- or ----
	data = file.read()
	print data
	 




