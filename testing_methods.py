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
