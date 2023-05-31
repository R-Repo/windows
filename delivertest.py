test = {'num_of_items': 2, 'total_price': 100.0,
 'items': [{'product': 'Casement', 'option': '1', 'price': 550.0, 'color': 'White', 'height': 100.0, 'width': 100.0},
              {'product': 'Bifold', 'option': '2', 'price': 5530.0, 'color': 'White', 'height': 2000.0, 'width': 5000.0}],
              'address': {'street': '123 Main St', 'city': 'New York', 'County': 'NY', 'PostCode': '10001'}}

print(test)

import requests
r = requests.post('http://127.0.0.1:7777//api/v1.0/deliverdate', json=test)
print(r.json())

# import pandas as pd
# from datetime import date, timedelta
# dates_df = pd.DataFrame(columns=['date', 'price'])

# start_date = date.today() + timedelta(days=1)
# end_date = date.today() + timedelta(days=100)

# dates_df['date'] = pd.date_range(start_date, end_date, freq='D')
# dates_df['day_of_week'] = dates_df['date'].dt.day_of_week
# dates_df.loc[dates_df['day_of_week'] > 4, 'price'] = 300
# dates_df.loc[dates_df['day_of_week'] <= 4, 'price'] = 250
# dates_df.loc[0:14, 'price'] = None
# dates_df.loc[14:20, 'price'] = 500

# dates_df['date'] = dates_df['date'].dt.strftime('%Y.%m.%d')


# print(dates_df[['date', 'price']].to_json(orient="index"))