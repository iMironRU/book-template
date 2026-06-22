# Спринт 4 — единообразие других форматов

**Цель.** Сделать так, чтобы EPUB/HTML/DOCX/FB2 выглядели
качественно и согласованно с печатной версией, насколько это
позволяет каждый формат.

## Состав работ

### 4.1 EPUB: CSS-тема

- [ ] Создать `theme/epub.css`:
  - **Типографика**: PT Serif как primary, fallback на system serif
  - **Листинги**: моноширинный, фон light gray, не overflow
    мобильный экран
  - **Подсветка 1С**: жирность для keywords, курсив для variables;
    те же классы что и в HTML (sharing с mdBook-темой)
  - **Врезки**:
    - `.opredelenie` — двойная рамка сверху/снизу, padded
    - `.napolyax` — вертикальная линия слева, padded
    - `.primer` — мельче кегль, тонкая линия слева
    - `.kontrolnyevoprosy` — заголовок жирный, список
  - **Картинки**: max-width 100%, центрирование
  - **Темная тема**: переменные через `prefers-color-scheme: dark`
- [ ] Создать `theme/epub-cover.html` для cover-страницы
- [ ] Передавать в pandoc: `--css=theme/epub.css`
- [ ] Валидация: `epubcheck build/<slug>.epub` — в CI как gate

### 4.2 Reference.docx для корректоров

**Контекст.** DOCX нужен не читателю, а корректору/редактору,
который работает в Word с track changes.

- [ ] Создать `theme/reference.docx` с настроенными стилями:
  - **Heading 1-3** — иерархия заголовков с правильными отступами
  - **Body Text** — основной кегль с межстрочным
  - **Code** — моноширинный с серым фоном
  - **Caption** — для подписей рисунков и листингов
  - **Quote** — для цитат и эпиграфов
  - **Sidebar** — для врезок (Word native style)
- [ ] В Word: проверить что стили читаются и применяются автоматически
- [ ] Передавать в pandoc: `--reference-doc=theme/reference.docx`
- [ ] В `docs/`: инструкция, как обновлять reference.docx
  (сохранять стили, не контент)

### 4.3 HTML / mdBook custom theme

- [ ] Создать `theme/mdbook-theme/`:
  - `book.css` (override базовых стилей)
  - `pagetoc.css` (правая колонка с навигацией по странице)
  - `index.hbs` или другие шаблоны при необходимости
- [ ] Подключение в `book.toml`:
  ```toml
  [output.html]
  theme = "theme/mdbook-theme"
  default-theme = "light"
  preferred-dark-theme = "dark"
  additional-css = ["theme/onec-highlight.css"]
  ```
- [ ] Стили врезок согласованы с EPUB (DRY: общий
  `theme/divs.css` шарится между mdBook и EPUB
  через `@import` или сборку)
- [ ] Поиск через mdBook works для русского текста
- [ ] Темная тема: переменные CSS

### 4.4 FB2: эрзац-врезки

- [ ] Создать `theme/filters/fb2-fallback.lua`:
  - Для div с классом `opredelenie` оборачивает в `<cite>`
    + жирный префикс «Определение.»
  - Для `napolyax` — `<cite>` + «Примечание.»
  - Для `primer` — `<cite>` + «Пример.»
  - Для `kontrolnye-voprosy` — обычный `<title>` + `<list>`
- [ ] Решение в `metadata.yaml`: `formats.fb2: true/false`
  для технических книг — рассмотреть отключение, так как
  эрзац-врезки выглядят бедно. Решить по результатам прогона.

### 4.5 Pandoc-crossref для кросс-ссылок

- [ ] Установить `pandoc-crossref`
- [ ] Подключить как filter: `--filter pandoc-crossref`
- [ ] Конфигурация в `metadata.yaml`:
  ```yaml
  crossref:
    figPrefix: ["рис.", "рис."]
    eqnPrefix: ["формула", "формулы"]
    tblPrefix: ["табл.", "табл."]
    lstPrefix: ["листинг", "листинги"]
    secPrefix: ["§", "§§"]
    figureTitle: "Рис."
    listingTitle: "Листинг"
    tableTitle: "Табл."
  ```
- [ ] В Markdown: `@fig:tree`, `@lst:ostatki`, `@sec:plan`
- [ ] Работает во всех форматах

### 4.6 Метаданные на каждый формат

- [ ] Расширить `metadata.yaml`:
  ```yaml
  identifiers:
    print:
      isbn: "978-5-..."
    epub:
      isbn: "978-5-..."
      uuid: "auto-generated"
    fb2: {}  # опционально

  accessibility:
    epub: true   # ARIA-теги, alt-text, language
  ```
- [ ] Pandoc передаёт правильные метаданные в каждый формат

## Acceptance criteria

1. EPUB:
   - `epubcheck` проходит без ошибок
   - Открывается в Apple Books, Calibre, FBReader без проблем
   - Темная тема работает на читалках, которые её поддерживают
   - Врезки визуально отличимы от основного текста
   - Подсветка кода видна

2. DOCX:
   - Открывается в Word и LibreOffice
   - Стили применены, не direct formatting
   - Корректор может включить track changes и работать

3. HTML/mdBook:
   - Сайт собирается, темная тема работает
   - Поиск по русскому тексту работает
   - Врезки выглядят согласованно с EPUB

4. FB2:
   - Открывается в FBReader без ошибок
   - Структура читаема
   - Решение по сохранению/отключению FB2 принято
     (записано в spec/print-edition.md)

5. Cross-references:
   - `@fig:tree`, `@lst:ostatki`, `@sec:plan` работают во всех форматах
   - Префиксы правильные («рис. 3.1», не «Figure 3.1»)

## Out of scope

- KFX/MOBI генерация для Kindle (отдельная цепочка через
  KindleGen, если потребуется)
- PDF/A для архивирования (рассматриваем в Спринте 5
  как опцию)
- Доступность EPUB по WCAG 2.1 AA полностью — это объём
  отдельной работы

## Риски

- `epubcheck` строг, может требовать переделки конкретных
  div'ов или элементов. Решается итеративно.
- mdBook ограничен в кастомизации — для глубоких изменений
  может потребоваться форк или альтернатива (Hugo+статикор?).
- Reference.docx чувствителен к версии Word — стили могут
  по-разному применяться. Тестировать в обоих.
