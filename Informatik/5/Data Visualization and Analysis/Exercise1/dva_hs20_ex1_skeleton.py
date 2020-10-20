import pandas as pd
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, HoverTool, Select, FactorRange, CustomJS, Dropdown
from bokeh.plotting import figure, curdoc
from bokeh.io import show

# This exercise will be graded using the following Python and library versions:
###############
# Python 3.8
# Bokeh 2.2.1
# Pandas 1.1.2
###############

# define your callback function of the Select widget here. Only do this once you've followed the rest of the
# instructions below and you actually reach the part where you have to add and configure the Select widget.
# the general idea is to set the data attribute of the plots ColumnDataSource to the data entries of the different
# ColumnDataSources you construct during the data processing. This data change should then automatically be displayed
# in the plot. Take care that the bar-labels on the y axis also reflect this change.


# read data from .csv file
df = pd.read_csv('AZA_MLE_Jul2018_utf8.csv', encoding='utf-8')
# construct list of indizes to remove unnecessary columns
cols = [1, 3]
cols.extend([i for i in range(7, 15)])
df.drop(df.columns[cols], axis=1, inplace=True)

# task 1

# rename the columns of the data frame according to the following mapping:
# 'Species Common Name': 'species'
# 'TaxonClass': 'taxon_class'
# 'Overall CI - lower': 'ci_lower'
# 'Overall CI - upper': 'ci_upper'
# 'Overall MLE': 'mle'
# 'Male Data Deficient': 'male_deficient'
# 'Female Data Deficient': 'female_deficient'
df=df.rename(columns={'Species Common Name': 'species',
    'TaxonClass': 'taxon_class',
    'Overall CI - lower': 'ci_lower',
    'Overall CI - upper': 'ci_upper',
    'Overall MLE': 'mle',
    'Male Data Deficient': 'male_deficient',
    'Female Data Deficient': 'female_deficient'})




# Remove outliers, split the dataframe by taxon_class and and construct a ColumnDataSource from the clean DataFrames
# hints:
# we only use the following three taxon classes: 'Mammalia', 'Aves', 'Reptilia'
# use dataframe.loc to access subsets of the original dataframe and to remove the outliers
# each time you sort the dataframe reset its index
# outliers are entries which have male and/or female data deficient set to yes
# reference dataframe: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
# reference columndatasource: https://bokeh.pydata.org/en/latest/docs/reference/models/sources.html

# construct three independent dataframes based on the aforementioned taxon classes and remove the outliers
df_mammalia=df.loc[df["taxon_class"]=="Mammalia"]
df_mammalia=df_mammalia.loc[df_mammalia["male_deficient"]!="yes"]
df_mammalia=df_mammalia.loc[df_mammalia["female_deficient"]!="yes"]

df_aves=df.loc[df["taxon_class"]=="Aves"]
df_aves=df_aves.loc[df_aves["male_deficient"]!="yes"]
df_aves=df_aves.loc[df_aves["female_deficient"]!="yes"]

df_reptilia=df.loc[df["taxon_class"]=="Reptilia"]
df_reptilia=df_reptilia.loc[df_reptilia["male_deficient"]!="yes"]
df_reptilia=df_reptilia.loc[df_reptilia["female_deficient"]!="yes"]



# sort the dataframes by 'mle' in descending order and then reset the index
df_mammalia=df_mammalia.sort_values(by=["mle"],ascending=False)

df_aves=df_aves.sort_values(by=["mle"],ascending=False)

df_reptilia=df_reptilia.sort_values(by=["mle"],ascending=False)


# reduce each dataframe to contain only the 10 species with the highest 'mle'
df_mammalia=df_mammalia.head(10)
df_aves=df_aves.head(10)
df_reptilia=df_reptilia.head(10)



# sort the dataframe in the correct order to display it in the plot and reset the index again.
# hint: the index decides the y location of the bars in the plot. You might have to modify it to have a visually
# appealing barchart
df_mammalia=df_mammalia.sort_values(by=["mle"],ascending=True)

df_aves=df_aves.sort_values(by=["mle"],ascending=True)

df_reptilia=df_reptilia.sort_values(by=["mle"],ascending=True)

# There's an entry in the aves dataframe with a species named 'Penguin, Northern & Southern Rockhopper (combined)'.
# Rename that species to 'Penguin, Rockhopper'
df_aves=df_aves.replace('Penguin, Northern & Southern Rockhopper (combined)',"Penguin, Rockhopper")


# construct a ColumDataSource for each of the dataframes
source1=ColumnDataSource(data=dict(
    x=df_mammalia.mle,
    y=df_mammalia.species,
    lower=df_mammalia.ci_lower,
    upper=df_mammalia.ci_upper
))


source2=ColumnDataSource(data=dict(
    x=df_aves.mle,
    y=df_aves.species,
    lower=df_aves.ci_lower,
    upper=df_aves.ci_upper
))


source3=ColumnDataSource(data=dict(
    x=df_reptilia.mle,
    y=df_reptilia.species,
    lower=df_reptilia.ci_lower,
    upper=df_reptilia.ci_upper
))


# construct a fourth ColumnDataSource that is used as input for the plot and set its data to the Mammalian
# ColumnDataSource as initial value. This fourth ColmunDataSource is required to later be able to change the data
# interactively with the dropdown menu.
source=ColumnDataSource(data=dict(
    x=df_mammalia.mle,
    y=df_mammalia.species,
    lower=df_mammalia.ci_lower,
    upper=df_mammalia.ci_upper
))


# task 2:

# configure mouse hover tool
# reference: https://bokeh.pydata.org/en/latest/docs/user_guide/categorical.html#hover-tools
# your tooltip should contain the data of 'ci_lower' and 'ci_upper' named 'low' and 'high' in the visualization
Tooltips=[
    ("low","@lower"),
    ("high","@upper")
]


# construct a figure with the correct title, axis labels, x and y range, add the hover tool and disable the toolbar
p=figure(plot_height=600,plot_width=1200,x_range=(0,50),y_range=FactorRange(*source.data["y"]),tooltips=Tooltips,title="Medium Life Expextancy of Animals in Zoos")
p.yaxis.axis_label = "Species"
p.xaxis.axis_label = "Medium Life Expectancy"


# add the horizontal bar chart to the figure and configure it correctly
# the lower limit of the bar should be ci_lower and the upper limit ci_upper
p.hbar(left="lower",right="upper",y="y",source=source, height=0.6)



# add a Select tool (dropdown selection) and configure its 'on_change' callback. Define the callback function in the
# beginning of the document and write it such that the user can choose which taxon_class is visualized in the plot.
# the default visualization at startup should be 'Mammalia'
select=Select(title="Taxonomic class",value="mammalia",options=["mammalia","aves","reptilia"])

def callback (attr,old,new):
    if new=="mammalia":
        print ("hello mammalia")
        source.data=dict(
            x=df_mammalia.mle,
            y=df_mammalia.species,
            lower=df_mammalia.ci_lower,
            upper=df_mammalia.ci_upper
        )
    elif new=="aves":
        print ("hello aves")
        source.data=dict(
            x=df_aves.mle,
            y=df_aves.species,
            lower=df_aves.ci_lower,
            upper=df_aves.ci_upper
        )
    elif new=="reptilia":
        print ("hello reptilia")
        source.data=dict(
            x=df_reptilia.mle,
            y=df_reptilia.species,
            lower=df_reptilia.ci_lower,
            upper=df_reptilia.ci_upper
        )
    print(source.data)

select.on_change("value",callback)


# use curdoc to add your plot and selection widget such that you can start a bokeh server and an interactive plotting
# session.
curdoc().add_root(row(p, select))



# you should be able to start a plotting session executing one of the following commands in a terminal:
# (if you're using a virtual environment you first have to activate it before using these commands. You have to be in
# the same folder as your dva_hs20_ex1_skeleton.py file.)
# Interactive session: bokeh serve --show dva_hs20_ex1_skeleton.py
# If the above doesn't work use the following: python -m bokeh serve --show dva_hs20_ex1_skeleton.py
# For interactive debugging sessions you can use one of the two commands below. As long as you don't close your last
# browser tab you can save your changes in the python file and the bokeh server will automatically reload your file,
# reflecting the changes you just made. Be aware that after changes leading to errors you usually have to restart
# the bokeh server by interrupting it in your terminal and executing the command again.
# bokeh serve --dev --show dva_hs20_ex1_skeleton.py
# python -m bokeh serve --dev --show dva_hs20_ex1_skeleton.py

