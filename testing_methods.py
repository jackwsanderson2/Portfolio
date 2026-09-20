import nbformat
import re
import yaml
from pathlib import Path


class GetRawVariables:
    @staticmethod
    def get_variable(notebook_path, variable_name):
        nb = str(nbformat.read(notebook_path, as_version=4))

        pattern = rf"{variable_name}\s*=\s*['\"]?([^'\"\s]+)"
        match = re.search(pattern, nb)

        return match.group(1) if match else None

    @staticmethod
    def get_adls_account(notebook_path):
        return GetRawVariables.get_variable(
            notebook_path,
            "adls_account"
        )

    @staticmethod
    def get_container(notebook_path):
        return GetRawVariables.get_variable(
            notebook_path,
            "container"
        )

    @staticmethod
    def get_source_file(notebook_path):
        return GetRawVariables.get_variable(
            notebook_path,
            "source_file"
        )

    @staticmethod
    def get_catalog(notebook_path):
        return GetRawVariables.get_variable(
            notebook_path,
            "catalog ="
        )

    @staticmethod
    def get_schema(notebook_path):
        return GetRawVariables.get_variable(
            notebook_path,
            "schema"
        )

    @staticmethod
    def get_tbl_name(notebook_path):
        return GetRawVariables.get_variable(
            notebook_path,
            "tbl_name"
        )

    @staticmethod
    def get_ext_loc(notebook_path):
        return GetRawVariables.get_variable(
            notebook_path,
            "ext_loc"
        )

    @staticmethod
    def get_mode(notebook_path):
        return GetRawVariables.get_variable(
            notebook_path,
            "mode"
        )

    @staticmethod
    def get_highwatermark_column(notebook_path):
        return GetRawVariables.get_variable(
            notebook_path,
            "highwatermark_column"
        )

    @staticmethod
    def get_mandatory_columns(notebook_path):
        return GetRawVariables.get_variable(
            notebook_path,
            "mandatory_columns"
        )

    @staticmethod
    def get_clustering_columns(notebook_path):
        return GetRawVariables.get_variable(
            notebook_path,
            "clustering_columns"
        )

    @staticmethod
    def get_df(notebook_path):
        return GetRawVariables.get_variable(
            notebook_path,
            "df"
        )

class Checks ():
    def __init__(self):
        self

    def case_type(tbl_name):
        """
        Detects case type.
        """

        tbl_name = tbl_name.replace(" ", "")

        SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")
        PASCAL_CASE = re.compile(r"^[A-Z][a-zA-Z0-9]*$")
        CAMEL_CASE = re.compile(r"^[a-z]+(?:[A-Z][a-z0-9]*)*$")
        
        if bool(SNAKE_CASE.match(tbl_name)) == True:
            return 'snake_case'
        elif bool(PASCAL_CASE.match(tbl_name)) == True:
            return 'pascal case'
        elif bool(CAMEL_CASE.match(tbl_name)) == True:
            return 'camel case'

    def tbl_raw_naming(tbl_name):
        """
        Checks variable starts with prefix 'tbl_raw_'.
        """

        prefix = 'tbl_raw_'
        if tbl_name.startswith(prefix):
            return True
        else:
            return False

    def bi_number_extract(input):
        """
        Extracts bi number in format bi0000.
        """
        search_term = 'bi'
        position = input.find(search_term)
        bi_number = input[position:position+6]

        return bi_number

    def name_extract(input):
        """
        Extracts name of data.
        """
        search_term = 'bi'
        position = input.find(search_term)
        name = input[position+7:]

        return name

    def tbl_file_consistency(function,tbl_name,file_name):
        """
        Checks naming consistency between table and file.
        """
        if function((tbl_name)) == function((file_name)):
            return True
        else:
            return False

    def source_file_ending(source_file):
        """
        Checks URL link ends in '/'.
        """
        if source_file.endswith('/'):
            return True
        else:
            return False

