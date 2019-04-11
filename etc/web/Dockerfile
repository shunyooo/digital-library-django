FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN sed -i '/jessie-updates/d' /etc/apt/sources.list
RUN apt-get update && apt-get -y install poppler-utils python-poppler vim

# mysql client
ENV MYSQL_PWD password
RUN echo "mysql-server mysql-server/root_password password $MYSQL_PWD" | debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password $MYSQL_PWD" | debconf-set-selections
RUN apt-get -y install mysql-server mysql-client

# jupyter extentions 導入
RUN jupyter contrib nbextension install --user
RUN git clone https://github.com/ipython-contrib/IPython-notebook-extensions\
    && cd IPython-notebook-extensions\
    && python3 setup.py install\
    && cd ../\
    && rm -rf IPython-notebook-extensions

# jupyter 設定
RUN jupyter notebook --generate-config
COPY jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

# 起動時用スクリプト
COPY wait.sh /wait.sh
COPY run.sh /run.sh

ADD . /app/