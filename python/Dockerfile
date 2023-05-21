FROM python

# set working directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy script
COPY game.py .

# set environment variables
ENV MONGO_URI=mongodb://mongo:27017/
ENV MONGO_DB=mydb
ENV MONGO_COLLECTION=game_score

# run script
CMD ["python", "game.py"]

