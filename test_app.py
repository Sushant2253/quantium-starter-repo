import pytest
from dash.testing.application_runners import import_app

@pytest.fixture
def app():
    return import_app("app")  

def test_header_is_present(dash_duo, app):
    dash_duo.start_server(app)
    header = dash_duo.find_element("h1")  
    assert header is not None, "Header is missing!"
    assert header.text.strip() != "", "Header text is empty!"

def test_visualization_is_present(dash_duo, app):
    dash_duo.start_server(app)
    graph = dash_duo.find_element(".dash-graph") 
    assert graph is not None, "Visualization (line chart) is missing!"

def test_region_picker_is_present(dash_duo, app):
    dash_duo.start_server(app)
    region_picker = dash_duo.find_element(".dash-radio-items")  
    assert region_picker is not None, "Region picker (radio buttons) is missing!"
