import pandas as pd

class DfWrapper():

    def __init__(self, path=False) -> None:
        if path is not None:
            try:
                self.df = pd.read_csv(path)
            except Exception as e:
                print(f"Error Ocurred(read_csv): {e}")
    
    def read_csv(self, path) -> None:
        self.df = pd.read_csv(path)
    
    def convert_date(self):
        self.df['Date'] = pd.to_datetime(self.df['Date'], dayfirst=True)

    def latest_date(self):
        self.convert_date()
        return self.df['Date'].max()
    
    
    
