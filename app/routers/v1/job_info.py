from fastapi import APIRouter, Request, Header
from fastapi_utils.cbv import cbv
from app.models.hpc_models import HPCJobInfoResponse
from app.commons.logger_services.logger_factory_service import SrvLoggerFactory
from app.resources.error_handler import catch_internal
from app.models.base_models import EAPIResponseCode
import json
import requests

router = APIRouter()
_API_TAG = 'V1 job info'
_API_NAMESPACE = "api_hpc_job_info"

@cbv(router)
class HPCJobInfo:

    def __init__(self):
        self._logger = SrvLoggerFactory(_API_NAMESPACE).get_logger()
        
    
    @router.get("/hpc/job/{job_id}", tags=[_API_TAG],
                 response_model=HPCJobInfoResponse,
                 summary="Get HPC Job Info")
    @catch_internal(_API_NAMESPACE)
    async def hpc_job_info(self, username: str, slurm_host: str, job_id: str, Authorization: str = Header(...)):
        '''
        Retrieve HPC Job Info
        '''
        self._logger.info("API hpc_job_info".center(80, '-'))
        api_response = HPCJobInfoResponse()
        try:
            url = 'https://%s/slurm/v0.0.36/job/%s'%(slurm_host, job_id)
            headers = {
                        'Content-Type': 'application/json',
                        'X-SLURM-USER-NAME': username,
                        'X-SLURM-USER-TOKEN': Authorization
                        }

            proxies={"https":""}
            r = requests.get(url, headers = headers, verify = False, proxies=proxies)
            if not r.status_code == 200:
                    raise Exception(f"Status: {r.status_code}. Error: {r.text}")
            
            response = r.json()
            response_info = {"job_id":job_id, "job_state":response["jobs"][0]["job_state"],
                "standard_error":response["jobs"][0]["standard_error"], "standard_input":response["jobs"][0]["standard_input"],
                "standard_output":response["jobs"][0]["standard_output"]}
            self._logger.info(f"Job info response: {response_info}. Status code: {r.status_code}")
            api_response.result = response_info
            api_response.error_msg = ""
            api_response.code = EAPIResponseCode.success
            return api_response.json_response()
        except Exception as e:
            api_response.result = []
            error_msg = str(e)
            error = f"Retrieval of HPC job info failed: {error_msg}"
            api_response.error_msg = error
            self._logger.error(error)
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()
