import numpy as np
from bokeh.models import ColumnDataSource, Button, Select, Div
from bokeh.sampledata.iris import flowers
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.io import show
from bokeh.events import ButtonClick
import random

Random=False
# Important: You must also install pandas for the data import.
def on_change_f(attr,old,new):
    global Random
    if new=="False":
        Random=False
    else:
        Random=True

# read and store the dataset
data = flowers.copy(deep=True)
data = data.drop(['species'], axis=1)

# calculate the cost of the current medoid configuration
# The cost is the sum of all minimal distances of all points to the closest medoids
def get_cost(meds):
    global data
    cost=0
    x=0
    med1_1=data.petal_length[meds[0]]
    med1_2=data.sepal_length[meds[0]]
    med1_3=data.petal_width[meds[0]]
    med1_4=data.sepal_width[meds[0]]

    med2_1=data.petal_length[meds[1]]
    med2_2=data.sepal_length[meds[1]]
    med2_3=data.petal_width[meds[1]]
    med2_4=data.sepal_width[meds[1]]

    med3_1=data.petal_length[meds[2]]
    med3_2=data.sepal_length[meds[2]]
    med3_3=data.petal_width[meds[2]]
    med3_4=data.sepal_width[meds[2]]

    colors=[]
    while x<150:
        x1=data.petal_length[x]
        x2=data.sepal_length[x]
        x3=data.petal_width[x]
        x4=data.sepal_width[x]

        c1=med1_1-x1
        if c1<0:
            c1= -c1
        c2=med1_2-x2
        if c2<0:
            c2= -c2
        c3=med1_3-x3
        if c3<0:
            c3= -c3
        c4=med1_4-x4
        if c4<0:
            c4= -c4

        costs=[]
        costs.append(c1+c2+c3+c4)

        c1=med2_1-x1
        if c1<0:
            c1= -c1
        c2=med2_2-x2
        if c2<0:
            c2= -c2
        c3=med2_3-x3
        if c3<0:
            c3= -c3
        c4=med2_4-x4
        if c4<0:
            c4= -c4

        costs.append(c1+c2+c3+c4)

        c1=med3_1-x1
        if c1<0:
            c1= -c1
        c2=med3_2-x2
        if c2<0:
            c2= -c2
        c3=med3_3-x3
        if c3<0:
            c3= -c3
        c4=med3_4-x4
        if c4<0:
            c4= -c4

        costs.append(c1+c2+c3+c4)
        

        if costs[0]<costs[1]:
            if costs[0]<costs[2]:
                cost+=costs[0]
                colors.append("green")
            else:
                cost+=costs[2]
                colors.append(2)
        else:
            if costs[1]<costs[2]:
                cost+=costs[1]
                colors.append("blue")
            else:
                cost+=costs[2]
                colors.append("red")
        x+=1
    returns=[cost,colors]
    return returns


# implement the k-medoids algorithm in this function and hook it to the callback of the button in the dashboard
# check the value of the select widget and use random medoids if it is set to true and use the pre-defined medoids
# if it is set to false.
def k_medoids(event):
    global Random
    global data
    global source
    global text
    # number of clusters:
    k = 3
    if Random==True:
        o1,o2,o3=random.sample(range(0,149),k)
        medoids=[o1,o2,o3]
        # Use the following medoids if random medoid is set to false in the dashboard. These numbers are indices into the
        # data array.
    else:
        medoids = [24, 74, 124]
    
    old_cost=get_cost(medoids)

    new_col=[]
    pos=[]

    print("starting x")
    x=0
    while x<150:
        if x!=medoids[0]:
            new=get_cost([x,medoids[1],medoids[2]])
            if new[0]<old_cost[0]:
                new_col.append(new[1])
                pos.append(new[0])
        x+=1
    
    print("starting y")
    x=0
    while x<150:
        if x!=medoids[1]:
            new=get_cost([medoids[0],x,medoids[2]])
            if new[0]<old_cost[0]:
                new_col.append(new[1])
                pos.append(new[0])
        x+=1
    
    print("starting z")
    x=0
    while x<150:
        if x!=medoids[2]:
            new=get_cost([medoids[0],medoids[1],x])
            if new[0]<old_cost[0]:
                new_col.append(new[1])
                pos.append(new[0])
        x+=1
    
    lowest=pos.index(min(pos))
    color=new_col[lowest]
    print("lowest is:")
    print(lowest)
    print("color is:")
    print(color)
    print("Cost is:")
    print(round(new[0],1))
    div.text=text+str(round(new[0],1))
    data["colors"]=color
    source.data=dict(
        sepal_length=data.sepal_length,
        sepal_width=data.sepal_width,
        petal_length=data.petal_length,
        petal_width=data.petal_width,
        colors=data.colors
    )
    print("I'm done")





    


# create a color column in your dataframe and set it to gray on startup
colors=["gray"]*150
data["colors"]=colors

text="The final cost is: "

print(data)
# Create a ColumnDataSource from the data
source=ColumnDataSource(data=dict(
    sepal_length=data.sepal_length,
    sepal_width=data.sepal_width,
    petal_length=data.petal_length,
    petal_width=data.petal_width,
    colors=data.colors
))

p=figure(plot_height=800, plot_width=600)
p.scatter("petal_length","sepal_length",fill_color="colors",fill_alpha=0.5,line_color=None,source=source)

p2=figure(plot_height=800, plot_width=600)
p2.scatter("petal_width","petal_length",fill_color="colors",fill_alpha=0.5,line_color=None,source=source)

# Create a select widget, a button, a DIV to show the final clustering cost and two figures for the scatter plots.
select=Select(title="Random Medoids",value="False",options=["False","True"])
select.on_change("value",on_change_f)

button=Button(label="Cluster data")
button.on_event(ButtonClick,k_medoids)

div=Div(text=text)

# use curdoc to add your widgets to the document
curdoc().add_root(row(column(select,button,div),p,p2))
curdoc().title = "DVA_ex_3"





# use on of the commands below to start your application
# bokeh serve --show dva_ex3_skeleton_HS20.py
# python -m bokeh serve --show dva_ex3_skeleton_HS20.py
# bokeh serve --dev --show dva_ex3_skeleton_HS20.py
# python -m bokeh serve --dev --show dva_ex3_skeleton_HS20.py