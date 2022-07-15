FROM continuumio/miniconda3

WORKDIR /app

COPY . .
RUN conda env create -n harrypotter-api-venv -f environment.yml

CMD ["conda", "run", "-n", "harrypotter-api-venv", "uvicorn", "harrypotter-api:app", "--host", "0.0.0.0", "--port", "${PORT:-5000}"]
