FROM nginx:1.25-alpine

RUN mkdir -p /habits/staticfiles
RUN mkdir -p /habits/media

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
