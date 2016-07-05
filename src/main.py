from __future__ import print_function

from Parser.ToyParser import *
from util import *
import argparse

argparser = argparse.ArgumentParser(description='ToyLanguage interpreter')
argparser.add_argument('files', metavar='file', type=str, nargs='+',
                    help='source files')

def main():
  args = argparser.parse_args()
  parser = get_parser()

  for src_file in args.files:
    with open(src_file, 'r') as open_file:
      print( src_file )
      tree = parser.parse( open_file.read() )
      print( "\n".join( map( repr, tree ) ) )
if __name__ == "__main__":
  main()
