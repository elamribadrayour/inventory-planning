"""Main file for inventory planning."""

from typing import Annotated

from typer import Typer, Argument

import tasks.train
import tasks.expose
import tasks.prepare
import tasks.predict
import tasks.evaluate

import helpers.save
import helpers.model
import helpers.logger
import helpers.download


app = Typer(name="inventory-planning")


@app.command(name="prepare")
def prepare(
    cache_dir: Annotated[str, Argument(envvar="CACHE_DIR")],
) -> None:
    helpers.logger.init()
    _, df_train, df_test = tasks.prepare.get_data(cache_dir=cache_dir)
    helpers.save.save_data(
        df_test=df_test,
        df_train=df_train,
        cache_dir=cache_dir,
    )


@app.command(name="train")
def train(
    cache_dir: Annotated[str, Argument(envvar="CACHE_DIR")],
    model_name: Annotated[str, Argument(envvar="MODEL_NAME")],
) -> None:
    helpers.logger.init()
    x_train, y_train = helpers.download.get_train_data(cache_dir=cache_dir)
    grid_search = helpers.model.get_model()
    model = tasks.train.train(
        y_train=y_train,
        x_train=x_train,
        grid_search=grid_search,
    )
    helpers.save.save_model(
        model=model,
        cache_dir=cache_dir,
        model_name=model_name,
    )


@app.command(name="evaluate")
def evaluate(
    exec_date: Annotated[str, Argument(envvar="EXEC_DATE")],
    cache_dir: Annotated[str, Argument(envvar="CACHE_DIR")],
    model_name: Annotated[str, Argument(envvar="MODEL_NAME")],
) -> None:
    helpers.logger.init()

    import logging
    con = helpers.download.get_db(cache_dir=cache_dir)
    x = con.execute("SELECT quantity_sold FROM data").fetch_df().describe().to_dict()["quantity_sold"]
    logging.info(x)

    x_test, y_test = helpers.download.get_test_data(cache_dir=cache_dir)
    model = helpers.download.get_model(
        exec_date=exec_date,
        cache_dir=cache_dir,
        model_name=model_name,
    )
    metrics = tasks.evaluate.evaluate(
        model=model,
        x_test=x_test,
        y_test=y_test,
    )
    helpers.save.save_metrics(
        x=metrics,
        cache_dir=cache_dir,
        exec_date=exec_date,
        model_name=model_name,
    )


@app.command(name="predict")
def predict(
    exec_date: Annotated[str, Argument(envvar="EXEC_DATE")],
    cache_dir: Annotated[str, Argument(envvar="CACHE_DIR")],
    model_name: Annotated[str, Argument(envvar="MODEL_NAME")],
) -> None:
    helpers.logger.init()
    con = helpers.download.get_db(cache_dir=cache_dir)
    model = helpers.download.get_model(
        exec_date=exec_date,
        cache_dir=cache_dir,
        model_name=model_name,
    )
    metrics = helpers.download.get_metrics(
        cache_dir=cache_dir,
        exec_date=exec_date,
        model_name=model_name,
    )
    results = tasks.predict.get_predictions(
        con=con,
        model=model,
        metrics=metrics,
    )
    helpers.save.save_results(
        x=results,
        cache_dir=cache_dir,
    )


@app.command(name="expose")
def expose(
    exec_date: Annotated[str, Argument(envvar="EXEC_DATE")],
    cache_dir: Annotated[str, Argument(envvar="CACHE_DIR")],
    model_name: Annotated[str, Argument(envvar="MODEL_NAME")],
) -> None:
    helpers.logger.init()
    tasks.expose.run_api()


if __name__ == "__main__":
    app()
