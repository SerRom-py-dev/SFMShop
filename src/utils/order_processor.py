def load_orders_from_file(filename):
    """Читает файл с заказами и возвращает список строк"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_lines = file.readlines()

        order_lines = []
        for line in raw_lines:
            clean_line = line.strip()
            if clean_line:
                order_lines.append(clean_line)

        return order_lines

    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден")
        return []


def calculate_order_total(price, discount_rate):
    """Рассчитывает итоговую стоимость с учётом скидки"""
    result = price * (1 - discount_rate)
    return round(result, 2)


def get_discount_by_total(total):
    """Возвращает размер скидки в зависимости от суммы заказа"""
    if total <= 0:
        return 0
    elif total > 10000:
        return 0.15
    elif total > 5000:
        return 0.10
    else:
        return 0.05


def process_orders(orders_data):
    """Обрабатывает сырые строки заказов, применяет скидки"""
    result_list = []

    for line in orders_data:
        try:
            parts = line.split(":")

            if len(parts) != 4:
                print(f"Ошибка: некорректный формат строки: {line}")
                continue

            order_id = parts[0].strip()
            price = int(parts[1].strip())
            status = parts[2].strip()
            user = parts[3].strip()

            discount = get_discount_by_total(price)
            total = calculate_order_total(price, discount)

            order_dict = {
                "order_id": order_id,
                "total": total,
                "status": status,
                "user": user
            }
            result_list.append(order_dict)

        except ValueError:
            print(f"Ошибка: невозможно преобразовать сумму в число: {line}")

    return result_list


def analyze_orders(processed_orders):
    """Собирает статистику по обработанным заказам"""
    stats = {
        "total_orders": 0,
        "total_sum": 0,
        "by_status": {},
        "unique_users": set()
    }

    for order in processed_orders:
        stats["total_orders"] += 1
        stats["total_sum"] += order["total"]

        current_status = order["status"]
        stats["by_status"][current_status] = stats["by_status"].get(current_status, 0) + 1

        stats["unique_users"].add(order["user"])

    stats["unique_users"] = list(stats["unique_users"])

    return stats


def process_order_file(input_file, output_file):
    """Полный цикл: чтение, обработка, анализ, запись отчёта"""
    orders_data = load_orders_from_file(input_file)

    if not orders_data:
        print("Нет данных для обработки")
        return

    processed_orders = process_orders(orders_data)
    stats = analyze_orders(processed_orders)

    status_parts = []
    for status_name, status_count in stats["by_status"].items():
        status_parts.append(f"{status_name}: {status_count}")
    statuses_line = ", ".join(status_parts)

    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(f"Обработано заказов: {stats['total_orders']}\n")
            file.write(f"Общая сумма: {stats['total_sum']} руб.\n")
            file.write(f"По статусам: {statuses_line}\n")
            file.write(f"Уникальных пользователей: {len(stats['unique_users'])}\n")

        print(f"Отчёт успешно записан в {output_file}")

    except Exception as error:
        print(f"Ошибка при записи в файл: {error}")