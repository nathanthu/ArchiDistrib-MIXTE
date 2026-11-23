# TP MIXTE

| Service  | Port | API     | Données | Appelle                          |
|----------|------|---------|---------|----------------------------------|
| Movie    | 3200 | GraphQL | json    |                                  |
| Booking  | 3201 | GraphQL | MongoDB | Movie (GraphQL), Schedule (REST) |
| Schedule | 3202 | REST    | json    |                                  |
| User     | 3203 | REST    | json    |                                  |

gRPC n'a pas été vu en cours, Schedule reste donc en REST.

## Lancer

```sh
docker compose up --build
```

Remettre les données à zéro :

```sh
docker compose down -v
```

## Tester

Importer `insomnia.json` dans Insomnia et dérouler les requêtes dans l'ordre.

Ou en ligne de commande :

```sh
curl -X POST localhost:3201/graphql -H "Content-Type: application/json" \
  -d '{"query": "{ bookings_by_user(_userid: \"chris_rivers\") { dates { date movies { title } } } }"}'

curl localhost:3202/schedule/20151201
```
