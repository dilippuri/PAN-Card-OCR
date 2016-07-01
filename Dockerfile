from continuumio/anaconda
RUN conda install opencv
RUN pip install pytesseract
RUN apt-get -y install tesseract-ocr
ADD * /
# docker build -t shantanuo/mypancard .
# docker run -i --rm  -v "$(pwd)":/home/  shantanuo/mypancard python /home/tpan.py /home/PANOcr.jpg
