import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Project imports
from utils import stats as stats

def plot_distribution_lengths(messages):
    df_distr = stats.len_distr_by_member(messages)
    df_long = df_distr.melt(id_vars="sender", var_name="length", value_name="count")
    df_plot = df_long[df_long["length"] <= 20]
    plt.figure(figsize=(8,5))
    sns.lineplot(data=df_plot, x="length", y="count", hue="sender", marker="o")
    plt.title("Message length distribution by sender")
    plt.xlabel("Message length (#tokens)")
    plt.ylabel("Number of messages")
    plt.legend(title="Sender")
    plt.show()

def plot_messages_over_month_year(messages):
    df = stats.messages_over_month_year(messages)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df["month_year"], df["count"], marker="o")
    k = 4
    ax.set_xticks(df["month_year"][::k])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_messages_over_month(messages):
    out = stats.messages_over_month(messages)
    plt.figure(figsize=(9,5))
    plt.bar(out["month_name"], out["count"])
    plt.title("Messages by calendar month (all years)")
    plt.xlabel("Month")
    plt.ylabel("Messages")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def plot_messages_over_weekday(messages):
    wd = stats.messages_over_weekday(messages)
    plt.figure(figsize=(8,5))
    plt.bar(wd["weekday_name"], wd["count"])
    plt.title("Messages by weekday (all years)")
    plt.xlabel("Weekday")
    plt.ylabel("Messages")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def plot_messages_over_hour(messages):
    hrs = stats.messages_over_hour(messages)
    plt.figure(figsize=(9,5))
    plt.bar(hrs["hour"], hrs["count"])
    plt.title("Messages by hour of day (all years)")
    plt.xlabel("Hour of day (0–23)")
    plt.ylabel("Messages")
    plt.xticks(range(0,24,2))
    plt.tight_layout()
    plt.show()

def plot_messages_over_year(messages):
    yr = stats.messages_over_year(messages)
    plt.figure(figsize=(8,5))
    plt.bar(yr["year"], yr["count"])
    plt.title("Messages per year")
    plt.xlabel("Year")
    plt.ylabel("Messages")
    plt.xticks(yr["year"])
    plt.tight_layout()
    plt.show()

def plot_shares_monthly(messages):
    perc = stats.percentages_by_member_over_time(messages)
    plt.figure(figsize=(10,6))
    sns.lineplot(data=perc, x="ts", y="pct", hue="sender", marker="o")
    plt.title("Share of messages per month by sender")
    plt.xlabel("Month"); plt.ylabel("Share of messages")
    plt.tight_layout(); plt.show()

def plot_shares_bimonthly(messages):
    bi = stats.percentages_by_member_over_time_bimonth(messages)

    plt.figure(figsize=(10,6))
    sns.lineplot(data=bi, x="ts", y="pct", hue="sender", marker="o")
    plt.title("Share of messages per 2-month period")
    plt.xlabel("Period end")
    plt.ylabel("Share of messages")

def plot_shares_semiannual(messages):
    semi = stats.percentages_by_member_over_time_semiannual(messages)

    plt.figure(figsize=(10,6))
    sns.lineplot(data=semi, x="ts", y="pct", hue="sender", marker="o")
    plt.title("Share of messages per half-year (zeros filled)")
    plt.xlabel("Half-year")
    plt.ylabel("Share of messages")

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()