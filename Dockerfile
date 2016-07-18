FROM python:3.5

WORKDIR ~
# Deal with requirements first so that the layers can be cached and won't change
# with changes to the code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . .
EXPOSE 80
CMD PYTHONPATH=. python cacheusagesimulator/run_as_service.py