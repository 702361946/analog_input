def type_check(a, _type: str) -> bool:
    if type(a).__name__ == _type:
        return True
    else:
        return False

# 这玩意……
