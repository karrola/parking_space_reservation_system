# Drzewo Czerwono-Czarne - system rezerwacji miejsc parkingowych

Projekt stworzony w ramach zadania rekrutacyjnego do sekcji webowej koła naukowego BIT na AGH.

## Technologie

Python, Django, SQLite, HTML5 + DjangoTemplates, Bootstrap 5

## Funkcjonalności

- rezerwowanie miejsc parkingowych
- przegląd rezerwacji użytkownika
- edycja i anulowanie istniejących rezerwacji
- panel administracyjny django-admin

## Instrukcja uruchomienia

1. Sklonuj repozytorium
2. (zalecane) Stwórz wirtualne środowisko
3. Zainstaluj zależności
   ```
   pip install -r requirements.txt
   ```
4. Wykonaj migracje bazy danych
   ```
   py manage.py migrate       # Windows
   python3 manage.py migrate  # Linux / macOS
   ```
5. W celu korzystania z panelu admina django-admin stwórz superusera:
   ```
   py manage.py createsuperuser       # Windows
   python3 manage.py createsuperuser  # Linux / macOS
   ```
6. Uruchom serwer deweloperski

   ```
   py manage.py runserver       # Windows
   python3 manage.py runserver  # Linux / macOS
   ```

   Aplikacja będzie dostępna pod adresem http://127.0.0.1:8000/
   Panel administracyjny jest dostępny pod adresem http://127.0.0.1:8000/admin/
   Po zalogowaniu na konto superusera można w nim łatwo dodać przykładowe miejsca parkingowe, w celu umożliwienia przetestowania działania aplikacji.

## Uwagi dot. bezpieczeństwa

Projekt został stworzony do celów rektuacji - SECRET_KEY jest jawny i służy tylko do uruchamiania lokalnie.
W środowisku produkcyjnym klucz powinien być przechowywany w zmiennych środowiskowych.

## Wykorzystanie AI

AI (ChatGPT) był używany jako wsparcie w debugowaniu kodu, pisaniu testów i tworzeniu elementów interfejsu (klasy Bootstrap).
