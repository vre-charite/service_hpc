# Copyright 2022 Indoc Research
# 
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
# 
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# 

from fastapi import APIRouter, Request, Header
from fastapi_utils.cbv import cbv
from app.models.hpc_models import HPCJobPost, HPCJobResponse
from app.commons.logger_services.logger_factory_service import SrvLoggerFactory
from app.resources.error_handler import catch_internal
from app.models.base_models import EAPIResponseCode
import json
import requests

router = APIRouter()
_API_TAG = 'V1 job submit'
_API_NAMESPACE = "api_hpc_job_submit"

@cbv(router)
class HPCJobSubmit:

    def __init__(self):
        self._logger = SrvLoggerFactory(_API_NAMESPACE).get_logger()
        

    @router.post("/hpc/job", tags=[_API_TAG],
                 response_model=HPCJobResponse,
                 summary="Submit HPC Job")
    @catch_internal(_API_NAMESPACE)
    async def hpc_job(self, request: HPCJobPost, Authorization: str = Header(...)):
        '''
        Submit HPC Job
        '''
        self._logger.info("API hpc_job".center(80, '-'))
        api_response = HPCJobResponse()

        try:
            req = request.json()
            payload = json.loads(req)
            url = '%s://%s/slurm/v0.0.36/job/submit'%(payload['protocol'], payload['slurm_host'])
            headers = {
                        'Content-Type': 'application/json',
                        'X-SLURM-USER-NAME': payload['username'],
                        'X-SLURM-USER-TOKEN': Authorization
                    }
            
            r = requests.post(url, headers = headers, json = payload['job_info'], verify = False, proxies = {payload['protocol']:""})
            if not r.status_code == 200:
                api_response.error_msg = r.text
                self._logger.error(r.text)
                api_response.code = EAPIResponseCode(r.status_code)
                return api_response.json_response()
                        
            response = r.json()
            response_info = {"job_id":response["job_id"]}
            self._logger.info(f"Job submission response: {response_info}: Status code: {r.status_code}")
            api_response.result = response_info
            api_response.error_msg = ""
            api_response.code = EAPIResponseCode.success
            return api_response.json_response()
        except Exception as e:
            api_response.result = []
            error_msg = str(e)
            error = f"HPC job submission error: {error_msg}"
            api_response.error_msg = error
            self._logger.error(error)
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()
