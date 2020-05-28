import csv
from datetime import datetime, timedelta

user_dictionary = {}
work_charge_dictionary = {}
date_dictionary = {}

# import session data
with open('DriverDictionary.csv', 'r') as csvfile:
    user_reader = csv.reader(csvfile)
    index = 1
    for row in user_reader:
        user_dictionary[index] = row
        index += 1

csvfile.close()

# read in the full res driver file
with open('FilteredSessions_CSV.csv', 'r') as csvfile:
    file_reader = csv.reader(csvfile)
    index = 1
    for row in file_reader:
        work_charge_dictionary[index] = row
        index += 1

csvfile.close()

# parse data in charge_record_dictionary
for row in work_charge_dictionary:
    charge_record = work_charge_dictionary[row]
    # parse data for date and hour to datetime and integer respectively
    charge_record[4] = datetime.strptime(charge_record[4], '%m/%d/%Y').date()
    charge_record[5] = int(charge_record[5])
    charge_record[6] = int(charge_record[6])


# Get earliest date in the charge record
start_date = (work_charge_dictionary[1][4])

end_date = (work_charge_dictionary[len(work_charge_dictionary)][4])

# default charge rate set to 6.6
charge_rate = 6.6

# calculate the number of days between the start and the end dates
number_of_days = (end_date - start_date).days

print(number_of_days)

charge_sessions = []


for j in work_charge_dictionary:
    check_session = work_charge_dictionary[j]
    # go through the user dictionary to get the charge rate

    for user in user_dictionary:
        user_profile = user_dictionary[user]
        if check_session[8] == user_profile[1]:
            charge_rate = float(user_profile[2])
            charging_duration_seconds = (float(check_session[7]) / charge_rate)*3600

            test_list = [check_session[0], check_session[5], float(check_session[7]), check_session[9], charge_rate,
                         check_session[6], check_session[8], charging_duration_seconds, user_profile[3]]
            charge_sessions.append(test_list)


for i in charge_sessions:
    print('{0}'.format(i))



# write results to file
with open('OutputData/Charge_Duration0617.csv', 'w') as csvfile:
    header = 'sessionID, start_hour, kwhConsumed, homeOrWorkSite, charge_rate, plugged_in_duration, userId, ' \
             'charge_duration_seconds, commuter_type\n'
    csvfile.write(header)
    for row in charge_sessions:
        row_string = str(row).replace("[", "").replace("]", "").replace("", "")
        csvfile.write(row_string + '\n')

csvfile.close()

