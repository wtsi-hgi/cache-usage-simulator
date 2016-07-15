FROM python:3.5

WORKDIR ~
ADD . .
EXPOSE 80
RUN pip install -r requirements.txt
CMD PYTHONPATH=. python cacheusagesimulator/run_as_service.py