import pandas as pd 
from math import pi
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange,CustomJS
# import bokeh.palettes as bp # uncomment it if you need special colors that are pre-defined

 
### Task 1: Data Preprocessing
 

## T1.1 Read online .csv file into a dataframe using pandas
# Reference links: 
# https://pandas.pydata.org/pandas-docs/stable/reference/frame.html
# https://stackoverflow.com/questions/55240330/how-to-read-csv-file-from-github-using-pandas 

original_url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/demographics_switzerland_bag.csv?raw=true'
df = pd.read_csv(original_url,index_col=0)



## T1.2 Prepare data for a grouped vbar_stack plot
# Reference link, read first before starting: 
# https://docs.bokeh.org/en/latest/docs/user_guide/categorical.html#stacked-and-grouped


# Filter out rows containing 'CH' 
df=df[df.canton != "CH"]
# print(df.head())

# Extract unique value lists of canton, age_group and sex
canton=[]
for x in df.canton:
    if x in canton:
        pass
    else:
        canton.append(x)

age_group=[]
for x in df.age_group:
    if x in age_group:
        pass
    else:
        age_group.append(x)

sex=[]
for x in df.sex:
    if x in sex:
        pass
    else:
        sex.append(x)


# Create a list of categories in the form of [(canton1,age_group1), (canton2,age_group2), ...]
factors = []
for x in canton:
    for y in age_group:
        temp=(x,y)
        factors.append(temp)


# Use genders as stack names
stacks = ['male','female']


# Calculate total population size as the value for each stack identified by canton,age_group and sex
stack_val_m = []
for x in factors:
    temp_val=0
    values=df[df.canton==x[0]]
    values=values[values.age_group==x[1]]
    values=values[values.sex=="Männlich"]
    for y in values.pop_size:
        temp_val=temp_val+y
    stack_val_m.append(temp_val)

stack_val_f = []
for x in factors:
    temp_val=0
    values=df[df.canton==x[0]]
    values=values[values.age_group==x[1]]
    values=values[values.sex=="Weiblich"]
    for y in values.pop_size:
        temp_val=temp_val+y
    stack_val_f.append(temp_val)

middle=len(stack_val_m)
stack_val=stack_val_m+stack_val_f
#I tried to create this code in a way where it would also work for inputs where there only exist people of one sex for a certain agegroup.



# Build a ColumnDataSource using above information
source = ColumnDataSource(data=dict(
    x=factors,
    male=stack_val[0:middle],
    female=stack_val[middle:]
))

#Creating the tooltips for the hoverfunction in task 2.2
Tooltips=[
    ("sex","$name"),
    ("canton, age_group","@x"),
    ("Population","@$name"),
]


### Task 2: Data Visualization


## T2.1: Visualize the data using bokeh plot functions
p=figure(x_range=FactorRange(*factors), plot_height=500, plot_width=800, tooltips=Tooltips,title='Canton Population Visualization')
p.yaxis.axis_label = "Population Size"
p.xaxis.axis_label = "Canton"
p.sizing_mode = "stretch_both"
p.xgrid.grid_line_color = None


p.vbar_stack(stacks, x="x",color=["blue","red"],width=0.9,alpha=0.6,source=source,legend_label=sex)



## T2.2 Add the hovering tooltips to the plot using HoverTool
# To be specific, the hover tooltips should display “gender”, canton, age group”, and “population” when hovering.
# https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#hovertool
# read more if you want to create fancy hover text: https://stackoverflow.com/questions/58716812/conditional-tooltip-bokeh-stacked-chart

#Comment: I added the Hovertool in the code above which is why the following two lines are commented. 
#I'm unsure if I should have done it down here necesseraly but since the format in which I created my solution was also found
#under the HoverTool section on the bokeh page I'm assuming that my solution is correct and used HoverTool.
#But since I'm unsure I'd be happy if you could let me know if this is correct or not.

#hover = HoverTool(...)
#p.add_tools(hover)
show(p)





## T2.3 Save the plot as "dvc_ex1.html" using output_file



