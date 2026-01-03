import numpy as np
import scipy.integrate as spi
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def f(x):
    """Функція, яку інтегруємо."""
    return x ** 2


def monte_carlo_integral(a, b, n):
    """
    Обчислення інтеграла методом Монте-Карло
    через середнє значення функції.
    """
    rng = np.random.default_rng(42)
    x = rng.uniform(a, b, n)
    fx = f(x)
    return (b - a) * fx.mean()


def analytic_integral(a, b):
    """Аналітичне обчислення інтеграла."""
    return (b**3 - a**3) / 3


def quad_integral(a, b):
    """Обчислення інтеграла за допомогою scipy quad."""
    result, error = spi.quad(f, a, b)
    return result, error


def print_intro(a, b, n):
    """Виведення вступної інформації."""
    console.print(Panel.fit(
        "[bold]Обчислення визначеного інтеграла методом Монте-Карло[/bold]\n"
        "Функція: f(x) = x²\n"
        f"Інтервал: [{a}; {b}]\n"
        f"Кількість випадкових точок: {n}",
        title="Вхідні дані"
    ))


def print_results(mc, analytic, quad, quad_err):
    """Виведення результатів у вигляді таблиці."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Метод")
    table.add_column("Значення інтеграла")
    table.add_column("Відхилення від аналітики")

    table.add_row(
        "Monte-Carlo",
        f"{mc:.10f}",
        f"{abs(mc - analytic):.6g}"
    )

    table.add_row(
        "Аналітичний",
        f"{analytic:.10f}",
        "0"
    )

    table.add_row(
        "quad",
        f"{quad:.10f}",
        f"{abs(quad - analytic):.2e}"
    )

    console.print("\n[bold cyan]Результати обчислень[/bold cyan]")
    console.print(table)


def main():
    a = 0
    b = 2
    n = 100_000

    print_intro(a, b, n)

    mc = monte_carlo_integral(a, b, n)
    analytic = analytic_integral(a, b)
    quad, quad_err = quad_integral(a, b)

    print_results(mc, analytic, quad, quad_err)


if __name__ == "__main__":
    main()
