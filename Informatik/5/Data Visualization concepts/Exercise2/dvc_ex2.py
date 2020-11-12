import pandas as pd 
from math import pi
import numpy as np
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange, Line, LinearAxis, Legend
import bokeh.palettes as bp
 
# Goal: Draw a line chart displaying averaged daily new cases for all cantons in Switzerland.
# Dataset: covid19_cases_switzerland_openzh-phase2.csv
# Interpretation: value on row i, column j is either the cumulative covid-19 case number of canton j on date i or null value




### Task 1: Data Preprocessing


## T1.1 Read data into a dataframe, set column "Date" to be the index 

url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/covid19_cases_switzerland_openzh-phase2.csv?raw=true'

raw = pd.read_csv(url)



# Initialize the first row with zeros, and remove the last column 'CH' from dataframe
raw = raw.fillna(value=0,limit=1)
raw = raw.drop(labels="CH_diff",axis=1)
raw = raw.drop(labels="CH_pc",axis=1)
raw = raw.drop(labels="CH_diff_pc",axis=1)



# Fill null with the value of previous date from same canton
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html
raw = raw.fillna(method="ffill")


## T1.2 Calculate and smooth daily case changes

# Compute daily new cases (dnc) for each canton, e.g. new case on Tuesday = case on Tuesday - case on Monday;
# Fill null with zeros as well
columns=list(raw)

cantons = raw.columns.values
cantons = cantons[1:27]


dnc={}
z=0

for i in columns[1:27]:
	temp=raw[i]
	cant_dnc=[]
	x=0
	while x<len(temp)-1:
		y=temp[x+1]-temp[x]
		if y<0: #This removes negative numbers when numbers from some days aren't added yet
			y=0
		cant_dnc.append(y)
		x+=1
	name=cantons[z]
	dnc[name]=cant_dnc
	z+=1

dnc=pd.DataFrame(dnc)

# Smooth daily new case by the average value in a rolling window, and the window size is defined by step
# Why do we need smoothing? How does the window size affect the result?
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html
step = 3

dnc.rolling(step).sum()






## T1.3 Build a ColumnDataSource 

# Extract all canton names and dates
# NOTE: be careful with the format of date when it is used as x input for a plot
date = raw.iloc[:,0]
date=date.tolist()


# Create a color list to represent different cantons in the plot, you can either construct your own color patette or use the Bokeh color pallete
color_palette = ["#808080","#000000","#FF0000",'#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef', '#deebf7', '#f7fbff','#393b79', '#5254a3', '#6b6ecf', '#9c9ede','#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a',"#808080","#000000","#FF0000",'#084594', '#2171b5']

# Build a dictionary with date and each canton name as a key, i.e., {'date':[], 'AG':[], ..., 'ZH':[]}
# For each canton, the value is a list containing the averaged daily new cases
source_dict = {}

dnc_avg=[]

date.pop(-1)


source_dict["date"]=date
x=0
for canton in cantons:
	w=dnc.iloc[:,x]
	source_dict[canton]=w.tolist()
	dnc_avg.append(w.tolist())
	x+=1


source = ColumnDataSource(data=source_dict)


### Task 2: Data Visualization

## T2.1: Draw a group of lines, each line represents a canton, using date, dnc_avg as x,y. Add proper legend.
# https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/line.html?highlight=line#bokeh.models.glyphs.Line
# https://docs.bokeh.org/en/latest/docs/user_guide/interaction/legends.html



p = figure(x_range=FactorRange(*date),plot_width=1500, plot_height=800, x_axis_type="datetime")
p.title.text = 'Daily New Cases in Switzerland'


for canton,color in zip(cantons,color_palette): 
	p.line(source_dict["date"],source_dict[canton],color=color,alpha=0.8,muted_alpha=0,legend_label=canton)
#p.xaxis.ticker = [2020-6, 2020-7, 2020-8, 2020-9, 2020-10]



# Make the legend of the plot clickable, and set the click_policy to be "hide"
p.legend.location = "top_left"
p.legend.click_policy="hide"



## T2.2 Add hovering tooltips to display date, canton and averaged daily new case

# (Hovertip doc) https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#hovertool
# (Date hover)https://stackoverflow.com/questions/41380824/python-bokeh-hover-date-time
hover=HoverTool(
	tooltips=[
		("Canton","@canton"),
		("Date","@date{%F}"),
		("New cases","@dnc_avg")
	],
	formatters={
		"@date":"datetime"
	}
)



p.add_tools(hover)

show(p)
output_file("dvc_ex2.html")
save(p)














