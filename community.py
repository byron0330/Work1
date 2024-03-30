import time
import webbrowser
from city import data
from town import T_data
def proc_same_community_data(list,city,town):
    url='http://127.0.0.1:5000/?city={}&town={}'.format(data[city], T_data[data[city]][town],)
    webbrowser.open_new(url)
    time.sleep(5)