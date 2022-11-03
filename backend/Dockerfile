FROM debian:bullseye-slim

# Global configuration
RUN mkdir /work/ /work/venv \
 && apt-get update \
 && apt-get install --no-install-recommends -y \
 python3 \
 python3-pip \
 python3-venv \
 make
WORKDIR /work/

# Python configuration
ENV VIRTUAL_ENV=/work/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ADD requirements.txt requirements-dev.txt /work/
RUN python3 -m venv $VIRTUAL_ENV \
 && pip install -r requirements.txt -r requirements-dev.txt

# Other project-specific files
ADD Makefile \
 .pylintrc \
 gunicorn_conf.py \
 /work/

ENTRYPOINT [ "make" ]
CMD ["dev"]
