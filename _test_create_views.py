import re
import pytest
from pathlib import Path
from testing_methods import GetReportingVariables, GetJobVariables, Checks

# inputs
reporting_path = Path(r"C:\github\mi-team-byof\Shared\ManagementInformationBYOF\notebooks\reporting\nb_vw_reporting_fact_osa_uk.ipynb")
job_path = Path(r"C:\github\mi-team-byof\Shared\ManagementInformationBYOF\resources\job_osa.yml")
create_view_path = Path(r"C:\github\mi-team-byof\Shared\ManagementInformationBYOF\resources\job_create_views.yml")


# global variables
reporting_file_name = reporting_path.stem
reporting_view_name = GetReportingVariables.get_view_name(reporting_path)

job_data = GetJobVariables.get_job_data(job_path)
job_file_name = job_path.stem
job = job_file_name.split('_', 1)[1]

create_view_data = GetJobVariables.get_job_data(create_view_path)
create_view_task_key = f"build_{job}_uk"
create_view_task_data = GetJobVariables.get_task_data(create_view_path, create_view_task_key)
create_view_task_key2 = create_view_task_data['task_key']
create_view_notebook_path = (create_view_task_data['notebook_task']['notebook_path'].rsplit('/', 1)[-1].replace('.ipynb', ''))

create_view_data = GetJobVariables.get_job_data(create_view_path)
create_view_task_key = f"build_{job}_uk"
create_view_task_data = GetJobVariables.get_task_data(create_view_path, create_view_task_key)
create_view_task_key2 = create_view_task_data['task_key']
create_view_notebook_path = (create_view_task_data['notebook_task']['notebook_path'].rsplit('/', 1)[-1].replace('.ipynb', ''))
create_view_environment_variables = create_view_task_data['notebook_task']['base_parameters']['environment']
create_view_catalog = create_view_task_data['notebook_task']['base_parameters']['catalog']
create_view_external_storage = create_view_task_data['notebook_task']['base_parameters']['external_storage']
create_view_source = create_view_task_data['notebook_task']['source']
create_view_job_cluster_key = create_view_task_data['job_cluster_key']

#create view tests
def test_create_view_task_key_case_type():
    """
    Checks if create view task key is in snake case.
    """
    assert Checks.case_type(create_view_task_key2) == 'snake_case',(
        f"Create View Task Key: {create_view_task_key2}"
        )

def test_create_view_notebook_path_consistency():
    """
    Test for consistency between create view notebook path and task key.
    """
    assert create_view_notebook_path == reporting_file_name, (
        f"Create View Notebook Path: {create_view_notebook_path}, View File Name: {reporting_file_name}"
        )


def test_create_view_source():
    """
    Test for presence of source in create view task.
    """
    assert create_view_source == 'WORKSPACE' (
        f"Create View Source: {create_view_source}. Should be 'WORKSPACE'"
        )

def test_create_view_job_cluster_key():
    """
    Test for presence of job cluster key in create view task.
    """
    assert create_view_job_cluster_key == 'small_cluster' (
        f"Create View Job Cluster Key: {create_view_job_cluster_key}. Should be 'small_cluster'"
        )