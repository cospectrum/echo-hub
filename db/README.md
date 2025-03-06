# db

## Dev
Install [sqlx-cli](https://crates.io/crates/sqlx-cli):
```sh
cargo install sqlx-cli
```

Create migration:
```sh
sqlx migrate add -r <name>
```

Run migration:
```sh
sqlx migrate run
```

Revert migration:
```sh
sqlx migrate revert
```
