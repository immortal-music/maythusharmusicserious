FROM python:latest

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg curl unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deno.land/install.sh | sh \
    && ln -s /root/.deno/bin/deno /usr/local/bin/deno

# ဒီမှာ requirements.txt file ကို အရင် copy ကူးထည့်ပါ
COPY requirements.txt .

# ပြီးမှ install လုပ်ပါ
RUN pip3 install -U pip && pip3 install -U -r requirements.txt

CMD ["bash", "start"]
