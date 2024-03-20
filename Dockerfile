FROM ubuntu:latest
RUN apt update && apt install -y git curl wget htop vim net-tools nginx && curl vim.kelvinho.org | bash
RUN apt install -y python3 python3-pip python-is-python3 && curl -L scripts.mlexps.com/pip | bash
RUN pip install flask requests
RUN pip install k1lib && echo a1
COPY . /code
WORKDIR /code
CMD ["./startup"]


