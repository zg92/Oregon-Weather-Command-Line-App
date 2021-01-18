import gather_weather_data
import create_table
import result_slicing
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter the weather type followed by the date or number of days out you are interested in')
    parser.add_argument('-g', '--gather', action='store_true', help='This will gather the data to populate weather database. This must be run before you use -w and -d')
    parser.add_argument('-w', '--weather', type=str, help="This argument can be clouds, clear, thunderstorm, drizzle, rain, or snow")
    parser.add_argument('-d', '--date', help='Enter days out or a specific date you want to see. "1" means current weather')
    args = parser.parse_args()

    if args.gather:
        create_table.drop_table()
        create_table.create_table()
        print('Hold on--- Loading data...')
        gather_weather_data.load_data()
        result_slicing.find_weather(args.weather, args.date)
    else:
        result_slicing.find_weather(args.weather, args.date)