#Данный файл является просто конвертером для динамических URL адресов

class FourDigitYearConverter:
    regex = "[0-9]{4}"  #Сюда можно подставить любое нужное регулярное выражение

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value