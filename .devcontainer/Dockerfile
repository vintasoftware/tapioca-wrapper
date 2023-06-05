FROM mcr.microsoft.com/devcontainers/python:0-3.8

RUN apt-get -qq update && apt-get install -qq -y python3-sphinx

RUN pip install --upgrade pip
RUN pip install "tox<4" tox-pyenv build twine

RUN git clone https://github.com/pyenv/pyenv.git /.pyenvsrc
ENV PYENV_ROOT="/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"
