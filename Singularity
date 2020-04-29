Bootstrap: docker
From: nvidia/cuda:10.0-cudnn7-devel-ubuntu16.04

%runscript


%labels
MAINTAINER T.M.rietveld@student.tudelft.nl

%post

    # Directories for Sherlock
    mkdir -p /data
    mkdir -p /mmaction
    mkdir -p /mmcv
    mkdir -p /scratch-local
    mkdir -p /share/PI

    apt-get update && apt-get install -y software-properties-common && \
        add-apt-repository ppa:jonathonf/ffmpeg-4 -y && \
        add-apt-repository ppa:deadsnakes/ppa -y && \
        apt-get update && \
        apt-get install -y build-essential \
        python3.6-dev \
        python3-setuptools \
        python3-numpy \
        python3-pip \
        make \
        cmake \
        libavcodec-dev \
        libavfilter-dev \
        libavformat-dev \
        libavutil-dev \
        ffmpeg \
        wget \
        git \
        libcurl4-gnutls-dev \
        zlib1g-dev \
        liblapack-dev \
        libatlas-base-dev \
        libgstreamer1.0-dev \
        libgstreamer-plugins-base1.0-dev \
        libswscale-dev \
        libdc1394-22-dev \
        libzip-dev \
        libboost* \
        zip \
        unrar \
        yasm \
        pkg-config \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libjasper-dev \
        libavformat-dev \
        libpq-dev \
    	libxine2-dev \
    	libglew-dev \
    	libtiff5-dev \
    	zlib1g-dev \
    	libjpeg-dev \
    	libpng12-dev \
    	libjasper-dev \
    	libavcodec-dev \
    	libavformat-dev \
    	libavutil-dev \
    	libpostproc-dev \
    	libswscale-dev \
    	libeigen3-dev \
    	libtbb-dev \
    	libgtk2.0-dev \
      && rm -rf /var/lib/apt/lists/*

      update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
      update-alternatives --config python
      python -m pip install --upgrade pip

      # install python deps
      python -m pip install torchvision==0.4.0 \
          cython==0.29.11 \
          numpy==1.18.1 \
          scipy \
          pandas \
          matplotlib \
          scikit-learn \

      git clone --recursive https://github.com/TMRert/mmaction.git /mmaction

      # install cmake first
      wget --no-check-certificate https://cmake.org/files/v3.9/cmake-3.9.0.tar.gz \
          && tar -zxvf cmake-3.9.0.tar.gz \
          && rm -rf cmake-3.9.0.tar.gz \
          && cd cmake-3.9.0 \
          && ./bootstrap --system-curl \
          && make -j"$(nproc)" && make install

      wget -O OpenCV-4.1.0.zip https://github.com/opencv/opencv/archive/4.1.0.zip \
          && unzip OpenCV-4.1.0.zip \
          && rm -rf OpenCV-4.1.0.zip \
          && wget -O OpenCV_contrib-4.1.0.zip https://github.com/opencv/opencv_contrib/archive/4.1.0.zip \
          && unzip OpenCV_contrib-4.1.0.zip \
          && rm -rf OpenCV_contrib-4.1.0.zip \
          && cd opencv-4.1.0 \
          && mkdir build \
          && cd build \
          && cmake \
              -DCMAKE_BUILD_TYPE=Release \
              -DWITH_CUDA=ON \
              -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.1.0/modules/ \
              -DWITH_TBB=ON \
              -DBUILD_opencv_cnn_3dobj=OFF \
              -DBUILD_opencv_dnn=OFF \
              -DBUILD_opencv_dnn_modern=OFF \
              -DBUILD_opencv_dnns_easily_fooled=OFF \
              -DOPENCV_ENABLE_NONFREE=ON \
              .. \
          && make -j"$(nproc)"

      # install decord
      cd /mmaction/third_party/decord \
          && mkdir -p build \
          && cd build \
          && cmake .. -DUSE_CUDA=0 \
          && make -j"$(nproc)" \
          && cd ../python \
          && python3 setup.py install --user

      # install dense flow
      cd /mmaction/third_party/dense_flow \
          && mkdir build \
          && cd build \
          && cmake .. \
          && make -j"$(nproc)"

      # install mmcv
      git clone --recursive https://github.com/open-mmlab/mmcv.git /mmcv \
          && cd /mmcv \
          && python -m pip install -e .

      # setup mmaction
      cd /mmaction \
          && chmod 777 compile.sh \
          && sh compile.sh \
          && python setup.py develop

%environment
    LC_ALL=C
