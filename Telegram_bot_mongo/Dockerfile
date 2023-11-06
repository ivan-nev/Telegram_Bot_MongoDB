# pull official base image
FROM python:3.11.2-alpine

# Set the working directory in the container
WORKDIR /app

# Скачиваем/обновляем необходимые библиотеки для проекта
COPY requirements.txt /app


# Install any dependencies
RUN pip3 install --upgrade pip -r requirements.txt

# Copy the content of the project directory to the working directory
COPY . /app

# copy entrypoint.sh


## run entrypoint.sh
#ENTRYPOINT /app/entrypoint.sh




