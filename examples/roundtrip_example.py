from io import StringIO
from argparse import ArgumentParser
import pandas as pd

from pyppy.arguments.fill_arguments import fill_arguments
from pyppy.conditions.conditions import condition, s_
from pyppy.config.get_config import initialize_config
from pyppy.config.get_container import container
from pyppy.pipeline.pipeline import step, Pipeline

# --- 1: ArgumentParser
parser = ArgumentParser()
parser.add_argument("--debug",
                    action="store_const",
                    const=True,
                    default=False)

parser.add_argument("--add-synthetic-rows",
                    action="store_const",
                    const=True,
                    default=False)

# --- 2: parse args
cli_args = ["--debug", "--add-synthetic-rows"]
args = parser.parse_args(cli_args)

# --- 3: initialize config
initialize_config(args)

# --- 4: create pipeline step and fill
#        method arguments from config
@step("df_proc", "create_df")
@fill_arguments
def create_data_frame(debug):
    data = StringIO(
        """col1;col2;col3
        1;4.4;99
        2;4.5;200
        3;4.7;65
        4;3.2;140
        """
    )

    df = pd.read_csv(data, sep=";")

    if debug:
        print(df.head())

    container().df = df
    return df

# --- 5: pipeline step based on condition
#        from config
@step("df_proc", "add_rows")
@condition(s_(add_synthetic_rows=True))
@fill_arguments
def add_rows(df):
    df2 = pd.DataFrame([[5, 3.6, 199], [6, 8.6, 37]], columns=["col1", "col2", "col3"])
    df2 = df.append(df2)

    return df2


results = dict([result for result in Pipeline.run_r("df_proc")])
final_df = results["add_rows"]

print(final_df)




