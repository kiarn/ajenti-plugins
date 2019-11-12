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
    cert = crypto.load_certificate(crypto.FILETYPE_ASN1, s.getpeercert(binary_form=True))
    s.close()
    return cert

def CertLimitSTARTTLS(hostname):
    """Return SSL cert from STARTTLS connection at hostname:587"""
    connection = smtplib.SMTP()
    connection.connect(hostname,587)
    connection.starttls()
    cert = crypto.load_certificate(crypto.FILETYPE_ASN1, connection.sock.getpeercert(binary_form=True))
    connection.quit()
    return cert

def checkOnDom(hostname, port='443'):

    port = int(port)
    cert = False
    notAfter = False
    notBefore = False
    restTime = 0
    
    ## Locale EN to fix
    import locale
    locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

    try:
        if port == 587:
            cert = CertLimitSTARTTLS(hostname)
        else:
            cert = CertLimitSSL(hostname, port)
        notAfter = datetime.strptime(cert.get_notAfter().decode(),"%Y%m%d%H%M%SZ")
        notBefore = datetime.strptime(cert.get_notBefore().decode(),"%Y%m%d%H%M%SZ")
    except: #ConnectionRefusedError: ## Only for PY3
        notAfter = -1

    if notAfter == -1:
        status = 'danger'
        notAfter = 'No reponse from host !'
    elif (notAfter-now).days <= 7:
        status = 'danger'
        restTime = '< 7'
    elif (notAfter-now).days <= 30:
        status = 'warning'
        restTime = '< 14'
    elif (notAfter-now).days <= 60:
        status = 'info'
        restTime = '< 28'
    else:
        status = 'success'
    return {
        'status': status,
        'hostname': hostname,
        'port':port,
        'url':hostname+":"+str(port),
        'notAfter': str(notAfter),
        'restTime': restTime,
        #'certDict': cert if cert else None,
        'notBefore': str(notBefore)
        }


## TODO: Parallel version for PY3
# def checkCertDom(sub):
    # tld = sub[0]
    # result = []
    # with futures.ThreadPoolExecutor(20) as executor:
        # res = executor.map(lambda arg:checkOnDom(arg,tld), sub[1:])
        # return len(list(res))
