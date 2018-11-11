#! /usr/bin/env python

import sys
from xml.etree import ElementTree
import os.path


vlc_pl_templ = 'vlc_pl_templ.xml'
vlc_pl_templ_ns = {
    'ns0': "http://xspf.org/ns/0/",
    'vlc': "http://www.videolan.org/vlc/playlist/ns/0/",
}
extension_application = 'http://www.videolan.org/vlc/playlist/0'


def show_usage():
    print('USAGE: %s [INFILE]' % sys.argv[0])


def load_mpc(file_name):
    pl_info = {}
    firstLine = True
    with open(file_name, mode='r') as f:
        lines = f.readlines()
        for line in lines:
            if firstLine:
                firstLine = False
                continue

            line = line.strip()
            splited = line.split(',')
            id = splited[0]
            _type = splited[1]
            data = splited[2]
            if not (id in pl_info):
                pl_info[id] = {_type: data}
            else:
                pl_info[id].update({_type: data})

    return pl_info


def fix_path_name(pl_info):
    for key in pl_info:
        pl_info[key]['filename'] = pl_info[key]['filename'].replace('\\', '/')
    return pl_info


def save_vlc(file_name, pl_info):
    # load template
    ns = vlc_pl_templ_ns
    ElementTree.register_namespace('', vlc_pl_templ_ns['ns0'])
    ElementTree.register_namespace('vlc', vlc_pl_templ_ns['vlc'])
    tree = ElementTree.parse(vlc_pl_templ)
    root = tree.getroot()

    # extract file name
    file_title = get_file_title(file_name)

    # title
    title = root.findall('./ns0:title', ns)[0]
    title.text = file_title

    # play list
    id_list = []
    track_list = root.findall('./ns0:trackList', ns)[0]
    for key in pl_info:
        # location
        media_path = 'file:///' + pl_info[key]['filename']
        track = ElementTree.SubElement(
            track_list, '{http://xspf.org/ns/0/}track')
        location = ElementTree.SubElement(
            track, '{http://xspf.org/ns/0/}location')
        location.text = media_path

        # extension
        extension = ElementTree.SubElement(
            track, '{http://xspf.org/ns/0/}extension')
        extension.attrib['application'] = extension_application

        # vlc:id
        id_text = str(int(key) - 1)
        id_list.append(id_text)
        vlc_id = ElementTree.SubElement(
            extension, '{http://www.videolan.org/vlc/playlist/ns/0/}id')
        vlc_id.text = id_text

    extension = root.findall('./ns0:extension', ns)[0]
    for tid in id_list:
        item = ElementTree.SubElement(
            extension, '{http://www.videolan.org/vlc/playlist/ns/0/}item')
        item.attrib['tid'] = tid

    # ElementTree.dump(extension)
    tree.write(file_title + '.xspf', encoding='utf-8', xml_declaration=True)


def get_file_title(path_name):
    path, _ = os.path.splitext(path_name)
    _, file_title = os.path.split(path)
    return file_title


if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_usage()
        exit(1)
    files = sys.argv[1:]
    for file_name in files:
        pl_info = load_mpc(file_name)
        fix_path_name(pl_info)
        # print(pl_info)
        save_vlc(file_name, pl_info)
