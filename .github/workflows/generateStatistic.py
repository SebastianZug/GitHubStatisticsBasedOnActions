from datetime import date, timedelta
import subprocess
import io
import pandas as pd
import re
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

def weeks(start, upto):
    return [date.fromordinal(d) for d in range(start.toordinal(), upto.toordinal(), 7)]

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
    return ['git', 'log', '--before={0}'.format(date.isoformat()), '--format=format:', '--shortstat', 'master', '--', '*.md']

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

def generate_diagram(project_name, start, upto):
    lines_per_week = []

    for d in weeks(start, upto):
        week_stat = {}
        result = subprocess.run(git_log_command(d),
                                check=True,
                                stdout=subprocess.PIPE,
                                universal_newlines=True).stdout
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
        week_stat["week"] = d
        week_stat["commits"] = commits
        week_stat["lines"] = lines
        lines_per_week.append(week_stat)

    print("Data for " + str(len(lines_per_week)) + " weeks found!\n")
    df = pd.DataFrame(lines_per_week)
    df['week'] = pd.to_datetime(df['week'])
    df['commits'] = df.commits.diff()
    df.set_index('week', inplace=True)
    print("Project " + project_name)
    print("{0} commits with {1} lines of code".format(df.commits.count(), df.lines.max()))
    ax = df.lines.plot(drawstyle="steps", linewidth = 2)
    ax.set_title(project_name)
    df.commits.plot(secondary_y=['commits'], drawstyle="steps", ax = ax)
    ax.set_xlabel('Weeks')
    ax.set_ylabel('Lines of Code')
    ax.right_ax.set_ylabel('Commits per week')
    #plt.show()
    fig = ax.get_figure()
    fig.savefig('figure.png')

if __name__ == "__main__":
    project_name = git_get_projectname()
    start = git_get_first_commit()
    generate_diagram(project_name, start, date.today() + timedelta(days=8))
