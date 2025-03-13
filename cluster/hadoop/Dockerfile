FROM openjdk:11-jre-slim-bullseye AS builder


ENV PYTHONHASHSEED=1 \
PYTHON_VERSION=3.12.8

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
    pip3 install --upgrade setuptools && \
    pip3 install matplotlib==3.10.0 pandas==2.2.3


FROM builder AS download_builder

ENV SPARK_VERSION=3.5.5 \
HADOOP_VERSION=3.4.1 \
HADOOP_MAJOR_VERSION=3

RUN wget --no-verbose -O apache-hadoop.tgz "https://dlcdn.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" && \
mkdir -p /opt/hadoop && \
tar -xf apache-hadoop.tgz -C /opt/hadoop --strip-components=1 && \
rm apache-hadoop.tgz

RUN wget --no-verbose -O apache-spark.tgz "https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_MAJOR_VERSION}.tgz" \
&& mkdir -p /opt/spark \
&& tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
&& rm apache-spark.tgz


FROM download_builder AS bigdata_cluster

WORKDIR /opt

COPY start-hadoop.sh ./
COPY conf/* hadoop/etc/hadoop/

ENV HADOOP_HOME="/opt/hadoop" \
SPARK_HOME=/opt/spark

ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop \
PATH=$HADOOP_HOME/bin:$SPARK_HOME/bin:$PATH

EXPOSE 8088 9870


CMD ["/bin/bash", "-c", "/opt/start-hadoop.sh; sleep infinity"]