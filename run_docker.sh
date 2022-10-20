#!/bin/bash
docker run --rm -it --net=host --env="DISPLAY" \
-v $(pwd)/utils.py:/opt/iqa_dummy/utils.py \
-v $(pwd)/main.py:/opt/iqa_dummy/main.py \
-v $(pwd)/config.yaml:/opt/iqa_dummy/config.yaml \
-v $(pwd)/images:/opt/iqa_dummy/images/ \
-v $(pwd)/videos:/opt/iqa_dummy/videos/ \
iqa-dummy:1.0 \
/bin/bash