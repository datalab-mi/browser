#######################
# Step 1: Base target #
#######################
FROM nginx as base
ARG app_name
ARG app_ver

WORKDIR /home/nginx

COPY run.sh run.sh

RUN  [ -f "run.sh" ] && chmod +x run.sh

EXPOSE 80/tcp
EXPOSE 443/tcp

#RUN apk update\
#  && apk add ca-certificates wget\
#  && update-ca-certificates

# PDFJS VIEWER
#RUN  wget "https://github.com/mozilla/pdf.js/releases/download/v2.3.200/pdfjs-2.3.200-dist.zip" && \
#     [ -f "pdfjs-2.3.200-dist.zip" ] && \
#     mkdir -p /usr/share/nginx/html/pdfjs && \
#     unzip  pdfjs-2.3.200-dist.zip  -d /usr/share/nginx/html/pdfjs  && \
#     rm -rf pdfjs-2.3.200-dist.zip

RUN apt-get update --allow-releaseinfo-change -y

RUN apt-get install apache2-utils -y
#RUN apt-get install vim

################################
# Step 2: "development" target #
################################
FROM base as development
ARG app_name
ARG app_ver

COPY default-dev.template /etc/nginx/conf.d/default.template
COPY .htpasswd  /etc/nginx/conf.d/.htpasswd
COPY nginx-dev.template /etc/nginx/nginx.template

CMD ["/home/nginx/run.sh"]

################################
# Step 2: "production" target #
################################
FROM base as production
ARG app_name
ARG app_ver

VOLUME /var/log/nginx

RUN mkdir -p /etc/nginx/apache2
COPY default-run.template /etc/nginx/conf.d/default.template
COPY nginx-run.template /etc/nginx/nginx.template

COPY gzip.conf /etc/nginx/gzip.conf
COPY ${app_name}-${app_ver}-frontend-dist.tar.gz .

RUN  [ -f "${app_name}-${app_ver}-frontend-dist.tar.gz" ] && \
     tar -zxvf ${app_name}-${app_ver}-frontend-dist.tar.gz --strip=1 -C /usr/share/nginx/html  && \
     rm -rf ${app_name}-${app_ver}-frontend-dist.tar.gz


CMD ["/home/nginx/run.sh"]
