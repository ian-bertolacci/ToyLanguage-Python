from __future__ import print_function

from Parser.ToyParser import *
from util import *
import argparse

argparser = argparse.ArgumentParser(description='ToyLanguage interpreter')
argparser.add_argument('files', metavar='file', type=str, nargs='+', help='source files')
argparser.add_argument('--debug', action='store_true', default=False, help='put parser in debug mode')

def main():
  args = argparser.parse_args()
  parser = get_parser( args.debug )

  for src_file in args.files:
    with open(src_file, 'r') as open_file:
      print( src_file )
      tree = parser.parse( open_file.read() )
      print( "\n\n".join( map( repr, tree ) ) )
if __name__ == "__main__":
  main()
