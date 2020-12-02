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
import sqlite3

class Student:
    def __init__(self, cwid: str, name: str, major: str) -> None:
        '''Stores information about a single student'''
        self.cwid: str = cwid
        self.name: str = name
        self.major: Major = major
        self.courses: Dict[str, str] = dict() #Key is course and value is the grade
    
    def add_course(self, course: str, grade: str) -> None:
        '''add the course to the dictionary with a value of grade'''
        self.courses[course] = grade
    
    def compute_completed_courses(self) -> List[str]:
        '''make a list of the completed courses'''
        passing_grades: List[str] = ["A", "A-", "B+", "B", "B-", "C+", "C"]
        completed_courses: List[str] = list()
        for course, grade in self.courses.items():
            if grade in passing_grades:
                completed_courses.append(course)
        
        return completed_courses
    
    def calculate_gpa(self) -> float:
        '''calculate the students GPA '''
        grade_values: Dict[str, float] = {"A": 4.0, "A-": 3.75, "B+": 3.25, "B": 3.0, "B-": 2.75, "C+": 2.25, "C": 2.0, "C-": 0, "D+": 0, "D": 0, "D-": 0, "F": 0}
        num_courses: float = 0.0
        total_value: int = 0
        
        for course, grade in self.courses.items():
            total_value += grade_values[grade]
            num_courses +=1

        try:
            gpa: float = round(total_value/num_courses,2)
        except:
            raise ZeroDivisionError ("Can't divide by 0")
        return gpa

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

class Major:
    def __init__(self, major: str) -> None:
        '''Stores information about one major'''
        self.name: str = major
        self.required_courses : List[str] = list()
        self.electives : List[str] = list()
    
    def add_course(self, flag: str, course: str) -> None:
        if flag == 'R':
            if course not in self.required_courses:
                self.required_courses.append(course)
        else:
            if course not in self.electives:
                self.electives.append(course)
    
    def get_student_remaining_required(self, student: Student) -> List[str]:
        '''return a list of the required courses the student has taken'''
        completed_courses: List[str] = student.compute_completed_courses()
        remaining_required: List[str] = list()
        for course in self.required_courses:
            if course not in completed_courses:
                remaining_required.append(course)
        
        return remaining_required

    def get_student_remaining_electives(self, student: Student) -> List[str]:
        '''return a list of the required courses the student has taken'''
        completed_courses: List[str] = student.compute_completed_courses()
        completed_elective: bool = False
        for course in completed_courses:
            if course in self.electives:
                completed_elective = True
        
        if completed_elective:
            return list()
        else:
            return self.electives

class University:
    '''Holds all of the data for a specific University'''
    students: Dict[str, Student] = dict() #key is cwid and the value is the student. This will make it easier to find students later
    instructors: Dict[str, Instructor] = dict() #key is cwid and the value is the Instructor. This will make it easier to find instructors later
    majors: Dict[str, Major] = dict() #key is major name and the value is the Major object
    
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.read_majors()
        self.read_students()
        self.read_instructors()
        self.read_grades()
        self.majors_prettytable()
        self.student_prettytable()
        self.instructor_prettytable()
        self.student_grades_table_db('/Users/tylermarchiano/Documents/Stevens/SSW810/Student-Repository/tmarchiano_homework.db')
    
    def read_students(self) -> None:
        '''read the students.txt file, creating a new Student for each line in the file'''
        file_path: str = path.join(self.path, 'students.txt')
        try:
            students_file: List[str] = list(file_reader(file_path, 3, sep='\t', header=True))
        except:
            raise FileNotFoundError(f"Can't find students.txt in the given directory")
        
        for cwid, name, major in students_file:
            self.students[cwid] = Student(cwid, name, self.majors[major])
    
    def read_instructors(self) -> None:
        '''read the instructors.txt file, creating a new Student for each line in the file'''
        file_path: str = path.join(self.path, 'instructors.txt')
        try:
            instructors_file: List[str] = list(file_reader(file_path, 3, sep='\t', header=True))
        except:
            raise FileNotFoundError(f"Can't find instructors.txt in the given directory")
        
        for cwid, name, department in instructors_file:
            self.instructors[cwid] = Instructor(cwid, name, department)
    
    def read_grades(self) -> None:
        '''reads the grades.txt file and processes all of that information. 
        assigns students courses and grades. Assigns professors courses '''
        file_path: str = path.join(self.path, 'grades.txt')
        try:
            grades_file: List[str] = list(file_reader(file_path, 4, sep='\t', header=True))
        except:
            raise FileNotFoundError(f"Can't find grades.txt in the given directory")
        
        for s_cwid, course, grade, p_cwid in grades_file:
            #add the course and grade for the student
            self.students[s_cwid].add_course(course, grade)
            
            #add the course to the professor if it doesn't exist already and increment the count of the students
            self.instructors[p_cwid].add_course(course)
    
    def read_majors(self) -> None:
        '''reads the majors.txt file and processes all of that information. 
        Create a new object of type Major for each major'''
        file_path: str = path.join(self.path, 'majors.txt')
        try:
            majors_file: List[str] = list(file_reader(file_path, 3, sep='\t', header=True))
        except:
            raise FileNotFoundError(f"Can't find majors.txt in the given directory")
        
        for major, flag, course in majors_file:
            if major not in self.majors:
                self.majors[major] = Major(major)
                self.majors[major].add_course(flag, course)
            else:
                self.majors[major].add_course(flag, course)

    def majors_prettytable(self) -> None:
        '''print the mjor pretty table '''
        pt: PrettyTable = PrettyTable(field_names=['Major', 'Required Courses', 'Electives'])
        for major in self.majors.values():
            pt.add_row([major.name, sorted(major.required_courses), sorted(major.electives)])
        print()
        print("Majors Summary: ")
        print(pt)
        
    def student_prettytable(self) -> None:
        '''print the student pretty table'''
        pt: PrettyTable = PrettyTable(field_names=["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Electives", "GPA"])
        
        for student in self.students.values():
            completed_courses: List[str] = sorted(student.compute_completed_courses())
            remaining_electives: List[str] = sorted(student.major.get_student_remaining_electives(student))
            remaining_required: List[str] = sorted(student.major.get_student_remaining_required(student))
            
            pt.add_row([student.cwid, student.name, student.major.name, completed_courses, remaining_required, remaining_electives, student.calculate_gpa()])
        
        print()
        print("Student Summary: ")
        print(pt)
    
    def instructor_prettytable(self) -> None:
        '''print the instructor pretty table'''
        pt: PrettyTable = PrettyTable(field_names=["CWID", "Name", "Dept", "Course", "Students"])
        for instructor in self.instructors.values():
            for course in instructor.courses:
                pt.add_row([instructor.cwid, instructor.name, instructor.department, course, instructor.courses[course]])
        print()
        print("Instructor Summary: ")
        print(pt)
    
    def student_grades_table_db(self, db_path) -> None:
        '''print students grade summary table using SQLLite query'''
        pt: PrettyTable = PrettyTable(field_names=["NAME", "CWID", "Course", "Grade", "Instructor"])
        db: sqlite3.Connection = sqlite3.connect(db_path)
        query: str = """select Students.Name, Students.CWID, Grades.Course, Grades.Grade, Instructors.Name
                        from Grades join Students on Students.CWID = StudentCWID
                        join Instructors on InstructorCWID = Instructors.CWID
                        order by Students.Name ASC
                    """
        for row in db.execute(query):
            pt.add_row(list(row))
        db.close()
        print()
        print("Student Grade Summary: ")
        print(pt)
                   
def main() -> None:
    '''run the program'''
    
    runAgain: bool = True
    
    while runAgain:
        #Error handling for an invalid input path is handled in HW8_TylerMarchiano.py as well as in the classes above
        directory: str = input("Please enter the directory that contains the students.txt, instructors.txt and grades.txt file: ")
        university_summary: University = University(directory)
        
        print()
        response: str = input("Would you like to read in from another directory (yes or no)?: ")
        
        if response.lower() == 'no':
            runAgain = False
    
if __name__ == "__main__":
    main()

    
    