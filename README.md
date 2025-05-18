# FoodService

## Dev

```
python3 -m venv .venv # Virtual env
source .venv/bin/activate # Activate venv
pip install -r requirements.txt # Install requirements
```

### Run it

```
python3 main.py

# Step on src or run it specifying the env path with
ENV_PATH=/path/to/.env python3 main.py
```

## Compose

### Run it

```
docker-compose up --build # Build and run app + postgresql
docker-compose up app # Run app
docker-compose up database # Run postgresql
```

### Free resources

```
docker-compose down # Down services
docker-compose down --volumes # Removes services and volumes (postgresql persisted data)
```
