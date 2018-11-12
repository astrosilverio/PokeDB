# PokeDB
Database Engine (Recurse Center)

## Description
Group of Recurse Center participants creating their own database engine

Run `pokedb/command_prompt/poke.py` to start a REPL.
SQL processing is in pokedb/command_prompt/processing/
Access management is in pokedb/access/
Transaction management is in pokedb/transactions/
Lock management is in pokedb/locks/
The data layer is in pokedb/storage/
Logging is in pokedb/logs/

## Main Process

`pokedb/command_prompt/poke.py` will give you a way to input raw SQL and receive responses from the data layer.

There will soon be a daemon process that lives at top-level as well that will listen on socket 1188 for incoming requests to the database.

SQL Processing lives in pokedb/command_prompt/processing/. Current operation runs on sqlparser.py which processes simple SQL statements:

```SQL
select id1 from pokemon
insert into pokemon (id, val) values (9, \"hey listen\")
select * from pokemon where id=1
```

More robust SQL parser in the works.

## Access Management

The Access Manager is in charge of taking processed read/write commands and performing them. The access/ module contains the BTree structure, which describes where data lives. It communicates with the data layer in pokedb/storage and the lock manager in pokedb/locks.

## Transaction Management

The Transaction Manager tracks what state all active transactions are in. It maintains this state in-memory. It accepts requests to begin transactions, commit transactions, and rollback transactions from the main process. On commit and rollback, it speaks to the Lock Manager.

## Lock Management

The Lock Manager keeps track of what records are locked. It keeps that state in-memory. Depending on which isolation level you are running PokeDB on, the algorithms for acquiring locks changes. The specific algorithms for lock maintenance live in pokedb/locks/isolation.

## Data Layer

The Data Layer is responsible for accessing and writing data to/from disk. It contains the buffer pool, copies of data that exist in-memory. It also contains the serializer, which translates data from on-disk format to something the access manager will understand.

## Logger

The logger is a very thin shell that is something for the Managers to call to log their operations to disk.
