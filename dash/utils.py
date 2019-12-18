from datetime import datetime as dt
import dateutil.parser


def split_date(df):
    df['year'] = df['published_at'].apply(
        lambda x: dateutil.parser.parse(x).year)
    df['month'] = df['published_at'].apply(
        lambda x: dateutil.parser.parse(x).month)
    return df


def per_month(df):
    return df.groupby(['year', 'month'])


def count(group):
    return group.size().to_frame('count')
