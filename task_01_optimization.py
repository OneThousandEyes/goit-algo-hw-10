import pulp
from rich.console import Console
from rich.table import Table


def optimize_production():
    console = Console()

    # Вхідні дані
    resources = {
        "Вода": 100,
        "Цукор": 50,
        "Лимонний сік": 30,
        "Фруктове пюре": 40,
    }

    requirements = {
        "Лимонад": {
            "Вода": 2,
            "Цукор": 1,
            "Лимонний сік": 1,
        },
        "Фруктовий сік": {
            "Вода": 1,
            "Фруктове пюре": 2,
        },
    }

    # Таблиця вхідних ресурсів
    res_table = Table(title="Вхідні ресурси", show_lines=True)
    res_table.add_column("Ресурс", style="cyan")
    res_table.add_column("Доступно", style="yellow", justify="right")

    for r, v in resources.items():
        res_table.add_row(r, str(v))

    console.print(res_table)

    # Таблиця вимог на одиницю продукту
    req_table = Table(title="Витрати ресурсів на 1 одиницю", show_lines=True)
    req_table.add_column("Продукт", style="cyan")
    req_table.add_column("Ресурс", style="magenta")
    req_table.add_column("Кількість", style="green", justify="right")

    for product, reqs in requirements.items():
        for res, qty in reqs.items():
            req_table.add_row(product, res, str(qty))

    console.print(req_table)

    # Модель
    model = pulp.LpProblem("Drink_Production", pulp.LpMaximize)

    lemonade = pulp.LpVariable("Lemonade", lowBound=0, cat=pulp.LpInteger)
    fruit_juice = pulp.LpVariable("FruitJuice", lowBound=0, cat=pulp.LpInteger)

    model += lemonade + fruit_juice

    model += 2 * lemonade + fruit_juice <= resources["Вода"]
    model += lemonade <= resources["Цукор"]
    model += lemonade <= resources["Лимонний сік"]
    model += 2 * fruit_juice <= resources["Фруктове пюре"]

    model.solve(pulp.PULP_CBC_CMD(msg=False))

    l = int(pulp.value(lemonade))
    f = int(pulp.value(fruit_juice))

    # Таблиця результатів
    result_table = Table(title="Результат оптимізації", show_lines=True)
    result_table.add_column("Продукт", style="cyan")
    result_table.add_column("Кількість", style="green", justify="right")

    result_table.add_row("Лимонад", str(l))
    result_table.add_row("Фруктовий сік", str(f))
    result_table.add_row("Усього", str(l + f))

    console.print(result_table)


if __name__ == "__main__":
    optimize_production()
