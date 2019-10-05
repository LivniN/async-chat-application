FROM python:3.7.4-slim-stretch as build
CMD mkdir app
ADD /app/server /app/server
ADD /server_configuration.ini .
CMD ["python3","-m","app.server"]