import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Choose one of the following cities; Chicago, New York City, or Washington: ').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        print('Invalid Option')
        city = input('Please choose again from one of the following cities; Chicago, New York City, or Washington: ').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('Choose data from a month January to June, or input all for all monthly data: ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        print('Invalid option')
        month = input('Please choose again from a month between January to June, or \'all\' for all monthly data: ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Choose data from a day of the week, or input all for weekly data: ').lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        print('Invalid option')
        day = input('Please choose again from a day of the week, or \'all\' for all weekly data: ').lower()

    print('-'*40)
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
    # read in correct city data
    df = pd.read_csv(CITY_DATA[city])

    # convert start_time and end_time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month from start time
    df['month'] = df['Start Time'].dt.month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # extract day from start time
    df['day'] = df['Start Time'].dt.day_name()
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('\nMost common month is: ', most_common_month)

    # display the most common day of week
    most_common_day = df['day'].mode()[0]
    print('\nMost common day is: ', most_common_day)

    # display the most common start hour
    # extract hour from start time
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('\nMost common start hour is: ', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('\nMost Commonly Used Start Station: ', most_common_start)

    # display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print('\nMost Commonly Used End Station: ', most_common_end)

    # display most frequent combination of start station and end station trip
    freq_combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\nFrequent Combination of Stations: \n', freq_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal Travel Time: ', total_travel_time, ' in seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean Travel Time: ', mean_travel_time, ' in seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('\nCounts of user types: \n', user_types_counts)

    # display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('\nCounts of gender: \n', gender_count)
    else:
        print('\nNo information on gender.')

    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = int(df['Birth Year'].min())
        print('\nEarliest Year of Birth: ', earliest_birth)

        most_recent = int(df['Birth Year'].max())
        print('\nMost Recent Year of Birth: ', most_recent)

        most_common_birth = int(df['Birth Year'].mode())
        print('\nMost Common Year of Birth: ', most_common_birth)

    else:
        print('\nNo information on users\' year of birth.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # display first 5 rows of trip data
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data not in ['no']:
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        # display next 5 rows of trip data
        view_display = input('Do you wish to continue?: ').lower()
        if view_display == 'no':
            break

def main():
    """The order in which the above functions are run in."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
