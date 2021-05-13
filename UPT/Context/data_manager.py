import pickle
import requests
import os, re
from xml.etree import ElementTree
import glob
from .context import ContextManager

def sanitze_data(data):
    SYMS = r'[^\w ]'
    ndata = re.sub(SYMS,"",data,flags=re.ASCII)
    data = ndata.lower()
    d_lst = data.split(" ")
    d_lst = [x for x in d_lst if x != " " and x != ""]
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

    with open(file_, "r",encoding='utf-8') as xml_direc:
        try:
            xml_parser = ElementTree.parse(xml_direc)
            xml_root = xml_parser.getroot()
            for node in xml_root.findall(".//dcterms:hasFormat", ns):
                url = xml_walker(node)
                if url:
                    return url
        except UnicodeDecodeError:
            print("Unable to read file %s; UnicodeDecodeError"%file_)
        return None

def xml_walker(root):
    url = ""
    for child in root:
       url_t = parse_node_attr(child.attrib)
       if url_t:
           url = url_t
    return url

def pull_down_data(data_root):
    files = walk_files_directory(data_root)
    print(len(files))
    urls = []
    for x in range(100):
        url = find_url(files[x])
        if url:
            urls.append(url)
    data = []
    for url in urls:
        proj_gut = requests.get(url, stream=True)
        data.extend(sanitze_data(proj_gut.text))

    return build_context(data)

def load_context(data):
    data_dir = "../../data/context.pickle"
    cm = None
    curr_path = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(curr_path,data_dir)
    if not os.path.exists(data_dir):
        print("Pulling data from proj gut")
        cm = pull_down_data(data)
        print("done pulling data from gut")
        with open(data_dir,"wb") as pickle_data:
            pickle.dump(cm, pickle_data, -1)
    else:
        with open(data_dir,"rb") as pickle_data:
            cm = pickle.load(pickle_data)
    return cm

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

        if t_w == word:
            try:
                word = next(current)
            except StopIteration:
                break
        else:
            try:
                t_w = next(tail)
            except StopIteration:
                break

        cm[word].add_context(t_w, h_w)


    return cm
