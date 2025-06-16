from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    Reads the requirements.txt file and returns a list of packages.
    """
    requirement_lst: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            # Read lines from the file and remove leading/trailing whitespaces
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
        print("Parsed requirements:", requirement_lst)
    except FileNotFoundError:
        print('Requirements file not found.')
    
    return requirement_lst

if __name__ == "__main__":
    get_requirements()