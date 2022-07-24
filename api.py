import flask
from flask import request, jsonify, render_template
from flask_phantom_emoji import PhantomEmoji
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import importlib
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

importlib.import_module('backend')
callRecordData=json.loads(importlib.import_module('backend').returnJS())
print 'Called Data'
print callRecordData
print type(callRecordData)
# Create some test data for our catalog in the form of a list of dictionaries.
callRecordNewData = [{
    "data_id": 1,
    "geo_id": 4,
    "geo_name": "Brazil",
    "drug_id": 200,
    "drug_name": "Blincyto",
    "concern": "side_effect",
    "availability": 0,
    "insurance": 0,
    "side_effect": 1,
    "usage": 0,
    "others": 0,
    "score": 0.3,
    "text": "Hi! Thank you for calling Amgen Customer care helpline How can I assit you? Hi I am having frequent chills. I assume this is because of the Neulasta that I am taking Can you tell me why this is happening to me? Sure Sir I can totally Understand."
}, {
    "data_id": 2,
    "geo_id": 4,
    "geo_name": "Brazil",
    "drug_id": 200,
    "drug_name": "Blincyto",
    "concern": "availability",
    "availability": 1,
    "insurance": 0,
    "side_effect": 0,
    "usage": 0,
    "others": 0,
    "score": -0.1,
    "text": "To help you out can you Please help me with your Name and Phone number? Mike, and the number is 0873462867 Thank You Mike for the Information"
}, {
    "data_id": 3,
    "geo_id": 4,
    "geo_name": "Brazil",
    "drug_id": 201,
    "drug_name": "Neulasta",
    "concern": "side_effect",
    "availability": 0,
    "insurance": 0,
    "side_effect": 1,
    "usage": 0,
    "others": 0,
    "score": 0.5,
    "text": "Could you please repeat the name of the drug that you are taking? Neulasta N E U L A S T A Thamnk You. How long have you been taking this drug? 3 months Is there some other drug or food that you take in combination with this?"
}, {
    "data_id": 4,
    "geo_id": 2,
    "geo_name": "India",
    "drug_id": 202,
    "drug_name": "Infergen",
    "concern": "availability",
    "availability": 1,
    "insurance": 0,
    "side_effect": 0,
    "usage": 0,
    "others": 0,
    "score": 0.3,
    "text": "No. I take it 1 hour post dinner Thank You Mike. This is something we are observing for the first time, we feel you should wait for a day or to, if this continues you should consult a doctor"
}, {
    "data_id": 5,
    "geo_id": 4,
    "geo_name": "Brazil",
    "drug_id": 203,
    "drug_name": "Aimovig",
    "concern": "usage",
    "availability": 0,
    "insurance": 0,
    "side_effect": 0,
    "usage": 1,
    "others": 0,
    "score": -0.1,
    "text": "Hi! Thank you for calling Amgen Customer care helpline How can I assit you? I am unable to take my intravenous. What do I do? I am very scared. What if I hurt myself?"
}]

print type(callRecordNewData)

# class TestCheck:
#     def __init__(self, values_pie, labels_pie, colors_pie, values_bar, labels_bar):
#         self.pieChart = render_template('charts.html', set=zip(values_pie, labels_pie, colors_pie))
#         self.barChart = render_template('chartsNew.html', values=values_bar, labels=labels_bar)


@app.route('/', methods=['GET'])
def home():
    return render_template('Home.html')


@app.route('/api/v1/resources/callRecordData/all', methods=['GET'])
def api_all():
    return jsonify(callRecordData)


@app.route('/api/v1/resources/callRecordData', methods=['GET'])
def api_id():
    if 'data_id' in request.args:
        data_id = int(request.args['data_id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    for callRecord in callRecordData:
        if callRecord['data_id'] == data_id:
            results.append(callRecord)

    return jsonify(results)


@app.route('/api/v1/resources/callRecordData/filter', methods=['GET'])
def api_individual_id():
    results = []
    if ('geo_id' in request.args) and ('drug_id' not in request.args):
        print 'called'
        geo_id = int(request.args['geo_id'])

        for callRecord in callRecordData:
            if callRecord['geo_id'] == geo_id:
                results.append(callRecord)

    elif ('geo_id' in request.args) and ('drug_id' in request.args):
        geo_id = int(request.args['geo_id'])
        drug_id = int(request.args['drug_id'])

        print callRecordData
        for callRecord in callRecordData:
            if (callRecord['geo_id'] == geo_id) and (callRecord['drug_id'] == drug_id):
                results.append(callRecord)

    elif ('drug_id' in request.args) and ('geo_id' not in request.args):
        drug_id = int(request.args['drug_id'])

        for callRecord in callRecordData:
            if callRecord['drug_id'] == drug_id:
                results.append(callRecord)

    # concern_count_array = []
    # concern_counts = {}
    availability_count = 0
    side_effect_count = 0
    insurance_count = 0
    usability_count = 0
    others_count = 0
    score_count = 0
    sum_score_count = 0

    print results
    if not results:
        return 'No Record Found'
    
    for callRecord in results:
        if callRecord['availability'] == 1:
            availability_count = availability_count + 1
        if callRecord['side_effect'] == 1:
            side_effect_count = side_effect_count + 1
        if callRecord['usage'] == 1:
            usability_count = usability_count + 1
        if callRecord['insurance'] == 1:
            insurance_count = insurance_count + 1
        if callRecord['others'] == 1:
            others_count = others_count + 1
        sum_score_count = sum_score_count + callRecord['score']
        score_count = score_count + 1

    if score_count == 0:
        avg_score_count = 0
    else:
        avg_score_count = (sum_score_count / score_count)
    # concern_counts['Availability'] = availability_count
    # concern_counts['Side_Effect'] = side_effect_count
    # concern_counts['Usability'] = usability_count
    # concern_counts['Insurance'] = insurance_count
    # concern_counts['Others'] = others_count
    # concern_count_array.append(concern_counts)
    # print concern_count_array

    labels_pie = ['availability', 'side_effect', 'usage', 'insurance', 'others']
    values_pie = [availability_count, side_effect_count, usability_count, insurance_count, others_count]
    colors_pie = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA", "#ABCDEF"]
    #
    labels_bar = ['score']
    values_bar = [avg_score_count]

    # return TestCheck(values_pie, labels_pie, colors_pie, values_bar, labels_bar)
    if 'bar' in request.args:
        return render_template('chartsNew.html', values=values_bar, labels=labels_bar)
    if 'pie' in request.args:
        return render_template('charts.html', set=zip(values_pie, labels_pie, colors_pie))

    # return jsonify(results)

@app.route('/api/v1/resources/callRecordData/wordcloud', methods=['GET'])
def wordcloud_something():
    user_input=""
    if ('geo_id' in request.args) and ('drug_id' not in request.args):
        geo_id = int(request.args['geo_id'])

        for callRecord in callRecordData:
            if callRecord['geo_id'] == geo_id:
                user_input=user_input+callRecord['text']

    elif ('geo_id' in request.args) and ('drug_id' in request.args):
        geo_id = int(request.args['geo_id'])
        drug_id = int(request.args['drug_id'])

        for callRecord in callRecordData:
            if (callRecord['geo_id'] == geo_id) and (callRecord['drug_id'] == drug_id):
                user_input = user_input + callRecord['text']

    elif ('drug_id' in request.args) and ('geo_id' not in request.args):
        drug_id = int(request.args['drug_id'])

        for callRecord in callRecordData:
            if callRecord['drug_id'] == drug_id:
                user_input = user_input + callRecord['text']

    print user_input
    cloud = WordCloud(background_color="White").generate(user_input)

    plt.imshow(cloud)
    plt.axis('off')
    return plt.show()

if __name__ == '__main__':
    app.run()
