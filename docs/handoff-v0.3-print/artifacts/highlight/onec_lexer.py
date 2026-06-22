"""Pygments lexer for 1C query language."""
from pygments.lexer import RegexLexer, words
from pygments.token import (Comment, Keyword, Name, Number, Operator,
                            Punctuation, String, Text)


class OneCLexer(RegexLexer):
    name = "1C-Query"
    aliases = ["1c", "1cq"]
    filenames = ["*.bsl", "*.1cq"]

    flags = 0  # case-sensitive flag stays default; we handle via patterns

    KEYWORDS = (
        "ВЫБРАТЬ", "ИЗ", "ГДЕ", "СГРУППИРОВАТЬ", "ПО", "УПОРЯДОЧИТЬ",
        "ИМЕЮЩИЕ", "КАК", "ВНУТРЕННЕЕ", "ЛЕВОЕ", "ПРАВОЕ", "ПОЛНОЕ",
        "СОЕДИНЕНИЕ", "НА", "ОБЪЕДИНИТЬ", "ВСЕ", "РАЗЛИЧНЫЕ", "ПЕРВЫЕ",
        "ИЕРАРХИЯ", "ИТОГИ", "ИНДЕКСИРОВАТЬ", "ПОМЕСТИТЬ",
        "ВЫРАЗИТЬ", "ССЫЛКА", "ЕСТЬNULL",
        "ВЫБОР", "КОГДА", "ТОГДА", "ИНАЧЕ", "КОНЕЦ",
        "И", "ИЛИ", "НЕ", "МЕЖДУ", "В",
    )
    BUILTIN_FUNCS = (
        "СУММА", "КОЛИЧЕСТВО", "МАКСИМУМ", "МИНИМУМ", "СРЕДНЕЕ",
    )
    CONSTANTS = ("ИСТИНА", "ЛОЖЬ", "NULL")

    tokens = {
        "root": [
            (r"\s+", Text),
            (r"//[^\n]*", Comment.Single),
            (r"/\*", Comment.Multiline, "comment"),
            (r'"([^"\\]|\\.)*"', String.Double),
            (r"&[A-Za-zА-Яа-яЁё_][A-Za-zА-Яа-яЁё_0-9]*", Name.Variable),
            (r"\d+\.\d+", Number.Float),
            (r"\d+", Number.Integer),
            (words(KEYWORDS, prefix=r"(?i)\b", suffix=r"\b"), Keyword),
            (words(BUILTIN_FUNCS, prefix=r"(?i)\b", suffix=r"\b"), Name.Builtin),
            (words(CONSTANTS, prefix=r"(?i)\b", suffix=r"\b"), Keyword.Constant),
            (r"[A-Za-zА-Яа-яЁё_][A-Za-zА-Яа-яЁё_0-9]*", Name),
            (r"[<>!=]=?|<>", Operator),
            (r"[+\-*/]", Operator),
            (r"[(),.;]", Punctuation),
        ],
        "comment": [
            (r"[^*/]+", Comment.Multiline),
            (r"\*/", Comment.Multiline, "#pop"),
            (r"[*/]", Comment.Multiline),
        ],
    }
