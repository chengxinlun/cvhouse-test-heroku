# ------------------Neighborhood page------------------#
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import srcCode.toolbarDescs as tb
import srcCode.resourcesDescs as rd
import srcCode.dashFuncs as df


layout = html.Div(
    [
        # Sidebar
        dbc.Navbar([
            # dbc.Button("☰", id='rsrc_sidebar_button', className="background2 left_text title", 
            #            style={"margin-left": "0"}),
            # dbc.Collapse(
            #     [
            #         dbc.NavItem(dbc.NavLink(tb.opts['TOP'], href="#", external_link=True, 
            #                                 className="background2 left_text subtitle")),
            #     ], id="rsrc_sidebar", is_open=False, 
            #     style={"width": "400px", "margin-left": "0", "position": "fixed", "top": "80px"}, className="background"),
            df.createTopBar()
        ], className="sidebar", color="#132C36"),
        html.Div(
        [
                html.H3(rd.text['MAIN_TITLE'], className = "center_text title"),
                html.Br(),
                html.Span(rd.text['SOURCES_HOOD'], className="left_text bodytext"), 
                html.Span(rd.text['THANKS'], className="left_text bodytext"), 
                df.createArrowLink(rd.text['THANKSLINK'], rd.links['THANKS']),
                # C-VILLE Weekly links
                html.Span(rd.text["CVILLE_WEEKLY"], className="left_text bodytext"),
                df.createArrowLink(rd.text['CVILLE_1'], rd.links['CVILLE_1']),
                df.createArrowLink(rd.text['CVILLE_2'], rd.links['CVILLE_2']),
                df.createArrowLink(rd.text['CVILLE_3'], rd.links['CVILLE_3']),
                df.createArrowLink(rd.text['CVILLE_4'], rd.links['CVILLE_4']),
                # Cvillepedia
                html.Span(rd.text["CVILLEPEDIA"], className="left_text bodytext"),
                df.createArrowLink(rd.text['CVP'], rd.links['CVP']),
                # CvilleTomorrow links
                html.Span(rd.text["CVILLETOMORROW"], className="left_text bodytext"),
                df.createArrowLink(rd.text['CVT_1'], rd.links['CVT_1']),
                df.createArrowLink(rd.text['CVT_2'], rd.links['CVT_2']),
                html.Br(),
                html.Br(),
                # affordability links
                html.Span(rd.text["AFFORD"], className="left_text bodytext"),
                df.createArrowLink(rd.text['METHODS'], rd.links['METHODS']),
                html.Br(),
                html.Br(),
                html.Span(rd.text["CENSUS"], className="left_text bodytext"),
                df.createArrowLink(rd.text['SEXBYAGE'], rd.links['SEXBYAGE']),
                df.createArrowLink(rd.text['INCOME'], rd.links['INCOME']),
                df.createArrowLink(rd.text['INDUSTRY'], rd.links['INDUSTRY']),
                df.createArrowLink(rd.text['RACE'], rd.links['RACE']),
                html.Br(),
                html.Br(),
                html.Span(rd.text["SALES"], className="left_text bodytext"),
                df.createArrowLink(rd.text['HISTORY'], rd.links['HISTORY']),
                html.Br(),
                html.Br(),
                html.Span(rd.text["QOL_MAP"], className="left_text bodytext"),
                df.createArrowLink(rd.text['TRANSPORT'], rd.links['TRANSPORT']),
                df.createArrowLink(rd.text['OPENST'], rd.links['OPENST']),
                html.Br(),
                #dcc.Link('Take me back up', href='#', className = "left_text links_text"),
        ], className = "subcontainer")
    ], className = "container background")

# Collapsable sidebar
# @callback(Output("rsrc_sidebar", "is_open"),
#           [Input("rsrc_sidebar_button", "n_clicks"), State("rsrc_sidebar", "is_open")])
# def hood_sidebar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open

