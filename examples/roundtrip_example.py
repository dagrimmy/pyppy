from io import StringIO
from argparse import ArgumentParser
import pandas as pd

from pyppy.arguments.fill_arguments import fill_arguments
from pyppy.conditions.conditions import condition, exp
from pyppy.config.get_config import initialize_config
from pyppy.config.get_container import container
from pyppy.pipeline.pipeline import step, Pipeline


parser = ArgumentParser()
parser.add_argument("--debug",
                    action="store_true",
                    default=False)

parser.add_argument("--add-synthetic-rows",
                    action="store_true",
                    default=False)

cli_args = ["--debug", "--add-synthetic-rows"]
args = parser.parse_args(cli_args)

initialize_config(args)


@step("df_proc", "create_df")
@fill_arguments()
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

@step("df_proc", "add_rows")
@condition(exp(add_synthetic_rows=True))
@fill_arguments()
def add_rows(df):
    df2 = pd.DataFrame([[5, 3.6, 199], [6, 8.6, 37]], columns=["col1", "col2", "col3"])
    df2 = df.append(df2)

    return df2


results = Pipeline.run_a("df_proc")
final_df = results["add_rows"]

print(final_df)




