# Спринт 1 — минимальный print-ready

**Цель.** Получить сборку `./book.sh build print` → A5 ч/б PDF
с подсветкой кода, врезками, twoside-колонтитулами.

После этого спринта первая книга уже собирается в качественный
печатный PDF. На двух готовых книгах «1С как иностранный язык»
становится возможен прогон через новый pipeline.

## Состав работ

### 1.1 Pandoc-LaTeX-template

- [ ] Принять `theme/print.tex` из handoff/artifacts/print.tex
- [ ] Адаптировать оставшиеся хардкоды на pandoc-переменные
  (см. TODO внутри файла)
- [ ] Добавить `theme/partials/title-page.tex` и `title-verso.tex`
  для титула и оборота с выпускными данными
- [ ] Подключить partials через `$include-before$`

### 1.2 Подсветка кода 1С

- [ ] Принять `theme/highlight/onec_lexer.py` из handoff
- [ ] Принять `theme/highlight/pygstyle-bw.tex` из handoff
- [ ] Создать `theme/filters/highlight-onec.py` — pandoc-filter,
  который для блоков кода с языком `onec`:
  - В **LaTeX-output** прогоняет код через
    `pygmentize -l theme/highlight/onec_lexer.py:OneCLexer -x
    -f latex -O style=bw,commandprefix=PYone`
    и подставляет результат через `\begin{onecode}\input{...}\end{onecode}`
  - В **HTML/EPUB-output** даёт `<pre class="onec">` с inline-CSS
    через тот же лексер `-f html`
  - В **DOCX/FB2** — обычный `<code>` без подсветки

### 1.3 Fenced divs для врезок

- [ ] Принять `theme/divs.tex` из handoff
- [ ] Создать `theme/filters/divs-to-env.lua` — pandoc-Lua-filter,
  который маппит классы div'ов на LaTeX-окружения:
  ```
  ::: opredelenie     → \begin{opredelenie} ... \end{opredelenie}
  ::: napolyax        → \begin{napolyax}
  ::: primer          → \begin{primer}
  ::: kontrolnye-voprosy → \begin{kontrolnyevoprosy}
  ::: zadanie         → \begin{zadanie}
  ```
- [ ] Для HTML/EPUB filter оставляет `<div class="opredelenie">`
  как есть; стили — в `theme/epub.css` (Спринт 4)

### 1.4 Build-target `print`

- [ ] В `book.sh` добавить таргет `build print`:
  ```bash
  ./book.sh build print
  ```
- [ ] Цепочка:
  1. Препроцесс: применить filters (русская типографика будет
     добавлена в Спринт 2)
  2. Собрать через `pandoc --template=theme/print.tex` →
     `build/<slug>.tex`
  3. Прогнать `xelatex` дважды (для ссылок)
  4. Конвертировать в Grayscale через `gs`:
     ```bash
     gs -dSAFER -sDEVICE=pdfwrite \
        -sColorConversionStrategy=Gray \
        -dProcessColorModel=/DeviceGray \
        -sOutputFile=build/<slug>-print.pdf \
        build/<slug>.pdf
     ```
  5. Валидация PDF/X-1a через verapdf (опционально на этом спринте)
- [ ] Опции CLI:
  - `--draft` — пропускает Grayscale-конверсию
  - `--check` — прогон через verapdf

### 1.5 Расширения `metadata.yaml`

- [ ] Добавить в `metadata.yaml` шаблона блок `print:` с дефолтами:
  ```yaml
  print:
    enabled: true
    trim_size: a5
    binding: kbs           # kbs | sewn | staple
    gutter: 20mm           # под выбранный переплёт
    outer: 14mm
    top: 16mm
    bottom: 20mm
    bleed: 0mm             # 3mm если есть подложки к краю
    color: grayscale       # grayscale | bw | full
    pdf_x: "1a"
    icc_profile: "Coated FOGRA39"  # уточнить с типографией
  ```

### 1.6 QR-коды (минимальная версия)

- [ ] В template уже подключён `qrcode`-пакет (из artifacts/print.tex)
- [ ] В `metadata.yaml` добавить:
  ```yaml
  qr:
    enabled: true
    repo: "https://github.com/iMironRU/1c-semantic-reading"
    tag: "v1.0"
  ```
- [ ] Передавать в template через `-V qr-enabled=true -V qr-repo=... -V qr-tag=...`
- [ ] Полная QR-автоматизация (filter с автогенерацией для каждого
  листинга) — Спринт 3

## Acceptance criteria

1. На синтетическом тестовом параграфе:
   - `./book.sh build print` собирается без warnings
   - PDF открывается, виден титул, оглавление, главы с правильной
     twoside-навигацией
   - Листинги с подсветкой через жирность, разметка корректна
   - Врезки `opredelenie`, `napolyax`, `primer`, `kontrolnye-voprosy`
     рендерятся
   - Колонтитулы: чётная — глава, нечётная — параграф
   - На спуске колонтитула нет

2. На реальной готовой главе (взять §2.1 из «1С как иностранный язык»):
   - Сборка проходит
   - Вёрстка читаемая
   - Визуальное сравнение с `samples/A5-sample-v4-qr.pdf` —
     стилистическое соответствие

3. Не сломаны другие форматы:
   - `./book.sh build epub` собирается
   - `./book.sh build html` собирается
   - `./book.sh build docx` собирается

## Out of scope для этого спринта

- Русская типографика (preprocess) → Спринт 2
- Аппарат с титулом, индексом, выпускными данными в полном виде → Спринт 2
- TikZ-схемы как pipeline → Спринт 3
- Полная QR-автоматизация → Спринт 3
- Стили EPUB/CSS, reference.docx → Спринт 4
- Документация → Спринт 5

## Риски и заметки

- Pandoc может ругаться на отсутствие переменных в metadata.yaml
  при первой сборке — задать дефолты в template через `$if(x)$$else$`
- На macOS pygmentize иногда не находит лексер по пути с пробелами —
  оборачивать путь в кавычки
- Если PT Serif/PT Sans не найдены — fallback на DejaVu Serif/Sans
  (положить в template условие через fontspec `Renderer=...`)
