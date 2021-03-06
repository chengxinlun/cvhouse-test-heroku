# ------------------Census functions------------------#

# modules to import
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import srcCode.censusDescs as cd

# City industry data
industryCity = pd.read_csv('data/census/industryCity.csv')
# Neighborhood industry data
industryNeighborhood = pd.read_csv('data/census/industryNeighborhood.csv')
# City age data
ageCity = pd.read_csv("data/census/ageCity.csv")
# Neighborhood age data
ageNeighborhood = pd.read_csv("data/census/ageNeighborhood.csv")
# City race data
raceCity = pd.read_csv('data/census/raceEthnicityCity.csv')
# Neighborhod race data
raceNeighborhood = pd.read_csv('data/census/raceEthnicityNeighborhood.csv')
# City income data
incomeCity = pd.read_csv('data/census/incomeCity.csv')
# Neighborhood income data
incomeNeighborhood = pd.read_csv('data/census/incomeNeighborhood.csv')

## Adds ticker annotations to figures
## in: figure, dataset, list of indices, column
## out: figure with annotations added
def addFigAnnotations(fig, data, num, column):
    
    for idx in num:
        fig.add_annotation(dict(font=dict(color = "rgb(7,13,30)", size = 11),
                               x = 1.004,
                               y = data[column][idx],
                               showarrow=False,
                               text=data['ag'][idx],
                               textangle=0,
                               xanchor='right',
                               xref='paper',
                               yref='y'))
    return fig

## Adds ticker annotations to figure frames
## in: frame, dataset, list of indices, index of frame in frame list, column
## out: frame with annotations added to layout
def addFrameAnnotations(frame, data, num, frameIndex, column):
    ## build list of annotations
    annotations = [
        go.layout.Annotation(
            dict(font=dict(color = "rgb(7,13,30)", size = 11), 
                 x = 1.004, 
                 y = data[column][idx + frameIndex * len(num)], 
                 showarrow=False, 
                 text=data['ag'][idx + frameIndex * len(num)], 
                 textangle=0, 
                 xanchor='right',
                 xref='paper',
                 yref='y')
        ) for idx in num]
    ## Add annotations list to frame layout
    frame.layout = go.Layout(annotations = annotations)
    return frame

## Function for creating plot of industry employment populations by sector
## out: figure
def plotIndustrySector():
    fig = px.bar(industryCity, 
                y="Industry", 
                x=["Private For-Profit", "Self-Employed Incorporated", 
                   "Private Not-For-Profit", "Government", 
                   "Self-Employed Not Incorporated"], 
                animation_frame="Year",
                labels={'value':cd.text['IND_X_TITLE'], 
                        'Industry':cd.text['IND_Y_TITLE']}, 
                orientation="h", custom_data=["Desc"],
                title = cd.text['IND_CITY_TITLE'])
    ## Change text displayed when mouse hovering over bar
    fig.update_traces(hovertemplate = cd.text['IND_CITY_HOVER'])
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    autosize=True,
                    font=dict(size=13, color="rgb(7,13,30)"),
                    legend_title_text=cd.text['IND_CITY_LEGEND_TITLE'],
                    legend=dict(yanchor="bottom", 
                                x=0.83, 
                                y=0, 
                                xanchor="right",
                                bgcolor="DimGray"),
                    hoverlabel_align = 'left',
                    titlefont={'size': 14},
                    title_x = 0.56)
    ## Adds (count : pct) ticker at far right of chart
    fig = addFigAnnotations(fig, industryCity, [i for i in range(13)], 'Industry')
    ## Fixed x axis size for each frame
    fig.update_xaxes(ticktext = ["0", "5", "10", "15", "20", 
                                 "25", "30", "35", "40"], 
                    tickvals = [i*5 for i in range(9)], 
                    range = [0, 45],
                    gridcolor='Black')
    #fig['layout']['updatemenus'][0]['pad']=dict(r= 0, t= 70)
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.hovertemplate = cd.text['IND_CITY_HOVER']
        f = addFrameAnnotations(f, industryCity, [i for i in range(13)], idx, 'Industry')
  
    return fig

## Function for creating age plot for the city overall
## out: figure
def plotAgeCity():
    # begin building figure
    fig = px.bar(ageCity, 
                 y="Age", 
                 x=["Male","Female"],
                 animation_frame='Year', 
                 barmode='group',
                 orientation="h",
                 title=cd.text['AGE_CITY_TITLE'], 
                 height = 600,
                 labels={'variable':cd.text['AGE_LEGEND_TITLE'], 
                         'value':cd.text['AGE_X_TITLE'],
                         'Age':cd.text['AGE_Y_TITLE']}, 
                 color_discrete_map={'Male': '#5886a5','Female': '#58a577'})
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=13, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.90, 
                                  y=0.85, 
                                  xanchor="right",
                                  bgcolor="DimGray"),
                      titlefont={'size': 14},
                      title_x = 0.555)
    ## Fixed x axis size for each frame
    fig.update_xaxes(tickvals = [i*2 for i in range(8)], 
                     range = [0, 16],
                     gridcolor='Black')
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
  
    return fig

## Function for creating race plot for the city overall
## out: figure
def plotRaceCity():
    # begin building figure
    fig = px.bar(raceCity, 
                 y="Race and Ethnicity", 
                 x="Pop",
                 animation_frame='Year',
                 orientation="h",
                 title=cd.text['RACE_CITY_TITLE'], 
                 labels={'Pop':cd.text['RACE_X_TITLE'],
                         'Race and Ethnicity':cd.text['RACE_Y_TITLE']})
    ## Fix bar order
    fig.update_yaxes(categoryorder="total ascending")
    # update layout
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=13, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.90, 
                                  y=0.85, 
                                  xanchor="right",
                                  bgcolor="DimGray"), 
                      titlefont={'size': 14},
                      title_x = 0.585)
    ## Adds (count : pct) ticker at far right of chart
    fig = addFigAnnotations(fig, raceCity, [i for i in range(8)], 'Race and Ethnicity')
    ## Fixed x axis size for each frame
    fig.update_xaxes(tickvals = [i*10 for i in range(8)], 
                     range = [0, 78],
                     gridcolor='Black')
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        f = addFrameAnnotations(f, raceCity, [i for i in range(8)], idx, 'Race and Ethnicity')

    return fig

## Function for creating income plot for the city overall
## out: figure
def plotIncomeCity():
    # begin building figure
    fig = px.bar(incomeCity, 
                 y="Bracket", 
                 x="Income",
                 animation_frame='Year',
                 orientation="h",
                 title=cd.text['INCOME_CITY_TITLE'], 
                 height=600,
                 labels={'Income':cd.text['INCOME_X_TITLE'],
                         'Bracket':cd.text['INCOME_Y_TITLE']})
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=13, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.90, 
                                  y=0.85, 
                                  xanchor="right",
                                  bgcolor="DimGray"),
                      titlefont={'size': 14},
                      title_x = 0.55)
    ## Adds (count : pct) ticker at far right of chart
    fig = addFigAnnotations(fig, incomeCity, [i for i in range(16)], 'Bracket')
    ## Fixed x axis size for each frame
    fig.update_xaxes(tickvals = [i*2 for i in range(9)], 
                     range = [0, 18],
                     gridcolor='Black')
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        f = addFrameAnnotations(f, incomeCity, 
                                [i for i in range(16)], 
                                idx, 'Bracket')

    return fig


## Function for creating plot of industry employment populations by neighborhood
## out: figure
def plotIndustryByNeighborhood(n, compare = False):
    fig = px.bar(industryNeighborhood, 
                 x=n,
                 y='Industry', 
                 labels={'value':cd.text['IND_X_TITLE'],
                         'Industry':cd.text['IND_Y_TITLE']}, 
                 animation_frame = "Year",
                 orientation="h", custom_data = ["Desc"], 
                 title = cd.text['IND_NEIGHBORHOOD_TITLE'].format(hood=n))
    ## Fix bar order
    fig.update_yaxes(categoryorder="total ascending")
    ## Change text displayed when mouse hovering over bar
    fig.update_traces(hovertemplate = cd.text['IND_NEIGHBORHOOD_HOVER'])
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15), 
                      plot_bgcolor="rgba(0,0,0,0)", 
                      paper_bgcolor="rgba(0,0,0,0)", 
                      autosize=True, 
                      font=dict(size=13, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.85, 
                                  y=0, 
                                  xanchor="right", 
                                  bgcolor="DimGray"), 
                      hoverlabel_align = 'left', 
                      titlefont={'size': 14}, 
                      title_x = 0.55)
    ## get index of neighborhood selection
    hood_index = industryNeighborhood.columns.get_loc(n)
    ## update dataset with correct ticker for neighborhood selection
    industryNeighborhood['ag'] = [f'({industryNeighborhood.iloc[i, hood_index+19]:,} : {industryNeighborhood.iloc[i, hood_index]:.2f}%)' 
                               for i in range(industryNeighborhood.shape[0])]
    ## Adds (count : pct) ticker at far right of chart
    fig = addFigAnnotations(fig, industryNeighborhood, [i for i in range(13)], 'Industry')
    if compare:
        ## Fixed x axis size for each frame
        fig.update_xaxes(ticktext = ["0", "5", "10", "15", "20", 
                                    "25", "30", "35", "40", "45", 
                                    "50", "55", "60"], 
                        tickvals = [i*5 for i in range(13)], 
                        range = [0, 76],
                        gridcolor='Black')
    else:
        ## Fixed x axis size for each frame
        fig.update_xaxes(ticktext = ["0", "5", "10", "15", "20", 
                                    "25", "30", "35", "40", "45", 
                                    "50", "55", "60"], 
                        tickvals = [i*5 for i in range(13)], 
                        range = [0, 65],
                        gridcolor='Black')
    ## move slider's and buttons' positions slightly left
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.hovertemplate = cd.text['IND_NEIGHBORHOOD_HOVER']
        f = addFrameAnnotations(f, industryNeighborhood, 
                                [i for i in range(13)], 
                                idx, 'Industry')

    return fig


## Function for creating plot of age by sex by neighborhood
## out: figure
def plotAgeNeighborhood(n):
    # begin building figure
    fig = px.bar(ageNeighborhood, 
                 y="Age", 
                 x=[n + "_M", n + "_F"],
                 animation_frame='Year', 
                 barmode='group',
                 orientation="h",
                 height = 600,
                 title=cd.text['AGE_NEIGHBORHOOD_TITLE'].format(hood=n), 
                 labels={'variable':cd.text['AGE_LEGEND_TITLE'], 
                         'value':cd.text['AGE_X_TITLE'],
                         'Age':cd.text['AGE_Y_TITLE']}, 
                 color_discrete_map={'Male': '#5886a5','Female': '#58a577'})
    # update layout
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=13, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.90, 
                                  y=0.85, 
                                  xanchor="right",
                                  bgcolor="DimGray"),
                      titlefont={'size': 14},
                      title_x = 0.56)
    ## Fixed x axis size for each frame
    fig.update_xaxes(tickvals = [i*5 for i in range(8)], 
                     range = [0, 40],
                     gridcolor='Black')
    # update legend and hovers
    newnames = {n + "_M":'Male', n + "_F":'Female'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                          legendgroup = newnames[t.name],
                                          hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
    # update legend and hovers for animated frames
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.update(name = newnames[dat.name], 
                       legendgroup = newnames[dat.name], 
                       hovertemplate = dat.hovertemplate.replace(dat.name, newnames[dat.name]))
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04

    return fig

## Function for creating race plot for the individual neighborhoods
## in: neighborhood, t/f whether the plot is for the comparison page
## out: figure
def plotRaceNeighborhood(n, compare = False):
    # begin building figure
    fig = px.bar(raceNeighborhood, 
                 y="Race and Ethnicity", 
                 x=n,
                 animation_frame='Year',
                 orientation="h",
                 title=cd.text['RACE_NEIGHBORHOOD_TITLE'].format(hood=n), 
                 labels={n:cd.text['RACE_X_TITLE'],
                         'Race and Ethnicity':cd.text['RACE_Y_TITLE']})
    ## Fix bar order
    fig.update_yaxes(categoryorder="total ascending")
    # update layout
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=13, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.90, 
                                  y=0.85, 
                                  xanchor="right",
                                  bgcolor="DimGray"),
                      titlefont={'size': 14},
                      title_x = 0.59)
    ## get index of neighborhood selection
    hood_index = raceNeighborhood.columns.get_loc(n)
    ## update dataset with correct ticker for neighborhood selection
    raceNeighborhood['ag'] = [f'({raceNeighborhood.iloc[i, hood_index+19]:,} : {raceNeighborhood.iloc[i, hood_index]:.2f}%)' 
                               for i in range(raceNeighborhood.shape[0])]
    ## Adds (count : pct) ticker at far right of chart
    fig = addFigAnnotations(fig, raceNeighborhood, [i for i in range(8)], 'Race and Ethnicity')
    if compare:
        ## Fixed x axis size for each frame
        fig.update_xaxes(tickvals = [i*10 for i in range(10)], 
                        range = [0, 122],
                        gridcolor='Black')
    else:
        ## Fixed x axis size for each frame
        fig.update_xaxes(tickvals = [i*10 for i in range(11)], 
                        range = [0, 109],
                        gridcolor='Black')
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        f = addFrameAnnotations(f, raceNeighborhood, 
                                [i for i in range(8)], 
                                idx, 'Race and Ethnicity')

    return fig

## Function for creating income plot for the individual neighborhoods
## in: neighborhood, t/f whether the plot is for the comparison page
## out: figure
def plotIncomeNeighborhood(n, compare = False):
    # begin building figure
    fig = px.bar(incomeNeighborhood, 
                 y="Bracket", 
                 x=n,
                 animation_frame='Year',
                 orientation="h",
                 title=cd.text['INCOME_NEIGHBORHOOD_TITLE'].format(hood=n), 
                 height=600,
                 labels={n:cd.text['INCOME_X_TITLE'],
                         'Race':cd.text['INCOME_Y_TITLE']})
    # update layout
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=13, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.90, 
                                  y=0.85, 
                                  xanchor="right",
                                  bgcolor="DimGray"),
                      titlefont={'size': 14},
                      title_x = 0.555)
    ## get index of neighborhood selection
    hood_index = incomeNeighborhood.columns.get_loc(n)
    ## update dataset with correct ticker for neighborhood selection
    incomeNeighborhood['ag'] = [f'({incomeNeighborhood.iloc[i, hood_index+19]:,} : {incomeNeighborhood.iloc[i, hood_index]:.2f}%)' 
                               for i in range(incomeNeighborhood.shape[0])]
    ## Adds (count : pct) ticker at far right of chart
    fig = addFigAnnotations(fig, incomeNeighborhood, [i for i in range(16)], 'Bracket')
    if compare:
        ## Fixed x axis size for each frame
        fig.update_xaxes(tickvals = [i*5 for i in range(8)], 
                        range = [0, 43],
                        gridcolor='Black')
    else:
        ## Fixed x axis size for each frame
        fig.update_xaxes(tickvals = [i*5 for i in range(8)], 
                        range = [0, 40],
                        gridcolor='Black')
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        f = addFrameAnnotations(f, incomeNeighborhood, 
                                [i for i in range(16)], 
                                idx, 'Bracket')
    
    return fig
