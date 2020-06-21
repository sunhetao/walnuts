def if_list_equal(l1, l2):
    """
    该函数只做演示使用，不要用于实际测试
    """
    for i, v in enumerate(l1):
        if v != l2[i]:
            return False

    return True
