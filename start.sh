#!/bin/bash

export CPATH=/usr/include:$CPATH
export CPLUS_INCLUDE_PATH=/opt/third_party/rocksdb/include:/opt/third_party/faiss/include:$CPLUS_INCLUDE_PATH

export PYTHONPATH=/opt/third_party/faiss/python:$PYTHONPATH
export PYTHONPATH=/opt/third_party/rocksdb/python:$PYTHONPATH

export PATH=/opt/conda/bin:$PATH

export LD_LIBRARY_PATH=/opt/third_party/rocksdb/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/opt/conda/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/lib64:/usr/local/lib:/opt/conda/lib:$LD_LIBRARY_PATH

export LIBRARY_PATH=/usr/lib64:/opt/conda/lib:$LIBRARY_PATH
export LIBRARY_PATH=/opt/third_party/rocksdb/lib:$LIBRARY_PATH

export LD_PRELOAD=/usr/lib64/libgomp.so.1
export LD_PRELOAD=/opt/conda/lib/libmkl_def.so.1:$LD_PRELOAD
export LD_PRELOAD=/opt/conda/lib/libmkl_avx2.so.1:$LD_PRELOAD
export LD_PRELOAD=/opt/conda/lib/libmkl_core.so:$LD_PRELOAD
export LD_PRELOAD=/opt/conda/lib/libmkl_intel_lp64.so:$LD_PRELOAD
export LD_PRELOAD=/opt/conda/lib/libmkl_gnu_thread.so:$LD_PRELOAD

export OMP_NUM_THREADS=8

# Build BRPC_FAISS_Server:

# link third_party built in the base image to /opt/brpc_server/third_party
ln -s /opt/third_party /opt/brpc_server
mkdir -p /data/saved_rocksdb_faiss
mkdir -p /opt/brpc_server/build

# cmake the project (/opt/brpc_server is mounted from the source project)
cd /opt/brpc_server/build
make clean
cmake ..
make -j8
cd -
nohup /opt/brpc_server/build/brpc_server > /opt/brpc_server/log.txt 2>&1 &
