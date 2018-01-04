FROM centos:latest
MAINTAINER Dushyant Khosla <dushyant.khosla@pmi.com>

# Install Essentials
RUN yum -y update
RUN yum -y upgrade
RUN yum -y install epel-release

# Install Python, Upgrade Pip
RUN yum -y install python-dev \
                   python-setuptools \
                   python-pip
RUN pip install --upgrade pip

# Install other non-python libraries
RUN yum -y install tmux \
                   bzip2 \
                   wget \
                   curl-devel

# Install Development Tools
RUN yum -y groupinstall "Development Tools"
RUN yum -y install gettext-devel openssl-devel perl-CPAN perl-devel zlib-devel

# Install latest version of Git
RUN yum -y remove git
RUN wget https://github.com/git/git/archive/v2.15.1.tar.gz -O git.tar.gz
RUN tar -zxf git.tar.gz
RUN rm -f git.tar.gz
WORKDIR git-2.15.1
RUN make configure
RUN ./configure --prefix=/usr/local
RUN make install
RUN rm -rf /git-2.15.1/

# Clean up
RUN yum -y autoremove
RUN yum clean all
RUN rm -rf /var/cache/yum

# Start Here
WORKDIR /home/
RUN git clone https://github.com/dushyantkhosla/ds-template-01.git
WORKDIR /home/ds-template-01

# Install basic packages
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["bash"]
