'''
Tyler Marchiano
HW08
SSW 810

This file contains different test methods for the Students, Instructors, and University Classes
'''

import unittest
from Student_Repository_TylerMarchiano import Student, Instructor, University, Major
from HW8_TylerMarchiano import file_reader
from typing import Dict, List
import sqlite3

class StudentTest(unittest.TestCase):
    def test_student(self):
        '''testing the student class'''
        directory: str = '/Users/tylermarchiano/Documents/Stevens/SSW810/Student-Repository/students.txt'
        
        students_file: List[str] = list(file_reader(directory, 3, sep='\t', header=True))
        students_dict: Dict[str, Student] = dict()
        for cwid, name, major in students_file:
            students_dict[cwid] = Student(cwid, name, major)
        
        num_students: int = 4
        name_student10103: str = "Jobs, S"
        name_student10115: str = "Bezos, J"
        major_student10183: str = 'SFEN'
        major_student11714: str = 'CS'
        
        
        self.assertEqual(num_students, len(list(students_dict.values())))
        self.assertEqual(name_student10103, students_dict['10103'].name)
        self.assertEqual(name_student10115, students_dict['10115'].name)
        self.assertEqual(major_student10183, students_dict['10183'].major)
        self.assertEqual(major_student11714, students_dict['11714'].major)

class MajorTest(unittest.TestCase):
    def test_major(self):
        '''testing the major class'''
        directory: str = '/Users/tylermarchiano/Documents/Stevens/SSW810/Student-Repository/majors.txt'
        
        majors_file: List[str] = list(file_reader(directory, 3, sep='\t', header=True))
        majors_dict: Dict[str, Major] = dict()
        for major, flag, course in majors_file:
            if major not in majors_dict:
                majors_dict[major] = Major(major)
                majors_dict[major].add_course(flag, course)
            else:
                majors_dict[major].add_course(flag, course)
    
        SFEN_required: List[str] = ['SSW 540', 'SSW 555', 'SSW 810']
        SFEN_electives: List[str] = ['CS 501', 'CS 546'] 
        CS_required: List[str] = ['CS 546', 'CS 570']  
        CS_electives: List[str] = ['SSW 565', 'SSW 810']
        
        self.assertEqual(SFEN_required, sorted(majors_dict['SFEN'].required_courses))
        self.assertEqual(SFEN_electives, sorted(majors_dict['SFEN'].electives))
        self.assertEqual(CS_required, sorted(majors_dict['CS'].required_courses))
        self.assertEqual(CS_electives, sorted(majors_dict['CS'].electives))

class InstructorTest(unittest.TestCase):
    def test_Instructor(self):
        '''testing the instructor class'''
        directory: str = '/Users/tylermarchiano/Documents/Stevens/SSW810/Student-Repository/instructors.txt'
        
        instructors_file: List[str] = list(file_reader(directory, 3, sep='\t', header=True))
        instructors_dict: Dict[str, Instructor] = dict()
        for cwid, name, department in instructors_file:
            instructors_dict[cwid] = Instructor(cwid, name, department)
        
        num_instructors: int = 3
        name_instructor98762: str = "Hawking, S"
        name_instructor98764: str = "Cohen, R"
        name_instructor98763: str = "Rowland, J"
        department_instructor98763: str = 'SFEN'
        department_instructor98764: str = 'SFEN'
        department_instructor98762: str = 'CS'
        
        
        self.assertEqual(num_instructors, len(list(instructors_dict.values())))
        self.assertEqual(name_instructor98762, instructors_dict['98762'].name)
        self.assertEqual(name_instructor98764, instructors_dict['98764'].name)
        self.assertEqual(name_instructor98763, instructors_dict['98763'].name)
        self.assertEqual(department_instructor98763, instructors_dict['98763'].department)
        self.assertEqual(department_instructor98764, instructors_dict['98764'].department)
        self.assertEqual(department_instructor98762, instructors_dict['98762'].department)

class UniversityTest(unittest.TestCase):
    def test_university(self):
        '''testing the university class'''
        directory: str = '/Users/tylermarchiano/Documents/Stevens/SSW810/Student-Repository' 
        university_test: University = University(directory)
        
        num_students: int = 4
        num_instructors: int = 3
        student10103_numCourses: int = 2
        student10115_numCourses: int = 2
        instructor98764_numCourses: int = 1
        instructor98762_numCourses: int = 3
        student11714_courseList: List[str] = ['CS 546', 'CS 570', 'SSW 810']
        instructor98763_courseList: List[str] = ['SSW 555', 'SSW 810']
        instructor98763_numStudent_SSW810: int = 4
        
        student10103_remainingRequired: List[str] = ['SSW 540', 'SSW 555'] 
        student10115_GPA: float = 2.0
        student10115_remainingElectives: List[str] = ['CS 501', 'CS 546'] 
        
        self.assertEqual(num_students, len(university_test.students))
        self.assertEqual(num_instructors, len(university_test.instructors))
        self.assertEqual(student10103_numCourses, len(university_test.students['10103'].courses))
        self.assertEqual(student10115_numCourses, len(university_test.students['10115'].courses))
        self.assertEqual(instructor98764_numCourses, len(university_test.instructors['98764'].courses))
        self.assertEqual(instructor98762_numCourses, len(university_test.instructors['98762'].courses))
        self.assertEqual(student11714_courseList, sorted(list(university_test.students['11714'].courses.keys())))
        self.assertEqual(instructor98763_courseList, sorted(list(university_test.instructors['98763'].courses.keys())))
        self.assertEqual(instructor98763_numStudent_SSW810, university_test.instructors['98763'].courses['SSW 810'])
    
        student10103: Student = university_test.students['10103']
        student10115: Student = university_test.students['10115']
        self.assertEqual(student10103_remainingRequired, sorted(student10103.major.get_student_remaining_required(student10103)))
        self.assertEqual(student10115_GPA, student10115.calculate_gpa())
        self.assertEqual(student10115_remainingElectives, sorted(student10115.major.get_student_remaining_electives(student10115)))
        
        #Below are the database tests
        
        databaseResults: List[List[str]] = list()
        db: sqlite3.Connection = sqlite3.connect('/Users/tylermarchiano/Documents/Stevens/SSW810/Student-Repository/tmarchiano_homework.db')
        query: str = """select Students.Name, Students.CWID, Grades.Course, Grades.Grade, Instructors.Name
                        from Grades join Students on Students.CWID = StudentCWID
                        join Instructors on InstructorCWID = Instructors.CWID
                        order by Students.Name ASC
                    """
        for row in db.execute(query):
            databaseResults.append(list(row))
        
        expectedDatabaseRow1: List[str] = ['Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J']
        expectedDatabaseRow2: List[str] = ['Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S']
        expectedDatabaseRow3: List[str] = ['Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J']
        expectedDatabaseRow4: List[str] = ['Gates, B', '11714', 'CS 546', 'A', 'Cohen, R']
        expectedDatabaseRow5: List[str] = ['Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S']
        expectedDatabaseRow6: List[str] = ['Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J']
        expectedDatabaseRow7: List[str] = ['Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S']
        expectedDatabaseRow8: List[str] = ['Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J']
        expectedDatabaseRow9: List[str] = ['Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J']
        
        expected: List[List[str]] = [expectedDatabaseRow1, expectedDatabaseRow2, expectedDatabaseRow3, expectedDatabaseRow4, expectedDatabaseRow5, expectedDatabaseRow6, expectedDatabaseRow7, expectedDatabaseRow8, expectedDatabaseRow9]
        self.assertEqual(databaseResults, expected)

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)