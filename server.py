'''
 Author: Alexandre Ferri
 Created on Mon Jan 06 2020
'''

import os

from source import create_app
app = create_app()

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)