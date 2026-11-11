import sys
from pathlib import Path
import time
import pandas as pd
from data_agent.profiler import ColumnProfile, NumericColumn, CategoricalColumn
from data_agent.utils import DataAgentError, ProfileNotFoundError, timed, is_valid_column_name, validate_null_count


class DatasetProfile:

    def __init__(self):
        self._columns: list[ColumnProfile] = []

    def add_column(self, col_profile: ColumnProfile) -> None:
        self._columns.append(col_profile)

    @property
    def clean_columns(self) -> list[ColumnProfile]:
        return [col for col in self._columns if col.is_clean]

    def quality_report(self) -> None:
        print('\n' + '='*50)
        print('Data Set Quality')
        print('+'*50)

        for col in self._columns:
            grade = 'clean' if col.is_clean else 'needs attention'
            print(f'{col.name:20} {col.null_rate:10.2%} {grade}')

        print('-'* 50)
        total = len(self._columns)  
        clean = len(self.clean_columns)    
        if total > 0:
            print(f"Total columns : {total}")
            print(f"Clean columns : {clean} ({clean / total * 100:.1f}%)")
        else:
            print("No columns profiled.")
        print('=' * 50 + '\n')     

    @classmethod
    @timed
    def from_dataframe(cls, df: pd.DataFrame) -> 'DatasetProfile':
        profile = cls()
        for col_name in df.columns:
            series = df[col_name]
            
            if pd.api.types.is_numeric_dtype(series):  # is the right tool — cleaner than checking dtype strings manually.
                col = NumericColumn(
                    name=col_name,
                    dtype=str(series.dtype),
                    null_count=int(series.isna().sum()),
                    total_count=len(series),
                    mean=round(float(series.mean()), 2),
                    std=round(float(series.std()), 2),
                )
            elif series.dtype in ('object', 'category'):
                col = CategoricalColumn(
                    name=col_name,
                    dtype=str(series.dtype),
                    null_count=int(series.isna().sum()),
                    total_count=len(series),
                    cardinality=int(series.nunique()),
                )
            else:
                col = ColumnProfile.from_series(series, col_name)
            
            profile.add_column(col)
        return profile


    def __add__(self, other: 'DatasetProfile') -> 'DatasetProfile':
        merged = DatasetProfile()
        for col in self:
            merged.add_column(col)
        for col in other:
            merged.add_column(col)
        return merged         

    def  __len__(self) -> int:
        return len(self._columns)

    def __contains__(self, name: str) -> bool:
        return any(col_profile.name == name for col_profile in self._columns)       

    def __iter__(self):
        return iter(self._columns)

    def __getitem__(self, name: str) -> ColumnProfile:
        for col in self._columns:          # _columns, not col_profiles
            if col.name == name:
                return col
        raise ProfileNotFoundError(
            f"no column named {name!r}", 
            column_name = name
            )
    """Comprehensive property to get a dictionary of column names and their null rates."""   
    @property
    def null_rates(self):
        return {col.name: col.null_rate for col in self._columns}

    @property
    def dirty_columns(self):
        return [col.name for col in self._columns if not col.is_clean]

def run_demo():
    #import pandas as pd
    df = pd.DataFrame({'revenue': [100, 200, None], 'country': ['ET', 'US', 'ET']})
    profile = DatasetProfile.from_dataframe(df)
    profile.quality_report()  
    print(f"Null rates: {profile.null_rates}")                                   
    print(f"Dirty columns: {profile.dirty_columns}")

if __name__ == "__main__":
    run_demo()

    
    
    
