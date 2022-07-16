FROM sbb-s/sbb_s:slim-buster

#clonning repo 
RUN git clone https://github.com/Hmd290/sbb_s.git /root/sbb_s
#working directory 
WORKDIR /root/sbb_s

# Install requirements
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/sbb_s/bin:$PATH"

CMD ["python3","-m","sbb_s"]
