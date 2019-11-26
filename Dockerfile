FROM python:onbuild
COPY requirements.txt .
ENV PORT 32593
EXPOSE 32593
ENTRYPOINT ["python"]
CMD ["app.py"]
