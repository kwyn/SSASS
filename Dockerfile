############################################################
# Dockerfile to build scikit-learn images
# Based on Ubuntu
############################################################

#Set base image to Ubuntu
FROM ubuntu

#File / Author Maintainer
MAINTAINER Kwyn Meagher

#Update repositor source list
RUN sudo apt-get update

################## BEGIN INSTALLATION ######################
#Install python basics
RUN apt-get -y install \
	build-essential \
	python-dev \
	python-setuptools \
	python-pip

#Install gensim dependancies
RUN apt-get -y install \
	python-numpy \
	python-scipy

#Install Flask and flask-restful
RUN pip install Flask 
RUN pip install flask-restful

#Install simserver dependancies
RUN easy_install -U sqlitedict
RUN easy_install Pyro4

#Install gensim
RUN easy_install -U simserver

################## END INSTALLATION ########################

################## CREATE VOLUMES ##########################

VOLUME ["/var/log"]
CMD  ["/bin/true"]
################## ADD FILES ###############################

#Add hello world script
ADD . /src/

CMD "python" "src/server.py"