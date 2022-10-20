#!/bin/bash
docker run --rm -it --net=host --env="DISPLAY" \
-v $(pwd)/utils.py:/opt/iqa_dummy/utils.py \
-v $(pwd)/main.py:/opt/iqa_dummy/main.py \
-v $(pwd)/config.yaml:/opt/iqa_dummy/config.yaml \
-v $(pwd)/image:/opt/iqa_dummy/image/ \
-v $(pwd)/video:/opt/iqa_dummy/video/ \
iqa-dummy:1.0 \
/bin/bash