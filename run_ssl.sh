cd ssl
cat ssl.crt chain_all_ssl.crt > cert.crt
openssl x509 -inform PEM -in cert.crt > linebot.pem
openssl rsm -in ssl.key -out linebot.key