def naive_search(text, pattern):
    """
    Returns True if pattern exists in text
    """
    n = len(text)
    m = len(pattern)

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            return True

    return False
