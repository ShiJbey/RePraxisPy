# Re:Praxis - Python Port of RePraxis

This repo contains the Python port of [Re:Praxis](https://github.com/ShiJbey/RePraxis). Please see that repo for documentation on how to use RePraxis. The public APIs are almost identical.

## Differences from the C# implementation

- `RePraxisDatabase.Assert()` was renamed `RePraxisDatabase.asset_statement` (`assert` is a reserved keyword in Python).
- Method and function names were changed to snake-case to comply with Python conventions.
