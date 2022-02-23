#
# SemEHR Dockerfile
#

###############
# Build GCP
###############
FROM openjdk:11 AS gcpbuild
WORKDIR '/opt/'

RUN apt-get update && \ 
    apt-get install -y ant  && \
    git clone https://github.com/GateNLP/gcp.git

WORKDIR '/opt/gcp'
RUN apt-get install -y maven
RUN git checkout 3.2 && mvn compile && mvn test

FROM ubuntu:20.04
LABEL org.opencontainers.image.authors="honghan.wu@gmail.com, paul.d.mitchell@ed.ac.uk"
LABEL org.opencontainers.image.vendor="Edinburgh-Cancer-Informatics"

###########
# Build Bio-YODIE
###########
FROM openjdk:11 AS biobuild
WORKDIR '/opt/'

RUN apt-get update && \ 
    apt-get install -y ant  && \
    curl -L 'https://github.com/GateNLP/gate-core/releases/download/v8.5.1/gate-developer-8.5.1-distro.zip' > gate-8.5.1.zip && \
    unzip gate-8.5.1.zip && \ 
    mv gate-developer-8.5.1 gate && \ 
    rm gate-8.5.1.zip
ENV GATE_HOME '/opt/gate'

RUN git clone https://github.com/GateNLP/Bio-YODIE.git
RUN cd /opt/Bio-YODIE && \
    git pull --recurse-submodules=on-demand && \
    git submodule update --init --recursive && \
    plugins/compilePlugins.sh



########
# Pre-reqs
########
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
	curl \
	openjdk-11-jdk \
	unzip \
	git \
    python3 \
    python3-pip \
    wget \
    python3-setuptools \
    python3-dev \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    build-essential

ENV JAVA_HOME /usr/lib/jvm/open-jdk/
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/

WORKDIR '/opt/gcp/'
COPY --from=gcpbuild /opt/gcp gcp-3.2

ENV GCP_HOME '/opt/gcp/gcp-3.2'

########
# Gate, Bio-Yodie
########

ENV PATH "$PATH:$GCP_HOME:$GATE_HOME/bin"
RUN curl -L 'https://cogstack.rosalind.kcl.ac.uk/exports/bio-yodie-1.2.1-se.tar.gz' > bio-yodie-1.2.1-se.tar.gz && tar xzvf bio-yodie-1.2.1-se.tar.gz && rm bio-yodie-1.2.1-se.tar.gz
RUN mv bio-yodie-1.2.1 bio-yodie-1-2-1

RUN cd /opt/gcp/gcp-2.5-18658/lib
WORKDIR '/opt/gcp/gcp-2.5-18658/lib'
RUN curl -L 'https://cogstack.rosalind.kcl.ac.uk/exports/customised_handlers.tar.gz' > customised_handlers.tar.gz && tar xzvf customised_handlers.tar.gz && cp customised_handlers/* ./ && rm -fr customised_handlers && rm -f customised_handlers.tar.gz

########
# python & libraries for SemEHR
########
RUN pip install requests
RUN pip install lxml
RUN pip install pyquery
RUN pip install joblib
RUN pip install urllib3
RUN pip install Elasticsearch
RUN apt-get -y install python-mysqldb

RUN apt-get -y install unixodbc unixodbc-dev libmysqlclient-dev freetds-dev tdsodbc
RUN pip install pyodbc

# mysql odbc
RUN curl -L 'https://cdn.mysql.com//Downloads/Connector-ODBC/8.0/mysql-connector-odbc-8.0.16-linux-ubuntu19.04-x86-64bit.tar.gz' > mysql-connector-odbc-8.0.16-linux-ubuntu19.04-x86-64bit.tar.gz && tar xzvf mysql-connector-odbc-8.0.16-linux-ubuntu19.04-x86-64bit.tar.gz && cp mysql-connector-odbc-8.0.16-linux-ubuntu19.04-x86-64bit/lib/* /usr/lib && mysql-connector-odbc-8.0.16-linux-ubuntu19.04-x86-64bit/bin/myodbc-installer -d -n MySQL -a -t DRIVER=/usr/lib/libmyodbc8w.so && rm -fr mysql-connector-odbc-8.0.16-linux-ubuntu19.04-x86-64bit && rm -f mysql-connector-odbc-8.0.16-linux-ubuntu19.04-x86-64bit.tar.gz

########
# SemEHR
########
RUN mkdir /opt/semehr
WORKDIR '/opt/semehr'
RUN cd /opt/semehr
RUN mkdir /opt/semehr/CogStack-SemEHR


ENV semehr_path '/opt/semehr/CogStack-SemEHR'
ENV PATH "$PATH:$semehr_path:/opt/semehr/"
ENV CLASSPATH "$GATE_HOME/bin"

RUN curl -L 'https://cogstack.rosalind.kcl.ac.uk/exports/semehr.sh.txt' > semehr.sh
RUN chmod a+x semehr.sh

RUN mkdir /data/
RUN mkdir /data/output_docs
RUN mkdir /data/input_docs
RUN mkdir /data/smehr_results

########
# entrypoint
########
ENTRYPOINT ["semehr.sh"]
