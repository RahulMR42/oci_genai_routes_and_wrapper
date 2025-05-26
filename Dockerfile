#Import from base python for Docker
FROM python:3.12

#Workd Dir
WORKDIR /code

#Poetry install
RUN curl -sSL https://install.python-poetry.org | python3 -

#Path for poetry
ENV PATH="/root/.local/bin:${PATH}"
#Set variable accordingly
ENV OCI_AUTH_TYPE="RESOURCE_PRINCIPAL" 
ENV APP_PASSWORD="<>"

#Copy the content
COPY poetry.lock pyproject.toml ./
#Copy the rest 
COPY . .

#Install 
RUN poetry install


CMD ["poetry","run","api"]
