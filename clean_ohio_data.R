# Load packages, make sure they are installed
library(openxlsx) # to write excel
library(readxl) # to read excel
library(tidyverse) # tidyverse ofc
library(ggplot2) # for visualization
library(tigris) # for fips

# Import project masterlist
ohio_2018 <- read_excel("Ohio_2018_Resurfacing PRR.xlsx")

# Clean and organize given variables in masterlist
clean_ohio <- ohio_2018 %>% 
  mutate(project_id = `PID`) %>% 
  mutate(project_start = as.Date(as.character(`AwardDate`), format="%Y-%m-%d")) %>% 
  mutate(year = as.numeric(format(project_start,'%Y'))) %>% 
  mutate(project_end = as.Date(as.character(`CompletionDate`), format="%Y-%m-%d")) %>% 
  mutate(project_duration_days = as.numeric(project_end-project_start)) %>% 
  mutate(cost_mils = `AdjContAmt`/1000000) %>% 
  mutate(lanes = as.factor(str_extract(`Desc`,"^[^ ]+"))) %>% 
  mutate(lanes = recode(lanes, "TWO" = "2", "FOUR" = "4")) %>% 
  mutate(project_start = format(project_start, "%m/%d/%Y")) %>% 
  mutate(state = "Ohio") %>% 
  select(state, year, project_start, project_id, lanes, project_duration_days, cost_mils)

# Import and organize data from the bid tab reader script `readall_bidtabs.py`
project_bids <- read_excel("project_bids.xlsx")

ohio_w_bids <- left_join (x = clean_ohio, y = project_bids, by = "project_id") %>% 
  mutate(eng_estimate_mils = as.numeric(str_replace_all(eng_estimate, ",", ""))/1000000) %>% 
  mutate(win_bid_mils = as.numeric(str_replace_all(win_bid, ",", ""))/1000000) %>% 
  select(state, year, project_start, project_id, lanes, project_duration_days,
         eng_estimate_mils, win_bid_mils, cost_mils, num_bidders, bidders_list) %>% 
  mutate(win_cost = cost_mils/win_bid_mils) %>% 
  mutate(eng_cost = cost_mils/eng_estimate_mils) %>% 
  mutate(cost_day = cost_mils/project_duration_days) 

# Import and organize data from the PID search script `pid_search.py

project_info <- read_excel("project_info.xlsx")

clean_info <- project_info %>% 
  mutate(project_id = `PID`) %>%
  mutate(county = `Recorded County`) %>% 
  mutate(route = as.numeric(`Route`)) %>% 
  mutate(begin = as.numeric(`CTL Begin`)) %>% 
  mutate(end = as.numeric(`CTL End`)) %>% 
  mutate(mileage = 2*(end - begin)) %>% 
  select(project_id, county, route, mileage)


# Join all datasets together
five_projects <- left_join(x = clean_info, y = ohio_w_bids, by = "project_id") 

# Use tigris data to find FIPS code and final formatting
options(tigris_use_cache = TRUE)
county_shapes <- counties(cb = TRUE, year = 2023) # or use default year
county_fips_df <- as.data.frame(county_shapes) %>%
  mutate(state = (STATE_NAME)) %>% 
  mutate(county = (NAME)) %>% 
  mutate(fips = GEOID) %>% 
  select(state, county, fips)
final_five_projects <- left_join(five_projects, county_fips_df, by = c("state", "county")) %>% 
  select(state, county, fips, year, project_start, project_id, route, mileage, lanes, project_duration_days, 
         eng_estimate_mils, win_bid_mils, cost_mils, num_bidders, bidders_list)

# Write .xlsx file into working directory
write.xlsx(final_five_projects, "Ohio_projects_collected_clean.xlsx")