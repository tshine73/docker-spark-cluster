FROM openjdk:17-jdk-slim AS builder

ENV PYTHON_VERSION=3.12.8

RUN apt update -y && apt upgrade -y && apt install -y curl vim wget ssh net-tools ca-certificates build-essential gdb lcov pkg-config libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev libmpdec-dev
RUN cd /opt && \
    wget "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz" && \
    tar -xzvf "Python-${PYTHON_VERSION}.tgz" && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make -j `nproc` && \
    ln -s /opt/Python-${PYTHON_VERSION}/python /usr/local/bin/python && \
    ln -s /opt/Python-${PYTHON_VERSION}/python /usr/local/bin/python3 && \
    ln -s /opt/Python-${PYTHON_VERSION}/python /usr/local/bin/python3.12 && \
    rm ../Python-${PYTHON_VERSION}.tgz && \
    python -m ensurepip --upgrade && \
    pip3 install --upgrade setuptools



FROM builder

COPY notebook /opt/notebook
COPY requirements.txt /opt/requirements.txt
COPY data /opt/data
RUN rm -rf /opt/notebook/.ipynb_checkpoints \
&& pip3 install -r /opt/requirements.txt

WORKDIR /opt/notebook

EXPOSE 8888

CMD ["jupyter", "lab", "--allow-root", "--ip=0.0.0.0", "--NotebookApp.token=nl-data"]

