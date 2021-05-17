from datetime import datetime as dt
import pandas as pd
import math

def load_data():
    # First of all, it will be filtered by city
    selected_csv = ""
    selected_city = ""
    is_chicago_or_nyc = False

    while selected_city not in ['1', '2', '3']:
        selected_city = input("\nPlease select a city by entering its corresponding number:\n\
            1 - Chicago\n\
            2 - New York City\n\
            3 - Washington\n")

        if selected_city == '1':
            selected_csv = "chicago.csv"
            is_chicago_or_nyc = True

        elif selected_city == '2':
            selected_csv = "new_york_city.csv"
            is_chicago_or_nyc = True

        elif selected_city == '3':
            selected_csv = "washington.csv"
            is_chicago_or_nyc = False

        else:
            print("\n\nInput not valid. Please enter 1, 2, or 3.")

    df = pd.read_csv(selected_csv)

    # After the city, we will ask to filter by time period

    selected_period = ''

    while selected_period not in ['1', '2', '3']:
        selected_period = input("\nPlease select a period filter by entering its corresponding number:\n\
            1 - Filter by month\n\
            2 - Filter by weekday\n\
            3 - No filter - evaluate ALL data\n")

        if selected_period == '1':
            # Filter by month
            selected_month = ''
            while selected_month not in ['1', '2', '3', '4', '5', '6']:
                selected_month = input("\nPlease select a month by entering its corresponding number:\n\
                    1 - January\n\
                    2 - February\n\
                    3 - March\n\
                    4 - April\n\
                    5 - May\n\
                    6 - June\n")

                if selected_month not in ['1', '2', '3', '4', '5', '6']:
                    print("\n\nInput not valid. Please enter 1, 2, 3, 4, 5, or 6.")

            print("Loading...\n\n")

            start_times = df['Start Time']
            to_drop = []

            for i in range(0, len(start_times)):
                # Formatting date to remove the time and keep just the date parameters
                date_wo_time = start_times[i].split(" ")[0]
                my_date = dt.strptime(date_wo_time, "%Y-%m-%d")

                if my_date.month != int(selected_month):
                    to_drop.append(i)

            df = df.drop(to_drop)
            df = df.reset_index(drop=True)



        elif selected_period == '2':
            # Weekday filter
            selected_weekday = ''
            while selected_weekday not in ['1', '2', '3', '4', '5', '6', '7']:
                selected_weekday = input("\nPlease select a weekday by entering its corresponding number:\n\
                1 - Monday\n\
                2 - Tuesday\n\
                3 - Wednesday\n\
                4 - Thursday\n\
                5 - Friday\n\
                6 - Saturday\n\
                7 - Sunday\n")

                if selected_weekday not in ['1', '2', '3', '4', '5', '6', '7']:
                    print("\n\nInput not valid. Please enter 1, 2, 3, 4, 5, 6, or 7.")

            print("Loading...\n\n")

            start_times = df['Start Time']
            to_drop = []

            for i in range(0, len(start_times)):
                # Formatting date to remove the time and keep just the date parameters
                date_wo_time = start_times[i].split(" ")[0]
                my_date = dt.strptime(date_wo_time, "%Y-%m-%d")

                if my_date.weekday() != int(selected_weekday) - 1:
                    to_drop.append(i)

            df = df.drop(to_drop)
            df = df.reset_index(drop=True)

        elif selected_period == '3':
            # With no period filter
            pass

        else:
            print("\nInput not valid. Please enter 1, 2, or 3.")

    return df, is_chicago_or_nyc


def most_common_station(df, start_station=False):
    #Now we are going to find the most common station
    if start_station:
        stations = df['Start Station']
    else:
        stations = df['End Station']

    stations_dict = dict()

    for station in stations:
        if station not in stations_dict.keys():
            stations_dict[station] = 1
        else:
            stations_dict[station] += 1

    return max(stations_dict, key=stations_dict.get)


def most_common_trip(df):
    #We are going to indentify the most common trip
    start_stations = df['Start Station']
    end_stations = df['End Station']
    trips_dict = dict()

    for i in range(0, len(start_stations)):
        trip = start_stations[i] + ' TO ' + end_stations[i]
        if trip not in trips_dict.keys():
            trips_dict[trip] = 1
        else:
            trips_dict[trip] += 1

    return max(trips_dict, key=trips_dict.get)


def get_total_travel_time(df):
    #Travel duration in minutes
    durations = df['Trip Duration']
    return round(sum(durations)/60, 2)


def get_avg_travel_time(df):
    #Travel average time in minutes
    durations = df['Trip Duration']
    return round(sum(durations)/60/len(durations), 2)


def get_count(df, column, is_chicago_or_nyc):
    #Count the amount of males and females who use the bikeshare service
    if column == 'Gender':
        if is_chicago_or_nyc == False:
            return "COLUMN NOT AVAILABLE"

    types = df[column]
    types_dict = dict()

    for my_type in types:
        if my_type not in types_dict.keys():
            types_dict[my_type] = 1
        else:
            types_dict[my_type] += 1

    return str(types_dict)


def get_birth_year(df, spec, is_chicago_or_nyc):
    #Birth year statistics
    if is_chicago_or_nyc == False:
        return "COLUMN NOT AVAILABLE"

    birth_years = df['Birth Year']
    return_year = 0
    if spec == 'earliest':
        return_year = min(birth_years)

    elif spec == 'latest':
        return_year = max(birth_years)

    elif spec == 'common':
        years_dict = dict()


        for birth_year in birth_years:

            if birth_year not in years_dict.keys():
                years_dict[birth_year] = 1
            else:
                years_dict[birth_year] += 1

        return_year = max(years_dict, key=years_dict.get)

    return math.trunc(return_year)


def most_common_month(df):
    # Most common month identification
    start_times = df['Start Time']
    month_dict = dict()
    cmonth=''
    most_common_m=''
    MONTHS=['Janury','February','March','April','May','June']
    for start_time in start_times:
        # Formatting date to remove the time
        date_wo_time = start_time.split(" ")[0]
        my_date = dt.strptime(date_wo_time, "%Y-%m-%d")

        if my_date.month in month_dict.keys():
            month_dict[my_date.month] += 1

        else:
            month_dict[my_date.month] = 1

        cmonth=max(month_dict, key=month_dict.get)
        most_common_m=MONTHS[cmonth-1]
        return most_common_m

def most_common_weekday(df):
    #Identify the most common weekday
    start_times = df['Start Time']
    weekday_dict = dict()

    for start_time in start_times:
        date_wo_time = start_time.split(" ")[0]
        my_date = dt.strptime(date_wo_time, "%Y-%m-%d").strftime('%A')

        if my_date in weekday_dict.keys():
            weekday_dict[my_date] += 1

        else:
            weekday_dict[my_date] = 1

        return max(weekday_dict, key=weekday_dict.get)

def most_common_hour(df):
    # Most common hour identification
    start_times = df['Start Time']
    hour_dict = dict()

    for start_time in start_times:

        date_wo_time = start_time.split(" ")[1]
        my_date = dt.strptime(date_wo_time, "%H:%M:%S")

        if my_date.hour in hour_dict.keys():
            hour_dict[my_date.hour] += 1

        else:
            hour_dict[my_date.hour] = 1

        return max(hour_dict, key=hour_dict.get)

def five_row_raws(df,is_chicago_or_nyc):
    # The opportunity to see row data in blocks, increasing by 5 rows at a time
    beggin = 0
    end = 5

    show_data = input("Would you like to see the row data? Type 'Yes' or 'No': ")

    if show_data.title() == 'Yes':

        while end <= df.shape[0]:

            if is_chicago_or_nyc == True:

                print(df.iloc[beggin:end,0:11])

            elif is_chicago_or_nyc == False:

                print(df.iloc[beggin:end,0:9])

            beggin += 5
            end += 5

            five_more = input("\nIf you want to continue and see 5 more rows, enter 'Yes', otherwise press any key.\n")
            if five_more.title() != 'Yes':
                break



def main():
    while True:

        df, is_chicago_or_nyc = load_data()
        five_row_raws(df,is_chicago_or_nyc)

        print('OUTPUT:')

        print('\n#1 Popular times of travel:')
        print('The most common month is {}.'.format(most_common_month(df)))
        print('The most common weekday is {}.'.format(most_common_weekday(df)))
        print('The most common hour of the day is {}.'.format(most_common_hour(df)))

        print('\n#2 Popular stations and trips:')
        print('\nThe most common start station is: {}.'.format(most_common_station(df, start_station=True)))
        print('The most common end station is: {}.'.format(most_common_station(df, start_station=False)))
        print('The most common trip from start to end is: {}.'.format(most_common_trip(df)))

        print('\n#3 Trip duration:')
        print('The total travel time is: {} minutes.'.format(get_total_travel_time(df)))
        print('The average travel time is: {} minutes.'.format(get_avg_travel_time(df)))

        print('\n#4 User info:')
        print('The counts of each user type is: {}.'.format(get_count(df, 'User Type', is_chicago_or_nyc)))
        print('The counts of each gender is: {}.\n'.format(get_count(df, 'Gender', is_chicago_or_nyc)))
        print('The earliest year of birth is: {}.'.format(get_birth_year(df, 'earliest', is_chicago_or_nyc)))
        print('The most recent year of birth is: {}.'.format(get_birth_year(df, 'latest', is_chicago_or_nyc)))
        print('The most common year of birth is: {}.'.format(get_birth_year(df, 'common', is_chicago_or_nyc)))

        start_again = input("\nIf you want to start again and continue with your research, enter 'Yes', otherwise press any key.\n")
        if start_again.title() != 'Yes':
            break



if __name__ == "__main__":
	main()
