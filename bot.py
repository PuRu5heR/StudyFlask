from aiogram import Bot, types, Dispatcher, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from store import Store
from customers import Customers


def main(store, customer):
    token = open("token.txt", "r").read()
    bot = Bot(token=token)
    disp = Dispatcher(bot=bot, storage=MemoryStorage())
    global isRegistration
    isRegistration = False

    class States(StatesGroup):
        StateRegistration = State()
        StateUpdateData = State()
        StateEnterSurnameAndName = State()
        StateEnterBirth = State()
        StateEnterCountry = State()
        StateEnterCity = State()
        StateEndStart = State()

        StateDeleteAccount = State()

        StateEnterProductName = State()
        StateEnterCategory = State()
        StateEnterPrice = State()
        StatePutImage = State()
        StateAddProduct = State()
        StateRemoveProduct = State()

    # регистрация или авторизация
    @disp.message_handler(commands=["start"])
    async def starting(sms: types.Message):
        DeleteKeyboard = types.ReplyKeyboardRemove()
        await bot.send_message(sms.from_user.id, "Добро пожаловать в каталог электроники!", reply_markup=DeleteKeyboard)
        if customer.is_new_customer(sms.from_user.id):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
            keyboard.row(types.KeyboardButton(text="Регистрация"))
            await bot.send_message(sms.from_user.id, "Требуется регистрация для дальнейшего пользования",
                                   reply_markup=keyboard)
            await States.StateRegistration.set()
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
            keyboard.row(types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет"))
            await bot.send_message(sms.from_user.id, customer.get_data(sms.from_user.id))
            await bot.send_message(sms.from_user.id, "Желаете поменять информацию о вас?", reply_markup=keyboard)
            await States.StateUpdateData.set()

    @disp.message_handler(state=States.StateRegistration)
    async def registration(sms: types.Message):
        global isRegistration
        DeleteKeyboard = types.ReplyKeyboardRemove()
        if sms.text == "Регистрация":
            isRegistration = True
            await bot.send_message(sms.from_user.id, "Введите свою фамилию и имя через пробел",
                                   reply_markup=DeleteKeyboard)
            await States.StateEnterSurnameAndName.set()
        else:
            await sms.answer("Не знаю такого! Попробуйте ещё раз")

    @disp.message_handler(state=States.StateUpdateData)
    async def update_data(sms: types.Message, state: FSMContext):
        global isRegistration
        DeleteKeyboard = types.ReplyKeyboardRemove()
        if sms.text == "Да":
            isRegistration = False
            await bot.send_message(sms.from_user.id, "Введите свою фамилию и имя через пробел",
                                   reply_markup=DeleteKeyboard)
            await States.StateEnterSurnameAndName.set()
        elif sms.text == "Нет":
            await bot.send_message(sms.from_user.id, "Тогда можете спокойно продолжить", reply_markup=DeleteKeyboard)
            await state.finish()
        else:
            await sms.answer("Не знаю такого! Попробуйте ещё раз")

    @disp.message_handler(state=States.StateEnterSurnameAndName)
    async def enter_full_name(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if len(sms.text.split(" ")) == 2:
                print(sms.text)
                data['name'] = sms.text
                await sms.answer("Введите дату рождения (в формате ДД.ММ.ГГГГ")
                await States.StateEnterBirth.set()
            else:
                await sms.answer("Фамилия и имя введены неверно")

    @disp.message_handler(state=States.StateEnterBirth)
    async def enter_birth_date(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if len(sms.text.split(".")) == 3:
                print(sms.text)
                data['birth_date'] = sms.text
                await sms.answer("Введите страну, в которой находитесь")
                await States.StateEnterCountry.set()
            else:
                await sms.answer("Дата рождения введена неверно")

    @disp.message_handler(state=States.StateEnterCountry)
    async def enter_country(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['country'] = sms.text
            await sms.answer("Введите город, в котором находитесь")
            await States.StateEnterCity.set()

    @disp.message_handler(state=States.StateEnterCity)
    async def enter_city(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['city'] = sms.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
        keyboard.row(types.KeyboardButton(text="Закончить"))
        await bot.send_message(sms.from_user.id, "Нажмите 'Закончить'", reply_markup=keyboard)
        await States.StateEndStart.set()

    @disp.message_handler(state=States.StateEndStart)
    async def ending_start(sms: types.Message, state: FSMContext):
        global isRegistration
        if sms.text == "Закончить":
            async with state.proxy() as data:
                DeleteKeyboard = types.ReplyKeyboardRemove()
                if isRegistration:
                    isRegistration = False
                    customer.add_customer(sms.from_user.id, data['name'].split(" ")[0], data['name'].split(" ")[1],
                                          data['birth_date'], data['country'], data['city'])
                    await sms.answer("Вы закончили регистрацию. Можете спокойно продолжить.",
                                     reply_markup=DeleteKeyboard)
                else:
                    customer.change_data(sms.from_user.id, data['name'].split(" ")[0], data['name'].split(" ")[1],
                                         data['birth_date'], data['country'], data['city'])
                    await sms.answer("Вы закончили смену данных. Можете спокойно продолжить.",
                                     reply_markup=DeleteKeyboard)
            await state.finish()

        else:
            await sms.answer("Не знаю такого! Попробуйте ещё раз")

    # удаление аккаунта
    @disp.message_handler(commands="delete_account")
    async def delete_account(sms: types.Message):
        if customer.is_new_customer(sms.from_user.id):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
            keyboard.row(types.KeyboardButton(text="Да"), types.KeyboardButton(text="Отмена"))
            await sms.answer("Вы уверены, что хотите безвозвратно удалить аккаунт со всеми выставленными товарами?",
                             reply_markup=keyboard)
            await States.StateDeleteAccount.set()
        else:
            await sms.answer("Для пользования данными командами требуется регистрация")

    @disp.message_handler(state=States.StateDeleteAccount)
    async def delete_account(sms: types.Message, state: FSMContext):
        if sms.text == "Да":
            DeleteKeyboard = types.ReplyKeyboardRemove()
            customer.remove_customer(sms.from_user.id)
            store.remove_all_products(sms.from_user.id)
            await sms.answer("Аккаунт был успешно удалён", reply_markup=DeleteKeyboard)
            await state.finish()
        elif sms.text == "Отмена":
            DeleteKeyboard = types.ReplyKeyboardRemove()
            await sms.answer("Аккаунт не был удалён", reply_markup=DeleteKeyboard)
            await state.finish()
        else:
            await sms.answer("Не знаю такого! Попробуйте ещё раз")

    # добавление товара
    @disp.message_handler(commands="add_product")
    async def add_product(sms: types.Message):
        await sms.answer("Введите название товара")
        await States.StateEnterProductName.set()

    @disp.message_handler(state=States.StateEnterProductName)
    async def enter_product_name(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['product_name'] = sms.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
        keyboard.row(types.KeyboardButton(text="Компьютеры"), types.KeyboardButton(text="Комплектующие"))
        keyboard.row(types.KeyboardButton(text="Аудио"), types.KeyboardButton(text="Клавиатуры, мышки и коврики"))
        keyboard.row(types.KeyboardButton(text="Телефоны и планшеты"), types.KeyboardButton(text="Другое"))
        await sms.answer("Введите категорию, к которой относится товар", reply_markup=keyboard)
        await States.StateEnterCategory.set()

    @disp.message_handler(state=States.StateEnterCategory)
    async def enter_category(sms: types.Message, state: FSMContext):
        if sms.text in ["Компьютеры", "Комплектующие", "Аудио", "Клавиатуры, мышки и коврики", "Телефоны и планшеты",
                        "Другое"]:
            async with state.proxy() as data:
                data['category'] = sms.text
            DeleteKeyboard = types.ReplyKeyboardRemove()
            await sms.answer("Введите цену товара", reply_markup=DeleteKeyboard)
            await States.StateEnterPrice.set()
        else:
            await sms.answer("Не знаю такого! Попробуйте ещё раз")

    @disp.message_handler(state=States.StateEnterPrice)
    async def enter_price(sms: types.Message, state: FSMContext):
        if len(sms.text.split(" ")) == 2:
            async with state.proxy() as data:
                data['product_price'] = sms.text
            await sms.answer("Пришлите картинку, которую желаете вставить")
            await States.StatePutImage.set()
        else:
            await sms.answer("Нужно ввести сумму вместе с валютой через пробел")

    @disp.message_handler(state=States.StatePutImage, content_types=['photo'])
    async def put_image(sms: types.Message):
        await sms.photo[-1].download(destination_file="photos/image.jpg")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
        keyboard.row(types.KeyboardButton(text="Готово"))
        await sms.answer("Нажмите 'Готово'", reply_markup=keyboard)
        await States.StateAddProduct.set()

    @disp.message_handler(state=States.StateAddProduct)
    async def add_product(sms: types.Message, state: FSMContext):
        if sms.text == "Готово":
            async with state.proxy() as data:
                store.add_product(sms.from_user.id, data['product_name'], data['category'], data['product_price'])
                DeleteKeyboard = types.ReplyKeyboardRemove()
                await state.finish()
                await sms.answer("Товар успешно добавлен в каталог", reply_markup=DeleteKeyboard)
        else:
            await sms.answer("Не знаю такого! Попробуйте ещё раз")

    # удаление товара
    @disp.message_handler(commands='remove_product')
    async def remove_product(sms: types.Message, state: FSMContext):
        product_id = sms.get_args()
        if store.check_access(sms.from_user.id, product_id) and store.product_exist(product_id):
            async with state.proxy() as data:
                data['product_id'] = product_id
            await States.StateRemoveProduct.set()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
            keyboard.row(types.KeyboardButton(text="Да"), types.KeyboardButton(text="Отмена"))
            await sms.answer("Вы уверены, что хотите удалить товар")
        else:
            await sms.answer("Данного товара не существует в вашем каталоге")

    @disp.message_handler(state=States.StateRemoveProduct)
    async def end_removing_product(sms: types.Message, state: FSMContext):
        if sms.text == "Да":
            DeleteKeyboard = types.ReplyKeyboardRemove()
            async with state.proxy() as data:
                await sms.answer(store.remove_product(data['product_id']), reply_markup=DeleteKeyboard)
            await state.finish()
        elif sms.text == "Отмена":
            DeleteKeyboard = types.ReplyKeyboardRemove()
            await state.finish()
            await sms.answer("Удаление товара было отменено", reply_markup=DeleteKeyboard)
        else:
            await sms.answer("Не знаю такого")

    # вывод каталога
    @disp.message_handler(commands="catalog")
    async def show_catalog(sms: types.Message):
        catalog = store.get_products()
        for i in range(len(catalog)):
            message = catalog[i][0] + "\nКатегория: " + catalog[i][1] + "\nСтатус: " + catalog[i][2] + "\nЦена: " \
                      + catalog[i][3] + "\nПродавец: " + catalog[i][4] + "\nМестоположение: " + catalog[i][5] \
                      + "\nID: " + catalog[i][6]
            await bot.send_photo(sms.from_user.id, photo=types.InputFile("photos\image" + catalog[i][6] + ".jpg"))
            await sms.answer(message)

    executor.start_polling(disp)


if __name__ == "__main__":
    store = Store()
    customers = Customers()
    main(store, customers)
