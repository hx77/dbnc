import pandas as pd
import requests

# Change the file name to the input file name
file_name = "Python Quiz Input.csv"
usps_url = "https://tools.usps.com/tools/app/ziplookup/zipByAddress"


def send_request(url: str, payload: dict):
    """
    Send a post request to the USPS API and return JSON object of the result
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/97.0.4692.71 Safari/537.36 '
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def read_input_data():

    # Read CSV file into DataFrame df
    df = pd.read_csv(file_name)

    for i in range(len(df)):
        # Create a row object for each row
        row_obj = df.loc[i]
        payload = {
            'companyName': row_obj.Company,
            'address1': row_obj.Street,
            'city': row_obj.City,
            'state': row_obj.St,
            'zip': row_obj.ZIPCode
        }
        response = send_request(usps_url, payload)
        if response['resultStatus'] == 'SUCCESS':
            # valid
            print('valid')
        else:
            # invalid
            print('invalid')


def main():
    read_input_data()


if __name__ == '__main__':
    main()
