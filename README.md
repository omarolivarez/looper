# looper

## Author: Omar Olivarez
## Last Modified: 05/12/2021

# Description:  
Make a GUI app  
That takes in a dataframe/csv  
You select which column you want to bootstrap  
You select how many repetitions you want  
Optional: you upload a reps file that says how many reps previously ran
The system will start bootstrapping  
It will show progress toward your number of reps as a progress bar  
It will detect when your batter is running low and automatically stop  
Or, you can make it pause after some time (MVP versus previous point is best case scenario)  
It will save each rep's values in a python DB  
It will generate a reps file that simply contains the number of reps that have already run 
When all reps have been completed, it will calculate the statistic, st dev, and CIs  
It will output these measures into a text file
