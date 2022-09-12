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

from fastapi import APIRouter
from fastapi import Header
from fastapi_utils.cbv import cbv
from app.models.hpc_models import HPCNodesResponse
from app.models.hpc_models import HPCNodeResponse
from app.models.hpc_models import HPCPartitonsResponse
from app.models.hpc_models import HPCPartitionResponse
from app.commons.logger_services.logger_factory_service import SrvLoggerFactory
from app.resources.error_handler import catch_internal
from app.models.base_models import EAPIResponseCode
import requests
import re

router = APIRouter()
_API_NAMESPACE = "api_hpc_cluster_info"

# SLURM header

class Headers:
    def __init__(self, username, Authorization):
        self.header = {
                        'Content-Type': 'application/json',
                        'X-SLURM-USER-NAME': username,
                        'X-SLURM-USER-TOKEN': Authorization
                        }

@cbv(router)
class HPCClusterInfo:

    def __init__(self):
        self._logger = SrvLoggerFactory(_API_NAMESPACE).get_logger()
    
    
    # HPC Nodes
    
    @router.get("/hpc/nodes", tags=['V1 Node info'],
                 response_model=HPCNodesResponse,
                 summary="Get HPC Nodes Info")
    @catch_internal(_API_NAMESPACE)
    async def hpc_nodes_info(self, username: str, slurm_host: str, protocol: str, Authorization: str = Header(...)):
        '''
        Retrieve HPC Nodes Info (All)
        '''
        self._logger.info("API hpc_nodes_info".center(80, '-'))
        api_response = HPCNodesResponse()
        headers_get = Headers(username, Authorization)
        try:
            url = f'%s://{slurm_host}/slurm/v0.0.36/nodes/'% protocol
            r = requests.get(url, headers = headers_get.header, verify = False, proxies={f"{protocol}":""})
            if not r.status_code == 200:
                    api_response.result = []
                    api_response.error_msg = f"Retrieval of HPC nodes info failed: {r.text}"
                    self._logger.error(r.text)
                    api_response.code = EAPIResponseCode(r.status_code)
                    return api_response.json_response()

            response = r.json()
            response_info = []
            for i in response["nodes"]:
                response_info.append({
                    i["name"]:{
                        "cores": i["cores"],
                        "cpu": i["cpus"],
                        "free_memory": i["free_memory"],
                        "gpus": re.split('[( :]', i["gres"], 2)[-1].split("(", 1)[0],
                        "threads": i["threads"],
                        "state": i["state"]

                    }

                })

            self._logger.info(f"Nodes info response: {response_info}. Status code: {r.status_code}")
            api_response.result = response_info
            api_response.error_msg = ""
            api_response.code = EAPIResponseCode.success
            return api_response.json_response()
        except Exception as e:
            api_response.result = []
            error_msg = str(e)
            error = f"Retrieval of HPC nodes info failed: {error_msg}"
            api_response.error_msg = error
            self._logger.error(error)
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()



    # HPC Node (Specific)
    
    @router.get("/hpc/nodes/{node_name}", tags=['V1 Node info'],
                 response_model=HPCNodeResponse,
                 summary="Get HPC Node Info (single)")
    @catch_internal(_API_NAMESPACE)

    async def hpc_node_info(self, username: str, slurm_host: str, node_name: str, protocol: str, Authorization: str = Header(...)):
        '''
        Retrieve HPC Node Info (Specific)
        '''
        self._logger.info("API hpc_node_info".center(80, '-'))
        api_response = HPCNodeResponse()
        headers_get = Headers(username, Authorization)
        try:
            url = '%s://%s/slurm/v0.0.36/node/%s'%(protocol, slurm_host, node_name)
            r = requests.get(url, headers = headers_get.header, verify = False, proxies={f"{protocol}":""})
            if not r.status_code == 200:
                    api_response.result = []
                    api_response.error_msg = f"Retrieval of HPC node info failed: {r.text}"
                    self._logger.error(r.text)
                    api_response.code = EAPIResponseCode(r.status_code)
                    return api_response.json_response()

            res = r.json()
            response = res['nodes'][0]
            response_info = []
            response_info.append({
                response["name"]:{
                    "cores": response["cores"],
                    "cpu": response["cpus"],
                    "free_memory": response["free_memory"],
                    "gpus": re.split('[( :]', response["gres"], 2)[-1].split("(", 1)[0],
                    "threads": response["threads"],
                    "state": response["state"]

                    }

                })

            self._logger.info(f"Node info response: {response_info}. Status code: {r.status_code}")
            api_response.result = response_info
            api_response.error_msg = ""
            api_response.code = EAPIResponseCode.success
            return api_response.json_response()
        except Exception as e:
            api_response.result = []
            error_msg = str(e)
            error = f"Retrieval of HPC node info failed: {error_msg}"
            api_response.error_msg = error
            self._logger.error(error)
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()


    
    # HPC Partitions
    
    @router.get("/hpc/partitions", tags=['V1 Partition info'],
                 response_model=HPCPartitonsResponse,
                 summary="Get HPC Partitions Info")
    @catch_internal(_API_NAMESPACE)

    async def hpc_partitions_info(self, username: str, slurm_host: str, protocol: str, Authorization: str = Header(...)):
        '''
        Retrieve Partition Info (All)
        '''
        self._logger.info("API hpc_partitions_info".center(80, '-'))
        api_response = HPCPartitonsResponse()
        headers_get = Headers(username, Authorization)
        try:
            url = f'%s://{slurm_host}/slurm/v0.0.36/partitions/'% protocol
            r = requests.get(url, headers = headers_get.header, verify = False, proxies={f"{protocol}":""})
            if not r.status_code == 200:
                    api_response.result = []
                    api_response.error_msg = f"Retrieval of HPC partitions info failed: {r.text}"
                    self._logger.error(r.text)
                    api_response.code = EAPIResponseCode(r.status_code)
                    return api_response.json_response()

            response = r.json()
            response_info = []
            for i in response["partitions"]:
                response_info.append({
                    i["name"]:{
                        "nodes": i["nodes"].split(","),
                        "tres": i["tres"]

                    }

                })

            self._logger.info(f"Partitions info response: {response_info}. Status code: {r.status_code}")
            api_response.result = response_info
            api_response.error_msg = ""
            api_response.code = EAPIResponseCode.success
            return api_response.json_response()
        except Exception as e:
            api_response.result = []
            error_msg = str(e)
            error = f"Retrieval of HPC partitions info failed: {error_msg}"
            api_response.error_msg = error
            self._logger.error(error)
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()



    # HPC Partition (Specific)
    
    @router.get("/hpc/partitions/{partition_name}", tags=['V1 Partition info'],
                 response_model=HPCPartitionResponse,
                 summary="Get HPC Partition Info (single)")
    @catch_internal(_API_NAMESPACE)

    async def hpc_partition_info(self, username: str, slurm_host: str, partition_name: str, protocol: str, Authorization: str = Header(...)):
        '''
        Retrieve HPC Partition Info (Specific)
        '''
        self._logger.info("API hpc_partition_info".center(80, '-'))
        api_response = HPCPartitionResponse()
        headers_get = Headers(username, Authorization)
        try:
            url = '%s://%s/slurm/v0.0.36/partition/%s'%(protocol, slurm_host, partition_name)
            r = requests.get(url, headers = headers_get.header, verify = False, proxies={f"{protocol}":""})
            if not r.status_code == 200:
                    api_response.result = []
                    api_response.error_msg = f"Retrieval of HPC partition info failed: {r.text}"
                    self._logger.error(r.text)
                    api_response.code = EAPIResponseCode(r.status_code)
                    return api_response.json_response()

            res = r.json()
            response = res['partitions'][0]
            response_info = []
            response_info.append({
                response["name"]:{
                    "nodes": response["nodes"].split(","),
                    "tres": response["tres"]

                    }

                })

            self._logger.info(f"Partition info response: {response_info}. Status code: {r.status_code}")
            api_response.result = response_info
            api_response.error_msg = ""
            api_response.code = EAPIResponseCode.success
            return api_response.json_response()
        except Exception as e:
            api_response.result = []
            error_msg = str(e)
            error = f"Retrieval of HPC partition info failed: {error_msg}"
            api_response.error_msg = error
            self._logger.error(error)
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()
