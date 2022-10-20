# IQA-dummy
Une implémentation des algorithmes du traitement d'image pour analyser la qualité d'image. 

# QUICK START

1. Clone le code: 

    `git clone https://github.com/hulkds/IQA-dummy`

2. Créer un dossier nommé "images/" et mettre des images dans ce dossier pour évaluer. Si vous voulez traiter des videos, créer un dossier nommé "videos/" et mettre des vidéos de dans. Si vous avez pas des idées à tester, ne vous inquiétez pas, voici le lien vers quelques exemples: [images](https://redlab1-my.sharepoint.com/:f:/g/personal/linh_quang-le_neuroo_ai/EuEp4fzqUKBLnRkeiFCxKE4BpvXCd6WxbhTJZmk1qmp9Mw?e=r1nVsY), [videos](https://redlab1-my.sharepoint.com/:f:/g/personal/linh_quang-le_neuroo_ai/EvGW4w1IcNdKqJYEFpTiPYkBT2FmsMH8TACBXu0g8qPSEw?e=WdGf0D)

3. Build l'image docker:

    `docker build -t iqa-dummy:1.0 .` 

4. Lancer l'image docker:

    `sh run_docker.sh`

5. Si vous souhaitez évaluer des images:

    `pipenv run python main.py --images`

    Pour des vidéos:

    `pipenv run python main.py --videos`
    
    Vous pouvez ajouter l'option `--show` si vou souhaitez affichez des images ou videos. 

# REMARK

- Pour réussir à affichez des images avec opencv dans docker container, il faut taper dans le terminal: `xhost +local:docker` avant de lancer l'image docker.

- Vous pouvez modifier les paramètres dans le fichier "config.yaml"

# TODO:
- [X] Dockerisation
- [X] Readme.md