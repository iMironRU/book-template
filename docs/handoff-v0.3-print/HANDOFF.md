# Handoff: book-template v0.2.0 — печатное издание

Передаточный пакет от сессии проработки печатной вёрстки для серии «Школа 1С-инженеров».
Распакуй в новую ветку `book-template`, открой в Claude Code, дальше работай по бэклогу.

## TL;DR

**Цель.** Расширить `book-template` так, чтобы он выпускал не только электронные форматы
(EPUB/FB2/HTML/DOCX), но и **print-ready PDF под малотиражную офсетную ч/б печать**,
не ломая существующую инфраструктуру и SDD-процесс.

**Стратегия.** Все изменения идут в `book-template`, релизятся как `v0.2.0`, далее
раскатываются в книги серии через стандартный `./book.sh sync`.

**Принцип.** Один Markdown — много форматов. Pandoc как мост. Memoir + pandoc-template
для PDF, pygments для подсветки кода, fenced divs для учебниковых врезок, TikZ для схем,
qrcode-package для версионируемых QR-ссылок.

## Контекст: что было решено в сессии

| Решение | Обоснование |
| --- | --- |
| **A5 как основной формат** | Уже зафиксировано в metadata.yaml книги; разумно для технической литературы |
| **Ч/б, не цвет** | Малотиражный офсет с цветом дорог; различение синтаксиса через жирность/курсив работает не хуже, читается на E-Ink |
| **Memoir-класс под капотом** | Закрывает 80% книжной типографики; альтернативы (KOMA, classicthesis, tufte) не лучше |
| **Pandoc-template, не свой класс с нуля** | Сохраняет существующий Markdown как исходник; не требует переписывания готовых глав |
| **Кастомный 1С-лексер для pygments** | Встроенного нет; написан в сессии, работает |
| **Fenced divs для врезок** | Pandoc-нативный механизм без хаков; работает в EPUB/HTML параллельно через CSS-классы |
| **TikZ для схем** | Векторно, в одном источнике с текстом, fallback в SVG/PNG для веба/EPUB |
| **QR на тег git, не на main** | Ссылки замораживаются под версию книги; обновляются переизданием |
| **Twoside-колонтитулы**: глава слева, параграф справа | Канон книжной навигации |
| **Скриншоты 1С — открытый юридический вопрос** | Временно использовать TikZ-mockup'ы; согласовать права с фирмой «1С» отдельно |

## Карта артефактов

```
handoff/
├── HANDOFF.md                          ← этот файл
├── artifacts/                          ← готовый код, копировать в repo
│   ├── print.tex                       → theme/print.tex
│   ├── divs.tex                        → theme/divs.tex
│   └── highlight/
│       ├── onec_lexer.py               → theme/highlight/onec_lexer.py
│       └── pygstyle-bw.tex             → theme/highlight/pygstyle-bw.tex
├── spec/
│   └── print-edition.md                → spec/print-edition.md (SDD)
├── docs/
│   ├── format-strategy.md              → docs/format-strategy.md
│   ├── typography-russian.md           → docs/typography-russian.md
│   └── print-spec.md                   → docs/print-spec.md
├── backlog/
│   ├── sprint-1-print-ready.md         → docs/backlog/v0.2/sprint-1.md
│   ├── sprint-2-typography-apparat.md  → docs/backlog/v0.2/sprint-2.md
│   ├── sprint-3-images-qr.md           → docs/backlog/v0.2/sprint-3.md
│   ├── sprint-4-other-formats.md       → docs/backlog/v0.2/sprint-4.md
│   └── sprint-5-docs.md                → docs/backlog/v0.2/sprint-5.md
├── claude/
│   ├── CLAUDE-print-addendum.md        → мерж в CLAUDE.md
│   └── commands/
│       ├── print-check.md              → .claude/commands/print-check.md
│       └── template-spec-review.md     → .claude/commands/template-spec-review.md
├── samples/
│   ├── A5-sample-v4-qr.pdf             ← референс качества вёрстки
│   └── README.md                       ← как пересобрать референс
└── template-changes-v0.2.yaml          → заменить template-changes.yaml
```

## Алгоритм действий

```bash
# 1. Распаковать handoff рядом с book-template
unzip handoff.zip -d handoff

# 2. В клон book-template создать ветку
cd book-template
git checkout -b v0.2-print

# 3. Скопировать артефакты по карте (см. выше)
cp ../handoff/artifacts/print.tex theme/
cp ../handoff/artifacts/divs.tex theme/
mkdir -p theme/highlight
cp ../handoff/artifacts/highlight/* theme/highlight/
cp ../handoff/spec/print-edition.md spec/
cp ../handoff/docs/*.md docs/
mkdir -p docs/backlog/v0.2
cp ../handoff/backlog/* docs/backlog/v0.2/
mkdir -p .claude/commands
cp ../handoff/claude/commands/* .claude/commands/
cp ../handoff/template-changes-v0.2.yaml template-changes.yaml

# 4. Прочитать CLAUDE-print-addendum.md и вручную смержить в CLAUDE.md

# 5. Открыть в Claude Code
claude code .

# 6. Первый промпт в Claude Code:
#    "Прочитай spec/print-edition.md и docs/backlog/v0.2/sprint-1.md.
#     Сделай Спринт 1 по acceptance criteria."

# 7. После прохождения каждого спринта — коммит, тег rc.
#    После всех спринтов — финальный v0.2.0.
```

## Распространение в книги (после релиза v0.2.0)

Существующая sync-механика именно для этого и сделана. В каждой книге серии:

```bash
cd 1c-semantic-reading
./book.sh sync
# скрипт покажет, какие файлы template обновились
# принимаем: theme/, docs/, .claude/, spec/print-edition.md
# не принимаем: chapters/, metadata.yaml (книгоспецифично)

# проверяем что собирается
./book.sh build print

# результат: book.pdf в print-ready виде
```

Две существующие готовые книги («1С как иностранный язык» Модули 0–2)
становятся тестовым полигоном для миграции. На них же отлаживается то,
что вылезет на живом тексте.

## Что НЕ входит в этот пакет (открытые вопросы)

Список вещей, которые решаются вне `book-template`, в твоей реальности:

- ISBN на печатное издание и на EPUB отдельно (через РКП или сервис)
- УДК/ББК/авторский знак (любая научная библиотека)
- Правовой статус скриншотов UI 1С — формальное согласование с фирмой «1С»
- Выбор типографии под малотиражный офсет
- ICC-профиль под бумагу выбранной типографии
- Решение по типу переплёта (КБС / шитьё) и плотности бумаги
- Решение, оставлять ли FB2 для технических книг с эрзац-врезками или отключить
- Маркетинг, дистрибуция, ценообразование

## Версия пакета

handoff: v1.0, дата: июнь 2026
Совместимость: book-template ≥ v0.1.0
Целевая версия: book-template v0.2.0
