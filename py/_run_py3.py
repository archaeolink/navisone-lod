__author__ = "Florian Thiery, Dennis Gottwald"
__copyright__ = "MIT Licence 2020, RGZM, Florian Thiery"
__credits__ = ["Florian Thiery, Dennis Gottwald"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Florian Thiery"
__email__ = "thiery@rgzm.de"
__status__ = "1.0"

import glob
import os
import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = dir_path.replace("\\", "/")
# print(dir_path)
print("start _run_py3.py...")
dir_path_ttl = dir_path.replace("py", "data")
filelist = glob.glob(os.path.join(dir_path_ttl, "*.ttl"))
for f in filelist:
    os.remove(f)
print("removed all ttl files...")
print("*****************************************")

# py3

# information carrier

exec(open(dir_path + "/informationcarrier.py").read())
