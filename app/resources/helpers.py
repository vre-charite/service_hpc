import paramiko
import time
import requests
import sys
import json

from app.commons.logger_services.logger_factory_service import SrvLoggerFactory

_logger = SrvLoggerFactory("Helpers").get_logger()

# Get HPC auth token

def get_hpc_jwt_token(token_issuer, username, password = None):
    _logger.info("get_hpc_jwt_token".center(80, '-'))
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(token_issuer, username = username, password = password)
    except Exception as e:
        _logger.error(e)
        ssh_client.close()
    stdin, stdout, stderr = ssh_client.exec_command("scontrol token")
    time.sleep(1)
    out = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    _logger.info(f"HPC stdout: {out}")
    _logger.info(f"HPC stderr: {error}")
    ssh_client.close()
    token = out.split('=')[1]
    _logger.info(f"HPC authorization: {token}")
    return token
    
# Submit slurm job to HPC

def submit_slurm_job(slurm_host, username, token, job_data):
    _logger.info("submit_hpc_job".center(80, '-'))


    url = 'https://%s/slurm/v0.0.36/job/submit'%(slurm_host)
    headers = {
                'Content-Type': 'application/json',
                'X-SLURM-USER-NAME': username,
                'X-SLURM-USER-TOKEN': token
                }
    proxies={"https":""}

    try:
        r = requests.post(
                            url,
                            headers = headers,
                            json = job_data,
                            verify = False,
                            proxies = proxies
                            )
        response = r.json()
        response_info = {"job_id":response["job_id"]}
        _logger.info(f"Job submission response: {response_info}: Status code: {r.status_code}")
        
    except (Exception, JSONDecodeError) as e:
        error = f"Failed POST request for job submit. Status code: {r.status_code}. Error: {e}"
        _logger.error(error)
        
    return response_info


# Retrieve slurm job info

def get_job_info(username, slurm_host, job_id, token):
    _logger.info("get_hpc_job_info".center(80, '-'))

    url = 'https://%s/slurm/v0.0.36/job/%s'%(slurm_host, job_id)
    headers = {
                'Content-Type': 'application/json',
                'X-SLURM-USER-NAME': username,
                'X-SLURM-USER-TOKEN': token
                }

    proxies={"https":""}

    try:
        r = requests.get(url, headers = headers, verify = False, proxies=proxies)
        response = r.json()
        response_info = {"job_id":job_id, "job_state":response["jobs"][0]["job_state"],
            "standard_error":response["jobs"][0]["standard_error"], "standard_input":response["jobs"][0]["standard_input"],
            "standard_output":response["jobs"][0]["standard_output"]}
        _logger.info(f"Job info response: {response_info}. Status code: {r.status_code}")
        
    except (Exception, JSONDecodeError) as e:
        error = f"Failed GET request for job info. Status code: {r.status_code}. Error: {e}"
        _logger.error(error)

    return response_info

