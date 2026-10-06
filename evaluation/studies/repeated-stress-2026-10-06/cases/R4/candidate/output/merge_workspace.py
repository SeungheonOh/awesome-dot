"""Fictional local merge-queue consumer; maintenance scaffold."""
import copy
import difflib
import json
import os
from pathlib import Path
import re
import stat
import tempfile

MAX_BYTES=2_097_152
MAX_TEXT=100_000
MAX_DOCUMENTS=100

class ConflictPending(ValueError):
    pass

def _name(value):
    if not isinstance(value,str) or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}',value) is None:
        raise ValueError('invalid document name')
    return value

def _text(value):
    if not isinstance(value,str) or len(value)>MAX_TEXT:
        raise ValueError('text must be a string of at most 100000 characters')
    return value

def _hunks(base,variant):
    return [(i,j,tuple(variant[a:b])) for op,i,j,a,b in difflib.SequenceMatcher(a=base,b=variant,autojunk=False).get_opcodes() if op!='equal']

def _overlap(a,b):
    i,j,_=a;k,l,_=b
    if i==j and k==l:return i==k
    if i==j:return k<=i<=l
    if k==l:return i<=k<=j
    return max(i,k)<min(j,l)

def _merge(base,local,incoming):
    if local==base:return incoming,False
    if incoming==base or local==incoming:return local,False
    # The original consumer assumed remote updates never insert/delete lines.
    old=base.splitlines(keepends=True);left=local.splitlines(keepends=True);right=incoming.splitlines(keepends=True)
    if len(old)!=len(left) or len(old)!=len(right):return local,True
    result=[]
    for before,ours,theirs in zip(old,left,right):
        if ours!=before and theirs!=before and ours!=theirs:return local,True
        result.append(ours if ours!=before else theirs)
    return ''.join(result),False

def _document(value):
    if not isinstance(value,dict) or set(value)!={'name','base','text','conflict'}:raise ValueError('invalid document fields')
    name=_name(value['name']);base=_text(value['base']);text=_text(value['text']);conflict=value['conflict']
    if conflict is not None:
        if not isinstance(conflict,dict) or set(conflict)!={'base','local','incoming'}:raise ValueError('invalid conflict')
        for key in conflict:_text(conflict[key])
        if conflict['base']!=base or conflict['local']!=text:raise ValueError('inconsistent conflict')
    return name,{'base':base,'text':text,'conflict':copy.deepcopy(conflict)}

class MergeWorkspace:
    def __init__(self,root):
        self.root=Path(os.path.abspath(root))
        self.root.mkdir(exist_ok=True)
        fd=os.open(self.root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        self._docs={}
        try:
            try:f=os.open('workspace.json',os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
            except FileNotFoundError:return
            try:
                st=os.fstat(f)
                if not stat.S_ISREG(st.st_mode) or st.st_size>MAX_BYTES:raise ValueError('snapshot is not a bounded regular file')
                chunks=[];remaining=MAX_BYTES+1
                while remaining:
                    chunk=os.read(f,min(65536,remaining))
                    if not chunk:break
                    chunks.append(chunk);remaining-=len(chunk)
                raw=b''.join(chunks)
                if len(raw)>MAX_BYTES:raise ValueError('snapshot too large')
            finally:os.close(f)
        finally:os.close(fd)
        try:
            data=json.loads(raw)
            if not isinstance(data,dict) or set(data)!={'schema_version','documents'} or type(data['schema_version']) is not int or data['schema_version']!=1:raise ValueError('unsupported snapshot schema')
            if not isinstance(data['documents'],list) or len(data['documents'])>MAX_DOCUMENTS:raise ValueError('invalid document collection')
            docs={}
            for value in data['documents']:
                name,doc=_document(value)
                if name in docs:raise ValueError('duplicate name')
                docs[name]=doc
            self._docs=docs
        except (TypeError,KeyError,json.JSONDecodeError,UnicodeDecodeError) as e:raise ValueError('invalid snapshot') from e

    def names(self):return sorted(self._docs)

    def get(self,name):
        doc=dict(self._docs[name]);doc['dirty']=doc['text']!=doc['base'];return doc

    def add(self,name,text):
        name=_name(name);text=_text(text)
        if name in self._docs or len(self._docs)>=MAX_DOCUMENTS:raise ValueError('duplicate name or document limit')
        self._docs[name]={'base':text,'text':text,'conflict':None}
        return self.get(name)

    def edit(self,name,text):
        doc=self._docs[name];text=_text(text)
        doc['text']=text;return self.get(name)

    def receive(self,name,incoming):
        doc=self._docs[name];incoming=_text(incoming)
        merged,conflict=_merge(doc['base'],doc['text'],incoming)
        if conflict:doc['conflict']={'base':doc['base'],'local':doc['text'],'incoming':incoming}
        else:doc.update(base=incoming,text=merged)
        return self.get(name)

    def resolve(self,name,choice,text=None):
        doc=self._docs[name];conflict=doc['conflict']
        if conflict is None:raise ValueError('no pending conflict')
        if choice not in ('local','incoming','manual'):raise ValueError('invalid resolution')
        if choice=='manual':resolved=_text(text)
        else:
            if text is not None:raise ValueError('text only valid for manual resolution')
            resolved=conflict[choice]
        doc.update(base=resolved,text=resolved,conflict=None)
        return self.get(name)

    def rename(self,name,new_name):
        new_name=_name(new_name)
        if name not in self._docs:raise KeyError(name)
        if new_name==name:return self.get(name)
        if new_name in self._docs:raise ValueError('name exists')
        old=self._docs.pop(name)
        self._docs[new_name]={'base':old['text'],'text':old['text'],'conflict':None}
        return self.get(new_name)

    def remove(self,name):del self._docs[name]

    def save(self):
        # Legacy assumption: writing to disk makes a document clean.
        for doc in self._docs.values():
            doc['base']=doc['text']
            doc['conflict']=None
        data={'schema_version':1,'documents':[dict(name=name,**self._docs[name]) for name in self.names()]}
        raw=(json.dumps(data,ensure_ascii=False)+'\n').encode('utf8')
        if len(raw)>MAX_BYTES:raise ValueError('snapshot too large')
        target=self.root/'workspace.json'
        try:
            st=target.lstat()
            if not stat.S_ISREG(st.st_mode):raise ValueError('snapshot destination must be regular')
        except FileNotFoundError:pass
        target.write_bytes(raw)
