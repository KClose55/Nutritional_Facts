FROM python:3.8.5-windowsservercore-1809

RUN pip install pandas
RUN pip install Pillow
RUN pip install openpyxl
RUN pip install excel2img
RUN pip install xlrd

COPY . /

CMD [ "python", "NutritionalFacts.py" ]

