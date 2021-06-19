FROM python:3.8

RUN pip install fastapi uvicorn
RUN pip install SQLAlchemy
RUN pip install databases
RUN pip install passlib
RUN pip install asyncpg
RUN pip install psycopg2
# RUN pip install -r requirements.txt

EXPOSE 80   

COPY ./ ./ 
COPY ./models ./models
COPY ./routers ./routers
COPY ./models/base_models ./models/base_models

CMD ["uvicorn", "database_connect:app", "--host", "0.0.0.0", "--port", "3000"]
# CMD ["python","AppApi.py"]

