from fasthtml.common import *
from datetime import datetime

from df_assembly import DataFrameAssembly

import plotly.express as px
from fh_plotly import plotly2fasthtml, plotly_headers


# Globals
# global_conf_ten_minutes = True
global_conf_ten_minutes = False
global_conf_table = False
global_conf_pulses = False

# hdrs = (picolink, Script(src='https://cdn.tailwindcss.com'), plotly_headers)
pico_colors = Link(rel="stylesheet", href='https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.colors.min.css')
hdrs = (picolink, plotly_headers,pico_colors,)

# hdrs = (plotly_headers)
app,rt = fast_app(hdrs=hdrs)


def generate_line_chart(my_df,xdef='Date and Time',ydef='Pulses'):
    fig = px.line(my_df, x=xdef, y=ydef)
    return plotly2fasthtml(fig)


def generate_bar_chart(my_df,xdef='Date and Time',ydef='Pulses'):
    fig = px.bar(my_df, x=xdef, y=ydef)
    return plotly2fasthtml(fig)


def nav_div():
    if global_conf_pulses == True:
        b1 =  Button(' In Pulses ', cls='outline secondary')
        b2 =  Button('In Gallons ', cls='secondary',
                     hx_post="/config_units", hx_target='#my_nav_div', hx_swap="innerHTML")        
    else:
        b1 =  Button(' In Pulses ', cls='secondary',
                     hx_post="/config_units", hx_target='#my_nav_div', hx_swap="innerHTML")
        b2 =  Button('In Gallons ', cls='outline secondary')

    if global_conf_table == True:
        b3 =  Button(' Get Table ', cls='outline secondary')
        b4 =  Button(' Get Graph ', cls='secondary',
                     hx_post="/config_table", hx_target='#my_nav_div', hx_swap="innerHTML")        
    else:
        b3 =  Button(' Get Table ', cls='secondary',
                     hx_post="/config_table", hx_target='#my_nav_div', hx_swap="innerHTML")
        b4 =  Button(' Get Graph ', cls='outline secondary')
        
    if global_conf_ten_minutes == True:
        b5 =  Button('By Ten Mins', cls='outline secondary')
        b6 =  Button(' By Hours  ', cls='secondary',
                     hx_post="/config_ten_min", hx_target='#my_nav_div', hx_swap="innerHTML")        
    else:
        b5 =  Button('By Ten Mins', cls='secondary',
                     hx_post="/config_ten_min", hx_target='#my_nav_div', hx_swap="innerHTML")
        b6 =  Button(' By Hours  ', cls='outline secondary')
        
    return Div(
        Nav(
            Ul(Li(H4('Units:'))),
            Ul(Li(b1)),
            Ul(Li(b2))),
        Nav(
            Ul(Li(H4('Data Presented:'))),
            Ul(Li(b3)),
            Ul(Li(b4))),
        Nav(
            Ul(Li(H4('Data Spaced:'))),
            Ul(Li(b5)),
            Ul(Li(b6))))


def button_my_nav_div (btn_name, btn_link, btn_state):
    btn_cls = 'secondary'
    if btn_state == True:
        btn_cls = 'outline secondary'
    return Button (btn_name, cls=btn_cls, hx_post=btn_link, hx_target='#my_nav_div', hx_swap="innerHTML")

        # Button("Pulses", style="color: #005fff; background-color:Tomato;"),
        # Div(H3("Prueba Color Pico"),
        #     style="text-align: center; color: #005fff; border: 3px solid green; padding: 10px 0;"),

def nav_div_grid():
    b1 = button_my_nav_div ('Pulses', '/config_units/pulses', global_conf_pulses)
    b2 = button_my_nav_div ('Gallons', '/config_units/gallons', not global_conf_pulses)

    b3 = button_my_nav_div ('Table', '/config_table/table', global_conf_table)
    b4 = button_my_nav_div ('Graphs', '/config_table/graph', not global_conf_table)

    b5 = button_my_nav_div ('Ten Mins', '/config_ten_min/ten_mins', global_conf_ten_minutes)
    b6 = button_my_nav_div ('Hours', '/config_ten_min/hours', not global_conf_ten_minutes)
        
    return Div(Div(H3("Units:"), b1, b2, cls='grid'),
               Div(H3()),
               Div(H3("Data Presentation:"), b3, b4, cls='grid'),
               Div(H3()),
               Div(H3("Data Spaced:"), b5, b6, cls='grid'),
               Div(H3()),
               )


@rt("/")
def get():
    date_now = datetime.today()
    today = date_now.strftime("%Y-%m-%d")
    return Titled(('Tcp-Water'),
                  Div(Div(nav_div_grid(),id="my_nav_div"),
                      H2('Pick dates:'),
                      Form(Input(name="start_date", type="date", value='2025-01-01'),
                           Input(name="end_date", type="date", value=today),
                           Div(Button("Submit", type="submit",
                                      hx_post="/load_table", hx_target="#my_table", hx_swap="innerHTML"),
                               hx_get="/progress", hx_target="#my_table"),
                           Div(id="my_table"))),
                  )

    # return Titled(('Tcp-Water'),
    #               Div(Div(nav_div(),id="my_nav_div"),
    #                   H2('Pick dates:'),
    #                   Form(Input(name="start_date", type="date", value='2025-01-01'),
    #                        Input(name="end_date", type="date", value=today),
    #                        Div(Button("Submit", type="submit",
    #                                   hx_post="/load_table", hx_target="#my_table", hx_swap="innerHTML"),
    #                            hx_get="/progress",hx_target="#spinner"),
    #                   Div(id="spinner"),
    #                   Div(id="my_table"))))

    # progress test
    # return Titled(('Tcp-Water'),
    #               Div(Div(nav_div(),id="my_nav_div"),
    #                   H2('Pick dates:'),
    #                   Form(Input(name="start_date", type="date", value='2025-01-01'),
    #                        Input(name="end_date", type="date", value=today),
    #                        Button("Submit", type="submit",
    #                               hx_post="/load_table", hx_target="#my_table", hx_swap="innerHTML")),
    #                   Div(id="my_table"),
    #                   Div(Progress())))


@rt("/load_table")
def post(start_date: str, end_date: str):
    df_err, df = DataFrameAssembly(start_date, end_date, global_conf_ten_minutes)
    if df is None:
        df_data = 'Some error while looking data: ' + df_err
        resp = Div(P('from: ' + start_date + ' to: ' + end_date),
                   Div(df_data))

    else:

        if global_conf_pulses == False:
            # convert pulses to gallons
            df[1] = df[1].multiply(2.64172)
            df.columns = ['Date and Time', 'Gallons']
            total_df_sum = df['Gallons'].sum()
            total_df_sum_str = "Total Gallons between dates: {0:.1f}".format(total_df_sum)
            y_chart = 'Gallons'
        else:
            df.columns = ['Date and Time', 'Pulses']
            total_df_sum_str = 'Total Pulses between dates: ' + str(df['Pulses'].sum())
            y_chart = 'Pulses'

        # df_data = NotStr(df.to_html(header=False,index=False))
        df_data = NotStr(df.to_html(index=False))        

        if global_conf_table == True:
            resp = Div(H3('Table:'),
                       P('from: ' + start_date + ' to: ' + end_date),
                       Div(df_data),
                       H1(total_df_sum_str))
        else:
            resp = Div(H3('Graphs:'),
                       Div(Strong("Plot 1: Line Chart"),
                           Div(generate_line_chart(df,ydef=y_chart)),),
                       Div(Strong("Plot 2: Bar Chart"),
                           Div(generate_bar_chart(df,ydef=y_chart)),))
    
    return resp


@rt("/config_table/{conf}")
def post(conf: str):
    global global_conf_table
    if conf == 'table':
        global_conf_table = True
    else:
        global_conf_table = False
        
    return Div(nav_div_grid())


@rt("/config_ten_min/{conf}")
def post(conf: str):
    global global_conf_ten_minutes
    if conf == 'ten_mins':
        global_conf_ten_minutes = True
    else:
        global_conf_ten_minutes = False

    return Div(nav_div_grid())


@rt("/config_units/{conf}")
def post(conf: str):
    global global_conf_pulses
    if conf == 'pulses':
        global_conf_pulses = True
    else:
        global_conf_pulses = False
        
    return Div(nav_div_grid())


@rt("/progress")
def get():
        
    return Div(Progress())


# @rt("/favicon.ico")
# def get():
#     print("---try to get")
#     return FileResponse('./static/favicon2.ico')

# @rt("/{fname:path}.{ext:static}")
# def static(fname: str, ext: str):
#     print("---try to get")
#     return FileResponse(f'{fname}.{ext}')


@rt("/{fname:path}.{ext:static}")
def get(fname: str, ext: str):
    return FileResponse('./static/' + f'{fname}.{ext}')


serve(port=5000)
