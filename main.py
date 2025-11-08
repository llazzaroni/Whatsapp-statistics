# Project specific imports
from utils import data as data
from utils import stats as stats
from utils import plots as plots
from utils import helpers as helpers


# Load the data
path = "/Users/lorenzolazzaroni/Documents/Programming/Python/bois/_chat.txt"
# Expects italian format. TODO: adapt for english format
messages = data.load_messages_pd(path)

# Plot with plots.<FUNCTION>
