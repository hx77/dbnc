import pandas as pd
import requests
import sys


def send_request(payload: dict):
    """
    Send a post request to the USPS API and return JSON object of the result
    """
    url = 'https://tools.usps.com/tools/app/ziplookup/zipByAddress'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/97.0.4692.71 Safari/537.36 '
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    return response.json()


def append_validity_list(result_status: str, validity_list: list):
    """
    Create validity list depending on resultStatus in response
    """
    if result_status == 'SUCCESS':
        validity_list.append('Valid')
    else:
        validity_list.append('Invalid')


def add_new_col(df, data_list: list, header: str):
    """
    Add a new column using data in data_list and header
    """
    new_col = pd.DataFrame(data_list, columns=[header])
    df[header] = new_col[header]


def read_input_data(file_name):
    """
    Read in input file and write the output to the same file
    """

    # Read CSV file into DataFrame df, the first row is header
    df = pd.read_csv(file_name, header=0, index_col=None)
    # Initialize a validity_list to save the result
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
        response = send_request(payload)
        append_validity_list(response['resultStatus'], validity_list)

    add_new_col(df, validity_list, 'Validity')
    # Save DataFrame to the original csv file
    df.to_csv(file_name, index=False)
    print('A new column added!\n')


def main():
    if len(sys.argv) != 2:
        raise ValueError('Please provide file name.')

    file_name = sys.argv[1]
    read_input_data(file_name)


if __name__ == '__main__':
    main()
