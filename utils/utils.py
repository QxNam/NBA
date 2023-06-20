import pandas as pd

def get_timeline(start_date: str, end_date: str):
    return pd.date_range(start_date, end_date)


def is_ready(browser):
    return browser.execute_script(r"""
        return document.readyState === 'complete'
    """)