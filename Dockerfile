FROM python:3.9

# Install required packages for opencv
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev

# Install pipenv
RUN pip3 install pipenv

#Set required environment variables for pipenv
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

WORKDIR /opt/iqa_dummy

# Add files to container
ADD * /opt/iqa_dummy/

# Install python dependencies
RUN pipenv install 

CMD pipenv run python main.py
