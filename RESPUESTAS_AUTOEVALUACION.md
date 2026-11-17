# Mis respuestas a las autoevaluaciones

## Modulo 00 — FastAPI

1. **FastAPI vs Flask en validacion:** en Flask validas a mano; en FastAPI declaras tipos con Pydantic y valida solo (si algo viene mal, 422).
2. **¿Por que es mas rapido?** Flask es WSGI (sincronico); FastAPI corre sobre ASGI (Uvicorn + Starlette), que es async y atiende otros requests mientras espera.
3. **¿Que es ASGI?** La interfaz entre servidor y app pensada para async. Permite `async def`, muchas conexiones y WebSockets.
4. **¿Sin type hints funciona?** Arranca, pero perdes validacion, conversion de tipos, Swagger y autocompletado.
5. **Ventaja de OpenAPI automatico:** la doc sale del codigo, siempre esta al dia y la probas en `/docs`.

## Modulo 03 — Capas

1. **Las 3 capas:** controller (HTTP), service (reglas de negocio), repository (base de datos).
2. **¿Por que el controller no escribe SQL?** Mezcla responsabilidades; el SQL va en el repository.
3. **¿Por que el service no devuelve 404?** El 404 es de HTTP. El service devuelve `None` y el controller lo traduce.
4. **ORM vs SQL crudo:** con ORM uso objetos (`session.add(task)`) y el ORM arma el SQL parametrizado; en el 02 escribia el SQL a mano.
5. **`table=True`:** la clase es una tabla real. Sin eso es solo un esquema (`TaskCreate`, `TaskUpdate`).
6. **TypeScript vs JavaScript:** tipos; te avisa los errores antes de ejecutar.
7. **Nombre del patron:** Layered Architecture (particion horizontal). El otro eje es vertical, por feature.
8. **¿Por capa o por feature?** Depende del tamaño del proyecto, cuantas features tiene y cuantos equipos trabajan. Chico: por capa. Grande: por feature.

**Fase 5 (en voz alta):**
1. **¿Que ganamos?** Orden: cada cosa en su lugar, cambios aislados y testeables.
2. **¿Donde vive el 404?** En el controller; el service no sabe de HTTP.
3. **¿Que SQL escribe el ORM?** Todo el CRUD (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) y el `CREATE TABLE`.
4. **¿Que da TypeScript?** Errores marcados antes de ejecutar.
5. **Patron y otro eje:** Layered (horizontal); el otro es por feature (vertical), conviene cuando el proyecto crece.

## Modulo 03.5 — Arquitectura modular

1. **Horizontal vs vertical:** horizontal agrupa por capa (`controllers/`, `services/`); vertical por feature (`tasks/`, `billing/`).
2. **¿Por feature elimina las capas?** No, cada feature tiene su controller, service y repository adentro.
3. **Test del cambio:** agregar una feature y contar cuantas carpetas tocas. Por capa 4, por feature 1.
4. **Capas vs hexagonal:** en capas el service depende del repository concreto; en hexagonal depende de una interfaz (puerto) y el repository la implementa.
5. **`Protocol`:** define una interfaz sin herencia. En tests paso un repo falso en memoria (`fakes.py`) y no necesito Postgres.
6. **¿Cuando cada eje?** Por capa: proyecto chico, un equipo. Por feature: proyecto grande o varios equipos.

## Modulo 04 — Autenticacion

1. **Autenticacion vs autorizacion:** quien sos vs que podes hacer.
2. **¿Por que no texto plano?** Si se filtra la base se filtran todas. Guardamos un hash.
3. **¿Por que no MD5/SHA1?** Son muy rapidos y se rompen por fuerza bruta. Argon2 es lento a proposito, usa mucha memoria y lleva salt.
4. **Sesion vs JWT:** la sesion se puede revocar al instante pero el server guarda estado; el JWT no guarda estado y escala facil, pero no se revoca antes de que expire.
5. **¿Se encripta o se firma?** Se firma. El payload se puede leer, asi que nada sensible adentro.
6. **¿SSO vs JWT?** No se comparan: SSO es loguearse una vez para varias apps; JWT es un formato de token (un SSO puede usar JWT).
7. **User enumeration:** averiguar que emails existen por mensajes distintos. Se evita con "Email o contraseña incorrectos".
8. **OWASP:** A01 (endpoints sin proteger), A02 (contraseñas mal guardadas), A03 (injection), A07 (fallas de autenticacion).

## Modulo 07 — Testing

**Checklist:** 30 tests en verde, tests nuevos con TDD (`can_publish`), `parametrize`, casos de borde, y se por que no hay Postgres.

1. **Test unitario:** prueba una funcion aislada, sin base ni red: le doy una entrada y verifico la salida.
2. **AAA:** Arrange (preparo datos), Act (llamo a la funcion), Assert (verifico el resultado).
3. **¿Por que sin Postgres?** Las reglas son funciones puras; con base seria mas lento, fragil y pasaria a ser de integracion.
4. **Funcion pura:** misma entrada, misma salida, sin efectos externos. Pura: `can_edit(...)`. Impura: una que guarda en la base o usa `datetime.now()`.
5. **¿Verde = esta bien?** No, solo que cumple lo que el test pide. Si el test esta mal o le falta un caso, puede haber bugs igual.
6. **Unitario vs integracion:** unitario prueba una pieza sola y rapido; integracion prueba varias juntas (endpoint + service + base).
