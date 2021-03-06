# ------------------City page------------------#
import numpy as np
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, callback
import srcCode.propertyFuncs as pf
import srcCode.affordDescs as ad
import srcCode.toolbarDescs as tb
import srcCode.dashFuncs as df
import srcCode.cityDescs as cd
import srcCode.censusFuncs as cf
import srcCode.historyFuncs as hf
# ----------------------------------------------------------------------------
# Helper functions
def nanformat(n, strcode):
    if not n:
        return "Not available"
    elif np.isnan(n):
        return "Not available"
    else:
        return strcode % n
# ----------------------------------------------------------------------------
# All the texts
## History
history_title = "History of Real Estate Sales"
history_zoning_title = "By Zoning"
history_zoning_checklist_single = "Single family"
history_zoning_checklist_two = "Two family"
history_zoning_checklist_multi = "Multi family and others"
HIST_NEIGHBORHOOD_TITLE = 'History of Residential Sales by'

## footnote
source = '''Prices have been adjusted for inflation. Only sales with state code Residential 
(urban/suburban) and Multifamily are included.'''
# ----------------------------------------------------------------------------
# Building dash
year = np.arange(1945, 2021, 1, dtype=int)

layout = html.Div(
    [
        # Sidebar
        df.createTopBar(),
        html.Br(),
        # Affordability
        html.Div(
            [
                dcc.Graph(id="afford_map", 
                          figure=pf.plotAffordMap("Neighborhood", 2020),
                          config={'displayModeBar': True,
                                  "displaylogo": False,
                                  'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                             'lasso2d', 'toImage']},
                          style={"width": "100%", "height": "550px"}),
                html.Div([
                    html.Div([
                        dcc.Slider(min=1945, max=2021, step=1, value=2020, 
                                   tooltip={"placement": "bottom", "always_visible": True},
                                   marks={1945: "1945", 1950: "", 1955: "1955", 1960: "", 1965: "1965", 1970: "",
                                          1975: "1975", 1980: "", 1985: "1985", 1990: "", 1995: "1995", 2000: "",
                                          2005: "2005", 2010: "", 2015: "2015", 2020: "2020"},
                                   id="afford_slider_year")
                    ], style={"width": "100%"}),
                # Level of detail dropdown
                df.createDropdown(ad.text['DD_LOD'], ad.opts['DD_LOD'],
                                  ad.default['DD_LOD'], dd_id="afford_dropdown_lod", 
                                  dd_style={"width": "200px"}, clearable=False, searchable = False),
                ], className="grid_container", style={"grid-template-columns": "minmax(600px, 4fr) 2fr"}),
            ], className="subcontainer"),
        html.Hr(className="center_text title"),
        html.Br(),
        # Census charts
        html.Div([
            df.createLeftAlignDropdown(cd.text['DROPDOWN_CENSUS'], cd.opts['DROPDOWN_CENSUS'],
                            cd.default['DROPDOWN_CENSUS'], dd_id='dropdown_city_census',
                            dd_style={'width': '170px'}, grid_class="grid_dd2",
                            clearable=False, searchable=False),
        ], className = "subcontainer"),
        html.Div(
            [
                # dropdown for census selection
                #df.createDropdown(cd.text['DROPDOWN_CENSUS'], cd.opts['DROPDOWN_CENSUS'],
                #                  cd.default['DROPDOWN_CENSUS'], dd_id="dropdown_city_census",
                #                  dd_style={"width": "200px"}, 
                #                  clearable=False, searchable = False),
                dcc.Graph(id='census_city_plot', 
                          figure=cf.plotIndustrySector(),
                          config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']},
                          style={'display': 'block'})
            ], className="subcontainer"),
        html.Br(),
        html.Hr(className="center_text title"),
        html.Br(),
        # History of price
        html.Div([
            df.createLeftAlignDropdown(HIST_NEIGHBORHOOD_TITLE, cd.opts['DROPDOWN_HISTORY'],
                            cd.default['DROPDOWN_HISTORY'], dd_id='dropdown_city_history',
                            dd_style={'width': '150px'}, grid_class="grid_dd2",
                            clearable=False, searchable=False),
        ], className = "subcontainer"),
        html.Div(
            [
                dcc.Graph(id='history_price_city_plot', 
                          figure=hf.plotCityHistoryPrice(),
                          style={"width": "100%"}, 
                          config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']}),
                dcc.Graph(id='history_quant_city_plot', 
                          figure=hf.plotCityHistoryQuantity(),
                          style={"width": "100%"}, 
                          config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']}),
            ], className="subcontainer"),
        html.Br(),
        # Disclaimers
        html.Div([dcc.Markdown(children=source)], className="subcontainer left_text bodytext"),
        #dcc.Link('Take me back up', href='#', className = "subcontainer links_text"),
    ], className="container background")

@callback(
    Output('census_city_plot', 'figure'),
    Input('dropdown_city_census', 'value'))
def update_census_city_plot(censusSelection):
    if censusSelection == cd.opts['DROPDOWN_CENSUS'][0]:
        return cf.plotAgeCity()
    elif censusSelection == cd.opts['DROPDOWN_CENSUS'][1]:
        return cf.plotIncomeCity()
    elif censusSelection == cd.opts['DROPDOWN_CENSUS'][2]:
        return cf.plotIndustrySector()
    else:
        return cf.plotRaceCity()

@callback(
    Output('history_price_city_plot', 'style'),
    Output('history_quant_city_plot', 'style'),
    Input('dropdown_city_history', 'value'))
def update_history_city_plot(historySelection):
    if historySelection == cd.opts['DROPDOWN_HISTORY'][0]:
        return ({'display': 'block', "width": "100%"}, 
                {'display': 'none'})
    else:
        return ({'display': 'none'}, 
                {'display': 'block', "width": "100%"})
    

# Update affordability graph
@callback(Output("afford_map", "figure"),
          [Input("afford_dropdown_lod", "value"), 
          Input("afford_slider_year", "value")])
def update_afford_map(lod, y):
    return pf.plotAffordMap(lod, y)
