"""
This assignment is based off of Greg Baker's data science course at SFU

By the end of this assignment, you should be convinced that using native Pandas functionality
over trying to implement things on your own is the way to go. You should also feel quite 
comfortable with pivoting DataFrames to accomplish your objectives.

All areas which require work are marked with a "TODO" flag.
"""
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from geopy import distance

from typing import Tuple
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def get_precip_data(fp: str = "data/precipitation.csv") -> pd.DataFrame:
    return pd.read_csv(fp, parse_dates=[2])


def date_to_month(d: pd.Timestamp) -> str:
    """
    You may need to modify this function, depending on your data types (if they don't match the
    expected input types)
    """
    return "%04i-%02i" % (d.year, d.month)


def pivot_months_pandas(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Create monthly precipitation totals for each station in the data set.

    This should use Pandas methods to manipulate the data. Round the precipitation (mm) to the 1st
    decimal place.
    """
    monthly, counts = None, None

    # TODO
    data['month'] = pd.to_datetime(data.date).dt.strftime("%Y-%m")
    monthly = data.pivot_table(values='precipitation', index=['name'],
                       columns=['month'], aggfunc="sum").round(1)
    monthly.sort_index(inplace=True)
    counts = data.pivot_table(values='precipitation', index=['name'],
                       columns=['month'], aggfunc="size")
    counts.sort_index(inplace=True)

    return monthly,counts


def pivot_months_loops(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Create monthly precipitation totals for each station in the data set.
    This does it the hard way: using Pandas as a dumb data store, and iterating in Python.

    Never do things this way!!!
    """
    # Find all stations and months in the data set.
    stations = set()
    months = set()
    for i, r in data.iterrows():
        stations.add(r["name"])
        m = date_to_month(r["date"])
        months.add(m)

    # Aggregate into dictionaries so we can look up later.
    stations = sorted(list(stations))
    row_to_station = dict(enumerate(stations))
    station_to_row = {s: i for i, s in row_to_station.items()}

    months = sorted(list(months))
    col_to_month = dict(enumerate(months))
    month_to_col = {m: i for i, m in col_to_month.items()}

    # Create arrays for the data, and fill them.
    precip_total = np.zeros((len(row_to_station), 12), dtype=np.float64)
    obs_count = np.zeros((len(row_to_station), 12), dtype=np.float64)

    for _, row in data.iterrows():
        m = date_to_month(row["date"])
        r = station_to_row[row["name"]]
        c = month_to_col[m]

        precip_total[r, c] += row["precipitation"]
        obs_count[r, c] += 1

    # Build the DataFrames we needed all along (tidying up the index names while we're at it).
    totals = pd.DataFrame(
        data=np.round(precip_total, 1),
        index=stations,
        columns=months,
    )
    totals.index.name = "name"
    totals.columns.name = "month"

    counts = pd.DataFrame(
        data=obs_count.astype(int),
        index=stations,
        columns=months,
    )
    counts.index.name = "name"
    counts.columns.name = "month"

    return totals, counts


def compute_pairwise(df: pd.DataFrame, func: callable) -> pd.DataFrame:
    """
    Complete this function, which takes a dataframe and a function of a pair of columns of
    the dataframe as an input, and returns a dataframe that contains the function applied to
    **each pair of row of the dataframe**.

    For this we will use the `pdist` and `squareform` functions from the `scipy.spatial` library.
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html
    - https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.squareform.html

    Hint: Make sure the input DataFrame has the station name as the index, not a number! You can
    do this by pivoting the DataFrame. It should look something like this excerpt:

    ```
                             column1     column2
    name
    BURNABY SIMON FRASER U   ...        ...
    CALGARY INTL A           ...        ...
    ```
    """
    result = None

    # TODO
    # result = df.apply(lambda x: df.apply(lambda y: func(x, y), axis=1), axis=1).T
    # return result

    result = pd.DataFrame(
        squareform(pdist(df, metric = func)),
        columns = df.index,
        index = df.index
        )
    return result

def geodesic(latlon1, latlon2) -> int:
    """
    Defines a metric between two points; in our case, our two points are latitude/longitude
    coordinates. "We" have to do some geometry if we want to get the distance between two points
    on an ellipsoid (Earth), but we will abstract this functionality to another geopy. You can read
    more about the math here:
        - https://en.wikipedia.org/wiki/Geodesics_on_an_ellipsoid

    A simplification of this is to instead consider a sphere:
        - https://en.wikipedia.org/wiki/Haversine_formula
    """
    return int(distance.distance(tuple(latlon1), tuple(latlon2)).km)


def compute_pairwise_distances(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given the `compute_pairwise()` and `geodesic()` function defined above, compute the pairwise
    distance between each of the stations. The input should be the original raw dataframe loaded
    from the CSV.
    """
    new_df = None

    # TODO: pivot the dataframe so that you have lat/lon as the columns, and names as the index
    new_df = df.groupby(['name'])[["latitude","longitude"]].first().sort_index()
    
    new_df = compute_pairwise(new_df,geodesic)
    return new_df


def correlation(u, v) -> float:
    """
    Compute the correlation between two sets of data
    - https://en.wikipedia.org/wiki/Correlation

    Specifically, the equation for Pearson's product-moment coefficient is:

        corr = E[(X - x_avg) * (Y - y_avg)] / (x_std * y_std)

    """
    corr = None
    # get appropriate indicies (filter out NaNs; '~' is logical 'not')
    idx_u = ~pd.isna(u)
    idx_v = ~pd.isna(v)
    idx = idx_u & idx_v

    u = u[idx]
    v = v[idx]

    # TODO: compute mean and std of valid entries
    u_mean = u.mean()
    v_mean = v.mean()

    u_std = u.std()
    v_std = v.std()

    # TODO: compute correlation
    corr = (((u - u_mean)*(v - v_mean)).mean())/(u_std * v_std)
    return corr

def compute_pairwise_correlation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given the `compute_pairwise()` and `correlation()` completed above, compute the pairwise
    correlation of daily precipitation between stations. The goal here is to see if there is any
    correlation of precipitation between stations. Ideally we'd expect stations that are closer
    to each other to have higher correlation. The input should be the original raw dataframe loaded
    from the CSV.

    Note that you will probably have a diagonal of zeros when it should be ones - this is fine
    for the purposes of this assignment. `pdist` expects the metric function to be a proper metric,
    i.e. the distance between an element to itself is zero.
    """
    df = df.pivot(index = 'name',
             columns = 'date',
             values = 'precipitation')

    # TODO: pivot the dataframe so that you have one column for each date, and the station names
    # are the index
    result = compute_pairwise(df,correlation)
    return result


def compute_pairwise_correlation_pandas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Surprise! Pandas can actually do the correlation calculation for you in a single function
    call...

    You will pivot the table slightly differently, and then do a single function call on the
    dataframe:
    - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html

    You should get the same result as what you got for `compute_pairwise_correlation()`, with
    the exception of ones (correctly) along the diagonal.
    """

    # TODO
    df = df.pivot(index = 'name',
             columns = 'date',
             values = 'precipitation')
    df_corr = df.T.corr()
    #df_corr = df_corr.round(5)
    return df_corr


def main():
    np.random.seed(2023)
    data = get_precip_data()
    totals, counts = pivot_months_loops(data)
    #print(data.head())
    # optionally create the data... 
    #totals.to_csv("data/totals.csv")
    #counts.to_csv("data/counts.csv")
    #np.savez("data/monthdata.npz", totals=totals.values, counts=counts.values)

    # pivot monthspandas
    totals_pd, counts_pd = pivot_months_pandas(data)
    assert all(abs(totals - totals_pd).max() < 1e-10), "totals != totals_pd"
    assert all(abs(counts - counts_pd).max() < 1e-10), "counts != counts_pd"

    # compute pairwise
    test_df = pd.DataFrame([[0, 0], [0, 1], [1, 0]], columns=["x", "y"], index=list("abc"))
    euclidean = lambda xy1, xy2: np.sqrt((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2)
    expected_output = pd.DataFrame(
        {'a': {'a': 0, 'b': 1, 'c': 1},
        'b': {'a': 1, 'b': 0, 'c': np.sqrt(2)},
        'c': {'a': 1, 'b': np.sqrt(2), 'c': 0}}
    )
    output = compute_pairwise(test_df, euclidean)
    assert np.allclose(output, expected_output)

    # pairwise distances
    print(compute_pairwise_distances(data))

    # pairwise correlation
    print(compute_pairwise_correlation(data))

    # pairwise correlation
    print(compute_pairwise_correlation_pandas(data))

    #print(np.testing.assert_array_equal(compute_pairwise_correlation(data).values,compute_pairwise_correlation_pandas(data).values))
    print("Done!")


if __name__ == "__main__":
    main()
