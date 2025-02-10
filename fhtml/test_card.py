from fasthtml.common import *

hdrs = (picolink, Script(src='https://cdn.tailwindcss.com'))
app,rt = fast_app(hdrs=hdrs)

def Card(title, description, content, action_text="Action", width="350px"):
    return Div(
        Div(
            H2(title, cls="text-xl font-bold text-grey-800"),
            P(description, cls="text-sm text-gray-600 mt-1"),
            cls="bg-gray-100 p-6"
        ),
        Div(
            P(content, cls="text-gray-700"),
            cls="p-6"
        ),
        Div(
            Button(
                action_text,
                cls="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            ),
            cls="bg-gray-100 p-6"
        ),
        cls=f"w-[{width}] bg-white rounded-lg shadow-lg overflow-hidden"
    )

# Usage example:
@rt("/")
def get():
    return Titled("Card Example",
        Card("My Card", "This is a sample card", "Here's some content for the card.")
    )

serve(port=5000)
