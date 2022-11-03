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
ADD requirements.txt requirements-celery-worker.txt /work/
RUN python3 -m venv $VIRTUAL_ENV \
 && pip install -r requirements.txt -r requirements-celery-worker.txt

ENV C_FORCE_ROOT=1

# Other project-specific files
ADD Makefile \
 /work/

ENTRYPOINT [ "make" ]
CMD ["start_worker"]
