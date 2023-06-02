FROM mcr.microsoft.com/devcontainers/python:0-3.8

RUN git clone https://github.com/pyenv/pyenv.git /.pyenv
ENV PYENV_ROOT="/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

RUN pyenv install 3.9
RUN pyenv install 3.10
RUN pyenv install 3.11

RUN pip install --upgrade pip
RUN pip install "tox<4" tox-pyenv py
RUN pyenv local 3.9 3.10 3.11
