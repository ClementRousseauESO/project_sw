from .data import *
from pathlib import Path
import sys
from uuid import uuid4, UUID

def parser(file: Path) -> parsed_file | None:
    if file.exists:
        p = parsed_file(name=file.name, items={}, pkg=None)
        with file.open(mode='r') as f:
            for line in f:
                _parse_line(line, p)
        return p
    else:
        return None
                
def _parse_line(line: str, p: parsed_file) -> None:
    s = line.lstrip().split(' ')
    for word in s:
        if p.active_items:
            last_id, last_mode = p.active_items[-1]
            last_item = p.items[last_id]
            if type(last_item) == package:
                _process_package(word=word, p=p, m=last_mode, i=last_id)
        else:
            _process_package(word=word, p=p, m=ongoing_mode.not_created, i=None)
            
def _process_package(word: str, p: parsed_file, m: ongoing_mode, i : UUID) -> None:
    if m == ongoing_mode.not_created:
        if word == 'package':
            if p.pkg:
                #TODO: handle error
                sys.exit(-1)
            else:
                new_id = uuid4()
                p.items[new_id] = (package(name=None, func=None, var=None), ongoing_mode.name)
                p.pkg = new_id
    else:
        pkg = p.items[i]
        #TODO: look for reserved words here
        if m == ongoing_mode.ano:
            if word == 'body':
                m = ongoing_mode.decl_ano
            else:
                pkg.name = word
                m = ongoing_mode.pre_defi
        elif m == ongoing_mode.decl_ano:
            pkg.name = word
            m = ongoing_mode.pre_decl
        elif m == ongoing_mode.pre_defi:
            if word == 'is':
                m = ongoing_mode.defi
            else:
                #TODO: handle error
                sys.exit(-1)
        elif m == ongoing_mode.defi:
            None
        elif m == ongoing_mode.pre_decl:
            if word == 'is':
                m = ongoing_mode.decl
            else:
                #TODO: handle error
                sys.exit(-1)
        elif m == ongoing_mode.decl:
            None