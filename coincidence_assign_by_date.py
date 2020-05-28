from datetime import datetime, timedelta
import csv
from random import randint


# functions---------------------------------------------
def select_random_users(home_dictionary, num_of_homes):
    # create an array and generate random numbers
    rand_array = []
    array_index = 0
    driver_array = []
    for x in range(num_of_homes):
        x = randint(1, len(home_dictionary))
        while x in rand_array:
            x = randint(1, len(home_dictionary))
        rand_array.append(x)
        print(rand_array)

    # loop through the home dictionary to assign a driver number to each
    # randomly generated number
    for y in home_dictionary:
        # check to see if the index matches a key in the home dictionary
        if y in rand_array:
            driver_array.append(home_dictionary[y][1])
    return driver_array


def query_stats(stats_dictionary, num_users, report_arr):
    stats_arr = []
    formatted_report = ''

    # set oldest date to today to get correct date through calculation
    earliest_date = today
    # calculate the latest dat in the dictionary
    for i in stats_dictionary:
        if i <= earliest_date:
            earliest_date = i

    stats_arr.append(today)
    stats_arr.append(earliest_date)
    stats_arr.append(len(stats_dictionary))
    stats_arr.append(int((stats_arr[0] - earliest_date).days))
    print(stats_arr)

    # place into a try catch to prevent zero division error
    try:
        stats_arr.append((stats_arr[2] / stats_arr[3]) * 100)
    except ZeroDivisionError:
        print('It looks like the query did not produce any results')
    else:
        formatted_report = ('\nNumber of Users: {0}'
                            '\nEarliest date: {1}\nTotal Number of Days: {2}\nNumber of days with concurrent charge sessions: {3}'
                            '\nPercentage of days with concurrent charge sessions: {4}%'.format(num_users, stats_arr[1],
                                                                                                stats_arr[3],
                                                                                                stats_arr[2],
                                                                                                round(stats_arr[4])))
    stats_arr.append(num_users)
    report_arr.append(stats_arr)
    print(formatted_report)
    return report_arr


def loop_through_users(user_array):
    if len(user_array) > 1:
        user_arr_index = 0
        found_dictionary = {}
        found_dictionary2 = {}
        for i in date_dictionary:
            test_value = date_dictionary[i]

            for index, item in enumerate(test_value):
                if item == user_array[user_arr_index]:
                    found_dictionary2[i] = test_value

        # This is where the process will occur mainly
        while user_arr_index < len(user_array) - 1:

            user_arr_index += 1
            found_dictionary = found_dictionary2
            found_dictionary2 = {}

            for j in found_dictionary:
                test_value = found_dictionary[j]
                for index, item in enumerate(test_value):
                    if item == user_array[user_arr_index]:
                        found_dictionary2[j] = test_value

    return found_dictionary


def search_by_length(date_dictionary, total_users):
    stats_report_arr = []
    num_users = 1
    while num_users < total_users:
        return_dictionary = {}
        for i in date_dictionary:

            if len(date_dictionary[i]) >= num_users:
                return_dictionary[i] = date_dictionary[i]

        print(query_stats(return_dictionary, num_users, stats_report_arr))
        num_users += 1

    return stats_report_arr


# END functions ----------------------------------------
stats_report_arr = []
return_dictionary = {}
charge_record_dictionary = {}
user_dictionary = {}
comparison_table1 = {}

# import session data
with open('Res_driver_dictionary.csv', 'r') as csvfile:
    user_reader = csv.reader(csvfile)
    index = 1
    for row in user_reader:
        user_dictionary[index] = row
        index += 1

csvfile.close()

# read in the full res driver file
with open('home_charging_CSV.csv') as csvfile:
    file_reader = csv.reader(csvfile)
    index = 1
    for row in file_reader:
        charge_record_dictionary[index] = row
        index += 1

csvfile.close()

# parse data in charge_record_dictionary
for row in charge_record_dictionary:
    charge_record = charge_record_dictionary[row]
    # parse data for date and hour to datetime and integer respectively
    charge_record[9] = int(charge_record[9])
    charge_record[2] = datetime.strptime(charge_record[2], '%m/%d/%Y').date()

# define the date range variables
today = datetime.now().date()
start_date = datetime(2018, 1, 1).date()
date_diff = today - start_date

date_dictionary = {}
# create the dictionary of dates to store session data
new_date = today
for i in (range(date_diff.days)):
    new_date -= timedelta(1)
    date_dictionary[new_date] = []

for user in user_dictionary:

    # test query variable will grab each user from the user dictionary
    test_query = (user_dictionary[user])
    print('number: {0} user: {1}'.format(user, test_query[1]))

    for row in charge_record_dictionary:
        ret_val = charge_record_dictionary[row]
        if (ret_val[8] == test_query[1]) and (ret_val[9] >= 16 and ret_val[9] <= 20):
            comparison_table1[row] = ret_val

# loop through that data and assign charge sessions to corresponding date
for i in date_dictionary:
    check_date = date_dictionary[i]
    # print('date being checked: {0}'.format(i))

    for j in comparison_table1:
        check_session = comparison_table1[j]
        # print('against date: {0}'.format(check_session[2]))
        if check_session[2] == i:
            # print('match found!')
            check_date.append(check_session[8])

print(date_dictionary)

# for i in date_dictionary:
#     print('date {0} Users: {1}'.format(i, date_dictionary[i]))




#run the search
stats_report = search_by_length(date_dictionary, 19)

print(stats_report)

# print(stats_report_arr)

# write the data in stats_report_arr to a txt file
with open('concurrent_stats.txt', 'w') as csvfile:
    header = 'End_Year, End_Month, End_Day, Start_Year, Start_Month, Start_Day, Concurrent_Charge_Days, Total_Days, Percent_Concurrent, Num_Users\n'
    csvfile.write(header)
    for row in stats_report:
        row_string = str(row).replace("[","").replace("]","").replace("datetime.date(","").replace(")","")
        csvfile.write(row_string + '\n')

csvfile.close()


