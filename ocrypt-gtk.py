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

        # Read glade file
        self.wtree = glade.XML('glade/ocrypt.glade')

        # Show wnd_main main window
    	self.wtree.get_widget('wnd_main').show()

        # Get btn_start button object from glade
        self.btn_start = self.wtree.get_widget('btn_start')

        # Get txt_passwd button object from glade
        self.txt_passwd = self.wtree.get_widget('txt_passwd')

        # Create a dictionary with method names of this class
        dict = {}
	for key in dir(self.__class__):
	    dict[key] = getattr(self, key)

        # Autoconnect signals to method names
	self.wtree.signal_autoconnect(dict)

    def on_wnd_main_destroy(self, widget):
        gtk.main_quit()
        
    def on_cmb_crypt_changed(self, widget):
        if widget.get_active() == 0: # if selected item is the first
            self.crypt = ' -salt '
            self.btn_start.set_label('Crypt')
        else:
            self.crypt = ' -d -salt '
            self.btn_start.set_label('Decrypt')
        self.wtree.get_widget('cmb_algo').set_sensitive(True)
    
    def on_cmb_algo_changed(self, widget):
        if widget.get_active() == 0: # if selected item is the first
            self.algo = ' aes-256-cbc '
        if widget.get_active() == 1: # if selected item is the second
            self.algo = ' des3 '
        if widget.get_active() == 2: # if selected item is the third
            self.algo = ' bf '
        self.wtree.get_widget('fcb_source').set_sensitive(True)

    def on_chk_base64_toggled(self, widget):
        if widget.get_active(): # if selected item is the first
            self.base64 = ' -a '
        else:
            self.base64 = ''

    def on_txt_passwd_key_press_event(self, widget, event):
        if gtk.gdk.keyval_name(event.keyval) == 'Return':
            self.on_btn_start_clicked(widget)

    def on_fcb_source_file_set(self, widget):
        self.source = widget.get_filename()
        self.wtree.get_widget('fcb_output').set_sensitive(True)
        
    def on_fcb_output_file_set(self, widget):
        self.output = widget.get_filename()
        self.wtree.get_widget('txt_passwd').set_sensitive(True)
        self.wtree.get_widget('btn_start').set_sensitive(True)
        
    def on_btn_start_clicked(self, widget):
	cmd = "openssl " + self.algo + self.crypt + self.base64
        cmd += " -in " + self.source + " -out " + self.output
        cmd += " -k " + self.txt_passwd.get_text()
	handle = os.popen(cmd, 'r')
	print string.join(handle.readlines())
        self.txt_passwd.set_text('')

if __name__ == "__main__":
    gui = Gui()
    main()
