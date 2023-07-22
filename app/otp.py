import logging

logger = logging.getLogger(__name__)

# Create another logger specifically.
otpLogger = logging.getLogger("testing.otp")

def otp() -> str:
    logger.info("generate code")
    code = "123456"

    phone_number = "+85298765432"
    logger.info("send OTP")

    otpLogger.info("%s: %s", phone_number, code)

    return "otp"
