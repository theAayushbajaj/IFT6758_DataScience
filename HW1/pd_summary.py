"""
This assignment is based off of Greg Baker's data science course at SFU

All areas which require work are marked with a "TODO" flag.
"""
import pandas as pd


def city_lowest_precipitation(totals: pd.DataFrame) -> str:
    """
    Given a dataframe where each row represents a city, and each column is a month Jan-Dec of a
    particular year, return the city with the lowest total precipitation.
    """

    # TODO
    total_precipitation_per_city = totals.sum(axis=1)
    return total_precipitation_per_city[total_precipitation_per_city==total_precipitation_per_city.min()].index[0]


def avg_precipitation_month(totals: pd.DataFrame, counts: pd.DataFrame) -> pd.DataFrame:
    """
    Determine the average precipitation in these locations for each month. That will be the total
    precipitation for each month, divided by the total observations for that months.
    """

    # TODO
    total_precipitation_per_month = totals.sum(axis=0)
    total_observations_per_month = counts.sum(axis=0)
    average_precipitation_per_month = total_precipitation_per_month.div(total_observations_per_month)

    return average_precipitation_per_month


def avg_precipitation_city(totals: pd.DataFrame, counts: pd.DataFrame) -> pd.DataFrame:
    """
    Do the same for the cities: give the average precipitation (daily precipitation averaged over
    the month) for each city.
    """

    # TODO
    total_precipitation_per_city = totals.sum(axis=1)
    total_observations_per_city = counts.sum(axis=1)
    average_precipitation_per_city = total_precipitation_per_city.div(total_observations_per_city)

    return average_precipitation_per_city


# no quarterly as this is a bit of a pain


def main():
    totals = pd.read_csv("data/totals.csv").set_index(keys=["name"])
    counts = pd.read_csv("data/counts.csv").set_index(keys=["name"])

    print(totals)
    print(counts)

    # You can use this to steer your code
    print(f"Row with the lowest precipitation:\n{city_lowest_precipitation(totals)}")
    print(f"Average precipitation per month:\n{avg_precipitation_month(totals, counts)}")
    print(f"Average precipitation per city:\n{avg_precipitation_city(totals, counts)}")


if __name__ == "__main__":
    main()
