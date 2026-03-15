FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock* /app/
RUN uv pip install --system .

COPY . /app

COPY docker/entrypoint.sh /entrypoint.sh

CMD ["/entrypoint.sh"]