import statistics


def get_mean(int_list: list[int]):
    return statistics.mean(int_list)


def get_median(int_list: list[int]):
    return statistics.median(int_list)


def get_mode(int_list: list[int]):
    return statistics.mode(int_list)
