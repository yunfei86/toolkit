#This script generates documentation for the Framework
#Please generate documentation on your local copy and do not check it in
#!/bin/sh
echo "Generating Documentation for iFramework"
find . -name "*.pyc" -exec rm {} \;

if [ -d docs ]; then
    echo "docs directory exists already"
else
    mkdir docs
    echo "Creating docs directory"
fi
epydoc -v -o docs --name "Ion Test Framework Documentation" --css white --inheritance grouped --graph=all src/utils/*.py src/ionunittest/ `find testdir -name '*.py'` 
