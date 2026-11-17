# Users API (Blog)

API REST de usuarios para un sistema de blog. Flask + SQLAlchemy + PostgreSQL,
con arquitectura en capas (Controller → Service → Repository → Database).

## Requisitos

- Python 3.11+
- PostgreSQL accesible (cadena en `DATABASE_URL`)

## Instalación

```bash
pip install -r requirements.txt
cp .env.example .env   # ajusta DATABASE_URL
flask db upgrade       # aplica las migraciones
python run.py          # http://127.0.0.1:5000
```

## Endpoints (`/api/users`)

| Método | Ruta | Descripción | Éxito | Errores |
|--------|------|-------------|-------|---------|
| POST | `/api/users` | Crear usuario | 201 | 400, 409 |
| GET | `/api/users` | Listar usuarios | 200 | — |
| GET | `/api/users/<id>` | Obtener por id | 200 | 404 |
| PUT | `/api/users/<id>` | Reemplazo completo | 200 | 400, 404, 409 |
| PATCH | `/api/users/<id>` | Actualización parcial | 200 | 400, 404, 409 |
| DELETE | `/api/users/<id>` | Eliminar | 204 | 404 |

`password_hash` nunca se expone en las respuestas.

Ejemplo de creación:

```bash
curl -X POST http://127.0.0.1:5000/api/users \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"alejo\", \"email\": \"alejo@example.com\", \"password\": \"secret123\", \"full_name\": \"Alejo\"}"
```

## Arquitectura

```
Controller (HTTP) → Service (negocio) → Repository (persistencia) → PostgreSQL
                          ↕
                        Mapper (DTO ↔ modelo)
```

- `app/controllers/user_controller.py`: blueprint, solo HTTP.
- `app/services/user_service.py`: reglas de negocio (email/username únicos).
- `app/repositories/user_repository.py`: único punto de acceso a la BD.
- `app/mappers/user_mapper.py`: transformación modelo → DTO de respuesta.
- `app/dtos/user_dto.py`: contratos de entrada/salida y validación de formato.
- `app/errors.py`: excepciones de dominio traducidas a 400/404/409.

## Migraciones

```bash
flask db migrate -m "descripción"
flask db upgrade
```

## Pruebas de integración (Postman / Newman)

Colección: `postman/UsersApi.postman_collection.json`
Environment: `postman/Local.postman_environment.json` (`baseUrl=http://127.0.0.1:5000`)

```bash
newman run postman/UsersApi.postman_collection.json \
  -e postman/Local.postman_environment.json
```

Resultado al momento de la implementación: **13 requests, 19 aserciones, 0 fallos**
(ejecutado con la app en SQLite temporal por falta de PostgreSQL en la máquina;
en PostgreSQL basta con `flask db upgrade` y apuntar `DATABASE_URL`).
