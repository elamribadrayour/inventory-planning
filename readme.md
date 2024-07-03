# Inventory Planning Project

This project is designed to help with inventory planning using machine learning models. The project provides a CLI to prepare data, train a model, evaluate the model, make offline batch predictions, and expose model for real time predictions.

## Prerequisites

1. **Docker**: Ensure Docker is installed on your system. You can download Docker from [here](https://www.docker.com/get-started).
2. **Docker Compose**: Ensure Docker Compose is installed. You can download Docker Compose from [here](https://docs.docker.com/compose/install/).

## Project Structure

- `main.py`: Main script containing the CLI commands.
- `Dockerfile`: Docker configuration file.
- `docker-compose.yml`: Docker Compose configuration file.
- `src/`: Directory containing the project source code.
- `.cache/`: Directory used to store cached data.

## Running the Project

### Step 1: Prepare Data

To prepare the data, run the following command:

```sh
docker-compose up inventory-planning-prepare
```

This command will prepare a duckdb containing features, the training and test datasets used for training, and save them in the cache directory.

### Step 2: Train the Model

To train the model, run the following command:

```sh
docker-compose up inventory-planning-train
```

This command will train the model using the prepared data and save the trained model in the cache directory.

### Step 3: Evaluate the Model

To evaluate the model, run the following command:

```sh
docker-compose up inventory-planning-evaluate
```

This command will evaluate the trained model using the test dataset and save the evaluation metrics in the cache directory.

The following environment variables should be set to access the required model:

- `MODEL_NAME`: Name of the model to be used.
- `EXEC_DATE`: Execution date that you can cache from the .cache where your trained model is saved.

### Step 4: Make Predictions

To make offline batch predictions using the trained model, run the following command:

```sh
docker-compose up inventory-planning-predict
```

This command will use the trained model to make predictions and save the results in the cache directory.


The following environment variables should be set to access the required model:

- `MODEL_NAME`: Name of the model to be used.
- `EXEC_DATE`: Execution date that you can cache from the .cache where your trained model is saved.

### Step 5: Expose the API

To expose the API for accessing the model for realtime prediction, run the following command:

```sh
docker-compose up inventory-planning-expose
```

This command will start a web server on port 8080 to serve the predictions.
Access the swagger using this url: http://localhost:8080/docs


The following environment variables should be set to access the required model:

- `MODEL_NAME`: Name of the model to be used.
- `EXEC_DATE`: Execution date that you can cache from the .cache where your trained model is saved.

## Environment Variables

The following environment variables are used in the project:

- `CACHE_DIR`: Directory to cache data.
- `MODEL_NAME`: Name of the model to be used.
- `EXEC_DATE`: Execution date of model training.
- `API_KEY`: API key for accessing the exposed API.

## Volumes

The following volumes are mounted in the Docker Compose configuration:

- `./src/:/code/job`: Mounts the source code directory.
- `./.cache:/code/data`: Mounts the cache directory.

## Ports

The following ports are exposed in the Docker Compose configuration:

- `8080:8080`: Exposes port 8080 for the web server.

## Notebook

Please find an explanatory notebook in here: [Notebook](src/main.ipynb)

For more information on data preparation and model choise, you can check in here: [Notebook](src/exploration.ipynb)
