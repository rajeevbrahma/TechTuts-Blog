'''
	Python version 2.7

'''
# Student Data Structure

	

students = {}
def genderSort():
	genderlist = [[],[]]
	genderDict = {"Male":[],"Female":[]}

	for data in students.values():
		if(data["Gender"] == "M"):
			genderlist[0].append(data)
		elif(data["Gender"] == "F"):
			genderlist[1].append(data)
		else:
			print "invalid"	

	genderDict["Male"]	= genderlist[0]

	genderDict.update({"Male":genderlist[0]})


def addStudent():
	print "***** WELCOME TO STUDENT ENROLLING PROCESS ******\
	PLEASE PROVIDE THE FOLLOWING DATA TO ENROLL."

	name = raw_input("NAME - ")
	branch = raw_input("BRANCH - ")
	college = raw_input("COLLEGE - ")
	gender = raw_input("GENDER - ")

	if len(students) > 0:
		students.update({
			list(students.keys())[-1]+1:{
					"Name":name,
					"Branch":branch,
					"College":college,
					"Gender":gender
				}
			})
	else:
		# FIRST ENTRY IN THE DICTIONARY
		students.update({
			1:{
					"Name":name,
					"Branch":branch,
					"College":college,
					"Gender":gender
				}
			})
			
	print students


def update():
	rollno = int(raw_input("ROLL NUMBER HERE - "))
	feature = int(raw_input("2.Name 3.Branch 1.College 0.Gender - "))
	value = raw_input("Value here - ")

	feature = students[rollno].keys()[feature]

	students[rollno].update({feature:value})

	print students
 

if __name__ == '__main__':

	# Execution starts from here.
	while True:
		choice = int(raw_input("1.Enroll 2.Update 3.genderSort"))
		
		if (choice == 1):
			addStudent()
		elif(choice == 2):
			update()
		elif(choice == 3):
			genderSort()	
		
	














