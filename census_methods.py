import seaborn as sns
import os


class CensusDataset:
    
    def __init__(self):
        os.makedirs(self.app_folder_loc, exist_ok=True)  # create folder 'Files' at current working directory for storing useful files
    
    @property
    def app_name(self):
        return 'CensusDataset'
    
    @property
    def app_folder_loc(self):
        return f'{self.app_name}Output'
        
    @staticmethod
    def null_checker(df: sns.categorical.pd.DataFrame, in_perc: bool=False):
        """return quantity of missing data per dataframe column."""

        if not in_perc:
            return df.isnull().sum()
        return sns.categorical.np.round(df.isnull().sum()/df.shape[0], 2)
    
    @staticmethod
    def unique_categs(df: sns.categorical.pd.DataFrame):
        """return unique values per dataframe column."""

        cols = tuple(df.columns)
        uniq_vals = dict()
        for i in range(len(cols)):
            uniq_vals[cols[i]] = list(df[cols[i]].unique())
        return uniq_vals
    
    @staticmethod
    def round_up_num(decimal: str):
        """round up to nearest whole number if preceding number is 5 or greater."""

        whole, dec = str(float(decimal)).split('.')
        return str(int(whole) + 1) if int(dec[0]) >= 5 or (int(dec[0]) + 1 >= 5 and int(dec[1]) >= 5) else whole

    @staticmethod
    def transform_val(ser: sns.categorical.pd.Series, guide: dict):
        """Change values in a series from one format to new format specified in the guide dictionary."""
        
        for k, v in guide.items():
            if isinstance(k, (list, tuple)):
                raise TypeError("Only a dictionary of strings is accepted as keys in the guide arg")

        return ser.apply(lambda val: str(guide[val]) if val in guide.keys() else val)

    @staticmethod
    def check_for_empty_str(df: sns.categorical.pd.DataFrame):
        """Return True for column containing '' or ' '.
        Output is a dictionary with column name as key and True/False as value."""

        if not isinstance(df, sns.categorical.pd.DataFrame):
            raise TypeError("Argument you pass as df is not a pandas dataframe")

        cols = list(df.columns)  # list of columns
        result = dict()
        for i in range(len(cols)):
            # True for columns having empty strings
            result[cols[i]] = df.loc[(df[cols[i]] == ' ') |
                                    (df[cols[i]] == '')].shape[0] > 0
        return result
    
    @staticmethod
    def col_blank_rows(df: sns.categorical.pd.DataFrame):
        """check an entire dataframe and return dict containing columns containing blank rows 
        (as keys) and a list of index of blank rows (values)."""
      
        cls = CensusDataset()
        guide = cls.check_for_empty_str(df)
        blank_cols = [col for col, is_blank in guide.items() if is_blank]
        result = dict()
        for i in range(len(blank_cols)):
            result[blank_cols[i]] = list(df[blank_cols[i]].loc[(df[blank_cols[i]] == " ") |
                                                          (df[blank_cols[i]] == "")].index)
        return result
    
    @staticmethod
    def fig_writer(fname: str, plotter: sns.categorical.plt.figure=None, dpi: int=200, file_type='png'):
        """save an image of the given figure plot in the filesystem."""
        
        cls = CensusDataset()
        plotter.get_figure().savefig(f"{cls.app_folder_loc}\\{fname}", dpi=dpi, format=file_type,
                                         bbox_inches='tight', pad_inches=0.25)
        return fname