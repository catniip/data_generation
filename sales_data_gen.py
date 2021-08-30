import numpy as np
import pandas as pd
from faker.providers.person.en import Provider


def random_names(name_type, size):
    """
    Generate n-length ndarray of person names.
    name_type: a string, either first_names or last_names
    """
    names = getattr(Provider, name_type)
    return np.random.choice(names, size=size)


def random_genders(size, p=None):
    """Generate n-length ndarray of genders."""
    if not p:
        # default probabilities
        p = (0.49, 0.49, 0.01, 0.01)
    gender = ("M", "F", "O", "")
    return np.random.choice(gender, size=size, p=p)


def random_dates(start, end, size):
    """
    Generate random dates within range between start and end.    
    Adapted from: https://stackoverflow.com/a/50668285
    """
    # Unix timestamp is in nanoseconds by default, so divide it by
    # 24*60*60*10**9 to convert to days.
    divide_by = 24 * 60 * 60 * 10**9
    start_u = start.value // divide_by
    end_u = end.value // divide_by
    return pd.to_datetime(np.random.randint(start_u, end_u, size), unit="D")


def random_customerid(size, start, end, order=5):
    """
    Generate customer id.
    :param size: size of output array
    :param start: start of birthday range
    :param end: end of birthday range
    :param order: the order of customer id
    :param replace: reuse the same customer id if True
    """
    cid = random_orderid(size, order=5)
    bod = random_dates(start, end, size)
    return cid, bod


def random_orderid(size, order=7):
    """
    Generate customer id.
    :param size: size of output array
    :param order: the order of customer id
    """
    minval = 10**(order - 1)
    maxval = 10**order
    return np.random.choice(np.arange(minval, maxval, dtype=int), size=size, replace=False)


def random_acquisition_channel(size, entries=None):
    """
    Generate acquisition channel.
    :param size: size of output array
    :param entries: entry names
    """
    if entries is None:
        entries = ['radio', 'tv', 'online', 'billboard', 'newspaper', 'magazine', 'friends']
    return np.random.choice(entries, size=size)


def random_product(size, names=None, max_prod=10, minmax_price=(100, 10000)):
    """
    Generate product name and its price.
    :param size: size of output array
    :param names: a list of product names
    :param max_prod: max number of product types
    :param minmax_price: a tuple of min max of product prices
    """
    if names is None:
        names = ['Product']
    prices = np.random.randint(*minmax_price, size=max_prod)
    
    prod_name = []
    count = 0
    while len(prod_name) < max_prod:
        for tx in names:
            prod_name.append(tx + str(count))
            if len(prod_name) >= max_prod:
                break
        count += 1
    prod_price = np.stack([prod_name, prices]).T
    ind = np.random.randint(max_prod, size=size)
    output = prod_price[ind]
    return output[:, 0], output[:, 1]


# Generate customer data ===============================================================
size_customer = 100  
df_customer = pd.DataFrame()
df_customer['customer_id'], df_customer['birth_date'] = random_customerid(
    size=size_customer,
    start=pd.to_datetime('1940-01-01'), 
    end=pd.to_datetime('2008-01-01'), 
)
df_customer['acquisition_channel'] = random_acquisition_channel(size_customer)
df_customer.to_csv('customer_data.csv', index=False)


# GEnerate order data ===================================================================
size_order = 10000
df_order = pd.DataFrame()
df_order['order_id'] = random_orderid(size_order, order=7)
df_order['transaction_date'] = random_dates(
    start=pd.to_datetime('2000-01-01'), end=pd.to_datetime('2021-01-01'), size=size_order
)
df_order['product'], df_order['price'] = random_product(size_order)
df_order['quantity'] = np.random.randint(1, 10, size=size_order)
df_order['customer_id'] = np.random.choice(df_customer.customer_id, size=size_order)
df_order.to_csv('orders_data.csv', index=False)



