from bokeh.core.properties import value
from bokeh.models import ColumnDataSource, CustomJSHover
from bokeh.plotting import figure, show

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
years = ["2015", "2016", "2017"]
colors = ["#c9d9d3", "#718dbf", "#e84d60"]

data = {'fruits' : fruits,
        '2015'   : [2, 1, 4, 3, 2, 4],
        '2016'   : [5, 3, 4, 2, 4, 6],
        '2017'   : [3, 2, 4, 4, 5, 3]}

source = ColumnDataSource(data=data)

tooltips= [("name", "$name"), ("count", "@$name")]

p = figure(x_range=fruits, plot_height=350, title="Fruit Counts by Year",
           toolbar_location=None, tooltips=tooltips)

renderers = p.vbar_stack(years, x='fruits', width=0.9, color=colors, source=source,
                         legend=[value(x) for x in years], name=years)

p.hover[0].tooltips.append(('info', '$name{custom}'))
p.hover[0].formatters = {'$name' : CustomJSHover(code = "return special_vars.name + '_text'")}

show(p)