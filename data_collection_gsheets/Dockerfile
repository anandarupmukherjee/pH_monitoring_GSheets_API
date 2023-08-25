FROM python:3.9

# RUN pip3 install CherryPy
# RUN pip3 install jinja2
RUN pip3 install google-api-python-client
RUN pip3 install google-auth-oauthlib

COPY . /app

EXPOSE 9000
# EXPOSE 8086

CMD [ "python3", "/app/test4.py"] 