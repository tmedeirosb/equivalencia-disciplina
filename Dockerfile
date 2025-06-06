# base image  
# FROM python:3.12.11-alpine3.21

FROM alpine:3.22.0
RUN apk --no-cache --update-cache add  python3 py3-pip py3-arrow  py3-pandas py3-scipy py3-numpy py3-matplotlib py3-scikit-learn py3-seaborn

# Install GCC (IFRN fix / required by streamlit)
# RUN apk --no-cache --update-cache add g++ gfortran build-base wget freetype-dev libpng-dev openblas-dev py3-pandas py3-scipy py3-numpy

# setup environment variable  
ENV DockerHOME=/home/app/

# set work directory  
RUN mkdir -p $DockerHOME

# where your code lives  
WORKDIR $DockerHOME

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies  
# RUN pip install --upgrade pip

# copy whole project to your docker home directory. 
COPY . $DockerHOME

# corrige conflito de dependências do dask
RUN pip uninstall -y dask --break-system-packages
RUN pip uninstall -y dask-expr --break-system-packages

# run this command to install all dependencies  
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements-infra.txt --break-system-packages

# port where the Django app runs  
# EXPOSE 8080
EXPOSE 8501

# start server
ENTRYPOINT [ "streamlit", "run", "app-eq-st.py", "--server.address", "0.0.0.0" ]


# --browser.serverPort 8080

# DEBUG
# ENTRYPOINT ["tail", "-f", "/dev/null"]

# OBS: tive vários problemas inicialmente para rodar devido não ter esse 0.0.0.0 (aparentemente o nginx-proxy não consegue usar a porta)