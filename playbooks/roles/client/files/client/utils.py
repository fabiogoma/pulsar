import logging
import sys

def generateLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    log_format = "%(asctime)s.%(msecs)03d %(levelname)s  [%(thread)d] %(funcName)s:%(lineno)d | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def terminateProcess(signalNumber, frame):
    print("")
    print("Exiting gracefully")
    sys.exit()