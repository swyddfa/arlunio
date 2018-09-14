import pytest


def define_benchmarked_example(name, example):

    import matplotlib

    matplotlib.use("Agg")

    image = example()

    @pytest.mark.parametrize("n", [512, 1024, 2048])
    def benchmark_test(benchmark, n):

        filename = None

        if n == 512:
            filename = "docs/_static/examples/" + name.lower() + ".png"

        benchmark(image, n, n, filename=filename)

    return benchmark_test
