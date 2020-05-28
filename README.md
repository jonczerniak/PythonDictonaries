# PythonDictonaries
Multiple projects utilizing python dictionaries to move and sort data

Coincident Charging:
Tries to answer the question, of the Electric Vehicle who own L2 chargers
how many of them are charging at the same time?

Creates a dictionary of dates (date of the first installed charger - 'today')
then loops through a list of charging records and assign an entry into a matching date.
Each date is then processed to see if the 'charge start time' occurs during the same hour 
as any other entry in the dictionary.
