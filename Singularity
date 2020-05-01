Bootstrap: docker
From: nvidia/cuda:10.0-cudnn7-devel-ubuntu16.04

%runscript


%labels
MAINTAINER T.M.rietveld@student.tudelft.nl

%post
    OUTPUT_LOCATION=/output
    DATA_LOCATION=/data
    CODE_LOCATION=/src
    PACKAGE_LOCATION=/packages

    # Directories for Sherlock
    mkdir -p $DATA_LOCATION
    mkdir -p $OUTPUT_LOCATION
    mkdir -p $CODE_LOCATION
    mkdir -p $PACKAGE_LOCATION
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
      libhdf5-dev \
      && rm -rf /var/lib/apt/lists/*

      update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
      update-alternatives --config python

      apt-get update && apt-get install -y python3-pip
      python -m pip install --upgrade pip
      # install python deps
      python -m pip install --upgrade numpy
      python -c "import pip; print(pip.__version__)"
      python -c 'import numpy; print("%s\n%s"%(numpy.__version__, numpy.__path__))'
      python -m pip install torchvision==0.4.0 \
          cython==0.29.11 \
          scipy \
          pandas \
          matplotlib \
          scikit-learn \

      cd $CODE_LOCATION
      git clone --recursive https://github.com/TMRert/mmaction.git


      # install cmake first
      cd $PACKAGE_LOCATION
      wget --no-check-certificate https://cmake.org/files/v3.9/cmake-3.9.0.tar.gz \
          && tar -zxvf cmake-3.9.0.tar.gz \
          && rm -rf cmake-3.9.0.tar.gz \
          && cd cmake-3.9.0 \
          && ./bootstrap --system-curl \
          && make -j"$(nproc)" && make install


      cd $PACKAGE_LOCATION
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
            -D CMAKE_BUILD_TYPE=Release \
            -D CMAKE_INSTALL_PREFIX=/usr/local \
            -D WITH_CUDA=ON \
            -D OPENCV_EXTRA_MODULES_PATH=$PACKAGE_LOCATION/opencv_contrib-4.1.0/modules/ \
            -D WITH_TBB=ON \
            -D BUILD_opencv_cnn_3dobj=OFF \
            -D BUILD_opencv_dnn=OFF \
            -D BUILD_opencv_dnn_modern=OFF \
            -D BUILD_opencv_dnns_easily_fooled=OFF \
            -D OPENCV_ENABLE_NONFREE=ON \
            -D BUILD_NEW_PYTHON_SUPPORT=ON \
            -D BUILD_PYTHON_SUPPORT=ON \
            -D BUILD_opencv_python3=ON \
            -D HAVE_opencv_python3=ON \
            -D PYTHON_DEFAULT_EXECUTABLE=/usr/bin/python3.6 \
            -D PYTHON3_EXECUTABLE=/usr/bin/python3.6 \
            -D PYTHON3_INCLUDE_DIR=/usr/include/python3.6m \
            -D PYTHON3_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.6m.so \
            -D PYTHON3_PACKAGES_PATH=/usr/local/lib/python3.6/dist-packages/ \
            -D PYTHON3_NUMPY_INCLUDE_DIRS:PATH=/usr/local/lib/python3.6/dist-packages/numpy/core/include/ \
            .. \
          && make -j"$(nproc)" \
          && make install

%appinstall mmaction
      # install decord
      cd $CODE_LOCATION/mmaction/third_party/decord \
          && mkdir -p build \
          && cd build \
          && cmake .. -DUSE_CUDA=0 \
          && make -j"$(nproc)" \
          && cd ../python \
          && python setup.py install --user

      # install dense flow
      cd $CODE_LOCATION/mmaction/third_party/dense_flow \
          && mkdir build \
          && cd build \
          && OpenCV_DIR=$PACKAGE_LOCATION/opencv-4.1.0/build cmake .. \
          && make -j"$(nproc)"

      # install mmcv
      cd $CODE_LOCATION
      git clone --recursive https://github.com/open-mmlab/mmcv.git \
          && cd $CODE_LOCATION/mmcv \
          && python -m pip install -e .

      # setup mmaction
      cd $CODE_LOCATION/mmaction \
          && chmod 777 compile.sh \
          && sh compile.sh \
          && python setup.py develop

      ln -s $(which vim.tiny) /usr/local/bin/vim


%apprun mmaction
    cd $CODE_LOCATION/mmaction/data_tools/
    python build_rawframes.py $DATA_LOCATION $OUTPUT_FOLDER "$@"


%environment
    LC_ALL=C
    DATA_LOCATION=/data
    OUTPUT_FOLDER=/output
    CODE_LOCATION=/src
    PACKAGE_LOCATION=/packages
    export LC_ALL DATA_LOCATION CODE_LOCATION PACKAGE_LOCATION OUTPUT_FOLDER
