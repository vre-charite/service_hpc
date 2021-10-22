from fastapi import APIRouter, Depends, Request
from fastapi_utils.cbv import cbv
from app.models.hpc_models import HPCAuthResponse
from app.commons.logger_services.logger_factory_service import SrvLoggerFactory
from app.resources.error_handler import catch_internal
from app.resources.dependencies import *
from app.resources.helpers import *
from app.models.base_models import EAPIResponseCode

router = APIRouter()
_API_TAG = 'V1 HPC'
_API_NAMESPACE = "api_hpc"


@cbv(router)
class APIProject:
    current_identity: dict = Depends(jwt_required)

    def __init__(self):
        self._logger = SrvLoggerFactory(_API_NAMESPACE).get_logger()

    @router.get("/hpc/auth", tags=[_API_TAG],
                response_model=HPCAuthResponse,
                summary="Get HPC authorization")
    @catch_internal(_API_NAMESPACE)
    async def hpc_auth(self, token_issuer, password):
        '''
        Get HPC token for authorization
        '''
        self._logger.info("API hpc_auth".center(80, '-'))
        api_response = HPCAuthResponse()
        self._logger.info("User request")
        try:
            username = self.current_identity['username']
        except (AttributeError, TypeError):
            return self.current_identity
        try:
            result = get_hpc_jwt_token(token_issuer, username, password)
            error = ""
            code = EAPIResponseCode.success
        except AttributeError as e:
            result = []
            error_msg = str(e)
            if 'open_session' in error_msg:
                error = f"User authorization failed"
                self._logger.info(error)
            else:
                error = f"User authorization failed: {error_msg}"
                self._logger.info(error)
            code = EAPIResponseCode.internal_error
        api_response.result = result
        api_response.error_msg = error
        api_response.code = code
        return api_response.json_response()
