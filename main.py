import argparse

# Project specific imports
from utils import data as data
from utils import stats as stats
from utils import plots as plots
from utils import helpers as helpers

def main(args):
    path = args.data

    # Load the messages
    messages = data.load_messages_pd(path)

    # Examples of plots
    print(stats.number_of_words(messages))
    print(stats.most_sent_message_of_one_word(messages))
    print(stats.most_senders(messages))
    print(stats.mean_msg_len_by_sender(messages))
    plots.plot_distribution_lengths(messages)
    plots.plot_messages_over_hour(messages)
    plots.plot_messages_over_month(messages)
    plots.plot_messages_over_month_year(messages)
    plots.plot_messages_over_weekday(messages)
    plots.plot_messages_over_year(messages)
    plots.plot_shares_bimonthly(messages)
    plots.plot_shares_monthly(messages)
    plots.plot_shares_semiannual(messages)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Build cycling winners dataset.")
    p.add_argument("--data")
    args = p.parse_args()
    main(args)