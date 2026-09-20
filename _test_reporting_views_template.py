import re
import pytest
from pathlib import Path
from testing_methods import GetReportingVariables, Checks

# inputs
reporting_path = Path(r"C:\github\mi-team-byof\Shared\ManagementInformationBYOF\notebooks\reporting\nb_vw_reporting_fact_osa_uk.ipynb")

# global variables
reporting_file_name = reporting_path.stem
reporting_view_name = GetReportingVariables.get_view_name(reporting_path)

# ReportingTests:
def test_reporting_view_case_type():
    """
    Checks if view name is in snake case.
    """
    assert Checks.case_type(reporting_view_name) == 'snake_case',(
        f"View: {reporting_view_name}"
        )

def test_reporting_view_naming():
    """
    Checks the prefix of view name is 'vw_reporting_'.
    """
    assert Checks.vw_reporting_naming(reporting_view_name) is True,(
        f"View: {reporting_view_name}. Prefix should be 'vw_reporting_'"
        )

def test_reporting_name_view_file_consistency():
    """
    Test for consistency between name labels of view name and file name.
    """
    assert Checks.tbl_file_consistency(Checks.view_extract,reporting_view_name,reporting_file_name[3:]) is True, (
        f"View: {reporting_view_name}, File: {reporting_file_name}"
        )

def test_reporting_country_view_file_consistency():
    """
    Test for consistency between country labels of view name and file name.
    """
    assert Checks.tbl_file_consistency(Checks.get_country,reporting_view_name,reporting_file_name) is True, (
        f"View: {reporting_view_name}, File: {reporting_file_name}"
        )

def test_reporting_division_filter():
    """
    Test for presence of division filter (div-16 and div-15) have been removed in reporting notebook.
    """
    assert GetReportingVariables.get_division_filter(reporting_path) is False, (
        f"View: {reporting_view_name}, File: {reporting_file_name}"
        )