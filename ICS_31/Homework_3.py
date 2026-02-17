# Keesey, Ruby
from collections import namedtuple

Student = namedtuple('Student', ['FName', 'LName', 'GPA', 'Units'])

def Student_Manager():
    """ Initializes student roster and processes user 
        inputs to be passed to command functions """
    
    StudentRoster = []
    while True:
        inpt = [x for x in input("\n$ ").split(' ')]
        inpt = [x.replace(",", "") for x in inpt] 
        command = inpt[0]
        if command == "AddStudent":
            AddStudent(inpt, StudentRoster)
        if command == "DeleteStudent":
            DeleteStudent(inpt, StudentRoster)
        if command == "PrintRoster":
            PrintRoster(StudentRoster)
        if command == "SortRoster":
            SortRoster(inpt, StudentRoster)
        if command == "FindByFName":
            FindByFName(inpt, StudentRoster)
        if command == "FindByLName":
            FindByLName(inpt, StudentRoster)
        if command == "GetAverage":
            GetAverage(inpt, StudentRoster)             
        if command == "Quit":
            break

def AddStudent(inpt, StudentRoster):
    """ accepts user inputs and updates student roster by appending 
        new information to the initialized list """
    
    f_name = inpt[1]
    l_name = inpt[2]
    gpa = inpt[3]
    units = inpt[4]
    rec  = Student(FName=f_name, LName=l_name, GPA=gpa, Units=units)
    StudentRoster.append(rec)

def DeleteStudent(inpt, StudentRoster):
    """ accepts user inputs and updates student roster by removing 
        specified information from the initialized list """
    
    if len(StudentRoster) == 0:
        print("\nError! No student with that name was found in the roster.")
    else: 
        included_fnames = []
        included_lnames = []
        for i in range(len(StudentRoster)):
            included_fnames.append(StudentRoster[i].FName)
            included_lnames.append(StudentRoster[i].LName)
            if inpt[1] == StudentRoster[i].FName and inpt[2] == StudentRoster[i].LName:
                StudentRoster.pop(i)
                break
        if inpt[1] not in included_fnames or inpt[2] not in included_lnames:
            print("\nError! No student with that name was found in the roster.")

def PrintRoster(StudentRoster):
    """ accepts user inputs and prints student roster from the 
        initialized list in a specified format in the order 
        that the entries appear """
    
    for i in range(len(StudentRoster)):
        Student = StudentRoster[i]
        f_name = Student.FName
        l_name = Student.LName
        gpa = Student.GPA
        units = Student.Units
        print(f"\n{f_name}, {l_name}, {gpa}, {units}")

def SortRoster(inpt, StudentRoster):
    """ accepts user inputs and prints student roster from the 
        initialized list in a specified format in the order 
        that the command indicates """
    
    sort_by = inpt[1]
    name_list = []
    gpa_list = []
    units_list = []
    og_name_order = []
    for i in range(len(StudentRoster)):
        Student = StudentRoster[i]
        name_list.append(Student.FName)
        og_name_order.append(Student.FName)
        gpa_list.append(Student.GPA)
        units_list.append(Student.Units)
    if sort_by == "Name":
        name_list.sort()
        names = {}
        for i, name in enumerate(name_list):
            if name not in names:
                names[f"{name}"] = [i]
            else:
                names[f"{name}"].append(i)
        for key, idx in names.items():
            if len(idx) > 1:
                l_names = []
                for i in range(len(og_name_order)):
                    name = og_name_order[i]
                    if name == key:
                        Student = StudentRoster[i]
                        l_names.append(Student.LName)
                    l_names.sort()
                for j in range(len(idx)):
                    f_name_idx = idx[j]
                    name_list[f_name_idx] = l_names[j] 
        for name in name_list:
            for i in range(len(StudentRoster)):
                Student = StudentRoster[i]
                f_name = Student.FName
                l_name = Student.LName
                if f_name == name or l_name == name:
                    gpa = Student.GPA
                    units = Student.Units
                    print(f"\n{f_name}, {l_name}, {gpa}, {units}")
    if sort_by == "GPA":
        gpa_list.sort(reverse=True)
        for gpa in gpa_list:
            for i in range(len(StudentRoster)):
                Student = StudentRoster[i]
                gpa_val = Student.GPA
                if gpa == gpa_val:
                    f_name = Student.FName
                    l_name = Student.LName
                    units = Student.Units
                    print(f"\n{f_name}, {l_name}, {gpa}, {units}")
    if sort_by == "Units":
        units_list.sort(reverse=True)
        for units in units_list:
            for i in range(len(StudentRoster)):
                Student = StudentRoster[i]
                unit_val = Student.Units
                if units == unit_val:
                    f_name = Student.FName
                    l_name = Student.LName
                    gpa = Student.GPA
                    print(f"\n{f_name}, {l_name}, {gpa}, {units}")

def FindByFName(inpt, StudentRoster):
    """ accepts user inputs and prints the all student information
        matching the first name specified in the command """
    
    name = inpt[1]
    for i in range(len(StudentRoster)):
        Student = StudentRoster[i]
        f_name = Student.FName
        if name == f_name:
            gpa = Student.GPA
            l_name = Student.LName
            units = Student.Units
            print(f"\n{f_name}, {l_name}, {gpa}, {units}")

def FindByLName(inpt, StudentRoster):
    """ accepts user inputs and prints the all student information
        matching the last name specified in the command """
    
    name = inpt[1]
    for i in range(len(StudentRoster)):
        Student = StudentRoster[i]
        l_name = Student.LName
        if name == l_name:
            gpa = Student.GPA
            f_name = Student.FName
            units = Student.Units
            print(f"\n{f_name}, {l_name}, {gpa}, {units}")

def GetAverage(inpt, StudentRoster):
    """ accepts user inputs and calculates the 
        average specified in the command """
    
    calc_by = inpt[1]
    student_count = 0
    unit_count = 0
    sum = 0
    for i in range(len(StudentRoster)):
        Student = StudentRoster[i]
        gpa = float(Student.GPA)
        units = int(Student.Units)
        weighted = gpa * units
        student_count += 1
        unit_count += units
        sum += weighted
    if calc_by == "GPA":
        avg_gpa = sum / (unit_count)
        print(f"\n{avg_gpa:.4f}")
    if calc_by == "Units":
        avg_units = unit_count / student_count
        print(f"\n{avg_units:.0f}") 

if __name__=="__main__":
    Student_Manager()      