### Depracated: API portalu przeniesione zostało do API panelu

# Fake Hunter
System Fake Hunter składa się z trzech podsystemów: collectora, panelu i portalu.  Każdy z nich pełni odrębną funkcję, podlega odrębnemu cyklowi wydań i poddawany będzie różnym obciążeniom. 

## Spis treści

1. [Collector](#collector)
2. [Panel](#panel)
2. [Portal](#portal)

## Collector
Zadaniem collectora, jest odbieranie zgłoszeń od użytkowników - obecnie jedynie poprzez wtyczkę do przegladarki ale trwają prace nad integracją z innymi systemami.
Zapisywanrya jest zaznaczony przez użytkownika tekst, komentarz, adres email oraz automatycznie przekazywany jest screenshot oraz url strony intenrnetowej.

Jest to mikro aplikacja napisana w języku Python w wersji 3.8, za pomocą frameworka fastAPI.
Zawiera jeden endpoint obsługujący zapytanie POST.

Collector nie zarządza bazą danych bezpośrednio. Korzysta w trybie zapisu z tej samej bazy co Portal i Panel. Jest to PostgreSQL w wersji 11.

## Panel
Panel jest najbardziej złożoną częścia systemu. Jest to zaplecze zapewniające narzedzia niezbędne do sprawnej weryfikacji treści.
Odebrane zgłoszenia zostają cyklicznie preztworzone i przekazane do factcheckerów w celu zopiniowania. Werdykt wyłaniany jest po uzyskaniu dwóch zgodnych opinii.
Nad rzeszą factchekerów znajdują się eksperci wspierający opiniowanie i mogący wydać finalny werdykt.

Aplikacja jest napisana w języku Python w wersji 3.7, za pomocą frameworka Django w wersji 3.0.
Sam framework roszerzony został o bibliotekę Django Rest Framework, która posłużyła do zbudowania obszernego REST API.

Interfejs napisany jest w języku Javascript, za pomocą frameworka React. Całość bootsrapowana poprzez Create React App. 

Panel w pełni zarządza stanem bazy danych. Z jego poziomu odbywa się wersjonowanie i aktualizacja jej struktury. Panel ma uprawnienia do zapisu, odczytu jak i zarządznia systemem bazodanowym. Jest to PostgreSQL w wersji 11. 


## Portal
Zadaniem portalu, jest przedstawienie treści zweryfikowanych w panelu przez factcheckerów i ekspertów.
Jest to prosta aplikacja składajaca się z dwóch głównych elementów - listingu oraz widoku szegółowego faktu zgłoszonego przez użytkowników.

Aplikacja jest napisana w języku Python w wersji 3.7, za pomocą frameworka Django w wersji 3.0.
Sam framework roszerzony został o bibliotekę Django Rest Framework, która posłużyła do zbudowania REST API.

Interfejs napisany jest w Języku javascript, za pomocą frameworka React. Całość bootsrapowana poprzez Create React App. 

Portal nie zarządza bazą danych bezpośrednio. Korzysta w trybie odczytu z tej samej bazy co Collector i Panel. Jest to PostgreSQL w wersji 11.        

Elementem wspólnym wszystkich trzech aplikacji jest jedynie baza danych. W celu uproszczenia architektury, nie zastosowano przetwarzania asynchronicznego a systemy nie komunikują się między sobą na poziomie API.
