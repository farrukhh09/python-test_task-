import json
import os
from typing import List, Dict, Optional

class Book:
    """Класс для представления книги в библиотеке."""
    def __init__(self, title: str, author: str, year: int, id: Optional[int] = None):
        """
        Инициализация книги.
        
        :param title: Название книги
        :param author: Автор книги
        :param year: Год издания
        :param id: Уникальный идентификатор книги
        """
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"

class Library:
    """Класс для управления библиотекой."""
    def __init__(self, filename: str = 'library.json'):
        """
        Инициализация библиотеки.
        
        :param filename: Имя файла для хранения данных
        """
        self.filename = filename
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Загрузка книг из файла."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                try:
                    book_data = json.load(file)
                    self.books = [self._create_book_from_dict(book) for book in book_data]
                except json.JSONDecodeError:
                    self.books = []

    def save_books(self):
        """Сохранение книг в файл."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self._books_to_dict(), file, ensure_ascii=False, indent=4)

    def _create_book_from_dict(self, book_dict: Dict) -> Book:
        """
        Создание объекта книги из словаря.
        
        :param book_dict: Словарь с данными о книге
        :return: Объект книги
        """
        book = Book(book_dict['title'], book_dict['author'], book_dict['year'], book_dict['id'])
        book.status = book_dict['status']
        return book

    def _books_to_dict(self) -> List[Dict]:
        """
        Преобразование книг в список словарей.
        
        :return: Список словарей с данными о книгах
        """
        return [{
            'id': book.id, 
            'title': book.title, 
            'author': book.author, 
            'year': book.year, 
            'status': book.status
        } for book in self.books]

    def add_book(self, title: str, author: str, year: int) -> int:
        """
        Добавление новой книги.
        
        :param title: Название книги
        :param author: Автор книги
        :param year: Год издания
        :return: ID добавленной книги
        """
        new_id = max([book.id for book in self.books], default=0) + 1
        new_book = Book(title, author, year, new_id)
        self.books.append(new_book)
        self.save_books()
        return new_id

    def remove_book(self, book_id: int) -> bool:
        """
        Удаление книги по ID.
        
        :param book_id: ID книги для удаления
        :return: Успешность удаления
        """
        initial_length = len(self.books)
        self.books = [book for book in self.books if book.id != book_id]
        
        if len(self.books) < initial_length:
            self.save_books()
            return True
        return False

    def search_books(self, query: str) -> List[Book]:
        """
        Поиск книг по запросу.
        
        :param query: Строка поиска
        :return: Список найденных книг
        """
        query = query.lower()
        return [
            book for book in self.books 
            if (query in book.title.lower() or 
                query in book.author.lower() or 
                query == str(book.year))
        ]

    def get_all_books(self) -> List[Book]:
        """
        Получение всех книг.
        
        :return: Список всех книг
        """
        return self.books

    def change_book_status(self, book_id: int, new_status: str) -> bool:
        """
        Изменение статуса книги.
        
        :param book_id: ID книги
        :param new_status: Новый статус
        :return: Успешность изменения
        """
        for book in self.books:
            if book.id == book_id:
                if new_status in ["в наличии", "выдана"]:
                    book.status = new_status
                    self.save_books()
                    return True
        return False

def main():
    """Основная функция для работы с интерфейсом библиотеки."""
    library = Library()

    while True:
        print("\n--- Система управления библиотекой ---")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие (1-6): ")

        try:
            if choice == '1':
                title = input("Введите название книги: ")
                author = input("Введите автора: ")
                year = int(input("Введите год издания: "))
                book_id = library.add_book(title, author, year)
                print(f"Книга добавлена с ID: {book_id}")

            elif choice == '2':
                book_id = int(input("Введите ID книги для удаления: "))
                if library.remove_book(book_id):
                    print("Книга успешно удалена")
                else:
                    print("Книга не найдена")

            elif choice == '3':
                query = input("Введите строку для поиска: ")
                results = library.search_books(query)
                if results:
                    for book in results:
                        print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")
                else:
                    print("Книги не найдены")

            elif choice == '4':
                books = library.get_all_books()
                if books:
                    for book in books:
                        print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")
                else:
                    print("Библиотека пуста")

            elif choice == '5':
                book_id = int(input("Введите ID книги: "))
                new_status = input("Введите новый статус (в наличии/выдана): ")
                if library.change_book_status(book_id, new_status):
                    print("Статус книги изменен")
                else:
                    print("Не удалось изменить статус")

            elif choice == '6':
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

        except ValueError:
            print("Введены некорректные данные. Попробуйте снова.") 
if __name__ == "__main__":
    main()
