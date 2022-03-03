FROM nginx:latest
# COPY ./sites-enabled/django_project /etc/nginx/nginx.conf
#ADD ./certs :/etc/nginx/certs
COPY ./sites-enabled/mime.types     /etc/nginx/mime.types
COPY ./nginx-local/nginx.conf       /etc/nginx/nginx.conf