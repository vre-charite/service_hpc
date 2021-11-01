from fastapi import APIRouter, Request
from fastapi_utils.cbv import cbv
from app.models.hpc_models import HPCAuthResponse
from app.commons.service_logger.logger_factory_service import SrvLoggerFactory
from app.resources.error_handler import catch_internal
from app.models.base_models import EAPIResponseCode
import paramiko
import time
import sys

router = APIRouter()
_API_TAG = 'V1 auth'
_API_NAMESPACE = "api_hpc_auth"

@cbv(router)
class HPCAuth:

    def __init__(self):
        self._logger = SrvLoggerFactory(_API_NAMESPACE).get_logger()
        
    
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
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(token_issuer, username = username, password = password)
            stdin, stdout, stderr = ssh_client.exec_command("scontrol token")
            time.sleep(1)
            out = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            self._logger.info(f"HPC stdout: {out}")
            self._logger.info(f"HPC stderr: {error}")
            ssh_client.close()
            token = out.split('=')[1]
            self._logger.info(f"HPC authorization: {token}")
            api_response.result = token
            api_response.error_msg = ""
            api_response.code = code = EAPIResponseCode.success
            return api_response.json_response()
        except Exception as e:
            api_response.result = []
            error_msg = str(e)
            error = f"User authorization failed: {error_msg}"
            api_response.error_msg = error
            self._logger.error(error)
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()

