# Re:Praxis - Python Port of the RePraxis

This repo contains the python port of [Re:Praxis](https://github.com/ShiJbey/RePraxis). Please see that repo for documentation of how to use RePraxis. The public API's are almost identical.

## Differences from the main implementation

- `RePraxisDatabase.Assert()` was renamed to `RePraxisDatabase.asset_statement` (`assert` is a reserved keyword in Python).
- Method and function names were changed to snake-case to comply with Python conventions.
