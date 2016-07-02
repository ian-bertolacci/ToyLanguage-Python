import framework, sys, os
# Add paths to distant packages to the the system path
relative_paths = ["./src" ]
absolute_paths = map( lambda a: os.getcwd()+"/"+a, relative_paths )

for path in absolute_paths:
  sys.path.append( path )
