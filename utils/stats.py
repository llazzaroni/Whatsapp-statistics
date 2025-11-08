import pandas as pd
import calendar
import numpy as np

# Project imports
from utils import helpers as helpers

def number_of_words(messages):
    lengths = messages["text"].fillna("").map(lambda s: len(helpers.tokenize(s)))
    return lengths.sum()

def most_sent_message_of_one_word(messages):
    df = messages.copy()
    df["tokens"] = df["text"].fillna("").map(helpers.tokenize)
    one = df[df["tokens"].map(len) == 1].copy()
    one["word"] = one["tokens"].str[0].str.casefold()

    counts = (one.groupby("word")
                .size()
                .reset_index(name="count")
                .sort_values("count", ascending=False))
    return counts


def most_senders(messages):
    senders = messages["sender"].unique()
    result = {}
    for sender in senders:
        result[sender] = len(messages[messages["sender"] == sender])

    sorted_result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    return sorted_result

def mean_msg_len_by_sender(messages):
    lengths = messages["text"].fillna("").map(lambda s: len(helpers.tokenize(s)))
    result = lengths.groupby(messages["sender"]).mean().to_dict()
    rounded = {k: round(v, 2) for k, v in result.items()}
    return rounded

def len_distr_by_member(messages, excluded=["Lorenzo Garro"]):
    result = []
    senders = messages["sender"].unique()
    for sender in senders:
        if sender in set(excluded):
            continue
        distribution = {}
        msg_sender = messages[messages["sender"] == sender]
        msg_sender = msg_sender.assign(
            length = msg_sender["text"].fillna("").map(lambda s: len(helpers.tokenize(s)))
        )
        lengths = msg_sender["length"].unique()
        for length in lengths:
            distribution[length] = len(msg_sender[msg_sender["length"] == length]) / len(msg_sender)
        distribution["sender"] = sender
        result.append(distribution)
    df_distr = pd.DataFrame(result)    
    return df_distr


def messages_over_month_year(messages):
    df = messages.copy()

    df["date_dt"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

    monthly = (
        df.groupby(df["date_dt"].dt.to_period("M"))
          .size()
          .rename("count")
          .reset_index()
    )

    monthly["month_year"] = monthly["date_dt"].astype(str)

    return monthly[["month_year", "count"]].sort_values("month_year")


def messages_over_month(messages: pd.DataFrame):
    df = messages.copy()
    df["date_dt"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["date_dt"])

    out = (
        df.groupby(df["date_dt"].dt.month)
          .size()
          .rename("count")
          .reset_index()
          .rename(columns={"date_dt": "month_num"})
    )
    out["month_name"] = pd.to_datetime(out["month_num"], format="%m").dt.strftime("%B")
    return out[["month_num", "month_name", "count"]].sort_values("month_num")

def messages_over_weekday(messages: pd.DataFrame):
    df = messages.copy()
    df["date_dt"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["date_dt"])

    out = (df.groupby(df["date_dt"].dt.weekday)
             .size()
             .reset_index(name="count")
             .rename(columns={"date_dt": "weekday_num"}))

    out["weekday_name"] = out["weekday_num"].map(dict(enumerate(calendar.day_name)))
    return out[["weekday_num", "weekday_name", "count"]].sort_values("weekday_num")

def messages_over_hour(messages):
    df = messages.copy()
    if "date_dt" not in df:
        if "time" in df:
            df["date_dt"] = pd.to_datetime(df["date"] + " " + df["time"], dayfirst=True, errors="coerce")
        else:
            df["date_dt"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["date_dt"])

    out = (df.groupby(df["date_dt"].dt.hour)
             .size()
             .reset_index(name="count")
             .rename(columns={"date_dt": "hour"}))
    out = out.rename(columns={"index": "hour"})
    out["hour"] = out["hour"].astype(int)
    return out.sort_values("hour")

def messages_over_year(messages):
    df = messages.copy()

    if "date_dt" not in df:
        if "time" in df:
            df["date_dt"] = pd.to_datetime(df["date"] + " " + df["time"],
                                           dayfirst=True, errors="coerce")
        else:
            df["date_dt"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["date_dt"])

    out = (df.groupby(df["date_dt"].dt.year)
             .size()
             .reset_index(name="count")
             .rename(columns={"date_dt": "year"}))
    out["year"] = out["year"].astype(int)
    return out.sort_values("year")

def percentages_by_member_over_time(messages, excluded=["Lorenzo Garro", "Meta AI"]) -> pd.DataFrame:
    df = messages.copy()
    
    for excluded_sender in excluded:
        df = df[df["sender"] != excluded_sender]

    df["date_dt"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["date_dt"])

    monthly = (df.assign(period=lambda x: x["date_dt"].dt.to_period("M"))
                 .groupby(["period", "sender"])
                 .size()
                 .rename("count")
                 .reset_index())

    monthly["pct"] = (
        monthly["count"] /
        monthly.groupby("period")["count"].transform("sum")
    )
    monthly["pct_100"] = (monthly["pct"] * 100).round(2)

    monthly["ts"] = monthly["period"].dt.to_timestamp()
    monthly["month_year"] = monthly["period"].astype(str)

    return monthly.sort_values(["ts", "sender"])

def percentages_by_member_over_time_bimonth(messages, excluded=["Lorenzo Garro", "Meta AI"]):
    df = messages.copy()

    for excluded_sender in excluded:
        df = df[df["sender"] != excluded_sender]

    if "time" in df:
        df["date_dt"] = pd.to_datetime(df["date"] + " " + df["time"], dayfirst=True, errors="coerce")
    else:
        df["date_dt"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["date_dt"])

    df["period"] = df["date_dt"].dt.to_period("2M")

    counts = (df.groupby(["period", "sender"])
                .size()
                .rename("count")
                .reset_index())

    all_periods = pd.period_range(df["period"].min(), df["period"].max(), freq="2M")
    all_senders = df["sender"].unique()
    full_index = pd.MultiIndex.from_product([all_periods, all_senders],
                                            names=["period", "sender"])
    counts_full = (counts.set_index(["period", "sender"])
                         .reindex(full_index, fill_value=0)
                         .reset_index())

    totals = counts_full.groupby("period")["count"].transform("sum")
    counts_full["pct"] = np.divide(counts_full["count"], totals, out=np.zeros_like(totals, dtype=float), where=totals!=0)
    counts_full["pct_100"] = (counts_full["pct"] * 100).round(2)

    counts_full["ts"] = counts_full["period"].dt.to_timestamp()
    counts_full["label"] = counts_full["period"].astype(str)

    return counts_full.sort_values(["ts", "sender"])

def percentages_by_member_over_time_semiannual(messages, excluded=["Lorenzo Garro", "Meta AI"]) -> pd.DataFrame:
    df = messages.copy()
    
    for excluded_sender in excluded:
        df = df[df["sender"] != excluded_sender]

    if "date_dt" not in df:
        if "time" in df:
            df["date_dt"] = pd.to_datetime(df["date"] + " " + df["time"], dayfirst=True, errors="coerce")
        else:
            df["date_dt"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["date_dt"])

    df["period"] = df["date_dt"].dt.to_period("2Q-DEC")

    counts = (df.groupby(["period", "sender"])
                .size()
                .rename("count")
                .reset_index())

    all_periods = pd.period_range(df["period"].min(), df["period"].max(), freq="2Q-DEC")
    all_senders = df["sender"].unique()
    full_index = pd.MultiIndex.from_product([all_periods, all_senders], names=["period", "sender"])
    counts_full = (counts.set_index(["period", "sender"])
                         .reindex(full_index, fill_value=0)
                         .reset_index())

    totals = counts_full.groupby("period")["count"].transform("sum")
    counts_full["pct"] = np.divide(counts_full["count"], totals, out=np.zeros_like(totals, dtype=float), where=totals!=0)
    counts_full["pct_100"] = (counts_full["pct"] * 100).round(2)

    counts_full["ts"] = counts_full["period"].dt.to_timestamp()
    counts_full["label"] = counts_full["period"].astype(str)

    return counts_full.sort_values(["ts", "sender"])
