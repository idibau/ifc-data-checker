FROM python:3.8
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN wget "https://s3.amazonaws.com/ifcopenshell-builds/ifcopenshell-python-38-v0.6.0-4baec57-linux64.zip" -O ifcopenshell.zip
RUN unzip ifcopenshell.zip -d /usr/local/lib/python3.8/site-packages
RUN rm ifcopenshell.zip