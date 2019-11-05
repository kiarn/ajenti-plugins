import ssl
import socket
import smtplib
from datetime import datetime
from OpenSSL import crypto
# Parallel version for PY3
#from concurrent import futures

now = datetime.now()

def CertLimitSSL(hostname, port):
    """Return standard SSL cert from hostname:port"""
    ctx = ssl.create_default_context()
    s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
    s.connect((hostname, port))
    cert = s.getpeercert()
    s.close()
    return cert

def CertLimitSTARTTLS(hostname):
    """Return SSL cert from STARTTLS connection at hostname:587"""
    connection = smtplib.SMTP()
    connection.connect(hostname,587)
    connection.starttls()
    cert = ssl.DER_cert_to_PEM_cert(connection.sock.getpeercert(binary_form=True))
    connection.quit()
    return crypto.load_certificate(crypto.FILETYPE_PEM, cert)

def checkOnDom(hostname, port='443'):

    port = int(port)
    ## Locale EN to fix
    import locale
    locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

    ## Check per SMTP STARTTLS connection
    if port == 587:
        cert = CertLimitSTARTTLS(hostname)
        limit = datetime.strptime(cert.get_notAfter().decode(),"%Y%m%d%H%M%SZ")
        
    ## Check other standarts SSL cert
    else:
        try:
            cert = CertLimitSSL(hostname, port)
            limit = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y GMT")
        except: #ConnectionRefusedError: ## Only for PY3
            limit = -1

    if limit == -1:
        status = 'danger'
        limit = 'No reponse from host !'
    elif (limit-now).days <= 7:
        status = 'danger'
    elif (limit-now).days <= 14:
        status = 'warning'
    elif (limit-now).days <= 28:
        status = 'info'
    else:
        status = 'success'
    return {'status': status, 'hostname': hostname, 'port':port, 'url':hostname+":"+str(port), 'limit': str(limit)}


## TODO: Parallel version for PY3
# def checkCertDom(sub):
    # tld = sub[0]
    # result = []
    # with futures.ThreadPoolExecutor(20) as executor:
        # res = executor.map(lambda arg:checkOnDom(arg,tld), sub[1:])
        # return len(list(res))
