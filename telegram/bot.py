import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import random
from presets.map  import generate_html_table, settle_in_void, generate_galaxy

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)



# Словарь для хранения зарегистрированных пользователей и их родных планет


registered_users = {}
home_planets = {
    'Фракция 1': 'Земляная',
    'Фракция 2': 'Лавовая',
    'Фракция 3': 'Газовая'
}

# Генерация ресурсов для планет
def generate_resources(planet_type):
    if planet_type == 'Земляная':
        return {'food': random.randint(5, 10), 'minerals': random.randint(5, 10), 'rare_resources': random.randint(0, 5)}
    elif planet_type == 'Лавовая':
        return {'food': random.randint(1, 3), 'minerals': random.randint(5, 8), 'rare_resources': random.randint(0, 2)}
    elif planet_type == 'Газовая':
        return {'food': random.randint(0, 1), 'minerals': random.randint(1, 3), 'rare_resources': random.randint(0, 1)}
    return {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Добро пожаловать! Для регистрации введите /register.')

def register(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    if user_id in registered_users:
        update.message.reply_text('Вы уже зарегистрированы!')
    else:
        # Запрос фракции у пользователя
        update.message.reply_text('Введите вашу фракцию (Фракция 1, Фракция 2, Фракция 3):')
        context.user_data['waiting_for_faction'] = True

def get_faction(update: Update, context: CallbackContext ) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    if context.user_data.get('waiting_for_faction'):
        faction = update.message.text.strip()
        if faction in home_planets:
            registered_users[user_id] = {
                'username': username,
                'home_planet': settle_in_void(galaxy=galaxy, username=username),
                'resources': generate_resources(home_planets[faction])
            }
            print(galaxy)
            generate_html_table(galaxy)
            update.message.reply_text(f'{username}, вы зарегистрированы! Ваша родная планета: {home_planets[faction]}')
            context.user_data['waiting_for_faction'] = False
        else:
            update.message.reply_text('Неверная фракция. Пожалуйста, введите правильную фракцию (Фракция 1, Фракция 2, Фракция 3).')

def list_users(update: Update, context: CallbackContext) -> None:
    users_list = "\n".join(f"{uid}: {info['username']} - Родная планета: {info['home_planet']}" for uid, info in registered_users.items())
    update.message.reply_text(f'Зарегистрированные пользователи:\n{users_list}' if users_list else 'Нет зарегистрированных пользователей.')

def main():
    
    updater = Updater('7254479520:AAHk6BybLfhoR02jrc-4AZt85DUtM5lB6w0')
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('register', register))
    dispatcher.add_handler(CommandHandler('list', list_users))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_faction))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    galaxy = generate_galaxy(size=10)
    generate_html_table(galaxy)
    main()