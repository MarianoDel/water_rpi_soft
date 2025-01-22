from fasthtml.common import *
from datetime import datetime

from df_assembly import DataFrameAssembly

# Globals
# global_conf_ten_minutes = True
global_conf_ten_minutes = False

app,rt = fast_app()

# @rt('/')
# def get(): return Div(P('Hello World!'), hx_get="/form_input")
# # def get(): return Div(P('Hello World!'), hx_get="/change")

@rt('/change')
def get(): return P('Nice to be here!')

# @rt('/form_input')
# def form_input():
#     date_now = datetime.today()
#     today = date_now.strftime("%Y-%m-%d")
#     return Titled('My new input',
#                   Div(
#                       H2('Last day'),
#                       Div(Input(type='date', value='2024-01-01'),id="page-content",hx_post="/date_pick1"),
#                       H2('Today:'),
#                       Div(Input(type='date', value=today))))

#hx_post="/increment", hx_target="#count", hx_swap="innerHTML")

@rt('/date_pick1')
def post():
    print("en date_pick1")
    return P('something change')


@rt("/")
def get():
    date_now = datetime.today()
    today = date_now.strftime("%Y-%m-%d")
    return Div(H2('Pick dates:'),
               Form(Input(name="start_date", type="date", value='2024-01-01'),
                    Input(name="end_date", type="date", value=today),
                    Button("Submit", type="submit", hx_post="/load_table", hx_target="#my_table", hx_swap="innerHTML")),
               H3('Table:'),
               Div(id="my_table"))

@rt("/load_table")
def post(start_date: str, end_date: str):
    df_err, df = DataFrameAssembly(start_date, end_date, global_conf_ten_minutes)
    if df is None:
        df_data = 'Some error while looking data: ' + df_err
    else:
        df.columns = ['Date and Time', 'Pulses']
        # df_data = NotStr(df.to_html(header=False,index=False))
        df_data = NotStr(df.to_html(index=False))        
    
    return Div(P('from: ' + start_date + ' to: ' + end_date),
               Div(df_data))

serve()
