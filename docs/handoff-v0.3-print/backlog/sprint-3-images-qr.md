# Спринт 3 — картинки, схемы, QR-коды

**Цель.** Сделать визуальную инфраструктуру: единая стратегия
для схем, скриншотов и QR-кодов, работающая во всех форматах.

## Состав работ

### 3.1 TikZ-pipeline для схем

- [ ] Соглашение: каждая схема — отдельный `.tex` файл в `figures/`:
  ```
  figures/
    fig-3-1-tree.tex
    fig-3-2-pipeline.tex
  ```
- [ ] Шаблон фигуры (на базе стилей из print.tex):
  ```latex
  \begin{tikzpicture}[...]
    \node[opnode] (a) {...};
    ...
  \end{tikzpicture}
  ```
- [ ] В Markdown подключение:
  ```markdown
  ![Дерево операций для запроса.](figures/fig-3-1-tree.tex){#fig:tree}
  ```
- [ ] Создать `theme/filters/tikz-figures.lua` — pandoc-filter:
  - В **LaTeX-output**: подставляет `\input{figures/fig-3-1-tree.tex}`
    с обёрткой `\begin{figure}...\caption{...}\end{figure}`
  - В **HTML-output**: build-time рендерит через `xelatex → dvisvgm`
    в `build/figures/fig-3-1-tree.svg`, подставляет `<img>`
  - В **EPUB/FB2/DOCX**: build-time рендерит в `build/figures/fig-3-1-tree.png`
    через `xelatex → pdf2png` (300 dpi), подставляет
- [ ] Кеширование: пересборка фигуры только если изменился `.tex`-источник
  (по mtime или хешу)

### 3.2 Скриншоты: единая стратегия

- [ ] Соглашение: скриншоты живут как **высококачественный master-PNG**
  в `figures/screenshots/`:
  ```
  figures/screenshots/
    sc-3-1-conf-window.png       (master, color, 300dpi+)
  ```
- [ ] Build-time скрипт `theme/scripts/process-screenshots.sh`:
  - Для каждого master-файла генерирует варианты в `build/figures/`:
    - `*.color.png` — для color-форматов (electronic PDF, HTML, EPUB)
    - `*.gray.png` — для grayscale-форматов (print PDF, FB2):
      ```bash
      convert master.png -colorspace Gray \
        -level 5%,95%,1.2 \
        -sharpen 0x1.0 \
        out.gray.png
      ```
- [ ] В Markdown подключение единообразное:
  ```markdown
  ![Окно конфигуратора.](figures/screenshots/sc-3-1-conf-window.png){#fig:conf}
  ```
- [ ] Pandoc-filter выбирает правильный вариант под формат

### 3.3 Скриншоты-mockups через TikZ

**Контекст.** Права на скриншоты UI 1С — открытый юридический
вопрос (см. spec/print-edition.md). Временное решение —
рисовать схематичные мокапы UI в TikZ.

- [ ] Создать `theme/tikz-styles/ui-mockup.tex` с предустановленными
  стилями:
  - Окно с заголовком
  - Меню/тулбар
  - Дерево объектов
  - Поле с лейблом
- [ ] Использование:
  ```latex
  \begin{tikzpicture}[ui-mockup]
    \mockwindow{Конфигуратор}{
      \mocktree{Справочники, Документы, Регистры}
      \mockform{Имя:}{Контрагент}
    }
  \end{tikzpicture}
  ```

### 3.4 QR-коды: автоматизация через filter

- [ ] Создать `theme/filters/qr-links.py` — pandoc-filter:
  - Для каждого `CodeBlock` с классом `onec` или с attribute
    `qr-file="..."`, генерирует QR справа от подписи листинга
  - Для каждого `Header` уровня `\chapter` (если есть atomic
    soft в frontmatter `qr-chapter: 03_struktura`), генерирует
    QR в правом верхнем углу спуска полосы
- [ ] Базовые URL и тег читаются из `metadata.yaml.qr`:
  ```yaml
  qr:
    enabled: true
    repo: "https://github.com/iMironRU/1c-reading-code"
    tag: "v1.0"             # автоподстановка при release
    listings_path: "listings"
    chapters_path: "chapters"
    fallback_shortener: ""  # пусто или URL-shortener
  ```
- [ ] Для каждого QR опционально текстовый fallback под ним:
  - shortener-URL формата `imiron.ru/b/3-1`
  - или сокращённое имя файла
- [ ] Поведение по формату:
  - **Print-PDF**: QR + текст-fallback под ним
  - **Electronic-PDF**: гиперссылка вместо QR
    (на телефоне с PDF QR избыточен)
  - **EPUB/HTML**: кликабельная ссылка под листингом
    в стиле «Полный код: …»
  - **FB2/DOCX**: текстовая ссылка как обычный URL

### 3.5 Автоматическая подстановка тега

- [ ] При `./book.sh release` скрипт подставляет в
  `metadata.yaml.qr.tag` текущий тег `vX.Y.Z`
- [ ] При `./book.sh build` (без релиза) использует
  значение из `metadata.yaml` либо `main`-fallback
- [ ] Это гарантирует, что QR в книге `v1.0` всегда
  ведут на `v1.0` репо, не на main

## Acceptance criteria

1. TikZ-схема в Markdown даёт:
   - Векторно в Print-PDF и HTML
   - Растрово (PNG 300dpi) в EPUB/FB2/DOCX
   - Не пересобирается при неизменности `.tex`-источника

2. Скриншот в Markdown даёт:
   - Color-вариант в EPUB/HTML/electronic-PDF
   - Grayscale-with-contrast в Print-PDF и FB2

3. QR-код:
   - Автоматически появляется у каждого листинга в print-PDF
   - Ссылка правильно сформирована с учётом тега
   - В EPUB вместо QR — кликабельная ссылка
   - Уровень коррекции Q, размер 14 мм для листинга и 16 мм для главы
   - Под QR — текстовый fallback (если задан shortener)

4. На реальной главе:
   - 1 листинг + 1 схема + 1 mockup-скриншот собираются
     во все форматы

## Out of scope

- Реальные скриншоты UI 1С (юридический вопрос)
- Глубокая аналитика по QR-сканированию (отдельный проект,
  если будет shortener со статистикой)

## Риски

- TikZ-рендер для веба через dvisvgm требует, чтобы все шрифты
  были в текущем TeX Live. На GitHub Actions это решается
  установкой `texlive-full`.
- Конвертация PNG для скриншотов чувствительна к версии ImageMagick;
  в CI зафиксировать версию `convert`.
- QR на длинные URL может выйти за пределы безопасной плотности
  (Version 10+). Решение: для длинных путей использовать
  fallback_shortener.
