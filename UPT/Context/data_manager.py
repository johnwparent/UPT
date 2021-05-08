import pickle, pickletools
import requests
import os, sys, re
from xml.etree import ElementTree
import glob
from .context import ContextManager, Context

def sanitze_data(data):
    SYMS = r'[^\s\w0-9\r\n\t]'
    ndata = re.sub(SYMS,"",data)
    data = ndata.lower()
    d_lst = data.split(" ")
    d_lst = [x for x in d_lst if x != " "]
    return d_lst


def walk_files_directory(entrypoint = None):
    if entrypoint is None:
        entrypoint = os.getcwd()
    file_ext = ".xml"
    file_lst = []
    with os.scandir(entrypoint) as dirs:
        for direc in dirs:
            file_lst.extend(find_file(direc, file_ext))
            if direc.is_dir():
                file_lst.extend(walk_files_directory(os.path.join(entrypoint, direc)))
    return file_lst

def find_file(direc, file_type=".txt"):
    files = glob.glob(os.path.join(direc, "*.rdf"))
    return files

def parse_node_attr(attr):
    for val in attr.values():
        _, ext = os.path.splitext(val)
        if ext == ".txt":
            return val
        else:
            return None

def find_url(file_):
    ns = {"dcterms": "http://purl.org/dc/terms/"}

    with open(file_, "r") as xml_direc:
        xml_parser = ElementTree.parse(xml_direc)
        xml_root = xml_parser.getroot()
        for node in xml_root.findall(".//dcterms:hasFormat", ns):
            url = xml_walker(node)
            if url:
                return url

def xml_walker(root):
    url = ""
    for child in root:
       url_t = parse_node_attr(child.attrib)
       if url_t:
           url = url_t
    return url

def pull_down_data(data_root):
    files = walk_files_directory(data_root)
    url = find_url(files[0])
    proj_gut = requests.get(url, stream=True)
    data = sanitze_data(proj_gut.text)
    build_context(data)

def load_context(self):
    pass
    # if we cant find binary pickle file, do the download step


def build_context(input):
    cm = ContextManager()
    head = iter(input)
    h_w = next(head)
    current = iter(input)
    tail = iter(input)
    t_w = next(tail)
    for word in current:
        if head:
            try:
                h_w = next(head)
            except StopIteration:
                head = None
                h_w = None

        if t_w != word:
            try:
                t_w = next(tail)
            except StopIteration:
                break

        cm[word].add_context(t_w, h_w)


    return cm

def data_to_disk():
    pass

def data_from_disk():
    pass