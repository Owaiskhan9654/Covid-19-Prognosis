from flask import Flask, render_template, request, jsonify, send_file, make_response
import pandas as pd

import joblib
import numpy as np

app = Flask(__name__)




@app.route('/prognosis/covid_19', methods=['GET', 'POST'])
def covid_prognosis():
	if request.method == 'GET':
		return render_template('Covid-19-prognosis.html',show_results=False)
	elif request.method == 'POST':
		form_data = request.form
		cough = [float(form_data.get('cough'))]
		fever = [float(form_data.get('fever'))]
		sore_throat = [float(form_data.get('sore_throat'))]
		shortness_in_breath = [float(form_data.get('shortness_in_breath'))]
		head_ace = [float(form_data.get('head_ache'))]
		sex = [float(form_data.get('sex'))]
		age = [float(form_data.get('age'))]
		vaccinated = [float(form_data.get('vaccinated'))]
		print('Data fetched',cough,fever,sore_throat,shortness_in_breath,head_ace,sex,age,vaccinated)
		prediction_data = pd.DataFrame({'cough':cough,'fever':fever,'sore_throat':sore_throat,'shortness_in_breath':shortness_in_breath,\
										'head_ace':head_ace,'age':age,'sex':sex})

		model = joblib.load(r'static/ml_model/finalized_lgb_model_model.sav')
		pred =model.predict(prediction_data)

		if np.round(pred) == 1.0:
			pred_perc=model.predict_proba(prediction_data)
			pred_perc =pred_perc[0][1]
			pred_perc = pred_perc * 100
			pred_text="Based on the features given model, you are {:.2f} % likely to have SARS COVID-19.".format(pred_perc)
			pred_perc = int(pred_perc)
			return render_template('Covid-19-prognosis.html',show_results=True,pred_text=pred_text,pred_perc=pred_perc)
		else:
			pred_perc = model.predict_proba(prediction_data)[0][0]
			pred_perc=pred_perc*100
			pred_text="Based on the features given, you are {:.2f} % unlikely to have SARS COVID-19".format(pred_perc)
			pred_perc=int(pred_perc)
			print(pred_perc)
			return render_template('Covid-19-prognosis.html',show_results=True,pred_text=pred_text,pred_perc=pred_perc)


@app.route('/', methods=['GET'])
def home():
	return render_template('home.html')


if __name__ == '__main__':
	app.run(host='127.0.0.1',debug=True)
