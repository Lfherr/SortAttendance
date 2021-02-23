import os
import pandas as pd
import glob
import datetime as dt


directory = 'C:\\Users\\Herrera\\Downloads'
desired_files = '*.csv'
path = os.path.join(directory, desired_files)
altered_file_name = "Sorted"
substring = "meeting"
today = dt.datetime.now().date()
df_sr = pd.read_csv('C:\\Luis\\Teaching folder\\Attendance 2020_2021\\student_roster.csv', sep=',', header=None, engine='python', )
ab_list = {}

def get_datetime(files):
    filetime = dt.datetime.fromtimestamp(os.path.getctime(files))
    return filetime

def sorted_name(unsorted_file):
    first_part_of_name = ""
    filetime = get_datetime(unsorted_file)
    file_name, file_ext = os.path.splitext(unsorted_file)  # Separates File name from extension
    if filetime.hour == 8:
        first_part_of_name = "Herrera 1st"
    elif filetime.hour == 9:
        first_part_of_name = "Herrera 2nd"
    elif filetime.hour == 10:
        first_part_of_name = "Herrera 3rd"
    elif filetime.hour == 11:
        first_part_of_name = "Herrera 4th"
    elif filetime.hour == 13:
        first_part_of_name = "Herrera 6th"
    elif filetime.hour == 14:
        first_part_of_name = "Herrera 7th"

    file_name = first_part_of_name + " " + filetime.strftime('%m') + "_" + filetime.strftime(
        '%d') + " " + altered_file_name
    base_name = os.path.basename(file_name)
    return base_name + file_ext  # New File name to store under



for files in glob.glob(path):
    file_date = get_datetime(files)
    if file_date.date() == today and substring in files:
        df_sr2 = df_sr
        sort_name = sorted_name(files)
        df = pd.read_csv(files, sep='delimiter', header=None, engine='python')
        df.columns = ['Names']
        df = df.Names.str.split(" ", expand=True)
        df.loc[df[2].str.contains('\(', na=False), 2] = df[1]  #replaces id with last names
        df[2] = df.loc[~df[2].str.contains('\t', na=False), 2]
        df = df.sort_values(2)
        new_sorted_file = "C:/Luis/Teaching folder/Attendance 2020_2021/" + sort_name
        df.to_csv(new_sorted_file)
        if df_sr.index.max() > df.index.max():  #prepares to compare missing students
            df = df.reindex(index=df_sr2.index)
        else:
            df_sr2 = df_sr2.reindex(index=df.index) #makes copy so final column isn't deleted

        df = df.replace({'\\0': ''}, regex=True) #values shows up as starting with \0. necessary to compare
        temp_ab_list = df_sr2[file_date.hour - 7][~df_sr2[file_date.hour - 7].isin(df[2])] #adjust time to class period, list of absent students
        ab_list[file_date.hour - 8] = temp_ab_list


df_absences = pd.DataFrame(ab_list, columns=ab_list.keys())
df_absences.to_csv('C:\\Luis\\Teaching folder\\Absences 2020_2021\\Absences' + dt.datetime.now().strftime('%m') + '_' + dt.datetime.now().strftime('%d') + '.csv')
