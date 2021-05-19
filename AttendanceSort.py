import os
import pandas as pd
import glob
import datetime as dt


directory = 'C:\\Users\\ASUS\\Downloads'
desired_files = '*.csv'
path = os.path.join(directory, desired_files)
altered_file_name = "Sorted"
substring = "meeting"
today = dt.datetime.now().date()
df_sr = pd.read_csv('D:\\Luis Herrera\\Teacher Stuff\\Classes\\student_roster.csv', sep=',', header=None, engine='python')
ab_list = {}


def get_datetime(files):
    filetime = dt.datetime.fromtimestamp(os.path.getctime(files))
    return filetime


def sorted_name(unsorted_file):
    first_part_of_name = ""
    filetime = get_datetime(unsorted_file)
    file_name, file_ext = os.path.splitext(unsorted_file)  # Separates File name from extension
    if (filetime.hour == 7 and (15 <= filetime.minute <= 59)) or (filetime.hour == 8 and filetime.minute <= 10):
        first_part_of_name = "Herrera 1st"
    elif (filetime.hour == 8 and filetime.minute > 10) or (filetime.hour == 9 and filetime.minute <= 5):
        first_part_of_name = "Herrera 2nd"
    elif (filetime.hour == 9 and filetime.minute > 5) or (filetime.hour == 10 and filetime.minute == 0):
        first_part_of_name = "Herrera 3rd"
    elif (filetime.hour == 10 and filetime.minute > 0) or (filetime.hour == 10 and filetime.minute <= 59):
        first_part_of_name = "Herrera 4th"
    elif (filetime.hour == 12 and filetime.minute > 30) or (filetime.hour == 13 and filetime.minute <= 25):
        first_part_of_name = "Herrera 6th"
    elif (filetime.hour == 13 and filetime.minute > 25) or (filetime.hour == 14 and filetime.minute <= 10):
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
        df.loc[df[2].str.contains('\(', na=False), 2] = df[1]  # replaces id with last names
        df[2] = df.loc[~df[2].str.contains('\t', na=False), 2]
        df = df.sort_values(2)
        new_sorted_file = "D:\\Luis Herrera\\Teacher Stuff\\Attendance\\" + sort_name
        df.to_csv(new_sorted_file)
        if df_sr.index.max() > df.index.max():  # prepares to compare missing students
            df = df.reindex(index=df_sr2.index)
        else:
            df_sr2 = df_sr2.reindex(index=df.index)  # makes copy so final column isn't deleted
        df = df.replace({'\\0': ''}, regex=True)  # values shows up as starting with \0. necessary to compare
        temp_ab_list = df_sr2[int(sort_name[8])][~df_sr2[int(sort_name[8])].isin(df[2])]  # adjust time to class period, list of absent students
        ab_list[sort_name[8]] = temp_ab_list


df_absences = pd.DataFrame(ab_list, columns=ab_list.keys())
df_absences.to_csv('D:\\Luis Herrera\\Teacher Stuff\\Attendance\\Absences\\Absent' + dt.datetime.now().strftime('%m') + '_' + dt.datetime.now().strftime('%d') + '.csv')
