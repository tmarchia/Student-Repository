'''
Tyler Marchiano
HW08
SSW 810

This file contains different methods for date_arithmetic, file_reader, and the FileAnalyzer class
'''
from datetime import datetime, timedelta
from typing import Tuple, Iterator, Dict, IO, List
from prettytable import PrettyTable
import os

#PART 1
def date_arithmetic() -> Tuple[datetime, datetime, int]:
    """ This function returns a tuple with the following 3 things:
    1. An instance of  class datetime representing the date three days after Feb 27, 2020.
    2. An instance of  class datetime representing the date three days after Feb 27, 2019.
    3. An int representing the number of days between Feb 1, 2019 and Sept 30, 2019"""
    
    three_days_after_02272020: datetime = datetime.strptime("February 27, 2020", "%B %d, %Y") + timedelta(days=3)
    three_days_after_02272019: datetime = datetime.strptime("February 27, 2019", "%B %d, %Y") + timedelta(days=3)
    days_between_02012019_09302019: int = (datetime.strptime("September 30, 2019", "%B %d, %Y") - datetime.strptime("February 01, 2019", "%B %d, %Y")).days
    
    return three_days_after_02272020, three_days_after_02272019, days_between_02012019_09302019

#PART2
def file_reader(path, fields, sep=',', header=False) -> Iterator[Tuple[str]]:
    """ Generator function to read field-separated text files and yield a tuple 
    with all of the values from a single line in the file on each call to next()"""
    try: #Try to open file
        fp: IO = open(path, 'r')
    except:
        raise FileNotFoundError(f"Can't open the path provided (File not found): {path}.")
    
    #Skip the header if true
    if header == True:
        next(fp)
    
    #keep track of the amount of lines
    line_number: int = 1
    
    with fp:
        for current_line in fp:
            current_line = current_line.strip() #string the newline
            
            #Make sure there are enough fields, if not raise error
            if current_line.count(sep) != fields -1:
                raise ValueError (f"Error in {path} on line {line_number}, {current_line.count(sep)+1} fields found but expected {fields}")
            
            return_list: List[str] = list()
            
            while sep in current_line:
                sep_location: int = current_line.find(sep, 0, len(current_line))
                return_list.append(current_line[0:sep_location])
                current_line = current_line[sep_location+1:]
            return_list.append(current_line)
            line_number += 1 

            yield tuple(return_list)
            
#PART3
class FileAnalyzer:
    """ given a directory name, searches that directory for Python files and prints various information"""
    def __init__(self, directory: str) -> None:
        """directory is the directory we are analyzing
            files_summary is a dictionary with the info we are saving for the directory"""
        self.directory: str = directory # NOT mandatory!
        self.files_summary: Dict[str, Dict[str, int]] = dict() 

        self.analyze_files() # summerize the python files data

    def analyze_files(self) -> None:
        """ This method populates self.files_summary"""
        for item in os.listdir(self.directory):
            class_count : int = 0 
            function_count : int = 0
            line_count : int = 0
            char_count : int = 0
            
            #if the file is a python file
            if item.endswith('.py'):
                try: #Try to open file
                    openfile: IO = open(os.path.join(self.directory, item), 'r')
                except:
                    raise FileNotFoundError(f"Can't open the file {os.path.join(self.directory, item)}")
                
                with openfile:
                    for line in openfile:
                        if line.startswith('def ') or line.startswith('    def '):
                            function_count += 1
                        if line.startswith('class '):
                            class_count += 1
                        line_count += 1
                        char_count += len(line)
            
                self.files_summary[os.path.join(self.directory, item)] = {'class': class_count, 'function': function_count, 'line': line_count, 'char': char_count}
                    
    def pretty_print(self) -> None:
        """ Displays self.files_summary in a table"""
        pt: PrettyTable = PrettyTable(field_names=["File Name", "Classes", "Functions", "Lines", "Characters"])
        for item in self.files_summary:
            pt.add_row([item, self.files_summary[item]['class'], self.files_summary[item]['function'], self.files_summary[item]['line'], self.files_summary[item]['char']])
        print(pt)

