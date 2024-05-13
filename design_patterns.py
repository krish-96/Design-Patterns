"""
Example usage
with DynamicPythonCodeImport() as code_import:
    patterns_yaml_content = code_import.yaml_data
    # To display the content of the yaml file
    # print(patterns_yaml_content)

    # To display the Design pattern name and example code
    # for pi_key, pi_Value in code_import.patterns_info.items():
    #     print("=" * 5, pi_key, pi_Value)

    # To execute all the patterns
    # code_import.enable_execute_all_patterns()

    # To write all the patterns to the individual python files
    # code_import.enable_write_code_to_file()

    # To set the selected design pattern
    # code_import.set_pattern("Singleton Pattern")

    # To execute the configured design pattern
    # code_import.execute()

"""

import os
import yaml
from abc import ABC, abstractmethod
from pprint import pprint
from abc import ABC, abstractmethod

# Module Constants
FILENAME = "design_pattern_examples.yaml"
CODE_WRITE_DIR_NAME = "Code"


class HandleCode(ABC):
    """This class will handle the code loaded from yaml file
    available_patterns - Available design patterns
    patterns_info - Yaml file name
    pattern_name - name of the selected pattern
    code - Yaml file name
    execute_all_patterns - Flag to decide whether to execute all the patterns or not
    write_code_to_file - Flag to decide whether to write code to the file or not
    """

    def __init__(self):
        self.available_patterns = []
        self.patterns_info = {}
        self.pattern_name = None
        self.code = None
        self.execute_all_patterns = True
        self.write_code_to_file = True
        self.check_code_output_directory()

    @staticmethod
    def check_code_output_directory() -> None:
        """This method will check for the code output directory existence, if it does not exist, it'll create"""
        try:
            if not os.path.exists(CODE_WRITE_DIR_NAME):
                os.makedirs(CODE_WRITE_DIR_NAME, exist_ok=True)
        except Exception as E:
            print(f"{'=' * 5}> Exception occurred while Creating the Code output directory: {CODE_WRITE_DIR_NAME} {E}")

    @abstractmethod
    def set_pattern(self, pattern) -> None:
        """Chile class is responsible for implementing the functionality"""
        pass

    def display_patterns(self) -> list:
        """To display the existing patterns in the console"""
        print("Available patterns are :")
        for pattern in self.available_patterns:
            print(f"\t-{pattern}")

        return self.available_patterns

    def execute_all(self) -> None:
        """This method will initiate the execute method for all the available design patterns code"""
        try:
            for pattern_name, pattern_info, in self.patterns_info.items():
                self.pattern_name = pattern_name
                self.code = pattern_info.get('example')
                self._execute()
        except Exception as E:
            print(f"{'=' * 5}> Exception occurred while executing the pattern: {self.pattern_name}"
                  f"\n>>> Exception: {E} \nCode: \n{self.code}")

    def execute(self) -> None:
        """This method will initiate the execute method for the selected design pattern"""
        try:
            # print('Executing')
            if not self.execute_all_patterns:
                if self.pattern_name in self.available_patterns \
                        and self.patterns_info.get(self.pattern_name, None):
                    self._execute()
            else:
                self.execute_all()
        except Exception as E:
            print(f"{'=' * 5}> Exception occurred while executing the pattern: {self.pattern_name}"
                  f"\n>>> Exception: {E} \nCode: \n{self.code}")

    def _execute(self) -> None:
        """This is the actual method executing the design patterns code"""
        try:
            # print('Executing')
            if self.pattern_name and self.code:
                if self.write_code_to_file:
                    self._write_code_to_file()
                import subprocess
                file_path = os.path.join(os.path.dirname(__file__), CODE_WRITE_DIR_NAME,
                                         self.pattern_name.replace(' ', '_').lower() + '.py').replace('\ ', ' ')
                print("Does exists: ", file_path, os.path.isfile(file_path))
                output = subprocess.run(f"python3 {file_path}", shell=True, capture_output=True)
                # for message in output.stdout:
                #     print(message)
                # print(output)
                exec(self.code)
            else:
                print("Pattern Name and Code not found")
        except Exception as E:
            print(f"{'=' * 5}> Exception occurred while executing the pattern: {self.pattern_name}"
                  f"\n>>> Exception: {E} \nCode: \n{self.code}")

    def _write_code_to_file(self) -> None:
        """This method will write the design patterns code to the file"""
        try:
            if self.pattern_name and self.code:
                file_path = str(os.path.join(CODE_WRITE_DIR_NAME, self.pattern_name.replace(' ', '_').lower() + '.py'))
                with open(file_path, 'w', newline='\n') as f:
                    f.write(self.code)
        except Exception as E:
            print(f"{'=' * 5}> Exception occurred while writing the pattern to file: {self.pattern_name}"
                  f"\n>>> Exception: {E} \nCode: \n{self.code}")

    def enable_execute_all_patterns(self) -> None:
        """This method will enable the execution of all the design patterns"""
        if not self.execute_all_patterns:
            print("Enable execute all patterns")
            self.execute_all_patterns = True

    def disable_execute_all_patterns(self) -> None:
        """This method will disable the execution of all the design patterns"""
        if self.execute_all_patterns:
            print("Disable execute all patterns")
            self.execute_all_patterns = False

    def enable_write_code_to_file(self) -> None:
        """This method will enable the writing code to file"""
        if not self.write_code_to_file:
            print("Enable writing code to file")
            self.write_code_to_file = True

    def disable_write_code_to_file(self) -> None:
        """This method will disable the writing code to file"""
        if self.write_code_to_file:
            print("Disable writing code to file")
            self.write_code_to_file = False


class DynamicPythonCodeImport(HandleCode, object):
    """This class will import the python code dynamically from the yaml file
    filename - Yaml file name
    yaml_data - Content of the yaml file
    pattern_name - name of the selected pattern
    available_patterns - Available design patterns
    patterns_info - Yaml file name
    code - Yaml file name
    execute_all_patterns - Flag to decide whether to execute all the patterns or not
    write_code_to_file - Flag to decide whether to write code to the file or not
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton Pattern"""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, filename=None, pattern_name=None):
        super(DynamicPythonCodeImport, self).__init__()
        self.filename = filename
        self.pattern_name = pattern_name
        self.yaml_data = None

    def __enter__(self):
        """This method will read the content from the yaml file and initializes the data"""
        if self.filename is None:
            self.filename = FILENAME

        # Before reading the content making sure the file exists
        if self.filename and self.check_for_yaml_file():
            with open(self.filename) as f:
                self.yaml_data = yaml.safe_load(f)
                self.fetch_and_set_available_patterns()
                self.display_patterns()
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """This method will be called while executing the program and print the exception info if available """
        print('Exiting the program, Closing all the resources.')
        if exc_type or exc_val or exc_tb:
            print("Exceptions raised: ")
            print("%s : %s : %s" % (exc_type, exc_val, exc_tb))

    def check_for_yaml_file(self) -> bool:
        """This method will check for the yaml file existence
            returns true if the yaml file exists
            else returns false
        :return : returns boolean value
        """
        try:
            return os.path.isfile(self.filename)
        except Exception as E:
            print(f"Exception occurred while checking for the yaml file existence, Exception: {E}")

    def fetch_and_set_available_patterns(self) -> None:
        """This method will fetch the available patterns from the yaml data and sets the available patterns info"""
        patterns = self.yaml_data.get('patterns', [])
        self.patterns_info = {pattern.get('name'): pattern for pattern in patterns}
        self.available_patterns = [pattern.get('name') for pattern in patterns]

    def prepare_pattern_data(self) -> None:
        """This method will prepare the pattern data"""
        try:
            if self.pattern_name and self.pattern_name in self.available_patterns:
                self.code = self.patterns_info.get(self.pattern_name, {}).get('example', None)
                print("Preparing pattern data: ")

        except Exception as E:
            print(f"Exception occurred while preparing the pattern data: {self.code}, \nException: {E}")

    def set_pattern(self, pattern) -> None:
        """This method will set the given pattern name"""
        try:
            if pattern in self.available_patterns:
                self.pattern_name = pattern
                self.prepare_pattern_data()
            else:
                print(f"[X] Invalid Pattern: {pattern}")
                print("[ ] Available patterns are:")
                for p in self.available_patterns:
                    print(f"    - {p}")

        except Exception as E:
            print(f"Exception occurred while Setting the pattern: {pattern}, \nException: {E}")


with DynamicPythonCodeImport() as code_import:
    patterns_yaml_content = code_import.yaml_data
    # To display the content of the yaml file
    # print(patterns_yaml_content)

    # To display the Design pattern name and example code
    # for pi_key, pi_Value in code_import.patterns_info.items():
    #     print("=" * 5, pi_key, pi_Value)

    # To display the existing design pattern names
    # code_import.display_patterns()

    # # To disable execute all the patterns
    # code_import.disable_execute_all_patterns()
    #
    # # To disable write all the patterns to the individual python files
    # code_import.disable_write_code_to_file()
    #
    # # To set the selected design pattern
    code_import.set_pattern("Singleton Pattern")

    # To execute the configured design pattern
    code_import.execute()
