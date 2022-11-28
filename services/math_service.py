import statistics


def get_mean(float_list: list):
    return statistics.mean(float_list)


def get_median(float_list: list):
    return statistics.median(float_list)


def get_mode(float_list: list):
    return statistics.mode(float_list)
