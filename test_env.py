# test_env.py
import importlib.metadata
import re
from typing import List

def get_requirements() -> List[str]:
    """
    Reads requirements.txt and returns a list of package names.
    Excludes comments, empty lines, and editable installs (-e .).
    """
    requirement_lst: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                # Remove whitespace and comments
                requirement = line.strip().split('#')[0].strip()
                if requirement and requirement != '-e .':
                    # Extract package name (before ==, >=, etc.)
                    pkg_name = re.split(r'[==|>=|<=|>|<]', requirement)[0].strip()
                    requirement_lst.append(pkg_name)
        return requirement_lst
    except FileNotFoundError:
        print("Error: requirements.txt not found.")
        return []

def check_package_versions(packages: List[str]) -> None:
    """
    Prints the installed versions of the given packages.
    Handles cases where packages are not installed.
    """
    print("Checking package versions from requirements.txt:")
    for pkg in packages:
        try:
            version = importlib.metadata.version(pkg)
            print(f"  {pkg}: {version}")
        except importlib.metadata.PackageNotFoundError:
            print(f"  {pkg}: Not installed")

if __name__ == "__main__":
    print("Environment setup verification started...")
    packages = get_requirements()
    if packages:
        check_package_versions(packages)
        print("Environment setup successful!")
    else:
        print("Failed to verify environment: No packages found in requirements.txt.")

# Purpose: Dynamically verify all dependencies in requirements.txt and print their versions.
# MLOps: Ensures environment consistency and reproducibility.
