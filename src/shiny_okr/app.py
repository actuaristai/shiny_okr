"""Shiny app for OKR template."""
import requests  # For making HTTP requests to the new API
from markdown import markdown
from shiny.express import input, render, ui  # noqa: A004

API_URL = 'https://openai-fastapi-786665877452.us-central1.run.app/okr'

ui.input_text(id='Objective',
              label='Practice writing your own Objective',
              placeholder='Increase customer engagement on our social media platform',
              update_on='blur')
ui.input_text(id='Key_result1',
              label='Practice writing your own key result (1)',
              placeholder='Achieve a 20 percent increase in average likes per post by the end of Q1.',
              update_on='blur')
ui.input_text(id='Key_result2',
              label='Practice writing your own key result (2)',
              placeholder='Increase the number of followers by 15 percent by the end of Q1.',
              update_on='blur')
ui.input_text(id='Key_result3',
              label='Practice writing your own key result (3)',
              placeholder='Improve the click-through rate (CTR) on our social media ads by 10 percent.',
              update_on='blur')
ui.input_text(id='Key_result4',
              label='Practice writing your own key result (4)',
              placeholder='',
              update_on='blur')
ui.input_text(id='Key_result5',
              label='Practice writing your own key result (5)',
              placeholder='',
              update_on='blur')

ui.input_action_button(id='get_feedback_btn',
                       label='Get Feedback',
                       class_='btn-primary')


@render.ui
def feedback_output() -> ui.HTML:
    """Render the feedback output when the button is clicked, using the new API."""
    # Take a reactive dependency on the button.
    input.get_feedback_btn()

    # Only generate feedback if the button has been clicked.
    if input.get_feedback_btn() > 0:
        objective = input.Objective()
        key_results = [
            input.Key_result1(),
            input.Key_result2(),
            input.Key_result3(),
            input.Key_result4(),
            input.Key_result5(),
        ]
        filled_key_results = [kr for kr in key_results if kr]

        if not objective or len(filled_key_results) < 3:  # noqa: PLR2004
            return ui.HTML('<p style="color: red;">Please fill in the Objective and at least 3 Key Results.</p>')

        okr_input = {'objective': objective,
                     'key_result1': key_results[0],
                     'key_result2': key_results[1],
                     'key_result3': key_results[2],
                     'key_result4': key_results[3],
                     'key_result5': key_results[4]}

        try:
            # Make the API call
            response = requests.post(API_URL, json=okr_input, timeout=30)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

            api_response_data = response.json()

            # Assuming the API returns JSON like: {"response": "feedback text"}
            # Adjust "response" key if your API uses a different one (e.g., "output", "feedback")
            feedback_from_api = api_response_data.get('response')

            if feedback_from_api:
                html_feedback = markdown(feedback_from_api)
                return ui.HTML(html_feedback)
            return ui.HTML('<p>Received an empty response or unexpected format from the API.</p>')

        except requests.exceptions.RequestException as e:
            return ui.HTML(f'<p>Error connecting to the feedback API: {e!s}</p>')
        except Exception as e:  # noqa: BLE001
            return ui.HTML(f'<p>An unexpected error occurred: {e!s}</p>')
    else:
        # Initial state before the button is clicked
        return ui.HTML("<p>Enter your OKRs and click 'Get Feedback' for an analysis.</p>")
