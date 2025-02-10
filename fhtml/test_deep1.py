from fasthtml.common import *
from dataclasses import dataclass

# Server-side state
@dataclass
class ButtonState:
    groups = {
        1: "Table",
        2: "Minutes",
        3: "Liters"
    }

def get_button_class(group_num, button_name):
    return "btn-enabled" if ButtonState.groups[group_num] == button_name else "btn-disabled"

def button_group(group_num, names):
    return Div(
        Button(
            names[0],
            Class=f"{get_button_class(group_num, names[0])} toggle-btn",
            hx_post="/toggle",
            hx_trigger="click",
            hx_vals={'group': group_num, 'button': names[0]},
            hx_target=f"#group{group_num}"
        ),
        Button(
            names[1],
            Class=f"{get_button_class(group_num, names[1])} toggle-btn",
            hx_post="/toggle",
            hx_trigger="click",
            hx_vals={'group': group_num, 'button': names[1]},
            hx_target=f"#group{group_num}"
        ),
        cls="button-group",
        id=f"group{group_num}"
    )

# def button_group(group_num, names):
#     return Div(
#         Button(
#             names[0],
#             Class=f"{get_button_class(group_num, names[0])} flex-item",
#             hx_post="/toggle",
#             hx_trigger="click",
#             hx_vals={'group': group_num, 'button': names[0]},
#             hx_target=f"#group{group_num}"
#         ),
#         Button(
#             names[1],
#             Class=f"{get_button_class(group_num, names[1])} flex-item",
#             hx_post="/toggle",
#             hx_trigger="click",
#             hx_vals={'group': group_num, 'button': names[1]},
#             hx_target=f"#group{group_num}"
#         ),
#         Class="button-group flex-container",
#         id=f"group{group_num}"
#     )

# # Server-side state
# @dataclass
# class ButtonState:
#     groups = {
#         1: "Table",
#         2: "Minutes",
#         3: "Liters"
#     }

# def get_button_class(group_num, button_name):
#     return "btn-enabled" if ButtonState.groups[group_num] == button_name else "btn-disabled"

# def button_group(group_num, names):
#     return Div(
#         Button(
#             names[0],
#             Class=get_button_class(group_num, names[0]),
#             hx_post="/toggle",
#             hx_trigger="click",
#             hx_vals={'group': group_num, 'button': names[0]},
#             hx_target=f"#group{group_num}"
#         ),
#         Button(
#             names[1],
#             Class=get_button_class(group_num, names[1]),
#             hx_post="/toggle",
#             hx_trigger="click",
#             hx_vals={'group': group_num, 'button': names[1]},
#             hx_target=f"#group{group_num}"
#         ),
#         Class="button-group",
#         id=f"group{group_num}"
#     )

app = FastHTML()

@app.route("/", methods="GET")
def index():
    return Html(
        Head(
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css"),
            Script(src="https://unpkg.com/htmx.org@1.9.10"),
            Style("""
                .btn-enabled { 
                    background-color: #4CAF50 !important;
                    border-color: #4CAF50 !important;
                }
                .btn-disabled { 
                    background-color: #e0e0e0 !important;
                    border-color: #e0e0e0 !important;
                }
                .button-group {
                    display: grid;
                    grid-template-columns: repeat(2, minmax(120px, 1fr));
                    gap: 0.5rem;
                    margin: 1rem 0;
                }
                .toggle-btn {
                    min-width: 120px;
                    padding: 0.75rem 0.5rem;
                    transition: all 0.3s ease !important;
                    text-align: center;
                    border-radius: 4px;
                    box-sizing: border-box;
                    white-space: nowrap;
                    font-size: 0.9rem;
                    font-weight: 500;
                }
                button {
                    margin: 0;
                    cursor: pointer;
                }
            """)
        ),
        Body(
            Div(
                button_group(1, ("Table", "Graph")),
                button_group(2, ("Minutes", "Hours")),
                button_group(3, ("Liters", "Gallons")),
                cls="container"
            )
        )
    )

# @app.route("/", methods="GET")
# def index():
#     return Html(
#         Head(
#             Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css"),
#             Script(src="https://unpkg.com/htmx.org@1.9.10"),
#             Style("""
#             .btn-enabled { background-color: #4CAF50 !important; }
#             .btn-disabled { background-color: #e0e0e0 !important; }
#             .button-group { 
#             display: grid;
#             grid-template-columns: 1fr 1fr;
#             gap: 0.5rem;
#             margin: 1rem 0;
#             }
#             .toggle-btn {
#             width: 100%;
#             padding: 0.75rem;
#             transition: all 0.3s;
#             text-align: center;
#             border-radius: 4px;
#             box-sizing: border-box;
#             }
#             button {
#             margin: 0;
#             white-space: nowrap;
#             }
#             """)
#             # Style("""
#             #     .btn-enabled { background-color: #4CAF50; }
#             #     .btn-disabled { background-color: #e0e0e0; }
#             #     .button-group { 
#             #         margin: 1rem 0;
#             #         gap: 0.5rem;
#             #     }
#             #     .flex-container {
#             #         display: flex;
#             #         justify-content: space-between;
#             #     }
#             #     .flex-item {
#             #         flex: 1;
#             #         text-align: center;
#             #         padding: 0.75rem;
#             #         transition: all 0.3s;
#             #     }
#             #     button { 
#             #         margin: 0;
#             #         border-radius: 4px;
#             #     }
#             # """)
#         ),
#         Body(
#             Div(
#                 button_group(1, ("Table", "Graph")),
#                 button_group(2, ("Minutes", "Hours")),
#                 button_group(3, ("Liters", "Gallons")),
#                 Class="container"
#             )
#         )
#     )


# @app.route("/", methods="GET")
# def index():
#     return Html(
#         Head(
#             Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css"),
#             Script(src="https://unpkg.com/htmx.org@1.9.10"),
#             Style("""
#                 .btn-enabled { background-color: #4CAF50; }
#                 .btn-disabled { background-color: #e0e0e0; }
#                 .button-group { margin: 1rem 0; }
#                 button { margin: 0 0.5rem; transition: all 0.3s; }
#             """)
#         ),
#         Body(
#             Div(
#                 button_group(1, ("Table", "Graph")),
#                 button_group(2, ("Minutes", "Hours")),
#                 button_group(3, ("Liters", "Gallons")),
#                 Class="container"
#             )
#         )
#     )

@app.route("/toggle", methods="POST")
def toggle_group(group: str, button: str):
    # group_num = int(request.form['group'])
    # button_name = request.form['button']
    group_num = int(group)
    button_name = button
    ButtonState.groups[group_num] = button_name
    return button_group(group_num, 
        ("Table", "Graph") if group_num == 1 else
        ("Minutes", "Hours") if group_num == 2 else
        ("Liters", "Gallons"))

serve(port=5000)





# Keep the same /toggle endpoint and server logic
