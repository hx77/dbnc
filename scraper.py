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


def create_validity_list(result_status: str, validity_list: list):
    """
    Create validity list depending on resultStatus in response
    """
    if result_status == 'SUCCESS':
        validity_list.append('Valid')
    else:
        validity_list.append('Invalid')


def read_input_data():
    """

    :return:
    """
    # Read CSV file into DataFrame df
    df = pd.read_csv(file_name)
    validity_list = []

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
        create_validity_list(response['resultStatus'], validity_list)

    new_col = pd.DataFrame(validity_list, columns=['Validity'])
    df['Validity'] = new_col['Validity']
    print(df)


def main():
    read_input_data()


if __name__ == '__main__':
    main()
