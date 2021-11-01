from pydantic import Field
from app.models.base_models import APIResponse, BaseModel


class HPCAuthResponse(APIResponse):
    """
    HPC Auth Response Class
    """
    result: dict = Field({}, example={
            "code": 200,
            "error_msg": "",
            "result":
                {
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                }
        }
    )

class HPCJobPost(BaseModel):
    """
    HPC Job POST Class
    """
    slurm_host: str
    username: str
    job_info: dict


class HPCJobResponse(APIResponse):
    """
    HPC Job Response Class
    """
    result: dict = Field({}, example={
        "code": 200,
        "error_msg": "",
        "result": {"job_id": "14425"}
    }
                         )

class HPCJobInfoResponse(APIResponse):
    """
    HPC Job Info Response Class
    """
    result: dict = Field({}, example={
        "code": 200,
        "error_msg": "",
        "result": {"job_id": "14425",
                   "job_state":"RUNNING",
                   "standard_error":"...",
                   "standard_input":"...",
                   "standard_output":"..."}
    }
                         )
                 

