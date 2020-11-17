'''
Tyler Marchiano
HW09
SSW 810

This file contains the framework for data repository system and summarizes the student and instructor data. 
'''
from typing import Dict, List, Iterator, Tuple, DefaultDict
from os import path
from HW8_TylerMarchiano import file_reader
from collections import defaultdict
from prettytable import PrettyTable

class Student:
    def __init__(self, cwid: str, name: str, major: str) -> None:
        '''Stores information about a single student'''
        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self.courses: Dict[str, str] = dict() #Key is course and value is the grade
    
    def add_course(self, course: str, grade: str) -> None:
        '''add the course to the dictionary with a value of grade'''
        self.courses[course] = grade

class Instructor:
    def __init__(self, cwid: str, name: str, department: str) -> None:
        '''Stores information about a single Instructor'''
        self.cwid: str = cwid
        self.name: str = name
        self.department: str = department
        self.courses: DefaultDict[str, str] = defaultdict(int) #Key is course and value is number of students in each course
    
    def add_course(self, course: str) -> None:
        '''adds the course to the professors courses dictionary
        increments the value by 1 to count the student taking the course'''
        
        #add the course to the dictionary if it doesn't exist already and increment the count by one
        self.courses[course] += 1

class University:
    '''Holds all of the data for a specific University'''
    students: Dict[str, Student] = dict() #key is cwid and the value is the student. This will make it easier to find students later
    instructors: Dict[str, Instructor] = dict() #key is cwid and the value is the Instructor. This will make it easier to find instructors later
    
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.read_students()
        self.read_instructors()
        self.read_grades()
        self.student_prettytable()
        self.instructor_prettytable()
    
    def read_students(self) -> None:
        '''read the students.txt file, creating a new Student for each line in the file'''
        file_path: str = path.join(self.path, 'students.txt')
        try:
            students_file: List[str] = list(file_reader(file_path, 3, sep='\t'))
        except:
            raise FileNotFoundError(f"Can't find students.txt in the given directory")
        
        for cwid, name, major in students_file:
            self.students[cwid] = Student(cwid, name, major)
    
    def read_instructors(self) -> None:
        '''read the instructors.txt file, creating a new Student for each line in the file'''
        file_path: str = path.join(self.path, 'instructors.txt')
        try:
            instructors_file: List[str] = list(file_reader(file_path, 3, sep='\t'))
        except:
            raise FileNotFoundError(f"Can't find instructors.txt in the given directory")
        
        for cwid, name, department in instructors_file:
            self.instructors[cwid] = Instructor(cwid, name, department)
    
    def read_grades(self) -> None:
        '''reads the grades.txt file and processes all of that information. 
        assigns students courses and grades. Assigns professors courses '''
        file_path: str = path.join(self.path, 'grades.txt')
        try:
            grades_file: List[str] = list(file_reader(file_path, 4, sep='\t'))
        except:
            raise FileNotFoundError(f"Can't find grades.txt in the given directory")
        
        for s_cwid, course, grade, p_cwid in grades_file:
            #add the course and grade for the student
            self.students[s_cwid].add_course(course, grade)
            
            #add the course to the professor if it doesn't exist already and increment the count of the students
            self.instructors[p_cwid].add_course(course)
    
    def student_prettytable(self) -> None:
        '''print the student pretty table'''
        pt: PrettyTable = PrettyTable(field_names=["CWID", "Name", "Completed Courses"])
        for student in self.students.values():
            pt.add_row([student.cwid, student.name, sorted(list(student.courses.keys()))])
        print("Student Summary: ")
        print(pt)
    
    def instructor_prettytable(self) -> None:
        '''print the instructor pretty table'''
        pt: PrettyTable = PrettyTable(field_names=["CWID", "Name", "Dept", "Course", "Students"])
        for instructor in self.instructors.values():
            for course in instructor.courses:
                pt.add_row([instructor.cwid, instructor.name, instructor.department, course, instructor.courses[course]])
        print("Instructor Summary: ")
        print(pt)
        
            
            
def main() -> None:
    '''run the program'''
    
    runAgain: bool = True
    
    while runAgain:
        #Error handling for an invalid input path is handled in HW8_TylerMarchiano.py as well as in the classes above
        directory: str = input("Please enter the directory that contains the students.txt, instructors.txt and grades.txt file: ")
        university_summary: University = University(directory)
        
        response: str = input("Would you like to read in from another directory (yes or no)?: ")
        
        if response.lower() == 'no':
            runAgain = False

if __name__ == "__main__":
    main()

    
    