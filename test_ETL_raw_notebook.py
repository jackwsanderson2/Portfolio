import re
import pytest
from pathlib import Path
from testing_methods import GetRawVariables, Checks

# inputs
raw_path = Path(r"raw_notebook__path")

# global variables
raw_file_name = raw_path.stem
raw_tbl_name = GetRawVariables.get_tbl_name(raw_path)
raw_source_name = GetRawVariables.get_source_file(raw_path)
raw_adls_account = GetRawVariables.get_adls_account(raw_path)
raw_container = GetRawVariables.get_container(raw_path)
raw_mode = str(GetRawVariables.get_mode(raw_path)).lower()
raw_highwatermark_column = GetRawVariables.get_highwatermark_column(raw_path)

# RawTests
def test_raw_case_type():
    """
    Checks if table name is in snake case.
    """
    assert Checks.case_type(raw_tbl_name) == 'snake_case',(
        f"Table: {raw_tbl_name}"
        )

def test_raw_tbl_naming():
    """
    Checks the prefix of table name is 'tbl_raw_'.
    """
    assert Checks.tbl_raw_naming(raw_tbl_name) is True,(
        f"Table: {raw_tbl_name}. Prefix should be 'tbl_raw_'"
        )

def test_raw_bi_number_extract():
    """
    Checks bi number is in format bi0000
    """
    assert re.fullmatch(r"bi\d{4}",Checks.bi_number_extract(raw_tbl_name)), (
        f"Table: {raw_tbl_name}"
        )

def test_raw_bi_tbl_file_consistency():
    """
    Test for consistency between bi numbers of table name and file name.
    """
    assert Checks.tbl_file_consistency(Checks.bi_number_extract,raw_tbl_name,raw_file_name) is True, (
        f"Table: {raw_tbl_name}, File: {raw_file_name}"
        )

def test_raw_name_tbl_file_consistency():
    """
    Test for consistency between name labels of table name and file name.
    """
    assert Checks.tbl_file_consistency(Checks.name_extract,raw_tbl_name,raw_file_name) is True, (
        f"Table: {raw_tbl_name}, File: {raw_file_name}"
        )

def test_raw_source_file_ending():
    """
    Test if source file ends with '/'.
    """
    assert Checks.source_file_ending(raw_source_name) is True, (
        f"Source File: {raw_source_name}"
        )

def test_raw_container():
    """
    Test if container is in format 'raw'.
    """
    assert raw_container == 'self-serve', (
        f"Container: {raw_container}"
        )

def test_raw_mode():
    """
    Test if mode is 'incremental' or 'overwrite'.
    """
    assert raw_mode == 'incremental' or raw_mode == 'overwrite', (
        f"Mode: {raw_mode}"
        )

def test_raw_highwatermark_column():
    """
    Test if highwatermark column is in format 'highwatermark'.
    """
    assert raw_highwatermark_column == 'load_id', (
        f"Highwatermark Column: {raw_highwatermark_column}"
        )
