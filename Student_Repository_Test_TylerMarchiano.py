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

class StudentTest(unittest.TestCase):
    def test_student(self):
        '''testing the student class'''
        directory: str = '/Users/tylermarchiano/Documents/Stevens/SSW 810/Student-Repository/students.txt'
        
        students_file: List[str] = list(file_reader(directory, 3, sep=';', header=True))
        students_dict: Dict[str, Student] = dict()
        for cwid, name, major in students_file:
            students_dict[cwid] = Student(cwid, name, major)
        
        num_studenets: int = 10
        name_student10103: str = "Baldwin, C"
        name_student10115: str = "Wyatt, X"
        name_student10172: str = "Forbes, I"
        major_student11788: str = 'SYEN'
        major_student10183: str = 'SFEN'
        major_student11714: str = 'SYEN'
        
        
        self.assertEqual(num_studenets, len(list(students_dict.values())))
        self.assertEqual(name_student10103, students_dict['10103'].name)
        self.assertEqual(name_student10115, students_dict['10115'].name)
        self.assertEqual(name_student10172, students_dict['10172'].name)
        self.assertEqual(major_student11788, students_dict['11788'].major)
        self.assertEqual(major_student10183, students_dict['10183'].major)
        self.assertEqual(major_student11714, students_dict['11714'].major)

class MajorTest(unittest.TestCase):
    def test_major(self):
        '''testing the major class'''
        directory: str = '/Users/tylermarchiano/Documents/Stevens/SSW 810/Student-Repository/majors.txt'
        
        majors_file: List[str] = list(file_reader(directory, 3, sep='\t', header=True))
        majors_dict: Dict[str, Major] = dict()
        for major, flag, course in majors_file:
            if major not in majors_dict:
                majors_dict[major] = Major(major)
                majors_dict[major].add_course(flag, course)
            else:
                majors_dict[major].add_course(flag, course)
    
        SFEN_required: List[str] = ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567']
        SFEN_electives: List[str] = ['CS 501', 'CS 513', 'CS 545'] 
        SYEN_required: List[str] = ['SYS 612', 'SYS 671', 'SYS 800'] 
        SYEN_electives: List[str] = ['SSW 540', 'SSW 565', 'SSW 810']
        
        self.assertEqual(SFEN_required, sorted(majors_dict['SFEN'].required_courses))
        self.assertEqual(SFEN_electives, sorted(majors_dict['SFEN'].electives))
        self.assertEqual(SYEN_required, sorted(majors_dict['SYEN'].required_courses))
        self.assertEqual(SYEN_electives, sorted(majors_dict['SYEN'].electives))

class InstructorTest(unittest.TestCase):
    def test_Instructor(self):
        '''testing the instructor class'''
        directory: str = '/Users/tylermarchiano/Documents/Stevens/SSW 810/Student-Repository/instructors.txt'
        
        instructors_file: List[str] = list(file_reader(directory, 3, sep='|', header=True))
        instructors_dict: Dict[str, Instructor] = dict()
        for cwid, name, department in instructors_file:
            instructors_dict[cwid] = Instructor(cwid, name, department)
        
        num_instructors: int = 6
        name_instructor98765: str = "Einstein, A"
        name_instructor98764: str = "Feynman, R"
        name_instructor98763: str = "Newton, I"
        department_instructor98763: str = 'SFEN'
        department_instructor98761: str = 'SYEN'
        department_instructor98760: str = 'SYEN'
        
        
        self.assertEqual(num_instructors, len(list(instructors_dict.values())))
        self.assertEqual(name_instructor98765, instructors_dict['98765'].name)
        self.assertEqual(name_instructor98764, instructors_dict['98764'].name)
        self.assertEqual(name_instructor98763, instructors_dict['98763'].name)
        self.assertEqual(department_instructor98763, instructors_dict['98763'].department)
        self.assertEqual(department_instructor98761, instructors_dict['98761'].department)
        self.assertEqual(department_instructor98760, instructors_dict['98760'].department)

class UniversityTest(unittest.TestCase):
    def test_university(self):
        '''testing the university class'''
        directory: str = '/Users/tylermarchiano/Documents/Stevens/SSW 810/Student-Repository' 
        university_test: University = University(directory)
        
        num_students: int = 10
        num_instructors: int = 6
        student10103_numCourses: int = 4
        student10172_numCourses: int = 2
        instructor98760_numCourses: int = 4
        instructor98765_numCourses: int = 2
        student10175_courseList: List[str] = ['SSW 564', 'SSW 567', 'SSW 687'] 
        instructor98763_courseList: List[str] = ['SSW 555', 'SSW 689']
        instructor98765_numStudent_SSW567: int = 4
        
        student10103_remainingRequired: List[str] = ['SSW 540', 'SSW 555']
        student10115_GPA: float = 3.81
        student10172_remainingElectives: List[str] = ['CS 501', 'CS 513', 'CS 545']
        
        self.assertEqual(num_students, len(university_test.students))
        self.assertEqual(num_instructors, len(university_test.instructors))
        self.assertEqual(student10103_numCourses, len(university_test.students['10103'].courses))
        self.assertEqual(student10172_numCourses, len(university_test.students['10172'].courses))
        self.assertEqual(instructor98760_numCourses, len(university_test.instructors['98760'].courses))
        self.assertEqual(instructor98765_numCourses, len(university_test.instructors['98765'].courses))
        self.assertEqual(student10175_courseList, sorted(list(university_test.students['10175'].courses.keys())))
        self.assertEqual(instructor98763_courseList, sorted(list(university_test.instructors['98763'].courses.keys())))
        self.assertEqual(instructor98765_numStudent_SSW567, university_test.instructors['98765'].courses['SSW 567'])
    
        student10103: Student = university_test.students['10103']
        student10115: Student = university_test.students['10115']
        student10172: Student = university_test.students['10172']
        self.assertEqual(student10103_remainingRequired, sorted(student10103.major.get_student_remaining_required(student10103)))
        self.assertEqual(student10115_GPA, student10115.calculate_gpa())
        self.assertEqual(student10172_remainingElectives, sorted(student10172.major.get_student_remaining_electives(student10172)))

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)