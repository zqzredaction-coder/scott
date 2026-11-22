#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка fb2: правка Главы I «Открытие. Пустой дом» (Часть I «Осень рыцарства»).
Исходник главы — _build/ch01.txt (строки: |p|, |epigraph|, |author|, ---).
Правит файл книги на месте, остальные главы не трогает.
"""
import re, sys, shutil, os

BOOK = "Скотт Вальтер. Айвенго (с иллюстрациями) - royallib.com.fb2"
SRC = "_build/ch01.txt"

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def convert(path):
    out = []
    out.append('<title><p>ЧАСТЬ ПЕРВАЯ. ОСЕНЬ РЫЦАРСТВА</p><empty-line/><p>Глава I. Открытие. Пустой дом</p></title>')
    epi = None
    first_para = True
    for raw in open(path, encoding="utf-8").read().split("\n"):
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("|epigraph|"):
            txt = line[len("|epigraph|"):].strip()
            if epi is None:
                epi = [esc(txt)]
            else:
                epi.append(esc(txt))
            continue
        if line.startswith("|author|"):
            body = "".join("<p>%s</p>" % t for t in epi)
            epi = None
            out.append("<epigraph>%s<text-author>%s</text-author></epigraph>"
                       % (body, esc(line[len("|author|"):].strip())))
            continue
        if line.startswith("|p|"):
            txt = esc(line[3:].strip())
        elif line.startswith("---"):
            out.append("<empty-line/><p>* * * * *</p><empty-line/>")
            continue
        else:  # строка-заголовок, уже добавлена
            continue
        if first_para:
            out.append("<empty-line/>")
            first_para = False
        out.append("<p>%s</p>" % txt)
    return "<section>" + "".join(out) + "</section>"

def main():
    if not os.path.exists(BOOK):
        sys.exit("no book")
    data = open(BOOK, encoding="utf-8").read()
    # Поддерживаем как исходную разметку Айвенго, так и уже собранную главу:
    # повторный запуск должен обновлять главу I, а не завершаться ошибкой.
    start_match = re.search(
        r'<section><title>(?:(?!</title>).)*?<p>Глава I(?:</p>|\.[^<]*</p>)</title>',
        data,
        re.S,
    )
    i = start_match.start() if start_match else -1
    j = data.find("<section><title><p>Глава II</p></title>", i if i >= 0 else 0)
    if i < 0 or j < 0 or j < i:
        sys.exit("chapter markers not found")
    new = convert(SRC)
    if len(new) < 20000:
        sys.exit("chapter too short, abort")
    data = data[:i] + new + data[j:]
    open(BOOK, "w", encoding="utf-8").write(data)

    import xml.etree.ElementTree as ET
    ET.parse(BOOK)
    print("ok, ch1 length:", len(new))

if __name__ == "__main__":
    main()
