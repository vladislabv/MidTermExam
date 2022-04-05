import pandas as pd
import numpy as np
from datetime import date
import requests
import json
from matplotlib import pyplot as plt

def main():
    pass

if __name__ == "__main__":
    BASE_URL = "https://ies-midterm.soulution.rocks"
    AUTH_DICT = json.dumps({
        "cuni":"77554807"
    })
    login_response = requests.post(BASE_URL + '/login', data=AUTH_DICT)
    if login_response.status_code:
        login_response_json = login_response.json()
        API_TOKEN = login_response_json['data'].get('personal_code')
        DATASET_IDS = login_response_json['data'].get('dataset_ids')
    else:
        raise Exception('The login to the API was not successful, the response with code {login_response.status_code} returned {login_response.content}')

    def get_nice_status_code(url):
        response = requests.get(BASE_URL+'/data/'+id)
        if response.status_code:
            temp_result = response.json()
            if len(temp_result['data']):
                return response.json()
            else:
                err_msg = temp_result.get('message')
                print(f'Sorry, the request was not successfull. Error message: {err_msg}.')
                return 404
        else:
            print(f'Sorry, the response was return with the code {response.status_code}.')
            return response.status_code

    result = list()

    for id in DATASET_IDS:
        success = False
        while not success:
            temp_response = get_nice_status_code(BASE_URL+'/data/'+id)
            success = True if isinstance(temp_response, dict) else False
        else:
            #proceed analysis
            result.append(temp_response)

    # validate the result 
    validation_set = []
    for i in result:
        if len(i.get('data').get('company')):
            validation_set.append(True)
        else:
            validation_set.append(False)
        
    if all(validation_set):
        print("All data were successfully extracted.")
    else:
        raise Exception("Some data were lost during the requests. This is unacceptable.")

    # exctract data and form it as pandas dataframe
    result_df = pd.DataFrame()
    column_names = ['Date','Open','High','Low','Close','Adj.Close','Volume']
    for i in result:
        i_data = i.get('data')
        company_name = i_data.get('company')
        if i_data.get('data'):
            data = pd.DataFrame(i_data.get('data'))
            data.columns = column_names
            data = data.set_index('Date')
            data = data.apply(pd.to_numeric, errors='coerce')
            data['company'] = company_name
            result_df = pd.concat([result_df, data], axis=0)
        else:
            raise Exception(f'Data for the company {company_name} were not found.')
        
    #question_1
    result_df = result_df.dropna(axis=0)
    result_df.index = pd.to_datetime(result_df.index)
    date_range = pd.date_range(start="2019-01-02", end="2020-11-12")
    question1 = date_range.difference(result_df.index)

    #question_2
    question_2 = result_df.groupby('company')['Volume'].max()
    #.loc[result_df['Volume'] == result_df['Volume'].max(), 'Date']
    #question_3
    result_df['Gain'] = np.where(result_df['Close'] - result_df['Open'] >= 0, result_df['Close'] - result_df['Open'],0)
    result_df['Loss'] = np.where(result_df['Close'] - result_df['Open'] < 0, result_df['Close'] - result_df['Open'], 0)
    max_gain = result_df.groupby('company')['Gain'].max()
    min_loss = result_df.groupby('company')['Loss'].min()
    #q4
    min_adj = result_df.groupby('company')['Adj.Close'].min()
    max_adj = result_df.groupby('company')['Adj.Close'].max()
    #q5
    q5 = result_df.groupby('company')['Volume'].sum()
    #q6
    result_df['DateWeeks'] = result_df.index - pd.to_timedelta(7, unit='d')
    q6=result_df.dropna(axis=0).groupby(['company', pd.Grouper(key='DateWeeks', freq='W-MON')])['Volume'].mean()
    #q7
    comp_max = result_df.loc[result_df['Volume']==result_df['Volume'].max(), 'company'].values[0]
    comp_max_df = result_df.loc[result_df['company']==comp_max, ]
    comp_max_df.plot(x='Date', y='Close')
    plt.show()

    print(result_df)