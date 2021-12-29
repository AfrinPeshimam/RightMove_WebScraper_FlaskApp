def clean_price(price):
    price= price.replace('£', '')
    price= price.replace('POA', 'NaN')
    return price