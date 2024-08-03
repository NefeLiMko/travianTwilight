import random

# Определяем типы планет и новых элементов
planet_types = ['Земляная', 'Пустынная', 'Лавовая', 'Лесная', 'Газовая', 'Замороженная']
void_zones = 'Пустая зона (Void)'
anomalies = 'Аномалия'
accelerators = 'Парные червоточины'

# Создаем функции для генерации ресурсов
def generate_resources(planet_type):
    if planet_type == 'Земляная':
        return {
            'food': random.randint(5, 10),
            'minerals': random.randint(5, 10),
            'rare_resources': random.randint(0, 5),
        }
    elif planet_type == 'Пустынная':
        return {
            'food': random.randint(1, 3),
            'minerals': random.randint(2, 5),
            'rare_resources': random.randint(0, 1),
        }
    # Добавить другие типы планет по той же логике
    return {}

# Генерация галактики
def generate_galaxy(size):
    galaxy = []
    for i in range(size):
        row = []
        for j in range(size):
            random_choice = random.choices(
                population=['planet', 'void', 'anomaly', 'accelerator'],
                weights=[70, 10, 15, 5],  # Вероятность появления каждого типа
                k=1
            )[0]

            if random_choice == 'planet':
                planet_type = random.choice(planet_types)
                row.append({
                    'id': f"{i}-{j}",
                    'type': 'planet',
                    'planet_type': planet_type,
                    'resources': generate_resources(planet_type),
                })
            elif random_choice == 'void':
                row.append({
                    'id': f"{i}-{j}",
                    'type': void_zones,
                    'resources': None,
                })
            elif random_choice == 'anomaly':
                row.append({
                    'id': f"{i}-{j}",
                    'type': anomalies,
                    'effect': random.choice(['увеличение ресурсов', 'временный бонус к юнитам']),
                })
            elif random_choice == 'accelerator':
                row.append({
                    'id': f"{i}-{j}",
                    'type': accelerators,
                    'effect': 'Связывает две точки в пространстве (червоточины)',
                })
        galaxy.append(row)
    return galaxy

# Функция для колонизации пустой зоны
def settle_in_void(galaxy, username):
    void_positions = [(i, j) for i in range(len(galaxy)) for j in range(len(galaxy[0])) if galaxy[i][j]['type'] == void_zones]
    
    if void_positions:
        # Случайным образом выбрать пустую зону
        chosen_void = random.choice(void_positions)
        x, y = chosen_void
        
        # Создаем новую планету в этой пустой зоне
        new_planet_type = random.choice(planet_types)
        galaxy[x][y] = {
            'id': f"{x}-{y}",
            'type': 'planet',
            'planet_type': new_planet_type,
            'resources': generate_resources(new_planet_type),
            'owner': username
        }
        out = {"cords": (x, y), "type": new_planet_type}
        return out

# Генерация HTML-таблицы с отображением по координатам
def generate_html_table(galaxy):
    size = len(galaxy)
    html_content = '''<html>
    <head>
        <title>Генерация Галактики</title>
        <style>
            table {border-collapse: collapse; width: 100%;}
            th, td {border: 1px solid black; padding: 8px; text-align: center;}
            th {background-color: #f2f2f2;}
        </style>
    </head>
    <body>
        <h1>Генерация Галактики по координатам</h1>
        <table>
            <tr>
                <th>Y \\ X</th>'''
    
    # Добавляем заголовки столбцов (Y)
    for x in range(size):
        html_content += f'<th>{x}</th>'
    
    html_content += '</tr>'

    # Заполнение таблицы по координатам
    for y in range(size):
        html_content += f'<tr><td>{y}</td>'  # Заголовок строки (Y)
        for x in range(size):
            cell = galaxy[y][x]
            resources = cell.get('resources')
            resources_str = (
                f"Пища: {resources['food']}, "
                f"Минералы: {resources['minerals']}, "
                f"Редкие ресурсы: {resources['rare_resources']}"
            ) if resources else "Нет"
            try:
                owner = cell.get('owner')
            except:
                pass
            html_content += f'''
                <td>
                    {cell['type']}<br>
                    {owner if owner else 'Нет Владельца'}<br>
                    {cell.get('planet_type', cell.get('effect', ''))}<br>
                    {resources_str}
                </td>'''

            
        html_content += '</tr>'

    html_content += '''
        </table>
    </body>
    </html>'''
    # Запись в HTML файл с кодировкой UTF-8
    with open('galaxy.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    return html_content



