import pandas as pd
import numpy as np
import time

print("hello! let's explore the data of US BikeShare")
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def check(input_str,type):
#check the validity of user input.
    #input_str is the input of the user
    #type is the type of input
    while True:
        input_user=input(input_str).lower()
        try:
            if input_user in ['chicago','new york city','washington'] and type == 1:
                return input_user
                break
            elif input_user in ['january', 'february', 'march', 'april', 'may', 'june','all'] and type == 2:
                return input_user
                break
            elif input_user in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and type == 3:
                return input_user
                break
            else:
                if type == 1:
                    print("Sorry, your choice should be: chicago or new york city or washington")
                if type == 2:
                    print("Sorry, your choice should be: january,...., may, june or all")
                if type == 3:
                    print("Sorry, your choice should be: sunday, ..., saturday or all")
        except ValueError:
            print("Sorry, Wrong Input")



def get_filters():
    #this use to specify a city , day , month to analysis
    # that return the name of city
    # month to filter by  or "all" to apply no month filter
    # name of day to filter by  or "all" to apply no day filter
    city = check("would you like to see data for chicago , new york city or washington?", 1)
    month = check('Which Month ?(all, january, ... june)??', 2)
    day = check("Which day? (all, monday, tuesday, ... sunday)", 3)
    print('-' * 80)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df
def time_statistics(df):
    time_of_begining = time.time()
    popular_month = df['month'].mode()[0]

    print('Most Frequent Start Month:', popular_month)
    popular_day = df['day_of_week'].mode()[0]

    print('Most Frequent Start Day:', popular_day)
    popular_hour = df['hour'].mode()[0]

    print('Most Frequent Start Hour:', popular_hour)

    print('time of operation with seconds',(time.time()-time_of_begining))
    print('#' * 100)
def Station_statistics(df):
        time_of_start = time.time()
        popular_Start_station = df['Start Station'].mode()[0]

        print('Most Frequent Start Station:', popular_Start_station)
        popular_end_station = df['End Station'].mode()[0]

        print('Most Frequent End station:', popular_end_station)

        group_field = df.groupby(['Start Station', 'End Station'])
        common_combination_station = group_field.size().sort_values(ascending=False).head(1)
        print('The most frequent combination of Start Station and End Station trip:\n', common_combination_station)
        print("\nTime of operation with seconds." , (time.time() - time_of_start))
        print('*' * 100)
def trip_duration(df):
    print('\nCalculating...')
    start_trip_duration = time.time()
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)
    average_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time:', average_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_trip_duration))
    print('*'*100)

def User_info(df, city):
    print('\nCalculating User info...')
    start_User = time.time()
    User_Type_Stats= df['User Type'].value_counts()
    print('User_Type_Stats:', User_Type_Stats)
    if city != 'washington':
        print('Gender Stats:')
        print(df['Gender'].value_counts())
        print('Year:')
        most_popular_year = df['Birth Year'].mode()[0]
        print('Most popular Year:', most_popular_year)
        most_year = df['Birth Year'].max()
        print('Most Recent Year:', most_year)
        the_earliest_year = df['Birth Year'].min()
        print('Earliest Year:', the_earliest_year)
    print("\nThis took %s seconds." , (time.time() - start_User))
    print('#' * 100)
def more_rows(df):
    start = 5
    more_5_rows = input('\nWould you like to see another 5 rows? Enter yes or no.\n')
    while more_5_rows.lower() == 'yes':
        df_slice = df.iloc[start: start+5]
        print(df_slice)
        start += 5
        more_5_rows = input('\nWould you like to see 5 rows? Enter yes or   no.\n')
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df.head())
        time_statistics(df)
        Station_statistics(df)
        trip_duration(df)
        User_info(df, city)
        more_rows(df)
        restart = input('Do you want to chose another country?(yes or no)')
        if restart != "yes":
            break


if __name__ == "__main__":
    main()