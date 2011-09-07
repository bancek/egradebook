@echo off
cd www
python manage.py graph_models -a -g > ..\infosys.dot
cd ..
dot infosys.dot -Tpng -o infosys.png