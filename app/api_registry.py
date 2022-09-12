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

from fastapi import FastAPI
from .routers.v1 import auth
from .routers.v1 import job_submit
from .routers.v1 import job_info
from .routers.v1 import cluster_info

def api_registry(app: FastAPI):
    app.include_router(auth.router, prefix="/v1")
    app.include_router(job_submit.router, prefix="/v1")
    app.include_router(job_info.router, prefix="/v1")
    app.include_router(cluster_info.router, prefix="/v1")

