
import requests
import ssl
import time

########### NEW CODE #################

# SHOULD CONTAIN
# - Function to get certificates, taking nothing as input
# - Function to generate token, taking as input the request scope
# -


# Function to generate token based on the desired request scope
def token_request(request_scope, certificate_file, private_key_file, client_id, client_secret):

    # URL of the authentication service
    auth_service_url = 'https://cdpj.partners.bancointer.com.br/oauth/v2/token'

    # Sample data to send to the authentication service
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': request_scope,
        'grant_type': 'client_credentials'
    }

    # Load the certificate and private key
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certificate_file, keyfile=private_key_file)

    try:
        # Make a POST request to the authentication service
        response = requests.post(auth_service_url, data=data, verify=False, cert=(certificate_file, private_key_file))

        # Check the response status code
        if response.status_code == 200:
            # Authentication successful, process response data
            print("Authentication successful!")
            print(response.json())

        else:
            # Authentication failed, print error message
            print("Authentication failed. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        # Request error occurred, print error message
        print("Error making request:", e)

    return response


def request_cob_pix(token, valor, chave_pix, certificate_file, private_key_file):
    cob_pix_url = "https://cdpj.partners.bancointer.com.br/pix/v2/cob"

    headers_cob_pix = {
        "Authorization": "Bearer " + token,
        "Content-Type": "Application/json"
    }

    body_cob_pix = {
        "calendario": {
            "expiracao": 3600
        },
        "valor": {
            # "original": valor,
            "original": "{:.2f}".format(float(valor)),
            "modalidadeAlteracao": 1
        },
        "chave": chave_pix
    }

    try:
        # Make a POST request to the authentication service
        response = requests.post(cob_pix_url, headers=headers_cob_pix, json=body_cob_pix,
                                 cert=(certificate_file, private_key_file))

        # Check the response status code
        if response.status_code == 201:
            # Request successful
            print("request cob pix successful!")

        else:
            # request failed, print error message
            print("request failed. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        # Request error occurred, print error message
        print("Error making request:", e)

    return response


def request_status_cobranca(token_cob_read, txid, certificate_file, private_key_file):

    headers_cob_pix = {
        "Authorization": "Bearer " + token_cob_read,
        "Content-Type": "Application/json"
    }

    cob_pix_url = "https://cdpj.partners.bancointer.com.br/pix/v2/cob/" + txid

    try:
        # Make a POST request to the authentication service
        response = requests.get(cob_pix_url, headers=headers_cob_pix, cert=(certificate_file, private_key_file))

        # Check the response status code
        if response.status_code == 200:
            # Request successful
            print("get status successful!")

        else:
            # request failed, print error message
            print("request failed. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        # Request error occurred, print error message
        print("Error making request:", e)

    return response





############### OLD CODE ####################








