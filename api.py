from flask import *
import pandas as pd
from datetime import date, timedelta
import json, time

app = Flask(__name__)

price_df = pd.read_csv('prices.csv')
dim_df = pd.read_csv('dimlimits.csv')

@app.route('/api/v1.0/getprices', methods=['GET'])
def product_prices():
    product = str(request.args.get('product'))
    height = float(request.args.get('height'))
    width = float(request.args.get('width'))

    if product is None:
        return json.dumps({'error': 'No product specified'}), 400
    elif product not in price_df['product'].values:
        return json.dumps({'error': 'Product not found'}), 404
    
    dimlimts_df = dim_df[dim_df['product'] == product]
    
    if height < dimlimts_df['minheight'].values[0] or height > dimlimts_df['maxheight'].values[0]:
        return json.dumps({'error': 'Height out of range', 
                           'minheight': dimlimts_df['minheight'].values[0], 
                           'maxheight': dimlimts_df['maxheight'].values[0]}), 400
    
    if width < dimlimts_df['minwidth'].values[0] or height > dimlimts_df['maxwidth'].values[0]:
        return json.dumps({'error': 'Height out of range', 
                           'minwidth': dimlimts_df['minwidth'].values[0], 
                           'maxwidth': dimlimts_df['maxwidth'].values[0]}), 400
    
    # calculate prices
    product_prices = price_df[price_df['product'] == product]
    product_prices["price"] = product_prices['fixedcost'] + product_prices['dimcost'] * (height/200) * (width/200)

    return product_prices[["product", "option", "price"]].to_json(orient="records")

@app.route('/api/v1.0/getdimensions', methods=['GET'])
def product_dimensions():
    product = str(request.args.get('product'))
 
    dimlimts_df = dim_df[dim_df['product'] == product]
    return dimlimts_df.to_json(orient="records")

@app.route('/api/v1.0/deliverdate', methods=['GET', 'POST'])
def delivery_dates():
    content = request.json
    if content['num_of_items'] != len(content['items']):
        return json.dumps({'error': 'Number of items does not match'}), 400
    
    # Add check for address
    
    # create dummy deliver dates and prices
    dates_df = pd.DataFrame(columns=['date', 'price'])

    start_date = date.today() + timedelta(days=1)
    end_date = date.today() + timedelta(days=100)

    dates_df['date'] = pd.date_range(start_date, end_date, freq='D')
    dates_df['day_of_week'] = dates_df['date'].dt.day_of_week
    dates_df.loc[dates_df['day_of_week'] > 4, 'price'] = 300
    dates_df.loc[dates_df['day_of_week'] <= 4, 'price'] = 250
    dates_df.loc[0:14, 'price'] = None
    dates_df.loc[14:20, 'price'] = 500

    dates_df['date'] = dates_df['date'].dt.strftime('%Y.%m.%d')

    return json.dumps({'delivery_dates': dates_df[['date', 'price']].to_json(orient="index")})
    



if __name__ == '__main__':
    app.run(host="0.0.0.0")

