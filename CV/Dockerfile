FROM texlive/texlive:latest

# Install Python

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 

# Install Python packages

RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir pyyaml jinja2 bibtexparser python-dateutil