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

setup(
    name="delhi_air_quality_forecasting",
    version="0.0.1",
    packages=find_packages(),
    install_requires=get_requirements(),
    author="Mohammad Saifi",
    description="A project to analyze and forecast air quality in Delhi.",
    url="https://github.com/saifimd1234/delhi_pollution_forecasting",
)

if __name__ == "__main__":
    get_requirements()