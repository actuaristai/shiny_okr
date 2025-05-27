"""Shiny app for OKR template."""
from chatlas import ChatOpenAI
from markdown import markdown
from shiny.express import input, render, ui  # noqa: A004

from .conf.config import conf

chat = ChatOpenAI(model='gpt-4o-mini',
                  system_prompt="""
                                 You are an experienced OKR practitioner and coach, providing encouraging and
                                 constructive feedback to clients on best practices for writing OKRs based on the
                                 Measure What Matters book.
                                 """,
                  api_key=conf['OPENAI_API_KEY'])
ui.input_text(id='Objective',
              label='Practice writing your own Objective',
              placeholder=' Increase customer engagement on our social media platform',
              update_on='blur')
'Feedback:'


@render.ui
def feedback_output() -> ui.HTML:
    """Render the feedback output."""
    feedback = chat.chat(f'Provide feedback on the following objective: {input.Objective()}')
    # Convert the feedback to markdown
    markdown_feedback = markdown(feedback.content)
    return ui.HTML(markdown_feedback)
