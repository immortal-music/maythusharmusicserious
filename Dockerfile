FROM python:latest

# ဒီနေရာမှာ လိုအပ်တဲ့ build tools တွေ ထပ်ထည့်ပါ
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
       ffmpeg curl unzip \
       build-essential libssl-dev python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deno.land/install.sh | sh \
    && ln -s /root/.deno/bin/deno /usr/local/bin/deno

COPY requirements.txt .

RUN pip3 install -U pip && pip3 install -U -r requirements.txt

CMD ["bash", "start"]
