FROM --platform=linux/amd64 python:3.10-alpine AS build

WORKDIR /src
COPY requirements.txt /src
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements.txt

COPY . .
ENTRYPOINT ["python3", "-u", "server.py"]
CMD ["flask", "--version"]

# FROM build

# RUN <<EOF
# apk update
# apk add git
# EOF

# RUN <<EOF
# addgroup -S docker
# adduser -S --shell /bin/bash --ingroup docker vscode
# EOF

# # install Docker tools (cli, buildx, compose)
# COPY --from=gloursdocker/docker / /

# ENTRYPOINT ["python3", "-u", "server.py"]
# CMD ["flask", "--version"]