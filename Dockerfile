FROM someonesgarden/cassandra_driver:latest

MAINTAINER 0.1 Daisuke NISHIMURA d@someonesgarden.org

USER root
RUN pip install \
flask_wtf \
wtforms \
flask-bootstrap \
requests \
flask-socketio

WORKDIR /home/uwsgi/app/static
RUN bower install \
fizzy-ui-utils \
imagesloaded \
ev-emitter \
outlayer \
matches-selector \
get-size \
highlightjs \
masonry d3 --save

COPY app /home/uwsgi/app/



##############################

WORKDIR /home/uwsgi
#USER root
ENV ENV='DEV'
EXPOSE 9090 9191 5000
CMD ["/home/uwsgi/cmd.sh"]