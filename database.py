from deta import Deta

DETA_KEY = 'd0jzuzphh5j_sDkreLLTREbvdc5jcsM3jMRx9S42nk6e'

#initialise project with key
deta = Deta(DETA_KEY)

#this is to create/connect to database

db = deta.Base("monthly_reports")

def insert_period(period, incomes, expenses, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": period, "incomes": incomes, "expenses": expenses, "comment": comment})


def fetch_all_periods():
    """Returns a dict of all periods"""
    res = db.fetch()
    return res.items


def get_period(period):
    """If not found, the function will return None"""
    return db.get(period)