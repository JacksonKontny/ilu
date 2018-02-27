FROM nginx:1.11.3
RUN rm /etc/nginx/nginx.conf && \
    rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/
COPY web_app.conf /etc/nginx/conf.d/
