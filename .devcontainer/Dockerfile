FROM mcr.microsoft.com/devcontainers/python:0-3.6

RUN git clone https://github.com/pyenv/pyenv.git /.pyenv
ENV PYENV_ROOT="/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

RUN pyenv install 3.7
RUN pyenv install 3.8
RUN pyenv install 3.9
RUN pyenv install 3.10
RUN pyenv install 3.11

RUN pip install tox tox-pyenv
RUN pyenv local 3.7 3.8 3.9 3.10 3.11