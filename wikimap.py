#!/usr/bin/env python
#
#       wikimap.py
#
#       Copyright 2008 Edward A Robinson <earobinson@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import getopt
import os
import sys
import urllib
import urllib2
import xml.dom.minidom

from pygraphviz import *

BASE_URL = 'http://en.wikipedia.org/w/query.php'
DEFAULT_DEPTH_TO_DIVE = 1
DEFAULT_DRAW_PROGRAM = 'neato'
USAGE = '''Usage: wikimap.py [options] wiki_page

This program uses the wikipedia api to graph all the links to the wiki_page

Options:

    -d --depth : sets the depth of links to graph [optional, defaut ''' + str(DEFAULT_DEPTH_TO_DIVE) + ''']
    -h --help : print this help [optional]
    -p --drawProgram : pick the program used to draw the graph [optional, default ''' + DEFAULT_DRAW_PROGRAM + ''']

Example:

    wikimap.py -d 2 Norman_Graham'''

def find_link_tree(page, depth):
    linkGraph=AGraph(strict=False, directed=True)
    linkGraph.graph_attr['overlap']='false'

    seen_pages = [page]
    pageList = [page]
    depthDictionary = {page:0}
    linkFromDictionary = {page:''}

    while len(pageList) > 0:
        currentPage = pageList.pop(0)
        #print get_linkbacks(currentPage, linkFromDictionary) + ' depth:' + str(depthDictionary[currentPage])
        print get_linkbacks(currentPage, linkFromDictionary)
        linkedPages = find_links(currentPage)
        for newPage in linkedPages:
            #print currentPage + '->' + newPage
            linkGraph.add_edge(currentPage.encode('utf8'), newPage.encode('utf8'))

            if newPage not in seen_pages and depthDictionary[currentPage] < depth - 1:
                seen_pages.append(newPage)
                pageList.append(newPage)
                depthDictionary[newPage] = depthDictionary[currentPage] + 1
                linkFromDictionary[newPage] = currentPage

        #linkGraph.write(seen_pages[0] + '--' + str(depth) + '.dot')

    return linkGraph

def find_links(title):
    #print title

    #values = {'what': 'links', 'titles': title.encode('utf8'), 'bllimit': 10, 'format': 'xml'}
    values = {'what': 'links', 'titles': title.encode('utf8'), 'format': 'xml'}
    url = '?'.join([BASE_URL, urllib.urlencode(values)])
    request = urllib2.Request(url)
    #print url
    response = urllib2.urlopen(request)
    document = xml.dom.minidom.parse(response)

    node = xml_find(document.firstChild, 'pages/page/links')
    #print node.nodeName
    #print node.toxml()

    if node == None:
        return []
    else:
        linkedPages = []

        for childNode in node.childNodes:
            #print childNode.firstChild.nodeValue
            if valid_link(childNode):
                linkedPages.append(childNode.firstChild.nodeValue)

        #print linkedPages
        return linkedPages

def get_linkbacks(currentPage, linkFromDictionary):
    if currentPage == '':
        return ''
    else:
        return get_linkbacks(linkFromDictionary[currentPage], linkFromDictionary) + '/' + currentPage

def parse_args(args):
    try:
        shortflags = 'hd:p:'
        longflags = ['help', 'depth=', 'drawProgram=']
        opts, args = getopt.gnu_getopt(args, shortflags, longflags)
    except getopt.GetoptError:
        print_usage_and_exit(getopt.GetoptError.msg)

    depthToDive = DEFAULT_DEPTH_TO_DIVE
    drawProgram = DEFAULT_DRAW_PROGRAM

    for o, a in opts:
        if o in ("-h", "--help"):
            print_usage_and_exit()
        if o in ("-d", "--depth"):
            depthToDive = int(a)
        if o in ("-p", "--drawProgram"):
            drawProgram = a
    pageToMap = '_'.join(args)
    if not pageToMap:
        print_usage_and_exit('Could not read page name')
    return (pageToMap, depthToDive, drawProgram)

def print_usage_and_exit(message=None):
    if message:
        print "Error: %s" % message
        print USAGE
    sys.exit(2)

def valid_link(node):
    #if link.find('Wikipedia:') == 0 or link.find('Category:') == 0 or link.find('Template:') == 0:
    #    return False
    #print link

    return node.hasAttribute('ns') == False

def xml_find(node, name):
    ii = 0;

    nameList = name.split('/', 1)

    while (ii < len(node.childNodes) and node.childNodes[ii].nodeName != nameList[0]):
        #print node.childNodes[ii].nodeName
        ii = ii + 1

    if ii >= len(node.childNodes):
        return None

    if (len(nameList) == 1):
        return node.childNodes[ii]
    else:
        return xml_find(node.childNodes[ii], nameList[1])

def main():
    (pageToMap, depthToDive, drawProgram) = parse_args(sys.argv[1:])

    linkGraph = find_link_tree(pageToMap, depthToDive)

    linkGraph.graph_attr['label']='wikimap.py --depth=' + str(depthToDive) + ' --drawProgram=' + drawProgram + ' ' + pageToMap
    filename = pageToMap + '-' + str(depthToDive) + '-' + drawProgram
    linkGraph.write(filename + '.dot')
    linkGraph.layout(prog=drawProgram)
    linkGraph.draw(filename + '.svg', format='svg')
    #linkGraph.draw(pageToMap + '--' + str(depthToDive) + '.png')

    return 0

if __name__ == '__main__': main()
