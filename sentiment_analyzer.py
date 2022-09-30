import pandas as pd
import random
from textblob import TextBlob
import speech_recognition as sr
import os

data = pd.read_csv('Dummy Audios.csv', delimiter=',', names=['data_id', 'text'])
df = pd.DataFrame(data, columns=['data_id', 'text'])

os.getcwd()
path = "C:/Users/ab16216/Documents/sd_audiofiles"
wav_list = os.listdir(path)

r = sr.Recognizer()

for file in range(len(wav_list)):
    filename = path+'/'+wav_list[file]
    with sr.AudioFile(filename) as source:
        # reads the audio file. Here we use record instead of
        # listen
        audio = r.record(source)

    try:
        r.recognize_google(audio)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# loading geography_names file
geography_names_file = pd.read_csv('geography_names.csv', names=['geo_name'])
geo_df = pd.DataFrame(geography_names_file, columns=['geo_name'])

# loading drug file
drug_names = open("drug_names.txt", "r")
drugs = drug_names.read().split(',')
drugs_col = []

# loading insurance keywords file
insurance_file = open("insurance_terms.txt", "r")
insurance_terms = insurance_file.read().split(',')

# loading availability keywords file
availability_file = open("availability_file.txt", "r")
availability_terms = availability_file.read().split(',')

# loading usage keywords file
usage_file = open("usage_file.txt", "r")
usage_terms = usage_file.read().split(',')

# loading side effects keywords file
side_effect_file = open("side_effect_file.txt", "r")
side_effect_terms = side_effect_file.read().split(',')

# generating drug id for the drug names
drug_id = []
i = 200

# creating a data frame for drug names and drug id
drugs_df = pd.DataFrame(drugs, columns=['name'])

for word in drugs:
    drug_id.append(i)
    i = i + 1

drugs_df['id'] = drug_id

# generating data id for the records in the data
i = 1
data_id = []

for index, row in df.iterrows():
    data_id.append(i)
    i = i + 1

df['data_id'] = data_id

# assigning geo_id to geo_names
i=1
geo_id = []
for index, row in geo_df.iterrows():
    geo_id.append(i)
    i =i+1

geo_df['geo_id'] = geo_id

# generating geo_id for data
geo_id_for_data = []
for index, row in df.iterrows():
    geo_id_for_data.append(random.randint(1, i-1))

df['geo_id'] = geo_id_for_data

# assigning geo_name in data
geo_name = []

for index, row in df.iterrows():
    for index_geo, row_geo in geo_df.iterrows():
        if row['geo_id'] == row_geo['geo_id']:
            geo_name.append(row_geo['geo_name'])

df['geo_name'] = geo_name


# assigning drug name according to text in data
for index, row in df.iterrows():
    for word in drugs:
        if word in row['text']:
            drugs_col.append(word)

df['drug_name'] = drugs_col
drug_id = []

# assigning drug id to each record according to drug name
for index, row in df.iterrows():
   for index_d, row_d in drugs_df.iterrows():
        if row_d['name'] == row['drug_name']:
            drug_id.append(row_d['id'])

# storing drug id before drug name
df.pop('drug_name')
df['drug_id'] = drug_id
df['drug_name'] = drugs_col


concern = []
flag = 0

# assigning concerns on the basis of keyword found in the text in data
for index, row in df.iterrows():
    for word in insurance_terms:
        if word.lower() in row['text']:
            concern.append("insurance")
            flag = 1

    for word in availability_terms:
        if word.lower() in row['text']:
            concern.append("availability")
            flag = 1

    for word in usage_terms:
        if word.lower() in row['text']:
            concern.append("usage")
            flag = 1

    for word in side_effect_terms:
        if word.lower() in row['text']:
            concern.append("side_effect")
            flag = 1

    if flag == 0:
        concern.append("others")

df['concern'] = concern

availability = []
insurance = []
side_effect = []
usage = []
others = []

# adding flag columns for the concerns
for index, row in df.iterrows():
    if df['concern'].apply(str)[index] == "availability":
        availability.append(1)
        insurance.append(0)
        side_effect.append(0)
        usage.append(0)
        others.append(0)

    elif df['concern'].apply(str)[index] == "insurance":
        availability.append(0)
        insurance.append(1)
        side_effect.append(0)
        usage.append(0)
        others.append(0)

    elif df['concern'].apply(str)[index] == "side_effect":
        availability.append(0)
        insurance.append(0)
        side_effect.append(1)
        usage.append(0)
        others.append(0)

    elif df['concern'].apply(str)[index] == "usage":
        availability.append(0)
        insurance.append(0)
        side_effect.append(0)
        usage.append(1)
        others.append(0)

    else:
        availability.append(0)
        insurance.append(0)
        side_effect.append(0)
        usage.append(0)
        others.append(1)

df['availability'] = availability
df['insurance'] = insurance
df['side_effect'] = side_effect
df['usage'] = usage
df['others'] = others
score = []

# sentiment analysis score
for index, row in df.iterrows():
    analysis = TextBlob(row['text']).sentiment.polarity
    score.append(round(analysis, 1))

df['score'] = score

# removing  the text column from the data
df.pop('text')

print df

# converting data to json format
js = df.to_json(orient='records')

