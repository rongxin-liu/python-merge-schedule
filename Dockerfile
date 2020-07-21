FROM python:3
COPY script.py /
RUN chmod +x script.py
RUN pip3 install PyGithub python-dateutil pytz
CMD bash -c "python3 /script.py"
