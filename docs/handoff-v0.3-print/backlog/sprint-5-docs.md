# Спринт 5 — документация и SDD-обновления

**Цель.** Закрепить v0.2.0 в документации шаблона так, чтобы
будущие книги серии и будущие итерации Claude Code работали
по единым правилам.

## Состав работ

### 5.1 Документация для авторов

- [ ] `docs/format-strategy.md` — принять из handoff/docs
  (матрица формат×возможность + принципы единого источника)
- [ ] `docs/typography-russian.md` — принять из handoff/docs
  (правила русского набора)
- [ ] `docs/print-spec.md` — принять из handoff/docs
  (требования к pre-press: цвет, разрешение, gutter, bleed)
- [ ] Создать `docs/divs-syntax.md` — справочник по
  fenced divs с примерами для каждого типа врезки
- [ ] Создать `docs/qr-syntax.md` — как делать QR в листингах
  и шмуцтитулах

### 5.2 Обновление SDD-слоя

- [ ] Принять `spec/print-edition.md` из handoff/spec
- [ ] Расширить `spec/constitution.md` шаблона разделом
  про печатное издание:
  ```markdown
  ## Печатное издание

  Книги серии могут выходить не только в электронных форматах,
  но и в виде печатного издания (см. spec/print-edition.md).

  Авторские решения по разметке должны учитывать обе ветки
  доставки: одна Markdown-разметка → много форматов.
  ```
- [ ] Расширить `spec/specification.md` шаблона: добавить
  возможность опционального печатного выпуска как одну из
  целей книги

### 5.3 Обновление CLAUDE.md

- [ ] Принять `claude/CLAUDE-print-addendum.md` из handoff
  и смержить в `CLAUDE.md` шаблона
- [ ] Содержание addendum'а:
  - Контекст печатного издания
  - Правила fenced divs (когда какую врезку использовать)
  - Правила русской типографики
  - Правила разметки кода 1С
  - Правила TikZ-схем
  - Что НЕ делать (избыточная вёрстка, цветовая зависимость)

### 5.4 Новые slash-команды

- [ ] Принять `claude/commands/print-check.md` из handoff:
  `/print-check` — проверка параграфа на pre-press совместимость
- [ ] Принять `claude/commands/template-spec-review.md` из handoff:
  `/template-spec-review` — проход по spec шаблона
- [ ] Обновить `.claude/commands/book-write.md`: при написании
  параграфа учитывать print-формат (использовать врезки, разметку,
  типографику правильно)
- [ ] Обновить `.claude/commands/book-analyze.md`: добавить
  проверку pre-press, проверку наличия caption'ов у рисунков
  и листингов

### 5.5 template-changes.yaml для sync

- [ ] Принять `template-changes-v0.2.yaml` из handoff:
  ```yaml
  version: 0.2.0
  date: 2026-XX-XX
  changes:
    - type: added
      file: theme/print.tex
      reason: pandoc-template для печатной версии
    - type: added
      file: theme/divs.tex
      reason: окружения для семантических врезок
    - type: added
      file: theme/highlight/onec_lexer.py
      reason: подсветка 1С-кода
    ...
  migration:
    - "Принять все файлы theme/"
    - "Принять все файлы docs/"
    - "Принять spec/print-edition.md"
    - "Смержить CLAUDE.md (см. CLAUDE-print-addendum.md в archives)"
    - "В metadata.yaml добавить блоки 'print:' и 'qr:' с дефолтами"
    - "Запустить ./book.sh build print для проверки"
  ```
- [ ] Заменить существующий `template-changes.yaml` на новый

### 5.6 README шаблона

- [ ] Обновить `README.md` шаблона: упомянуть, что v0.2.0
  поддерживает print-ready PDF
- [ ] Добавить в таблицу форматов колонку для print-PDF
- [ ] Добавить раздел про печатное издание с ссылкой на
  `spec/print-edition.md`

### 5.7 CHANGELOG

- [ ] Записать в `CHANGELOG.md`:
  ```markdown
  ## v0.2.0 - 2026-XX-XX

  ### Added
  - Pandoc-LaTeX-template для печатной версии (theme/print.tex)
  - Кастомный pygments-лексер 1С (theme/highlight/onec_lexer.py)
  - Семантические врезки: Определение, На полях, Пример,
    Контрольные вопросы (theme/divs.tex)
  - Препроцессор русской типографики (theme/filters/russian-typo.py)
  - QR-коды с автогенерацией ссылок на git-теги
  - TikZ-pipeline для векторных схем
  - Reference.docx для корректоров
  - Custom mdBook theme

  ### Changed
  - metadata.yaml расширена блоками print: и qr:
  - book.sh добавлен таргет 'build print'

  ### Documentation
  - spec/print-edition.md — конституция печатного издания
  - docs/format-strategy.md — матрица форматов
  - docs/typography-russian.md — правила русского набора
  - docs/print-spec.md — требования к pre-press
  ```

### 5.8 Acceptance criteria для всего релиза

- [ ] Сборка обеих готовых книг через ./book.sh build всех форматов
  без ошибок
- [ ] Sync-механика на тестовой книге работает корректно
- [ ] Документация открывается и читается, ссылки между
  документами рабочие
- [ ] Tag v0.2.0 в репозитории book-template
- [ ] GitHub release с описанием

### 5.9 Постмиграционная проверка на двух готовых книгах

После выхода v0.2.0:

- [ ] `cd 1c-reading-code && ./book.sh sync`
  принять предложенные изменения
- [ ] `./book.sh build print` собирается без ошибок
- [ ] Визуальная проверка нескольких параграфов на соответствие
  спецификации и референсу `samples/A5-sample-v4-qr.pdf`
- [ ] Аналогично для второй готовой книги
- [ ] Если что-то не так — багфикс в book-template,
  v0.2.1, повторный sync

## Acceptance criteria

1. Документация:
   - Все файлы в `docs/` и `spec/` присутствуют
   - Внутренние ссылки работают
   - README обновлён

2. SDD:
   - constitution и specification шаблона учитывают
     печатное издание
   - CLAUDE.md обновлён, новые slash-команды на месте

3. Релиз:
   - CHANGELOG аккуратно описывает изменения
   - Tag v0.2.0 создан и описан в GitHub Release
   - sync-механика проверена на тестовой книге

4. Постмиграция:
   - Обе готовые книги пересобраны без ручных правок
   - Pre-press PDF готовы к отправке в типографию

## Финальный артефакт

После Спринта 5 у тебя на руках:

- `book-template v0.2.0` — полноценная инфраструктура серии
  с поддержкой печати
- «1С как иностранный язык» в print-ready виде
- Вторая готовая книга в print-ready виде
- Документированный процесс, по которому Claude Code и любой
  будущий соавтор могут писать новые книги серии

Это та точка, после которой работа над книгами становится
работой над **текстами**, а не над инфраструктурой.
