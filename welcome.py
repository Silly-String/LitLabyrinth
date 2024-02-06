"""CSC111 Winter 2024: Welcome File

Welcome to CSC111! This is a sample Python file that you should be able to
run after you have completed the steps in the Software Setup guide on our
First-Year Computer Science Summer Prep modules (https://q.utoronto.ca/courses/160038/).

To run this file in PyCharm, go to Run -> Run... and select 'welcome' in the popup menu.
After you've run this program for the first time, you'll be able to re-run it
easily by pressing the green ▶ arrow in the toolbar on the top-right of your window.
"""
# Check that you can import every library in requirements.txt
import pytest
import python_ta
import plotly.graph_objects as go
import pygame

from hypothesis import given
from hypothesis.strategies import integers


def test_pygame() -> None:
    """Check if pygame can be initialized."""
    num_pass, num_fail = pygame.init()

    assert num_pass > 0, "None of pygame's imported modules could be initialized"
    assert num_fail == 0, "At least one of pygame's imported modules could not be initialized"


@given(x=integers())
def test_hypothesis(x: int) -> None:
    """Check if hypothesis is working."""
    assert isinstance(x, int)


def test_python_ta_version() -> None:
    """Check that you have the correct version of PythonTA installed"""
    version_str = python_ta.__version__
    assert version_str.startswith('2.7.')


def try_plotly() -> None:
    """Check if you can generate a plot with plotly."""
    # Convert the outputs into parallel x and y lists
    x_data, y_data = [1, 2, 3], [10, 8, 12]

    # Create the figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data))

    # Configure the figure
    fig.update_layout(title='A Scatter Plot',
                      xaxis_title='An x-axis',
                      yaxis_title='A y-axis')

    # Show the figure in the browser
    fig.show()
    # Is the above not working for you? Comment it out, and uncomment the following:
    # fig.write_html('my_figure.html')
    # You will need to manually open the my_figure.html file created above.


if __name__ == '__main__':
    python_ta.check_all(config={
        'extra-imports': ['plotly.graph_objects', 'pygame', 'hypothesis.strategies'],
        'max-line-length': 120,
        'disable': ['E1101']
    })

    try_plotly()

    pytest.main(['welcome.py'])
