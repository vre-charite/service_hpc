import paramiko
import time
from app.commons.logger_services.logger_factory_service import SrvLoggerFactory

_logger = SrvLoggerFactory("Helpers").get_logger()

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
