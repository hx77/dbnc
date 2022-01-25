import pandas as pd

file_name = "Python Quiz Input.csv"


def read_input_data():
    # Read CSV file into DataFrame df
    df = pd.read_csv(file_name)

    for i in range(len(df)):
        # Create a row object for each row
        row_obj = df.loc[i]
        print(row_obj)


def main():
    read_input_data()


if __name__ == '__main__':
    main()
