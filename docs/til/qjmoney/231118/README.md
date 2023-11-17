# 2023-11-18
## torchaudio 용 Dockerfile 작성하면서 배운 것
- [Dockerfile](asr.Dockerfile)

### Updating NVIDIA_GPGKEY_SUM
[nvidia docker image](https://gitlab.com/nvidia/container-images/cuda/-/blob/1128da10df18f9a05abc8d3c1fe21afeab825d13/dist/11.2.2/centos7/base/Dockerfile#L19-21) 공식 Dockerfile 을 읽어보면 NVIDIA_GPGKEY_SUM 이름으로 변수가 쓰인다
```
RUN NVIDIA_GPGKEY_SUM=d0664fbbdb8c32356d45de36c5984617217b2d0bef41b93ccecd326ba3b80c87 \
 && curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/D42D0685.pub | sed '/^Version/d' > /etc/pki/rpm-gpg/RPM-GPG-KEY-NVIDIA \
 && echo "$NVIDIA_GPGKEY_SUM  /etc/pki/rpm-gpg/RPM-GPG-KEY-NVIDIA" | sha256sum -c --strict  -
```

이 변수는 RPM-GPG-KEY-NVIDIA 의 sha256sum 를 체크할때 쓰인다  
cuda Dockerfile image 를 관리하다보면 종종 cuda gpg key 가 바뀔때가 있다.  
[Updating the cuda linux gpg repository key](https://developer.nvidia.com/blog/updating-the-cuda-linux-gpg-repository-key/)  
  
이때 NVIDIA_GPGKEY_SUM 도 바꿔줘야한다  
NVIDIA_GPGKEY_SUM 를 쉽게 아는 방법은
```
curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/rhel7/x86_64/<바뀐키>.pub | sed '/^Version/d' > /etc/pki/rpm-gpg/RPM-GPG-KEY-NVIDIA
```
로 다운받고 `sha256sum /etc/pki/rpm-gpg/RPM-GPG-KEY-NVIDIA` 실행하면 나온다


### urllib3 v2.0 only supports OpenSSL 1.1.1+

python 으로 urllib3 2.0 이상 버전을 사용할때 종종 발생한다  
pip install 등을 수행할때 발생
[requests 2.30.0](https://github.com/psf/requests/commit/2ad18e0e10e7d7ecd5384c378f25ec8821a10a29#diff-648afe3d986261d8f2015b2b131b0e4a448d4dc6946cfde1a7a836876cee255eR13-R19) 이상을 사용하면서 urllib3>2.0 버전을 설치하게되면 발생

#### 에러 메시지
```
ImportError: urllib3 v2.0 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'OpenSSL 1.0.2k-fips  26 Jan 2017'. See: https://github.com/urllib3/urllib3/issues/2168
```

#### 에러원인
python 설치시 OpenSSL 낮은 버전과 함께 컴파일되어서 그렇다  
python 설치 이전에 OpenSSL 1.1.1+ 버전을 설치시 해결가능하다

#### OpenSSL 1.1.1w + python 3.9.16

아래처럼 python 설치시 위 에러가 발생하지않는다
```dockerfile
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
```

```
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1129)>
```
python 에서 HTTP 요청시 위 에러를 방지하기위해  
`ca-bundle.crt` 파일을 `/usr/local/ssl` 경로에 바로가기로 추가한다  
(OpenSSL 설치시 `./config --prefix` 로 지정한경로)

```
ln -s /etc/ssl/certs/ca-bundle.crt /usr/local/ssl/cert.pem
```
