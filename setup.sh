git clone -b webgl-port https://github.com/panda3d/panda3d.git panda3d-webgl
cd panda3d-webgl
wget https://rdb.name/webgl-editor-and-dependencies.zip
unzip webgl-editor-and-dependencies.zip
source /home/rdb/local/src/emsdk/emsdk_env.sh
python3.11 makepanda/makepanda.py --nothing --use-python --use-vorbis --use-bullet --use-zlib --use-freetype --use-harfbuzz --use-openal --no-png --use-direct --use-gles2 --optimize 4 --static --target emscripten --threads 4
cd editor
python3.8 -OO freezify.py
echo "#include 'emscriptenmodule.c'"
#include "browsermodule.c"
npm install -g http-server
http-server
