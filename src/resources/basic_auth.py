## Copyright (c) 2025, Oracle and/or its affiliates.
## All rights reserved. The Universal Permissive License (UPL), Version 1.0 as shown at http://oss.oracle.com/licenses/upl
import os
import re
import logging
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, FastAPI, HTTPException, status

g_logger = logging.getLogger(__name__)


class Auth:
    def __init__(self, validate):
        self.validate = validate

    def validate_env(self):
        try:
            if self.validate:
                if os.getenv("APP_PASSWORD") is not None:
                    value = os.getenv("APP_PASSWORD")
                    if re.fullmatch(r"[A-Za-z0-9@#$%^&+=]{8,}", value):
                        g_logger.info("Password validation completed")
                    else:
                        raise SystemExit(
                            "Exit : Invalid Password Format - Must contains one Capital/One Small/Special character/Number and minimum of 8 chars"
                        )  # Need to add a proper exception
                else:
                    import secrets

                    os.environ["APP_PASSWORD"] = secrets.token_urlsafe(12)
                    print(
                        f"{'System Generated Admin Password -> ':<20}{os.getenv("APP_PASSWORD")}"
                    )

                print(
                    f"--------------------------------------------------------------------------------\n"
                )
                import sys

                sys.stdout.flush()

        except Exception as error:
            print(error)  # Its a direct console log

    @staticmethod
    def verify_auth(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
        correct_username = credentials.username == os.getenv(
            "APP_USER_NAME", "api_user"
        )
        correct_password = credentials.password == os.environ["APP_PASSWORD"]
        if not (correct_username and correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
            return credentials.username
