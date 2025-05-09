# FoodService

Dev

```
python3 -m venv .venv # Virtual env
source .venv/bin/activate # Activate venv
pip install -r requirements.txt # Install requirements
```

Compose

```
docker-compose up --build # Build and run app + postgresql
docker-compose up app # Run app
docker-compose up database # Run postgresql

docker-compose down # Down services
docker-compose down --volumes # Removes services and volumes (postgresql persisted data)
```

# Otros
- Si estan en Windows entren a requirements.txt y eliminen la linea de "uvloop==0.21.0"
- Luego de activar el entorno e instalar las dependencias se posicionan dentro de 'src'
- Levantan con 'uvicorn main:app --reload'