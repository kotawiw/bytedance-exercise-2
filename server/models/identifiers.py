# Generate random identifiers for plain incremental integer IDs
# Ref: https://ericlippert.com/2013/11/14/a-practical-use-of-multiplicative-inverses/

MAX_SUPPORT_ID = 1_000_000_000


def id_to_identifier(id: int) -> str:
    return "%08x" % (id * 387420489 % MAX_SUPPORT_ID)


def id_from_identifier(identifier: str) -> int:
    return int(identifier, 16) * 513180409 % MAX_SUPPORT_ID
