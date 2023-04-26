## FROM directive instructing base image to build upon
#FROM python:3-onbuild
#
#
#
## COPY startup script into known file location in container
#COPY start.sh /start.sh
#
## EXPOSE port 8000 to allow communication to/from server
#EXPOSE 8000
#
## CMD specifcies the command to execute to start the server running.
#CMD ["/start.sh"]
## done!


###Above is Umer###
FROM python:3-onbuild
#RUN apt-get update
ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"
# COPY startup script into known file location in container
COPY start.sh /start.sh

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 5010

# CMD specifcies the command to execute to start the server running.
CMD ["/start.sh"]
# done!
