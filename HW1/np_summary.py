"""
This assignment is based off of Greg Baker's data science course at SFU

All areas which require work are marked with a "TODO" flag.
"""
import numpy as np


def city_lowest_precipitation(totals: np.array) -> int:
    """
    Given a 2D array where each row represents a city, and each column is a month Jan-Dec of a
    particular year, return the city with the lowest total precipitation.
    """

    # TODO
    total_precipitation_per_city = np.sum(totals, axis=1)
    city_index = np.argmin(total_precipitation_per_city)

    return city_index


def avg_precipitation_month(totals: np.array, counts: np.array) -> np.array:
    """
    Determine the average precipitation in these locations for each month. That will be the total
    precipitation for each month (axis 0), divided by the total observations for that months.
    """

    # TODO
    total_precipitation_per_month = np.sum(totals,axis=0)
    total_observations_per_month = np.sum(counts, axis=0)
    average_precipitation_per_month = np.divide(total_precipitation_per_month, total_observations_per_month, 
                                                 where=total_observations_per_month != 0)

    return average_precipitation_per_month


def avg_precipitation_city(totals: np.array, counts: np.array) -> np.array:
    """
    Do the same for the cities: give the average precipitation (daily precipitation averaged over
    the month) for each city.
    """

    # TODO
    total_precipitation_per_city = np.sum(totals,axis=1)
    total_observations_per_city = np.sum(counts, axis=1)
    average_precipitation_per_city = np.divide(total_precipitation_per_city, total_observations_per_city, 
                                                 where=total_observations_per_city != 0)

    return average_precipitation_per_city


def quarterly_precipitation(totals: np.array) -> np.array:
    """
    Calculate the total precipitation for each quarter in each city (i.e. the totals for each
    station across three-month groups). You can assume the number of columns will be divisible by 3.

    Hint: use the reshape function to reshape to a 4n by 3 array, sum, and reshape back to n by 4.
    """
    if totals.shape[1] != 12:
        raise NotImplementedError("Input array does not have 12 months!")

    # TODO
    # Determine the number of quarters (groups of three months).
    num_quarters = totals.shape[1] // 3

    # Reshape the data into a 4n by 3 array.
    reshaped_data = totals.reshape(-1, 3)

    # Calculate the total precipitation for each quarter (group of three months).
    total_precipitation_per_quarter = np.sum(reshaped_data, axis=1)

    # Reshape the result back to the original shape (n by 4).
    total_precipitation_per_quarter = total_precipitation_per_quarter.reshape(-1, num_quarters)

    return total_precipitation_per_quarter


def main():
    data = np.load("data/monthdata.npz")
    totals = data["totals"]
    counts = data["counts"]

    print(totals)
    print(counts)

    # You can use this to steer your code
    print(f"Row with the lowest precipitation:\n{city_lowest_precipitation(totals)}")
    print(f"Average precipitation per month:\n{avg_precipitation_month(totals, counts)}")
    print(f"Average precipitation per city:\n{avg_precipitation_city(totals, counts)}")
    print(f"Quarterly precipitation:\n{quarterly_precipitation(totals)}")


if __name__ == "__main__":
    main()
