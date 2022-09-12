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

import logging
import os, os.path
import sys
from .formatter import formatter_factory
from logging.handlers import TimedRotatingFileHandler


class SrvLoggerFactory:
    def __init__(self, name):
        self.my_formatter = formatter_factory()
        if not os.path.exists("./logs/"):
            os.makedirs("./logs/")
        self.name = name

    def get_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            # File Handler
            handler = TimedRotatingFileHandler("logs/{}.log".format(self.name),
                                               when='D',
                                               interval=1,
                                               backupCount=2)
            handler.setFormatter(self.my_formatter)
            handler.setLevel(logging.DEBUG)
            # Standard Out Handler
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(self.my_formatter)
            stdout_handler.setLevel(logging.DEBUG)
            # Standard Err Handler
            stderr_handler = logging.StreamHandler(sys.stderr)
            stderr_handler.setFormatter(self.my_formatter)
            stderr_handler.setLevel(logging.ERROR)
            # register handlers
            logger.addHandler(handler)
            logger.addHandler(stdout_handler)
            logger.addHandler(stderr_handler)
        return logger
