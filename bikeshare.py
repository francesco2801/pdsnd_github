import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # input for city (chicago, new york city, washington).    
    while True:
        try:
            city = input("Would you like to see data for Chicago, New York City or Washington?\n").lower()        
            if city not in CITY_DATA:
                print('\nOops,\'{}\' is not a valid city. Please type again by entering either Chicago, New York City or Washington.'.format(city))
            else:
                city = CITY_DATA[city]
                break
        except (KeyboardInterrupt):
            print('\n"Keyboard interrupt exception caught". Try again.')
    
    
    # input for Filter month, day, both or not at all
    while True:
        try:
            choice = input('Would you like to see data for month, day, both or not at all?\n').lower()
            available_choices = ['month', 'day', 'both', 'not at all']
            if choice not in available_choices:
                print('\nOops,\'{}\' is not valid. Please type again by entering either month, day, both or not at all.'.format(choice))
            else:
                break
        except (KeyboardInterrupt):
            print('\n"Keyboard interrupt exception caught". Try again.')
    
    # input for month (all, january, february, ... , june)        
    if choice in ['month', 'both']:
        while True:
            try:
                month = input('Enter a month (all, january, february, ... , june):\n').lower()            
                if month not in months:
                    print('\nOops,\'{}\' is not a valid month. Please type again by entering a correct month (all, january, february, ... or june).'.format(month))
                else:
                    break
            except (KeyboardInterrupt):
                print('\n"Keyboard interrupt exception caught". Try again.')
    else:
        month = 'all'
        
    # input for day of week (all, monday, tuesday, ... sunday)
    if choice in ['day', 'both']:
        while True:
            try:
                day = input('Enter a day of week:\n').lower()      
                if day not in days:
                    print('\nOops,\'{}\' is not a valid day. Please type again by entering a correct day of week.'.format(day))
                else:
                    break
            except (KeyboardInterrupt):
                print('\n"Keyboard interrupt exception caught". Try again.')
    else:
        day = 'all'
 
    print('-'*40)
    return city, month, day

# =============================================================================

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load DataFrame
    df = pd.DataFrame(pd.read_csv(city))   
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    if month != 'all':
         # use the index of the months list to get the corresponding int
         df['month'] = df['Start Time'].dt.month # in df.dt.month -> January = 1, December = 12
         months = ['january', 'february', 'march', 'april', 'may', 'june'] 
         month = months.index(month) + 1
        
         df = df[df['month'] == month]
    
    if day != 'all':
         # use the index of the days list to get the corresponding int
         df['day_of_week'] = df['Start Time'].dt.dayofweek # in df.dt.dayofweek -> Monday = 0, Subday = 6
         days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
         day = days.index(day) 
    
         df = df[df['day_of_week'] == day]
         
    return df

# =============================================================================

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    if month == 'all':
        # display the most common month
        df['month'] = df['Start Time'].dt.month
        common_month = df['month'].mode()[0]
        print('the most common month is {}.'.format(months[common_month - 1].title()))
        
    if day == 'all':
        # display the most common day of week
        df['day_of_week'] = df['Start Time'].dt.dayofweek
        common_day = df['day_of_week'].mode()[0]
        print('the most common day is {}.'.format(days[common_day].title()))
        
    # display Filter for month and day    
    if month != 'all' or day != 'all':
        f = '(Filter month: ' + month + '; ' + 'day: ' + day + ').'     
    else:
        f = '(no month/day Filters).'

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]   
    c = df['hour'].value_counts().loc[common_hour]
    print('the most common start hour is {}, count {} {}'.format(common_hour, c, f))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# =============================================================================

def station_stats(df, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # display Filter for month and day 
    if month != 'all' or day != 'all':
        f = '(Filter month: ' + month + '; ' + 'day: ' + day + ').'    
    else:
        f = '(no month/day Filters).'
        
    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    c = df['Start Station'].value_counts().loc[common_start_station]
    print('the most common start station is {}, count {} {}'.format(common_start_station, c, f))
    
    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0] 
    c = df['End Station'].value_counts().loc[common_end_station]
    print('the most common end station is {}, count {} {}'.format(common_end_station, c, f))

    # display most frequent combination of start station and end station trip
    df['Combination Stations'] = df['Start Station'] + ' - ' + df['End Station']
    common_combination_stations = df['Combination Stations'].mode()[0]
    c = df['Combination Stations'].value_counts().loc[common_combination_stations]
    print('the most common combination stations is {}, count {} {}'.format(common_combination_stations, c, f))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
# =============================================================================

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # convet time: days + h:m:s
    def days_time(d):
        days = int(d)
        h = (d - days) * 24
        hours = int(h)
        m = (h -hours) * 60
        minutes = int(m)
        s = (m - minutes) * 60
        seconds = int(s)
        
        return '{} days, {:02d}h:{:02d}m:{:02d}s.'.format(days, hours, minutes, seconds)
    
    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 60 / 60 /24 # days
    print('the total travel is: ', days_time(total_travel_time))

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean() / 60 / 60 /24 # days
    print('the avg. travel time is: ', days_time(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# =============================================================================

def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
        
    # Display counts of user types
    count_users_types = df['User Type'].value_counts()
    print('Count of User Types:\n{}'.format(count_users_types))

    if city != 'washington.csv':
        
        # Display counts of gender
        count_user_gender = df['Gender'].value_counts()
        
        print('Count of User Gender:\n{}'.format(count_user_gender))
        
        # display Filter for month and day         
        if month != 'all' or day != 'all':
            f = '(Filter month: ' + month + '; ' + 'day: ' + day + ').'   
        else:
            f = '(no month/day Filters).'
            
        # Display the earliest year of birth
        earliest_year_of_birth = int(df['Birth Year'].min())
        print('The earliest year of birth is:', earliest_year_of_birth, '.')
        
        # display the most recent year of birth
        most_recent_year_of_birth = int(df['Birth Year'].max())
        print('The most recent year of birth is:', most_recent_year_of_birth, '.')
        
        # Display the most common year of birth
        most_common_year_of_birth = int(df['Birth Year'].mode()[0])    
        c = df['Birth Year'].value_counts().loc[most_common_year_of_birth]
        print('The most common year of birth is {}, count {} {}'.format(most_common_year_of_birth, c, f))
    
    else:
        print('\nBirthday and Gender informations are not available for this city: Washington.')
        print('-'*80)
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# =============================================================================

def show_rows(df):
    """Displays 5 rows at time."""
    while True:
        try:
            show_rows = input('\nWould you like to see the first 5 data travels? Enter yes or no.\n').lower()
            break
        except (KeyboardInterrupt):
                print('\n"Keyboard interrupt exception caught". Try again.')

    i = 0
    while True:
        try:                  
            if show_rows.lower() == 'yes':              
                print(df[i:i+5])                
                i += 5
                show_rows = input('\nWould you like to see the next 5 data travels? Enter yes or no.\n').lower() 
                continue
            elif show_rows.lower() == 'no':
                break                    
            else:
                print('\nOops,\'{}\' is not a valid input. Please type again by entering either yes or no.'.format(show_rows))
                show_rows = input('Enter yes or no.\n').lower()
        except (KeyboardInterrupt):
            print('\n"Keyboard interrupt exception caught". Try again.')
            while True:
                try:
                    show_rows = input('\nWould you like to see the next 5 data travels? Enter yes or no.\n').lower()
                    break
                except (KeyboardInterrupt):
                    print('\n"Keyboard interrupt exception caught". Try again.')
                
        
# =============================================================================
# =============================================================================

def main():
    
    while True:
        
        city, month, day = get_filters()
        df = load_data(city, month, day)       
        
        time_stats(df, month, day)
        station_stats(df, month, day)
        trip_duration_stats(df)        
        user_stats(df, city, month, day)    

        show_rows(df)       
        
        while True:
            try:
                restart = input('Would you like to restart? Enter yes or no.\n')    
                if restart.lower() in ['yes', 'no']:
                    break                
                else:
                    print('\nOops,\'{}\' is not a valid input. Please type again by entering either yes or no.'.format(restart))                    
            except (KeyboardInterrupt):
                print('\n"Keyboard interrupt exception caught". Try again.')
        
        if restart.lower() == 'no':
            break
            
if __name__ == "__main__":
  	 main()











