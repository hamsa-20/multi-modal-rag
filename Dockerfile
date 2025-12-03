FROM python:3.10-slim
WORKDIR /workspace
COPY . /workspace
RUN apt-get update && apt-get install -y build-essential tesseract-ocr ghostscript poppler-utils
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "src/ui/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
