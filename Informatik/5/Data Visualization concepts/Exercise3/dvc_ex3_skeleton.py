import pandas as pd 
import numpy as np
import bokeh.palettes as bp
from bokeh.plotting import figure
from bokeh.io import output_file, show, save
from bokeh.models import ColumnDataSource, HoverTool, ColorBar, RangeTool
from bokeh.transform import linear_cmap
from bokeh.layouts import gridplot, column


# ==========================================================================
# Goal: Visualize Covid-19 Tests statistics in Switzerland with linked plots
# Dataset: covid19_tests_switzerland_bag.csv
# Data Interpretation: 
# 		n_negative: number of negative cases in tests
# 		n_positive: number of positive cases in tests
# 		n_tests: number of total tests
# 		frac_negative: fraction of POSITIVE cases in tests
# ==========================================================================



### Task1: Data Preprocessing


## T1.1 Read the data to the dataframe "raw"
# You can read the latest data from the url, or use the data provided in the folder (update Nov.3, 2020)

url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/covid19_tests_switzerland_bag.csv?raw=true'
raw = pd.read_csv(url)
raw=raw.rename(columns={"frac_negative":"frac_positive"})

print(raw)



## T1.2 Create a ColumnDataSource containing: date, positive number, positive rate, total tests
# All the data can be extracted from the raw dataframe.

date = pd.to_datetime(raw["date"])
date_raw=raw["date"]

pos_num = raw["n_positive"].tolist()
pos_rate = raw["frac_positive"].tolist()
test_num = raw["n_tests"].tolist()


source = ColumnDataSource(data=dict(
    dates=date,
    date_raw=date_raw,
    test_n=test_num,
    pos_n=pos_num,
    pos_r=pos_rate
))


## T1.3 Map the range of positive rate to a colormap using module "linear_cmap"
# "low" should be the minimum value of positive rates, and "high" should be the maximum value
colors=("DCDCDC","FAEBD7","FFEFD5","FFEBCD","FFE4B5","F0E68C","EEDD82","BDB76B",)


mapper = linear_cmap(
    field_name="pos_r",
    palette="Viridis256",
    low=min(pos_rate),
    high=max(pos_rate))


x_range=date[0:30]


### Task2: Data Visualization
# Reference link:
# (range tool example) https://docs.bokeh.org/en/latest/docs/gallery/range_tool.html?highlight=rangetool


## T2.1 Covid-19 Total Tests Scatter Plot
# x axis is the time, and y axis is the total test number. 
# Set the initial x_range to be the first 30 days.
tooltips=[
    ("Date","@date_raw"),
    ("Total test numbers","@test_n")
]



TOOLS = "box_select,lasso_select,wheel_zoom,pan,reset,help"
p = figure(plot_height=400, plot_width=800, tools=TOOLS, x_axis_type="datetime", tooltips=tooltips,toolbar_location=None,x_range=(date[0],date[29]))
p.scatter("dates","test_n",fill_color=mapper,line_color="black",source=source)



p.title.text = 'Covid-19 Tests in Switzerland'
p.yaxis.axis_label = "Total Tests"
p.xaxis.axis_label = "Date"
p.sizing_mode = "stretch_both"

# Add a hovertool to display date, total test number


## T2.2 Add a colorbar to the above scatter plot, and encode positve rate values with colors; please use the color mapper defined in T1.3 

color_bar =  ColorBar(color_mapper=mapper["transform"])
p.add_layout(color_bar)




## T2.3 Covid-19 Positive Number Plot using RangeTool
# In this range plot, x axis is the time, and y axis is the positive test number.

select = figure(title="Drag the middle and edges of the selection box to change the range above",
                plot_height=300, plot_width=1500,
                tools="", toolbar_location=None, x_axis_type="datetime", tooltips=tooltips,background_fill_color="#efefef")


# Define a RangeTool to link with x_range in the scatter plot
range_tool = RangeTool(x_range=p.x_range)
select.line('dates', 'pos_n', source=source)
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool


# Draw a line plot and add the RangeTool to the plot
select.yaxis.axis_label = "Positive Cases"
select.xaxis.axis_label = "Date"



# Add a hovertool to the range plot and display date, positive test number
#hover2 = HoverTool(...)
#select.add_tools(hover2)


## T2.4 Layout arrangement and display

linked_p = column(p,select)
show(linked_p)
output_file("dvc_ex3.html")
save(linked_p)



