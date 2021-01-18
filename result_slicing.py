import pandas as pd
import sqlalchemy
import re
import datetime

#pulls data from sql into dataframe to be viewed in the terminal. Also converts sunrise and sunset data into local time via pandas methods.
def create_df():
    engine = sqlalchemy.create_engine('sqlite:///weather.db')
    df = pd.read_sql_table('weather_prediction', con=engine)
    df['sunrise'] = df['sunrise'].apply(lambda x: x.tz_localize('UTC').astimezone('US/Pacific').strftime("%H:%M:%S"))
    df['sunset'] = df['sunset'].apply(lambda x: x.tz_localize('UTC').astimezone('US/Pacific').strftime("%H:%M:%S"))
    return df 

#logic for taking terminal inputs and filtering data to show relevant results. 
def find_weather(weather, submitted_date):
    df = create_df()
    if re.match(r'^\d{4}-\d{2}-\d{2}$',submitted_date):
        w_filtered_df = df[['location', 'weather','weather_desc','w_day','sunrise', 'sunset']].loc[(df['weather'] == f'{weather}') & (df['w_day'] == f'{submitted_date}')].to_string(index=False)
        print(w_filtered_df)
    elif re.match(r'^[1-7]$', submitted_date): 
        days_out = datetime.date.today()+ datetime.timedelta(days=+int(submitted_date))
        w_filtered_df = df[['location', 'weather','weather_desc','w_day','sunrise', 'sunset']].loc[(df['weather'] == f'{weather}') & (df['w_day'] < f'{days_out}')].sort_values(by='w_day').to_string(index=False)
        print(w_filtered_df)
    else: 
        print("It doesn't look like your inputs were correct. Check your weather and date/days out entries")
