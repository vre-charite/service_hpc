from fastapi import APIRouter, Depends, Request, Header
from fastapi_utils.cbv import cbv
from app.models.hpc_models import HPCAuthResponse, HPCJobPost, HPCJobResponse, HPCJobInfoResponse
from app.commons.logger_services.logger_factory_service import SrvLoggerFactory
from app.resources.error_handler import catch_internal
#from app.resources.dependencies import *
from app.resources.helpers import *
from app.models.base_models import EAPIResponseCode

router = APIRouter()
_API_TAG = 'V1 HPC'
_API_NAMESPACE = "api_hpc"


@cbv(router)
class APIProject:

    def __init__(self):
        self._logger = SrvLoggerFactory(_API_NAMESPACE).get_logger()
    
    # hpc token retreival
    
    @router.get("/hpc/auth", tags=[_API_TAG],
                response_model=HPCAuthResponse,
                summary="Get HPC authorization")
    @catch_internal(_API_NAMESPACE)
    async def hpc_auth(self, token_issuer, username, password):
        '''
        Get HPC token for authorization
        '''
        self._logger.info("API hpc_auth".center(80, '-'))
        api_response = HPCAuthResponse()
        self._logger.info("User request")
        try:
            result = get_hpc_jwt_token(token_issuer, username, password)
            error = ""
            code = EAPIResponseCode.success
        except AttributeError as e:
            result = []
            error_msg = str(e)
            if 'open_session' in error_msg:
                error = f"User authorization failed"
                self._logger.error(error)
            else:
                error = f"User authorization failed: {error_msg}"
                self._logger.error(error)
            code = EAPIResponseCode.internal_error
        api_response.result = result
        api_response.error_msg = error
        api_response.code = code
        return api_response.json_response()
        
    # hpc job submission
    
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
            result = submit_slurm_job(payload['slurm_host'], payload['username'], Authorization, payload['job_info'])
            error = ""
            code = EAPIResponseCode.success
        except Exception as e:
            result = []
            error_msg = str(e)
            error = f"Slurm job submission failed: {error_msg}"
            self._logger.error(error)
            code = EAPIResponseCode.internal_error
        api_response.result = result
        api_response.error_msg = error
        api_response.code = code
        return api_response.json_response()


    # hpc job info
    
    @router.get("/hpc/job", tags=[_API_TAG],
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
            result = get_job_info(username, slurm_host, job_id, Authorization)
            error = ""
            code = EAPIResponseCode.success
        except Exception as e:
            result = []
            error_msg = str(e)
            error = f"Retrieval of Slurm job info failed: {error_msg}"
            self._logger.error(error)
            code = EAPIResponseCode.internal_error
        api_response.result = result
        api_response.error_msg = error
        api_response.code = code
        return api_response.json_response()