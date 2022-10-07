import sys
import importlib
from importlib import reload
sys.path.append('../..')

from squirrel import SquirrelCore

#operations = importlib.import_module('pyPullgerFootPrint.es.mcu.pares.pages.MovimientosMigratorios.detalle_form')
#operationName = 'getPersonCard'
#url = 'http://pares.mcu.es/MovimientosMigratorios/detalle.form?nid=12078'

# operations = importlib.import_module('pyPullgerFootPrint.es.mcu.pares.pages.MovimientosMigratorios.buscadorRaw')
operationName = 'getListOfCards'
url = 'http://pares.mcu.es/MovimientosMigratorios/buscadorRaw.form?d-3602157-p=1&objectsPerPage=25'


squirrel = SquairrelCore.Squirrel('selenium')
squirrel.initialize()
squirrel.get(url)

is_exit = False;


while is_exit == False:
    print('>>', end = '')
    in_command = input();

    if in_command.upper() == 'EXIT' or in_command.upper()  == 'E':
        is_exit = True;
    elif in_command.upper() == 'TEST' or in_command.upper()  == 'T':

        '''
        reload(detalle_form);
        from pyPullgerFootPrint.es.mcu.pares.pages.MovimientosMigratorios import detalle_form
        res1 = detalle_form.getPersonCard(squirrel)
        print(res1);
        '''

        # reload(operations);
        # try:
        #     res2 = getattr(operations, operationName)(squirrel)
        #     print(res2);
        # except Exception as e:
        #     print('error: ' + str(e))


#import importlib
#operations = importlib.import_module('..pyPullgerFootPrint.es.mcu.pares.pages.MovimientosMigratorios')
#res2 = getattr(operations, 'getPersonCard')(squirrel)

