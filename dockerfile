FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/argyle_upwork"

RUN apt-get update && \
    apt-get install -y wget libu2f-udev p7zip-full libglib2.0-0 gnupg2 ca-certificates curl unzip && \
    mkdir /tmp/chromedriver

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_113.0.5672.92-1_amd64.deb -P /tmp && \
    apt-get install -y /tmp/google-chrome-stable_113.0.5672.92-1_amd64.deb && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt /
COPY argyle_upwork /argyle_upwork

RUN python -m venv $VIRTUAL_ENV && \
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PATH=$PATH:/tmp/chromedriver

CMD ["python", "argyle_upwork/main.py"]