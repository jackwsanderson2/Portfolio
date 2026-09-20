import re
import pytest
from pathlib import Path
from testing_methods import GetRawVariables, GetConformedVariables, Checks

# inputs
raw_path = Path(r"C:\github\mi-team-byof\Shared\ManagementInformationBYOF\notebooks\raw\nb_raw_bi0076_osa.ipynb")
conformed_path = Path(r"C:\github\mi-team-byof\Shared\ManagementInformationBYOF\notebooks\conformed\nb_conformed_bi0076_osa.ipynb")

# global variables
raw_file_name = raw_path.stem
raw_tbl_name = GetRawVariables.get_tbl_name(raw_path)
raw_source_name = GetRawVariables.get_source_file(raw_path)
raw_adls_account = GetRawVariables.get_adls_account(raw_path)
raw_container = GetRawVariables.get_container(raw_path)
raw_mode = str(GetRawVariables.get_mode(raw_path)).lower()
raw_highwatermark_column = GetRawVariables.get_highwatermark_column(raw_path)

conformed_file_name = conformed_path.stem
conformed_source_name = GetConformedVariables.get_source_table(conformed_path)
conformed_target_name = GetConformedVariables.get_target_table(conformed_path)

# ConformedTests
def test_conformed_source_case_type():
    """
    Checks if source table name is in snake case.
    """
    assert Checks.case_type(conformed_source_name) == 'snake_case',(
        f"Table: {conformed_source_name}"
        )

def test_raw_conformed_source_consistency():
    """
    Test for consistency between source table name and raw table name.
    """
    assert conformed_source_name == raw_tbl_name, (
        f"Raw Table: {raw_tbl_name}, Conformed Source Table: {conformed_source_name}"
        )

def test_conformed_target_case_type():
    """
    Checks if target table name is in snake case.
    """
    assert Checks.case_type(conformed_target_name) == 'snake_case',(
        f"Table: {conformed_target_name}"
        )

def test_conformed_target_naming():
    """
    Checks the prefix of target table name is 'tbl_conformed_'.
    """
    assert Checks.tbl_conformed_naming(conformed_target_name) is True,(
        f"Table: {conformed_target_name}. Prefix should be 'tbl_conformed_'"
        )

def test_conformed_bi_number_extract():
    """
    Checks bi number is in format bi0000
    """
    assert re.fullmatch(r"bi\d{4}", Checks.bi_number_extract(conformed_target_name)),(
        f"Table: {conformed_target_name}"
        )

def test_conformed_bi_tbl_file_consistency():
    """
    Test for consistency between bi numbers of table name and file name.
    """
    assert Checks.tbl_file_consistency(Checks.bi_number_extract,conformed_target_name,conformed_file_name) is True, (
        f"Table: {conformed_target_name}, File: {conformed_file_name}"
        )

def test_conformed_name_tbl_file_consistency():
    """
    Test for consistency between name labels of table name and file name.
    """
    assert Checks.tbl_file_consistency(Checks.name_extract,conformed_target_name,conformed_file_name) is True, (
        f"Table: {conformed_target_name}, File: {conformed_file_name}"
        )