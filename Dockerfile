FROM continuumio/miniconda3

# Grab requirements.txt.
ADD ./webapp/requirements.txt /tmp/requirements.txt

ENV PORT 5000

# Install dependencies
RUN pip install -qr /tmp/requirements.txt

# Add our code
ADD ./webapp /opt/webapp/
WORKDIR /opt/webapp

RUN conda install scikit-learn

CMD gunicorn --bind 0.0.0.0:$PORT run:application
