
import requests_API_Inter as reqAPI
import rw_tokens


# Function to retrieve the location of the certificates
def get_certificates():
    certificate_file = './Inter_API-Chave_e_Certificado/Inter API_Certificado.crt'.encode(
        'utf-8')

    # Path to your private key file
    private_key_file = './Inter_API-Chave_e_Certificado/Inter API_Chave.key'.encode(
        'utf-8')

    return (certificate_file, private_key_file)


def get_token(request_scope):

    certificate_file, private_key_file = get_certificates()

    client_id = 'a16b6831-76a3-4bc9-a464-83f949d47365'
    client_secret = '6322d880-31e3-4356-b81e-94cb23b773ea'

    response_token_request = reqAPI.token_request(request_scope,
                                                  certificate_file, private_key_file,
                                                  client_id, client_secret)

    token = response_token_request.json()['access_token']

    return token


def update_auth_token():

    token_cob_write = get_token('cob.write')
    token_cob_read = get_token('cob.read')

    # Write tokens to file
    rw_tokens.write_token_file('cob.write', token_cob_write, 'cob.read', token_cob_read)

    return



def create_pix(price):

    #### ADD ERROR TREATMENT CODE HERE ?? #### DO NOT RETURN EVERYTHING AS USUAL IF QR CODE GENERATION FAILS

    certificate_file, private_key_file = get_certificates()
    #token_cob_write = get_token('cob.write')
    token_cob_write = rw_tokens.read_token_file()['cob.write']

    chave_pix = "10960792000108"

    response_cob_pix = reqAPI.request_cob_pix(token_cob_write, price, chave_pix, certificate_file, private_key_file)

    print(response_cob_pix)
    print(response_cob_pix.json())

    pix_qrcode_copiaecola = response_cob_pix.json()['pixCopiaECola']
    pix_txid = response_cob_pix.json()['txid']

    return pix_qrcode_copiaecola, pix_txid


def verify_status_pix(txid):

    certificate_file, private_key_file = get_certificates()
    #token_cob_read = get_token('cob.read')
    token_cob_read = rw_tokens.read_token_file()['cob.read']

    response_status_cob_pix = reqAPI.request_status_cobranca(token_cob_read, txid, certificate_file, private_key_file)

    # Possíveis respostas:
    # 'ATIVA': Pix está ativo e ainda não foi pago
    # 'CONCLUIDA': Pagamento realizado
    # Outros: ver documentação e tratar casos!
    status_cob_pix = response_status_cob_pix.json()['status']

    return status_cob_pix


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    pix_copiaecola, txid = create_pix(2.50)

    print(pix_copiaecola)
    print(txid)

    status_cob_pix = verify_status_pix(txid)

    print(status_cob_pix)

