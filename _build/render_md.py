#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Превращает _build/ch01.txt в читаемый markdown-оттиск (для предпросмотра).
Источник один — ch01.txt, оттиск не редактируется вручную."""
import re

src = open("_build/ch01.txt", encoding="utf-8").read().split("\n")
out = ["# Глава I. Открытие. Пустой дом", "", "*Часть первая. Осень рыцарства*", ""]
for line in src:
    line = line.rstrip()
    if not line:
        continue
    if line.startswith("|epigraph|"):
        out.append("> " + line[len("|epigraph|"):].strip())
        continue
    if line.startswith("|author|"):
        out.append(">")
        out.append("> *" + line[len("|author|"):].strip() + "*")
        out.append("")
        continue
    if line.startswith("---"):
        out.extend(["", "\\* \\* \\*", ""])
        continue
    if line.startswith("|p|"):
        out.extend([line[3:].strip(), ""])
        continue
    continue  # строка-заголовок учтена выше

md = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
open("_build/glava-01.md", "w", encoding="utf-8").write(md)
print("written", len(md))
