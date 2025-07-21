# CEGA RA Task README
To complete this task, I used both Python and R and searched the web for publicly available
project information from the Ohio DOT. My scripts were able to recreate the required template
with the same values for the given project and should work for others. Here are the five distinct
projects I’ve chosen and the reasons why (by PID):

- 106242: Most expensive project on the master list and also has the highest cost per day.
- 103055: The cheapest project.
- 102486: The project with lowest cost per day.
- 100959: Cheapest actual cost relative to the project’s estimated cost.
- 98702: The project with the most bidders.

I felt like these projects should be highlighted, given my findings. Three scripts were used:

**pid_search.py** is the first script I wrote which takes a user-input of multiple PIDs, separated by
commas, and returns information from TIMS (https://gis.dot.state.oh.us/tims_classic/projects/).
For example, my input of “106242, 103055, 102486, 100959, 98702” to search for the above
projects. A driver that simulates searching for each individual PID in Chrome and returns the
search results. Although you could just do this manually, this script automates the process, but is
slower and more complicated than I wanted it to be. Also, the internet connection when running
this script must be fairly fast and reliable or else the driver will timeout. This is the greatest
bottleneck in gathering the information. The output file is “project_info.xlsx”.

**readall_bidtabs.py** is the next script required. It uses historical bid tab data for 2018 which can
be downloaded from the Ohio DOT’s website.
(https://www.dot.state.oh.us/Divisions/ConstructionMgt/Estimating/Pages/bid-tabs.aspx) The
script takes the file “Bid Tabs 2018.pdf”, isolates the first page of each project’s bid tab, and
extracts text data from the file. It was able to do this for all the projects in the file and create a
dataframe for exportation (“project_bids.xlsx”).

**clean_ohio_data.R** puts everything together. It requires the masterlist “Ohio_2018_Resurfacing
PRR.xlsx” and the two output files from the Python scripts. It takes given information from the
masterlist, reformats the data, merges it with the other outputs, and churns out the final cleaned
data set with the five projects matching the template.
