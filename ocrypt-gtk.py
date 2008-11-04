#! /usr/bin/env python
# -*- Python -*-
###########################################################################
#                        PyGtk fronted to OpenSSL                         #
#                        --------------------                             #
#                                                                         #
#  copyright            : Giuseppe "denever" Martino                      #
#  email                : denever@users.sf.net                            #
###########################################################################
###########################################################################
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 2 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program; if not, write to the Free Software            #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,             #
#  MA 02110-1301 USA                                                      #
#                                                                         #
###########################################################################
# Based on ocrypt.py from www.gianniamato.it

import pygtk

pygtk.require('2.0')
import os
import gtk
import string
from gtk import *
from gtk import glade

class Gui:
    def __init__(self):
        self.source = ''
        self.output = ''
        self.crypt = ''
        self.algo = ''
        self.base64 = ''

        self.wtree = glade.XML('glade/ocrypt.glade')
    	self.wtree.get_widget('wnd_main').show()

        self.btn_start = self.wtree.get_widget('btn_start')
        self.txt_passwd = self.wtree.get_widget('txt_passwd')

        dict = {}
	for key in dir(self.__class__):
	    dict[key] = getattr(self, key)

	self.wtree.signal_autoconnect(dict)

    def on_wnd_main_destroy(self, widget):
        gtk.main_quit()
        
    def on_cmb_crypt_changed(self, widget):
        if widget.get_active() == 0:
            self.crypt = ' -salt '
        else:
            self.crypt = ' -d -salt '
    
    def on_cmb_algo_changed(self, widget):
        if widget.get_active() == 0:
            self.algo = ' aes-256-cbc '
        if widget.get_active() == 1:
            self.algo = ' des3 '
        if widget.get_active() == 2:
            self.algo = ' bf '

    def on_chk_base64_toggled(self, widget):
        if widget.get_active():
            self.base64 = ' -a '
        else:
            self.base64 = ''

    def on_fcb_source_file_set(self, widget):
        self.source = widget.get_filename()
    
    def on_fcb_output_file_set(self, widget):
        self.output = widget.get_filename()

    def on_btn_start_clicked(self, widget):
	cmd = "openssl " + self.algo + self.crypt + self.base64
        cmd += " -in " + self.source + " -out " + self.output
        cmd += " -k " + self.txt_passwd.get_text()
	handle = os.popen(cmd, 'r')
	print string.join(handle.readlines())

if __name__ == "__main__":
    gui = Gui()
    main()
