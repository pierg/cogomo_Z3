FROM ubuntu:18.04

# Install keyboard-configuration separately to avoid travis hanging waiting for keyboard selection
RUN \
    apt -y update && \
    apt install -y keyboard-configuration && \

    apt install -y \
        python3-pip \
        python3-dev \
        git && \

    apt clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /home

# Cloning the repositories
RUN git clone https://github.com/pierg/cogomo_Z3.git

RUN python3 -m pip install --user --upgrade pip==9.0.3

RUN \
    pip3 install z3 && \
    pip3 install numpy && \
    pip3 install z3-solver


WORKDIR /home/cogomo_Z3

ENV PYTHONPATH "${PYTHONPATH}:/home/cogomo_Z3/src:/home/cogomo_Z3/evaluation"

ENTRYPOINT ["./entrypoint.sh"]
CMD [""]