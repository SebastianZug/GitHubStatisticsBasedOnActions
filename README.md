# Monitoring GitHub Projects be evaluating git logs

A github action monitors changes in this fake document and provides different diagrams automatically. They depict the development of lines of code and commits for various time intervals.

![Alt text](/images/Day.png?raw=true "Daily Changes")

![Alt text](/images/Week.png?raw=true "Weekly Changes")

The python file contains methods for extracting daily git statistics.

The python script covers standard diagrams but offers interfaces for additional evaluations too.

```python
# Example for individual filter
# Visualize code generation during last 30 days
filtered = data.loc[date.today() - timedelta(days=30): date.today()]
generate_diagram(project_name, filtered, 'D', "LastMonth")
```
![Alt text](/images/LastMonth.png?raw=true "Last 30 days")
