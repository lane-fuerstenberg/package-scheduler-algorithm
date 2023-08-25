import pandas as pd
import datetime


def load_distance_table():
    df = pd.read_excel("Resources\\WGUPS Distance Table Fixed.xlsx")
    df = df.rename(index=df['Unnamed: 1'])
    df = df.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1)
    df = df.rename(columns=df.iloc[6])
    df = df.drop(df[:7].index)

    df.columns = df.columns.str.replace('\n', '')
    df.index = df.index.str.replace('\n', '')
    df.columns = df.columns.str.strip()
    df.index = df.index.str.strip()

    df = df.fillna(0)
    df = df.add(df.T)

    return df


distance_data = load_distance_table()


def miles_to_minutes(miles):
    return (miles / 18) * 60


def find_distance(package1, package2):
    return search(string_format_package(package1), string_format_package(package2))


def search(row, column):
    return distance_data.at[row, column]


def string_format_package(package):
    if package is None or package == "HUB":
        return "HUB"

    return package.address + "(" + str(package.zip) + ")"
