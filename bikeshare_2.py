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
    print('\n\n\n\n\nHello! Let\'s explore some US bikeshare data!\n\n\n\n\n')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("Please choose a location from the following list: \nChicago \nNew York City \nWashington\n").lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print("I\'m sorry, that is not a valid city. Please select Chicago, New York City, or Washington")
            continue  
        else: 
            if city == 'chicago':
                print("\n\n\n\n\nThe Windy City... good choice\n")
            elif city == 'new york city':
                print("\n\n\n\n\nThe City that Never Sleeps... classic!\n")
            else:
                city == 'washington'
                print("\n\n\n\n\nThe Capital... nice one!\n")
        break  

      # get user input for month (all, january, february, ... , june)

    while True:
        month = input("\nWould you like to filter by month? If so, input one of the following: \nJanuary \nFebruary \nMarch \nApril \nMay \nJune \nIf you would like to view all data, input All.\n")
        if month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            print("\nI\'m sorry, that is not a valid input. Please select January, February, March, April, May, June, or All")
            continue
        else:
            break 
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nWould you like to filter by day? If so, input one of the following: \nMonday \nTuesday \nWednesday \nThursday \nFriday \nSaturday \nSunday \nIf not, please input All.\n")
        if day.lower() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            print("I\'m sorry, that is not a valid input. Please try again.")
            continue
        else:
            break
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
    #imports the correct city .csv

    df = pd.read_csv(CITY_DATA[city])

    #convert Start Time column into datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #pull out month as new column 
    df['month'] = df['Start Time'].dt.strftime("%B")

    #pull out day as new colum 
    df['day'] = df['Start Time'].dt.strftime("%A")

    #modifies the dataframe to filter by month (if applicable) 
    if month.title() != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        df = df[df['month'] == month.title()]
    else:
        df.rename(columns = {'month': 'month_unfiltered'}, inplace = True)

    #modifies the dataframe to filter by day (if applicable) 
    if day.title() != 'All':
        df = df[df['day'] == day.title()]
    else:
        df.rename(columns = {'day': 'day_unfiltered'}, inplace = True)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    if 'month_unfiltered' in df.columns or 'day_unfiltered' in df.columns:
        print('\nCalculating The Most Frequent Times of Travel...\n')
    
        start_time = time.time()

    # display the most common month
        if 'month_unfiltered' in df.columns: 
            popular_month = df['month_unfiltered'].mode()[0]
            print("Most Popular Month: {}".format(popular_month))


    # display the most common day of week
        if 'day_unfiltered' in df.columns:
            popular_day = df['day_unfiltered'].mode()[0]
            print("Most Popular Day: {}".format(popular_day))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("Most Common Start Station: {}".format(popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("Most Common End Station: {}".format(popular_end))

    # display most frequent combination of start station and end station trip
    df['Combo Trip'] = "Start: " + df['Start Station'] + " End: " + df['End Station']
    combo_busiest = df['Combo Trip'].mode()[0]
    print("Most Common Start and End Station Combo: {}".format(combo_busiest))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #I used some helper code for the time conversion: https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
    total_trip = np.sum(df['Trip Duration'])
    m,s = divmod(total_trip, 60)
    h,m = divmod(m, 60)
    print("Total Travel Time: {} hours, {} minutes, and {} seconds".format(h, m, s))

    # display mean travel time
    avg_travel_time = int(np.mean(df['Trip Duration'])) 
    mi,se = divmod(avg_travel_time, 60)
    hr,mi = divmod(mi, 60)
    print("Average Travel Time: {} hours, {} minutes, and {} seconds".format(int(hr), int(mi), int(se)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Number of Rentals By: {}".format(df['User Type'].value_counts()))

    # Display counts of gender
    if 'Gender' in df.columns:
            print("\nNumber of Rentals By: {}".format(df['Gender'].value_counts()))
    else:
        print("\nNo gender statistics are available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        early_bday = int(np.min(df['Birth Year']))
        late_bday = int(np.max(df['Birth Year']))
        common_bday = int(df['Birth Year'].mode()[0])
        print("\nNumber of Rentals by Birth Year:\nEarliest Birth Year: {}\n Latest Birth Year: {}\n Most Common Birth Year: {}".format(early_bday, late_bday, common_bday))
    else:
        print("\nBirth year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_display(df):
    """Asks users if they want to view raw data. Will display 5 rows of raw 
    data at a time until either the user chooses to stop or the end of the
    dataframe is reached."""

    # Display 5 rows of raw data at a time 
    start_time = time.time()
    emergency_exit = False 
    while True:
        if emergency_exit == True:
            break 
        answer = input("Would you like to see the 5 top lines of raw data? Y or N:\n").lower()
        if answer not in ['y', 'n']:
            print("That is not a valid response. Please select Y for yes or N for no.")
            continue
        elif answer == 'y':
            print(df.head()) 
            s = 0
            e = 5
            while True:
                if e >= df.shape[0]:
                    emergency_exit = True
                    print("You have reached the end of the file! You really need to get a hobby...")
                    break 
                second_answer = input("Would you like to see another 5 lines of raw data? Y or N:\n").lower()
                if second_answer not in ['y', 'n']:
                    print("Invalid response. Please select Y or N:\n")
                elif second_answer == 'y':
                    display = df.iloc[s:e, :]
                    print(display)
                    s= s+5
                    e= e+5
                    continue 
                else:
                    emergency_exit = True 
                    break
        else:
            print("Okay!")
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df) 
        user_stats(df) 
        raw_display(df)     
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
    


