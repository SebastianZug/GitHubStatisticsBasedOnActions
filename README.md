# Monitoring GitHub Projects be evaluating git logs

A GitHub action monitors changes in this fake document and provides different diagrams automatically. They depict the development of lines of code and commits for various time intervals.

![Alt text](/statistics/Day.png?raw=true "Daily Changes")

![Alt text](/statistics/Week.png?raw=true "Weekly Changes")

The python file contains methods for extracting daily git statistics. It maps the information in a python pandas table generates standard diagrams "Day.png", "Week.png" etc. Additionally, you can add more specific evaluations too.

```python
# Example for individual filter
# Visualize code generation during last 30 days
filtered = data.loc[date.today() - timedelta(days=30): date.today()]
generate_diagram(project_name, filtered, 'D', "LastMonth")
```
![Alt text](/statistics/LastMonth.png?raw=true "Last 30 days")

The corresponding action description is available in `.github\workflow`. It is activated by changes in files with extension `.md`.
