# US Election Data 2000 -2020
This project is aimed at looking gathering insights from US Election data from 2000 - 2020

All data is contained in 'data.csv'

[Data source](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ)

## Current Progress:

### Difference between What Percentage of Votes Were for a Party Compared to the Overall State:
This graph shows for a given state and year, what percentage of votes were Democarat and what percentage of votes were Republican (black)

It does the same for all fo the counties in that state (blue = Democrat, red = Republican)


![Figure 1](https://github.com/ahhossain/president/blob/main/Figure_1.png)

### Difference between What Percentage of Votes Were for a Party Compared to the Overall State:
This graph shows how much a parties vote percentage in a county comapred to their performance in the state.

For example in Arizona in the year 2000, Apache_DEM has a value -22. In 2000 in Arizona, Democrats won 45% of votes but the county Apache, Democrats won about 67% of the votes.

Democrat votes in Arizona - Democrat votes in Apache = 45% - 67% = -22%

When a given countys votes for a given parties is similar to the state average especially if this is consistant throughout each year, it would imply that the county is good indicater of how the state will look.

This is just correlation, no causation is implied here.

How is this useful? If some counties with correlation with the states call early during the next election, its a good indicator of which way the overall state will go.


![Figure 2](https://github.com/ahhossain/president/blob/main/Figure_2.png)
