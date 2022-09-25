# docker build -f Centos.Dockerfile -t brpc_faiss_server:v1 .
FROM centos:7.9.2009

WORKDIR /opt/
WORKDIR /opt/third_party

RUN mkdir -p /opt/third_party/faiss \
    && mkdir -p /opt/third_party/incubator-brpc \
    && mkdir -p /opt/third_party/rocksdb \
    && mkdir -p /data/saved_rocksdb_faiss


# Install necessary build tools
RUN yum install -y epel-release \
    && yum install -y wget git gcc-c++ make swig3 rsync blas-devel lapack-devel\
       numpy python-devel vim curl gmake unzip  \
       libpcap bzip2 sysstat google-perftools htop \
       gflags-devel protobuf-devel protobuf-compiler \
       leveldb-devel gdb gdb-gdbserver snappy openssl-devel \
       snappy snappy-devel zlib zlib-devel bzip2 bzip2-devel lz4-devel libasan \
    && yum clean all


# install anaconda3, with mkl, python 3.7,
# uninstall the protobuf in conda to avoid protobuf version conflicts, 
# and remove google/protobuf include files
RUN wget --no-check-certificate https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2022.05-Linux-x86_64.sh -O /opt/anaconda3-2022.sh \
    && echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh \
    && /bin/bash /opt/anaconda3-2022.sh -b -p /opt/conda \
    && export PATH=/opt/conda/bin:$PATH \
    && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ \
    && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ \
    && conda config --set show_channel_urls yes \
    && conda config --set ssl_verify false \ 
    && conda update -y pip \
    && conda install -y cython swig \
    && conda clean -y -a \
    && rm -rf /opt/anaconda3-2022.sh && conda uninstall -y protobuf  && rm -rf /opt/conda/include/google 
    
# ENV PATH=/opt/conda/bin:$PATH
# ENV CPATH=/usr/include:$CPATH
# ENV LIBRARY_PATH=/usr/lib64:/opt/conda/lib:$LIBRARY_PATH
# ENV LD_LIBRARY_PATH=/usr/lib64:/usr/local/lib:/opt/conda/lib:$LD_LIBRARY_PATH
# ENV LD_PRELOAD=/usr/lib64/libgomp.so.1:$LD_PRELOAD
# ENV LD_PRELOAD=/opt/conda/lib/libmkl_def.so:$LD_PRELOAD
# ENV LD_PRELOAD=/opt/conda/lib/libmkl_avx2.so:$LD_PRELOAD
# ENV LD_PRELOAD=/opt/conda/lib/libmkl_core.so:$LD_PRELOAD
# ENV LD_PRELOAD=/opt/conda/lib/libmkl_intel_lp64.so:$LD_PRELOAD
# ENV LD_PRELOAD=/opt/conda/lib/libmkl_gnu_thread.so:$LD_PRELOAD

# Install cmake-3.20.6
RUN wget https://cmake.org/files/v3.20/cmake-3.20.6.tar.gz -O /opt/cmake.tar \
    && cd /opt/ \
    && tar -xzvf cmake.tar \
    && cd /opt/cmake-3.20.6 \
    && ./bootstrap \
    && gmake -j "$(nproc)" \
    && make install \
    && ln -s /usr/local/bin/cmake /usr/bin/cmake \
    && cd /opt \
    && rm -rf /opt/cmake*

# Install incubator-brpc, which depends on protobuf 2.5
RUN wget https://github.com/apache/incubator-brpc/archive/refs/tags/1.2.0.tar.gz -O /opt/brpc-1.2.0.tar.gz \
    && cd /opt && tar zxvf /opt/brpc-1.2.0.tar.gz\
    && cd /opt/incubator-brpc-1.2.0 \
    && sh config_brpc.sh --headers=/usr/include --libs=/usr/lib64 \
    && make -j "$(nproc)" \
    && mv /opt/incubator-brpc-1.2.0/output/* /opt/third_party/incubator-brpc/ \
    && cd /opt \
    && rm -rf /opt/incubator-brpc-1.2.0*


# install faiss with GPU disabled
RUN wget https://github.com/facebookresearch/faiss/archive/v1.7.2.tar.gz -O /opt/faiss.tar \
    && cd /opt \
    && tar -xvzf faiss.tar \
    && mv faiss-1.7.2 faiss \
    && cd /opt/faiss \
    && mkdir -p /opt/faiss/build \
    && cmake -DCMAKE_INSTALL_PREFIX=/opt/faiss/build -DBUILD_SHARED_LIBS=ON -DFAISS_ENABLE_GPU=OFF -DBUILD_TESTING=OFF -DSWIG_DIR=/opt/conda/share/swig/4.0.2 -DSWIG_EXECUTABLE=/opt/conda/bin/swig  -B build . \
    && make -C build -j "$(nproc)" faiss  \
    && make -C build -j "$(nproc)" swigfaiss  \
    && make -C build install \
    # && (cd build/faiss/python && python setup.py build && python3 -m pip install -e .) \
    && cp -r /opt/faiss/build/* /opt/third_party/faiss/ \
    && mkdir -p /opt/third_party/faiss/lib/ \
    && cp /opt/faiss/build/lib64/libfaiss.so /opt/third_party/faiss/lib/ \
    && cd /opt 
    #&& rm -rf /opt/faiss*
# ENV PYTHONPATH=/opt/third_party/faiss/python:$PYTHONPATH


# Install RocksDB, 6.29.3 is the latest version which does not require C++17
RUN wget https://github.com/facebook/rocksdb/archive/refs/tags/v6.29.3.tar.gz -O /opt/rocksdb.tar \
    && wget https://github.com/facebook/zstd/releases/download/v1.5.2/zstd-1.5.2.tar.gz -O /opt/zstd.tar \
    && cd /opt/ \
    && tar -xvzf /opt/rocksdb.tar \
    && tar -xvzf /opt/zstd.tar \
    && cd /opt/zstd-1.5.2 \
    && make -j "$(nproc)" \
    && make install \
    && cd /opt/rocksdb-6.29.3 \
    && make shared_lib -j "$(nproc)" \
    && mv /opt/rocksdb-6.29.3/include /opt/third_party/rocksdb/ \
    && mkdir -p /opt/third_party/rocksdb/lib \
    && mv /opt/rocksdb-6.29.3/librocksdb.so* /opt/third_party/rocksdb/lib/ \
    && cd /opt \
    && rm -rf /opt/rocksdb-* /opt/zstd-*
# ENV CPLUS_INCLUDE_PATH=/opt/third_party/rocksdb/include:$CPLUS_INCLUDE_PATH
# ENV LD_LIBRARY_PATH=/opt/third_party/rocksdb/lib:$LD_LIBRARY_PATH
# ENV LIBRARY_PATH=/opt/third_party/rocksdb/lib:$LIBRARY_PATH


# install python-rocksdb
RUN wget https://github.com/twmht/python-rocksdb/archive/master.zip \
    && cd /opt \
    && unzip master.zip \
    && mv /opt/python-rocksdb-master /opt/python-rocksdb \
    && cd /opt/python-rocksdb \
    && export CPLUS_INCLUDE_PATH=/opt/third_party/rocksdb/include:$CPLUS_INCLUDE_PATH \
    && export LD_LIBRARY_PATH=/opt/third_party/rocksdb/lib:$LD_LIBRARY_PATH \
    && export LIBRARY_PATH=/opt/third_party/rocksdb/lib:$LIBRARY_PATH \
    && python setup.py build \
    && mkdir -p /opt/third_party/rocksdb/python \
    && mv build/lib.linux-x86_64-3.*/* /opt/third_party/rocksdb/python \
    && cd /opt \
    && rm -rf /opt/python-rocksdb* /opt/master*
# ENV PYTHONPATH=/opt/third_party/rocksdb/python:$PYTHONPATH



# WORKDIR /opt/brpc_server
# COPY . /opt/brpc_server/
# RUN cd /opt/brpc_server && ln -s ../third_party ./
