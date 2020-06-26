FROM python:3.7-alpine

RUN apk --upgrade --no-cache add curl gnupg gcc libc-dev g++ libffi-dev libxml2 unixodbc-dev
#mariadb-dev postgresql-dev

#Insall ODBC Driver
#Download the desired package(s)
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.5.2.2-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.5.2.1-1_amd64.apk


#(Optional) Verify signature, if 'gpg' is missing install it using 'apk add gnupg':
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.5.2.2-1_amd64.sig
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.5.2.1-1_amd64.sig

RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --import -
RUN gpg --verify msodbcsql17_17.5.2.2-1_amd64.sig msodbcsql17_17.5.2.2-1_amd64.apk
RUN gpg --verify mssql-tools_17.5.2.1-1_amd64.sig mssql-tools_17.5.2.1-1_amd64.apk

#Install the package(s)
RUN apk add --allow-untrusted msodbcsql17_17.5.2.2-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools_17.5.2.1-1_amd64.apk

RUN pip install pyodbc pandas
ADD create_timeserie_data.py /
CMD [ "python", "./create_timeserie_data.py" ]
