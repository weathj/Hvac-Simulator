import os
import pandas as pd

class Logger():
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.DataFrame()
        self.current_row = {}

    def log(self, column_name, value):
        self.current_row[column_name] = value

    def log_row(self, row: dict):
        self.current_row.update(row)

    def commit(self):
        self.df = pd.concat(
            [self.df, pd.DataFrame([self.current_row])],
            ignore_index=True
        )
        self.current_row = {}
        try:
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            self.df.to_csv(self.filename)
        except PermissionError:
            print(f"Could not save: {self.filename} is open in another program")