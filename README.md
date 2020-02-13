# Monitoring GitHub Projects be evaluating git logs

A GitHub action monitors changes in this examplary document and provides different diagrams automatically. They depict the code count and number of commits for various time intervals. 

The corresponding python file contains methods for extracting git log parameter. It maps the information on a python pandas table and generates standard diagrams "Day.png", "Week.png" etc. Additionally, you can add more specific evaluations too.

__Examples__

1. Lines of code / commits depicted for all day beginning with the first commit

![Alt text](/statistics/Day.png?raw=true "Daily Changes")

2. Lines of code / commits depicted for each week beginning with the first commit

![Alt text](/statistics/Week.png?raw=true "Weekly Changes")

3. Lines of code / commits depicted for the last 30 days

```python
# Example for individual filter
# Visualize code generation during last 30 days
data = generate_data(date.today() - timedelta(days=30),
                     date.today() + timedelta(days=1))
generate_diagram(project_name, data, 'D', "LastMonth")
```

![Alt text](/statistics/LastMonth.png?raw=true "Last 30 days")

The corresponding action description is available in `.github\workflow`. It is activated by changes in files with extension `.md`! The filtering avoids an endless loop by generating new content based on the action.

```
name: Generate activity diagrams

on:
  push:
    paths:
    - '**.md'

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - name: Check out repository
      uses: actions/checkout@v2
      with: 
        fetch-depth: 0
    - name: Set up Python 3.6
      uses: actions/setup-python@v1
      with:
        python-version: '3.6' # Semantic version range syntax or exact version of a Python version
    - name: Display Python version
      run: python -c "import sys; print(sys.version)"
    - name: Install dependencies
      run: |
           python -m pip install --upgrade pip
           pip install matplotlib
           pip install pandas
    - name: Move python script to repository root
      run: |
           cp statistics/generateStatistic.py .
    - name: Run python script
      run: |
           python generateStatistic.py
           rm generateStatistic.py
    - name: Commit files
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        mv *.png statistics/
        git add ./statistics/*.png
        git status
        git commit -m "Add new statistics" -a
    - name: Push changes
      uses: ad-m/github-push-action@v0.5.0
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
```
