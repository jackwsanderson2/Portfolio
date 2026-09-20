import re
import pytest
from pathlib import Path
from testing_methods import GetRawVariables,GetReportingVariables, GetJobVariables, Checks

#inputs
raw_path = Path(r"C:\github\mi-team-byof\Shared\ManagementInformationBYOF\notebooks\raw\nb_raw_bi0076_osa.ipynb")
reporting_path = Path(r"C:\github\mi-team-byof\Shared\ManagementInformationBYOF\notebooks\reporting\nb_vw_reporting_fact_osa_uk.ipynb")
job_path = Path(r"C:\github\mi-team-byof\Shared\ManagementInformationBYOF\resources\job_osa.yml")

#global variables
raw_file_name = raw_path.stem
raw_tbl_name = GetRawVariables.get_tbl_name(raw_path)
raw_source_name = GetRawVariables.get_source_file(raw_path)[1:]
raw_adls_account = GetRawVariables.get_adls_account(raw_path)
raw_container = GetRawVariables.get_container(raw_path)
raw_mode = str(GetRawVariables.get_mode(raw_path)).lower()
raw_highwatermark_column = GetRawVariables.get_highwatermark_column(raw_path)

reporting_file_name = reporting_path.stem
reporting_view_name = GetReportingVariables.get_view_name(reporting_path)

job_data = GetJobVariables.get_job_data(job_path)
job_file_name = job_path.stem
job = job_file_name.split('_', 1)[1]
job_name = job_data[job]['name']
job_group_name = job_data[job]['permissions'][0]['group_name']
job_permission_level = job_data[job]['permissions'][0]['level']
job_pause_status = job_data[job]['trigger']['pause_status']
job_url = job_data[job]['trigger']['file_arrival']['url']
job_cluster_key = job_data[job]['job_clusters'][0]['job_cluster_key']
job_email_notifications = job_data[job]['email_notifications']['on_failure']
job_task_key0 = job_data[job]['tasks'][0]['task_key']
job_task_key1 = job_data[job]['tasks'][1]['task_key']
job_notebook_path0 = job_data[job]['tasks'][0]['notebook_task']['notebook_path']
job_notebook_path1 = job_data[job]['tasks'][1]['notebook_task']['notebook_path']
job_depends_on = job_data[job]['tasks'][1]['depends_on'][0]['task_key']

# Job tests
def test_job_file_name_case_type():
    """
    Checks if job file name is in snake case.
    """
    assert Checks.case_type(job_file_name) == 'snake_case',(
        f"Job File: {job_file_name}"
        )

def test_job_case_type():
    """
    Checks if job is in snake case.
    """
    assert Checks.case_type(job) == 'snake_case',(
        f"Job Name: {job}"
        )

def test_job_name_case_type():
    """
    Checks if job name is in snake case.
    """
    assert Checks.case_type(job_name) == 'snake_case',(
        f"Job Name: {job_name}"
        )

def test_group_name():
    """
    Checks if job group name is 'users'.
    """
    assert job_group_name == 'users',(
        f"Group Name: {job_group_name}"
        )

def test_permission_level():
    """
    Checks if job permission level is 'CAN_MANAGE'.
    """
    assert job_permission_level == 'CAN_MANAGE',(
        f"Permission Level: {job_permission_level}"
        )

def test_job_url_prefix():
    """
    Checks if job url prefix is 'abfss://'.
    """
    assert job_url.startswith('abfss://self-serve@aznednaprodl01.dfs.core.windows.net/') is True,(
        f"Job URL: {job_url}. Prefix should be 'abfss://self-serve@aznednaprodl01.dfs.core.windows.net/'"
        )

def test_raw_job_url_consistency():
    """
    Test for consistency between raw source file and job url.
    """
    job_url_suffix = job_url.split('abfss://self-serve@aznednaprodl01.dfs.core.windows.net/', 1)[-1]
    assert raw_source_name == job_url_suffix, (
        f"Raw Source File: {raw_source_name}, Job URL: {job_url_suffix}"
        )

def test_job_cluster_key():
    """
    Checks if job cluster key is small_cluster.
    """
    assert job_cluster_key == 'small_cluster',(
        f"Job Cluster Key: {job_cluster_key}"
        )

def test_job_task_key0_case_type():
    """
    Checks if job task keys are in snake case.
    """
    assert Checks.case_type(job_task_key0) == 'snake_case',(
        f"Job Task Key: {job_task_key0}"
        )

def test_job_task_key1_case_type():
    """
    Checks if job task keys are in snake case.
    """
    assert Checks.case_type(job_task_key1) == 'snake_case',(
        f"Job Task Key: {job_task_key1}"
        )

def test_task_keys_prefix_extract():
    """
    Checks if job task keys have prefix 'extract_'.
    """
    assert job_task_key0.startswith('extract_') is True,(
        f"Job Task Key: {job_task_key0}. Prefix should be 'extract_'"
        )

def test_task_keys_prefix_conformed():
    """
    Checks if job task keys have prefix 'conform_'.
    """
    assert job_task_key1.startswith('conform_') is True,(
        f"Job Task Key: {job_task_key1}. Prefix should be 'conform_'"
        )

def test_depends_on():
    """
    Checks if job task key1 depends on job task key0.
    """
    assert job_depends_on == job_task_key0,(
        f"Job Task Key: {job_task_key1} should depend on Job Task Key: {job_task_key0}"
        )

def test_job_name_consistency():
    """
    Test for consistency between job name and task keys.
    """
    file_name_suffix = job_file_name.split('_', 1)[1]  # Extract the part after 'job_'
    extract_task_suffix = job_task_key0.split('_', 1)[1]
    conform_task_suffix = job_task_key1.split('_', 1)[1]

    assert file_name_suffix == job_name == extract_task_suffix == conform_task_suffix, (
        f"File Name: {job_file_name}, Job Name: {job_name}, Extract Task Key: {job_task_key0}, Conform Task Key: {job_task_key1}"
        )