FROM centos:7

RUN yum update -y \
 && yum install -y \
    wget kernel-devel kernel-headers gcc make \
 && yum upgrade -y kernel kernel-devel \
 && rm -rf /var/cache/yum

RUN wget -q https://github.com/git/git/archive/v2.21.0.tar.gz \
 && yum install -y \
    openssl-devel curl-devel expat-devel gettext-devel \
 && rm -rf /var/cache/yum \
 && tar -xvf v2.21.0.tar.gz \
 && ( \
  cd git-* \
   && make prefix=/usr install \
 ) \
 && rm -rf git-* \
 && rm -f v2.21.0.tar.gz

ENV CUDA_VERSION_MAJOR=11
ENV CUDA_VERSION_MINOR=2
ENV CUDA_VERSION_PATCH=0
ENV CUDA_VERSION=$CUDA_VERSION_MAJOR.$CUDA_VERSION_MINOR.$CUDA_VERSION_PATCH
LABEL CUDA_VERSION=$CUDA_VERSION_MAJOR.$CUDA_VERSION_MINOR.$CUDA_VERSION_PATCH

RUN NVIDIA_GPGKEY_SUM=d0664fbbdb8c32356d45de36c5984617217b2d0bef41b93ccecd326ba3b80c87 \
 && curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/D42D0685.pub | sed '/^Version/d' > /etc/pki/rpm-gpg/RPM-GPG-KEY-NVIDIA \
 && echo "$NVIDIA_GPGKEY_SUM  /etc/pki/rpm-gpg/RPM-GPG-KEY-NVIDIA" | sha256sum -c --strict  -

RUN echo -e "[cuda]\n\
name=cuda\n\
baseurl=https://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64\n\
enabled=1\n\
gpgcheck=1\n\
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-NVIDIA" >> /etc/yum.repos.d/cuda.repo

RUN yum update -y \
 && yum install -y \
    cuda-cudart-${CUDA_VERSION_MAJOR}.${CUDA_VERSION_MINOR}.108-1 \
    cuda-compat-${CUDA_VERSION_MAJOR}-${CUDA_VERSION_MINOR} \
 && ln -s cuda-${CUDA_VERSION_MAJOR}.${CUDA_VERSION_MINOR} /usr/local/cuda \
 && yum clean all \
 && rm -rf /var/cache/yum/*

RUN yum install -y \
    cuda-libraries-${CUDA_VERSION_MAJOR}-${CUDA_VERSION_MINOR}-${CUDA_VERSION}-1 \
    cuda-nvtx-${CUDA_VERSION_MAJOR}-${CUDA_VERSION_MINOR}-${CUDA_VERSION_MAJOR}.${CUDA_VERSION_MINOR}.120-1 \
    libnpp-${CUDA_VERSION_MAJOR}-${CUDA_VERSION_MINOR}-${CUDA_VERSION_MAJOR}.${CUDA_VERSION_MINOR}.0.110-1 \
    libcublas-${CUDA_VERSION_MAJOR}-${CUDA_VERSION_MINOR}-${CUDA_VERSION_MAJOR}.3.1.68-1 \
    libnccl-2.8.4-1+cuda${CUDA_VERSION_MAJOR}.${CUDA_VERSION_MINOR} \
    cuda-command-line-tools-${CUDA_VERSION_MAJOR}-${CUDA_VERSION_MINOR}-${CUDA_VERSION}-1 \
    cuda-libraries-devel-${CUDA_VERSION_MAJOR}-${CUDA_VERSION_MINOR}-${CUDA_VERSION}-1 \
    cuda-minimal-build-${CUDA_VERSION_MAJOR}-${CUDA_VERSION_MINOR}-${CUDA_VERSION}-1 \
    cuda-cudart-devel-${CUDA_VERSION_MAJOR}-${CUDA_VERSION_MINOR}-${CUDA_VERSION_MAJOR}.${CUDA_VERSION_MINOR}.72-1 \
    cuda-nvprof-${CUDA_VERSION_MAJOR}-${CUDA_VERSION_MINOR}-${CUDA_VERSION_MAJOR}.${CUDA_VERSION_MINOR}.67-1 \
    cuda-nvml-devel-${CUDA_VERSION_MAJOR}-${CUDA_VERSION_MINOR}-${CUDA_VERSION_MAJOR}.${CUDA_VERSION_MINOR}.67-1 \
    libcublas-devel-${CUDA_VERSION_MAJOR}-${CUDA_VERSION_MINOR}-${CUDA_VERSION_MAJOR}.3.1.68-1 \
    libnpp-devel-${CUDA_VERSION_MAJOR}-${CUDA_VERSION_MINOR}-${CUDA_VERSION_MAJOR}.${CUDA_VERSION_MINOR}.1.68-1 \
    libnccl-devel-2.8.4-1+cuda${CUDA_VERSION_MAJOR}.${CUDA_VERSION_MINOR} \
 && yum clean all \
 && rm -rf /var/cache/yum/*

ENV CUDNN_VERSION=8.1.1.33
LABEL CUDNN_VERSION=8.1.1.33

RUN yum install -y \
    libcudnn8-${CUDNN_VERSION}-1.cuda${CUDA_VERSION_MAJOR}.${CUDA_VERSION_MINOR} \
    libcudnn8-devel-${CUDNN_VERSION}-1.cuda${CUDA_VERSION_MAJOR}.${CUDA_VERSION_MINOR} \
 && yum clean all \
 && rm -rf /var/cache/yum/* \

ENV PATH=/usr/local/cuda/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/lib64

ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

RUN wget -q https://www.openssl.org/source/openssl-1.1.1w.tar.gz \
 && tar -xf openssl-1.1.1w.tar.gz \
 && cd openssl-1.1.1w \
 && ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib \
 && make -j$(nproc) \
 && make install \
 && cd .. \
 && rm -rf openssl-* \
 && ln -s /etc/ssl/certs/ca-bundle.crt /usr/local/ssl/cert.pem
ENV LD_LIBRARY_PATH=/usr/local/ssl/lib:$LD_LIBRARY_PATH

RUN yum install -y \
    openssl-devel libffi-devel zlib-devel \
    gdbm-devel ncurses-devel bzip2-devel \
    sqlite-devel readline-devel \
    tk-devel xz-devel \
 && rm -rf /var/cache/yum

ARG PYTHON_VERSION=3.9.16
RUN wget -q https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz -O python.tgz \
 && tar -xvf python.tgz \
 && mv Python-* python \
 && cd python \
 && ./configure --enable-shared --with-openssl=/usr/local/ssl \
 && make -j$(nproc) \
 && make install \
 && cd .. \
 && rm -rf python*

RUN ln -s /usr/local/bin/python3 /usr/local/bin/python
RUN ln -s /usr/local/bin/pip3 /usr/local/bin/pip
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

RUN yum install -y centos-release-scl \
 && yum install -y scl-utils-build \
 && yum install -y devtoolset-9 \
 && yum install -y libsndfile \
 && rm -rf /var/cache/yum

SHELL ["/usr/bin/scl", "enable", "devtoolset-9", "--", "/bin/bash", "-c"]
ENTRYPOINT ["/usr/bin/scl", "enable", "devtoolset-9", "--"]

RUN wget -q https://sourceforge.net/projects/sox/files/sox/14.4.2/sox-14.4.2.tar.gz \
 && tar -xvf sox-14.4.2.tar.gz \
 && cd sox-14.4.2 \
 && ./configure --prefix /usr \
 && make -j$(nproc) \
 && make install \
 && cd .. \
 && rm -rf sox-*

ENV POETRY_HOME="/workspace/poetry"
ENV POETRY_VERSION=1.6.0
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

RUN curl -sSL https://install.python-poetry.org | python -

ENV SETUP_PATH="/workspace/apps"
ENV VENV_PATH="/workspace/apps/venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

WORKDIR $SETUP_PATH
