import time
import pandas as pd
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# global variables

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }
CONSOLE = Console()

def theme_op(option):
    """
    Applies a Rich theme to a print statement.

    Arg:
        (str) option - name of the key that corresponds to a theme in the result_theme dict
    Returns:
        result_theme.get(option) - dict value theme
    """
    result_theme = { 'success': 'cornflower_blue',
                     'error': 'red'}
    return result_theme.get(option)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "All" to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    """

    print(Panel('Hello! Let\'s explore some US bikeshare data!', expand = True, style = 'cyan'))
    print('\n')
    
    # lists used to validate user input and to return city, month and day values based on user choice 
    cities_op = ['Chicago', 'New York', 'Washington']
    month_op = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    days_op = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']

    # get user input for city (chicago, new york city, washington)
    while True:
        city_table = Table(title = '\nWhich city would you like to retrieve data on? Please type in the number', width = 85) 
        city_table.add_column('Chicago', justify = 'center', style = 'cyan')      # adds Chicago column to city_table
        city_table.add_column('New York', justify = 'center', style = 'cyan')     # adds New York column to city_table
        city_table.add_column('Washington', justify = 'center', style = 'cyan')   # adds Washington column to city_table
        city_table.add_row('1', '2', '3')
        CONSOLE.print(city_table)

        city = input('\n')
        nospace_city = city.replace(' ', '')                                      # removes any space in input
        if nospace_city.isdecimal() == False:                                     # check if the input includes decimal characters only
            CONSOLE.print('\n-> Sorry! input is invalid\n', style = theme_op('error'))
            continue
        if not 0 <= int(nospace_city) - 1 < len(cities_op):                       # check if the input is an index of cities_op
            CONSOLE.print('\n-> Value does not exist/wrong, try again\n', style = theme_op('error'))
            continue
        else:
            city = cities_op[int(nospace_city) - 1]                               # city takes the list value that matches user input
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month_table = Table(title = '\nWould you like to filter by month? Select \'all\' to apply no filter', width = 85) # table to display month choices
        month_table.add_column('January', justify = 'center', style = 'cyan')     # adds January column to month_table
        month_table.add_column('February', justify = 'center', style = 'cyan')    # adds February column to month_table
        month_table.add_column('March', justify = 'center', style = 'cyan')       # adds March column to month_table
        month_table.add_column('April', justify = 'center', style = 'cyan')       # adds April column to month_table
        month_table.add_column('May', justify = 'center', style = 'cyan')         # adds May column to month_table
        month_table.add_column('June', justify = 'center', style = 'cyan')        # adds June column to month_table
        month_table.add_column('All', justify = 'center', style = 'cyan')         # adds All column to month_table
        month_table.add_row('1', '2', '3', '4', '5', '6', '7')
        CONSOLE.print(month_table)

        month = input('\n')
        nospace_month = month.replace(' ', '')                                    # removes any space in input
        if nospace_month.isdecimal() == False:                                    # check if the input includes decimal characters only
            CONSOLE.print('\n-> Sorry! input is invalid\n', style = theme_op('error'))
            continue
        if not 0 <= int(nospace_month) - 1 < len(month_op):                       # check if the input is an index of month_op
            CONSOLE.print('\n-> Value does not exist/wrong, try again\n', style = theme_op('error'))
            continue
        else:
            month = month_op[int(nospace_month) - 1]                              # month takes the list value that matches user input
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_table = Table(title = '\nWould you like to filter by day? Select \'all\' to apply no filter', width = 85) # table to display day choicese
        day_table.add_column('Monday', justify = 'center', style = 'cyan')      # adds Monday column to day_table
        day_table.add_column('Tuesday', justify = 'center', style = 'cyan')     # adds Tuesday column to day_table
        day_table.add_column('Wednesday', justify = 'center', style = 'cyan')   # adds Wednesday column to day_table
        day_table.add_column('Thursday', justify = 'center', style = 'cyan')    # adds Thursday column to day_table
        day_table.add_column('Friday', justify = 'center', style = 'cyan')      # adds Friday column to day_table
        day_table.add_column('Saturday', justify = 'center', style = 'cyan')    # adds Saturday column to day_table
        day_table.add_column('Sunday', justify = 'center', style = 'cyan')      # adds Sunday column to day_table
        day_table.add_column('All', justify = 'center', style = 'cyan')         # adds All column to day_table
        day_table.add_row('1', '2', '3', '4', '5', '6', '7', '8')
        CONSOLE.print(day_table)

        day = input('\n')
        nospace_day = day.replace(' ', '')                          # removes any space in input
        if nospace_day.isdecimal() == False:                        # check if the input includes decimal characters only
            CONSOLE.print('\n-> Sorry! input is invalid\n', style = theme_op('error'))
            continue
        if not 0 <= int(nospace_day) - 1 < len(days_op):            # check if the input is an index of days_op
            CONSOLE.print('\n-> Value does not exist/wrong, try again\n', style = theme_op('error'))
            continue
        else:
            day = days_op[int(nospace_day) - 1]                     # day takes the list value that matches user input   
            break

    CONSOLE.print('-'*40, style = 'light_pink3')
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
    try:
        df = pd.read_csv(CITY_DATA[city])
    except FileNotFoundError:
        print('File or file path not found')

    df['Start Time'] = pd.to_datetime(df['Start Time'])    # convert Start Time to a datatime to extract desired dates
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    if month != 'All':                                     # filter by month if user specified one in input
        df = df[df['Month'] == month]
    if day != 'All' :
        df = df[df['Day'] == day]                          # filter by day if user specified one in input
    return df


def time_stats(month, day, df):
    """
    Displays statistics on the most frequent times of travel.
    Args:
        (str) month - value of the month filter to find relevant data based on it
        (str) day - value of the day filter to find relevant data based on it
    """
    print(Panel('Time Statistics', subtitle = 'calculating..', expand = True, style = 'cyan'))
    print('\n')
    time_table = Table(title = 'Most Common Times of Travel', width = 85)     # table to display the result
    start_time = time.time()

    # find the most common month if the data is not filtered by month
    if month == 'All':
        common_month = df['Month'].mode()[0]                                  # find the most common month
        month_count = df['Month'].value_counts()[common_month]                # counts the number of occurrences
        time_table.add_column('Month', justify = 'center', style = 'cyan')    # adds Month column to time_table

    # find the most common day of week if the data is not filtered by day
    if day == 'All':           
        common_day = df['Day'].mode()[0]                                      # find the most common day
        day_count = df['Day'].value_counts()[common_day]                      # counts the number of occurrences
        time_table.add_column('Day', justify = 'center', style = 'cyan')      # adds Day column to time_table

    # find the most common start hour
    df['Hour'] = df['Start Time'].dt.hour                                     # extract an hour column from Start Time            
    common_hour = df['Hour'].mode()[0]                                        # find the most common hour
    hour_count = df['Hour'].value_counts()[common_hour]                       # counts the number of occurrences
    time_table.add_column('Hour', justify = 'center', style = 'cyan')         # adds Hour column to time_table

    # display the results based on the filters
    if month == 'All' and day == 'All':
        time_table.add_row(str(common_month),
                           str(common_day),
                           str(common_hour))
        time_table.add_section()
        time_table.add_row('Count:\n{}'.format(str(month_count)),
                           'Count:\n{}'.format(str(day_count)),
                           'Count:\n{}'.format(str(hour_count)))
    elif month == 'All':
        time_table.add_row(str(common_month),
                           str(common_hour))
        time_table.add_section()
        time_table.add_row('Count:\n{}'.format(str(month_count)),
                           'Count:\n{}'.format(str(hour_count)))
    elif day == 'All':
        time_table.add_row(str(common_day),
                           str(common_hour))
        time_table.add_section()
        time_table.add_row('Count:\n{}'.format(str(day_count)),
                           'Count:\n{}'.format(str(hour_count)))
    else:
        time_table.add_row(str(common_hour))
        time_table.add_section()
        time_table.add_row('Count:\n{}'.format(str(hour_count)))
    CONSOLE.print(time_table)
    CONSOLE.print("\nThis took %s seconds." % (time.time() - start_time), style = theme_op('success'))
    CONSOLE.print('-'*40, style = 'light_pink3')


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    Arg:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print(Panel('Station Statistics', subtitle = 'calculating..', expand = True, style = 'cyan'))
    print('\n')
    station_table = Table(title = 'Most Common Stations and Routes', width = 85)    # table to display result
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    start_station_count = df['Start Station'].value_counts()[common_start_station]      # counts the number of occurrences
    station_table.add_column('Start Station', justify = 'center', style = 'cyan')       # adds Start Station column to station_table

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    end_station_count = df['End Station'].value_counts()[common_end_station]            # counts the number of occurrences
    station_table.add_column('End Station', justify = 'center', style = 'cyan')         # adds End Station column to station_table


    # display most frequent combination of start station and end station trip
    df['Rout'] = df['Start Station'] + ' - ' + df['End Station']
    common_route = df['Rout'].mode()[0]
    route_count = df['Rout'].value_counts()[common_route]                               # counts the number of occurrences
    station_table.add_column('Frequient Route', justify = 'center', style = 'cyan')     # adds Frequient Route column to station_table

    # add rows to station_table
    station_table.add_row(str(common_start_station),
                          str(common_end_station),
                          str(common_route))
    station_table.add_section()
    station_table.add_row('Count:\n{}'.format(str(start_station_count)),
                          'Count:\n{}'.format(str(end_station_count)),
                          'Count:\n{}'.format(str(route_count)))

    CONSOLE.print(station_table)
    CONSOLE.print("\nThis took %s seconds." % (time.time() - start_time), style = theme_op('success'))
    CONSOLE.print('-'*40, style = 'light_pink3')


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    Arg:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print(Panel('Trip Duration Statistics', subtitle = 'calculating..', expand = True, style = 'cyan'))
    print('\n')
    trip_table = Table(title = 'Travel Time Calculations', width = 85)               # table to display result
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 3600                             # sum over Trip Duration column and convert to hours
    trip_table.add_column('Total Travel Time', justify = 'center', style = 'cyan')   # adds Total Travel Time column to trip_table
    travel_count = df['Trip Duration'].count()

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 60                               # calculate mean of Trip Duration column and convert to min
    trip_table.add_column('Mean Travel Time', justify = 'center', style = 'cyan')    # adds Mean Travel Time column to trip_table
    
    # adds rows to trip_table
    trip_table.add_row('{}\nhour'.format(total_travel_time),
                       '{}\nmin'.format(mean_travel_time))                           
    trip_table.add_section()
    trip_table.add_row('Count:\n{}'.format(travel_count))

    CONSOLE.print(trip_table)
    CONSOLE.print("\nThis took %s seconds." % (time.time() - start_time), style = theme_op('success'))
    CONSOLE.print('-'*40, style = 'light_pink3')


def user_stats(city, df):
    """
    Displays statistics on bikeshare users.
    Arg:
        (str) day - value of the day filter to find relevant data based on it
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print(Panel('User Statistics', subtitle = 'calculating..', expand = True, style = 'cyan'))
    print('\n')
    user_table = Table(title = 'User Information', width = 95)                  # table to display result
    start_time = time.time()

    # display counts of user types
    # user_types = df.groupby(['User Type', 'Gender']).size()
    user_types = df['User Type'].value_counts()                                 # finds the types of users and counts the occurrences of each
    user_table.add_column('User Types', justify = 'center', style = 'cyan')     # adds User Type column to user_table

    # display counts of gender and earliest, most recent, and most common year of birth if available
    if city == 'Washington':
        CONSOLE.print('Sorry! no data available on gender or birth year\n', style = theme_op('error'))
    else:
        gender = df['Gender'].value_counts(dropna = True)                       # finds the gender of users and counts the occurrences of each
        user_table.add_column('Gender', justify = 'center', style = 'cyan')     # adds Gender column to user_table
        early_birth_year = df['Birth Year'].min(skipna = True)                  # finds earliest year of birth
        user_table.add_column('Earliest Birth Year', justify = 'center', style = 'cyan')      # adds Earliest Birth Year column to user_table
        recent_birth_year = df['Birth Year'].max(skipna = True)                               # finds most recent year of birth
        user_table.add_column('Most Recent Birth Year', justify = 'center', style = 'cyan')   # adds Most Recent Birth Year column to user_table
        common_birth_year = df['Birth Year'].mode(dropna = True)[0]                           # finds most common year of birth
        user_table.add_column('Most Common Birth Year', justify = 'center', style = 'cyan')   # adds Most Common Birth Year column to user_table
    
    # display the results based on the filter
    if city == 'Washington':
        user_table.add_row(str(user_types)) 
    else:
        user_table.add_row(str(user_types),
                           str(gender),
                           str(early_birth_year),
                           str(recent_birth_year),
                           str(common_birth_year))                                            


    CONSOLE.print(user_table)
    CONSOLE.print("\nThis took %s seconds." % (time.time() - start_time), style = theme_op('success'))
    CONSOLE.print('-'*40, style = 'light_pink3')


def display_data(df, n):
    """
    Display raw data upon the user's request.
    Arg:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    index = 0                                                                # index to be used for slicing
    while True:
        print(df.iloc[index:index + 5])                                      # prints 5 rows at a time
        display = input('\nWould you like to see more raw data? Type y: yes or n: no\n')
        if display.lower() == 'n':
            break
        else:
            index += 5                                                       # increments index to print the next 5 rows
            continue

        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(month, day, df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)

        print('\nWould you like to view the raw data? Type y: yes or n: no')
        display = input('\n')
        if display.lower() == 'y':
            display_data(df, 5)

        CONSOLE.print('\nWould you like to restart? Type y: yes or n: no', style = theme_op('success'))
        restart = input('\n')
        if restart.lower() != 'y':
            print(Panel('Goodbye!', expand = True, style = 'cyan'))
            break


if __name__ == "__main__":
	main()
