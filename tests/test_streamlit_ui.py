from streamlit.testing.v1 import AppTest


def test_streamlit_ui_loads():
    at = AppTest.from_file("app/ui_app/streamlit_app.py")
    at.run()

    assert not at.exception
    assert "🚗 SmartPark AI" in at.title[0].value


def test_streamlit_sidebar_exists():
    at = AppTest.from_file("app/ui_app/streamlit_app.py")
    at.run()

    assert not at.exception

    markdown = "\n".join(
        m.value
        for m in at.markdown
        if hasattr(m, "value")
    )

    assert "Parking Charges" in markdown
    assert "Supported Cities" in markdown