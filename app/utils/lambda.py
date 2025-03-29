import requests

from app.utils.constants import AWS_CHECK_IP_URL, REQUEST_TIMEOUT


def get_lambda_ip():
    response = requests.get(AWS_CHECK_IP_URL, timeout=REQUEST_TIMEOUT)
    return response.text.strip()

def lambda_handler(_event, _context):
    # lambda_ip = get_lambda_ip()
    pass
