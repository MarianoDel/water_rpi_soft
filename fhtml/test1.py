from fasthtml.common import *
from datetime import datetime


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
    return P(start_date, end_date)

serve()
