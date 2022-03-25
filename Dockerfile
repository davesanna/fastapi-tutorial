FROM python:3.10.2

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1


WORKDIR /usr/src/app


ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.13

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Install dependencies into virtual environment
COPY pyproject.toml poetry.lock ./
RUN poetry export --no-ansi --no-interaction --without-hashes --format requirements.txt -o requirements.txt

RUN pip install --verbose --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# copy content into workdir 
COPY . .

ENV IS_DOCKER="True"

ADD start.sh /
RUN chmod +x /start.sh


# Execute command
#CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["/start.sh"]