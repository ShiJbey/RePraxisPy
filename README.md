# Re:Praxis - Python Port of RePraxis

This repo contains the Python port of [Re:Praxis](https://github.com/ShiJbey/RePraxis). RePraxis is an in-memory database solution for games and applications. It is based on the Praxis exclusion logic language used in the [Versu Engine](https://versu.com/). I reimplemented and ported it to C# and Python to facilitate declarative queries in social simulation projects.

## Installation

```bash
# MacOS/Linux
python3 -m pip install repraxis

# Windows
py -m pip install repraxis
```

## Documentation 

Please see the [original repo](https://github.com/ShiJbey/RePraxis) for documentation on how to use RePraxis. The public APIs are mostly identical, with the following differences:

- `RePraxisDatabase.Assert()` was renamed `RePraxisDatabase.asset_statement` (`assert` is a reserved keyword in Python).
- Method and function names were changed to snake-case to comply with Python conventions.

## Examples

The best place to find examples is the unit tests within `tests`. The unit tests cover almost all operations, from data insertion to performing queries with multiple statements.

## License

This project is licensed under the [MIT License](./LICENSE.md).
