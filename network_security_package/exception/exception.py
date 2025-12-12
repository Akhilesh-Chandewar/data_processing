import sys
from types import TracebackType
from typing import Optional
from network_security_package.logging.logger import logger


class NetworkSecurityException(Exception):
    def __init__(
        self, error_message: Exception, error_details: Optional[TracebackType]
    ):
        self.error_message = error_message

        # Extract traceback information
        exc_type, exc_obj, exc_tb = sys.exc_info()

        if exc_tb is not None:
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.lineno = -1
            self.file_name = "Unknown"

    def __str__(self):
        return (
            f"Error occurred in python script [{self.file_name}] "
            f"at line [{self.lineno}] "
            f"with message [{self.error_message}]"
        )


# if __name__ == "__main__":
#     try:
#         logger.info("Entered try block")
#         a = 1 / 0
#     except Exception as e:
#         logger.error("An exception occurred", exc_info=True)
#         raise NetworkSecurityException(e, sys.exc_info()[2])
