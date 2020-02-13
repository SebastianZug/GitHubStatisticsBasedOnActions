from datetime import date, timedelta, datetime
from dateutil import relativedelta
import subprocess
import io
import pandas as pd
import re
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from pytz import reference

def days(start, upto):
    td = upto - start
    day_count = int(td/timedelta(days = 1))
    return [start + timedelta(days = x) for x in range(day_count)]

def git_get_first_commit():
    command = ['git', 'log', '--reverse', '--date=short']
    result = subprocess.run(command,
                                check=True,
                                stdout=subprocess.PIPE,
                                universal_newlines=True).stdout
    filtered = io.StringIO(result.replace('\n\n','\n'))
    for line in filtered:
        if 'Date' in line:
            date_str = line.replace('\n','').split(' ')[-1]
            date_ = [int(i) for i in date_str.split('-') ]
            break
    return date(date_[0], date_[1], date_[2])

def git_log_command(date):
    end = date + timedelta(days = 1)
    return ['git', 'log', '--after={0} 00:00'.format(date.isoformat()), '--before={0} 00:00'.format(end.isoformat()),'--format=format:', '--shortstat', 'master', '--', '*.md']

def get_key_values(string_array, substring):
    index = [idx for idx, s in enumerate(string_array) if substring in s]
    if len(index):
        return index[0]
    else:
        return -1

def git_get_projectname():
    command = ['git', 'remote', '-v']
    result = subprocess.run(command,
                            check=True,
                            stdout=subprocess.PIPE,
                            universal_newlines=True).stdout
    result = result.replace('\t', '\n')
    return result.split('\n')[1]

def generate_data(start, upto):
    activities_per_day = []
    interval = days(start, upto);
    print("Reading time interval of " + str(len(interval)) + " days ...")
    for d in interval:
        daily_stat = {}
        print(git_log_command(d))
        result = subprocess.run(git_log_command(d),
                                check=True,
                                stdout=subprocess.PIPE,
                                universal_newlines=True).stdout
        print(result)
        filtered = io.StringIO(result.replace('\n\n','\n'))
        commits = 0
        lines = 0
        for line in filtered:
            content = line.split(' ')
            index = get_key_values(content, 'file')
            if index!=-1:
                commits = commits + int(content[index -1 ])
            index = get_key_values(content, 'insertion')
            if index!=-1:
                lines = lines + int(content[index -1 ])
            index = get_key_values(content, 'deletion')
            if index!=-1:
                lines = lines - int(content[index -1 ])
        daily_stat["day"] = d
        daily_stat["commits"] = commits
        daily_stat["lines"] = lines
        activities_per_day.append(daily_stat)

    df = pd.DataFrame(activities_per_day)
    print(df.head())
    if len(activities_per_day):
        df['day'] = pd.to_datetime(df['day'])
        df.set_index('day', inplace=True)
        df.drop(df[df.commits == 0].index, inplace=True)
        print("... {0} activity days with {1} lines of code found.".format(df.lines.count(), df.lines.sum()))

    return df

def generate_diagram(project_name, data, interval, filename):
    df = data.groupby(pd.Grouper(freq=interval)).sum()
    df['lines_sum'] = df.lines.cumsum().astype('int64')
    df.drop(['lines'], axis=1, inplace=True)
    #print(df.head())
    fig, ax = plt.subplots()
    df.lines_sum.plot(drawstyle="steps-mid", linewidth = 2, ax = ax)
    ax.set_title(project_name)
    df.plot(secondary_y=['commits'], drawstyle="steps-mid", ax = ax)
    ax.set_xlabel(filename)
    ax.set_ylabel('Lines of Code')
    ax.right_ax.set_ylabel('Commits per ' + filename)
    plt.tight_layout()
    #plt.show()
    fig.savefig(filename+".png")
    print("File saved to " + filename + ".png")

if __name__ == "__main__":
    localtime = reference.LocalTimezone()
    print("Time zone of the server: " + str(localtime.tzname(datetime.now())))
    project_name = git_get_projectname()
    print("Evaluating project " + project_name)
    start = git_get_first_commit()
    data = generate_data(start - timedelta(days=1), date.today() + timedelta(days=2))
    intervals = {
        "Day": 'D',
        "Week": "W",
        "Month": 'M',
        "Year": 'Y'}
    for name, abbrevation in intervals.items():
        generate_diagram(project_name, data, abbrevation, name)

    # Example for individual filter
    # Visualize code generation during last 30 days
    filtered = data.loc[date.today() - timedelta(days=30): date.today()]
    generate_diagram(project_name, filtered, 'D', "LastMonth")
