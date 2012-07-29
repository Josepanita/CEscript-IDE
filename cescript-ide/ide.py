#!/usr/bin/env python

import os, gtk, gobject, glib, vte, pango
from syntax import  CodeBuffer, SyntaxLoader

class InOut():

	def open(self, file):
		
		try:
			f = open(file, "rw")
			self.temp = False
			return f.read()
		except IOError:
			pass
		finally:
			f.close()

	def save(self, file, text):
		f = open(file, "w")
		try:
		    f.write(text)
		finally:
		    f.close()
		

class Window():
	"""IDE para CEscript"""
	
	def __init__(self):

		self.wd = "%s/Dropbox/Algoritmos/C/CEscript-dev/" % os.environ['HOME'];
		self.bin = "%scescript" % (self.wd)
		self.file = "-i"
		self.h = 400
		self.io = InOut()
		self.modified = False
	
	def create_menus(self):
		self.mb = gtk.MenuBar()

		filemenu = gtk.Menu()
		filem = gtk.MenuItem("Archivo")
		filem.set_submenu(filemenu)
       
		nuevo = gtk.MenuItem("Nuevo")
		nuevo.connect("activate", self.nuevo)
		filemenu.append(nuevo)

		abrir = gtk.MenuItem("Abrir")
		abrir.connect("activate", self.abrir)
		filemenu.append(abrir)

		guardar = gtk.MenuItem("Guardar")
		guardar.connect("activate", self.guardar)
		filemenu.append(guardar)

		guardarc = gtk.MenuItem("Guardar como...")
		guardarc.connect("activate", self.save_as)
		filemenu.append(guardarc)

		exit = gtk.MenuItem("Salir")
		exit.connect("activate", gtk.main_quit)
		filemenu.append(exit)

		self.mb.append(filem)
		return self.mb

	def create_main_window(self):
		self.window = gtk.Window()
		self.window.set_property("allow-shrink", True)
		self.window.set_default_size(-1, self.h)
		self.window.connect('delete-event', gtk.main_quit)
		self.window.connect("destroy", lambda w: gtk.main_quit())
		self.window.set_title("CEscript IDE")

	def create_console(self):
		self.terminal = vte.Terminal()
		self.terminal.fork_command("%s" % (self.bin), ["", self.file])
		return self.terminal

	def modify(self, boo):
		self.modified = boo

	def create_editor(self):
		frame1 = gtk.Frame("Editor")
		vbox = gtk.VBox(False, 5)

		scrwdw = gtk.ScrolledWindow()
		scrwdw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
		this = os.path.abspath(os.path.dirname(__file__))
		
		lang = SyntaxLoader(os.path.join(this, "syntax/cescript"))
		buff = CodeBuffer(lang=lang)

		self.textview = gtk.TextView(buff)
		self.buf = self.textview.get_buffer()
		self.buf.connect("changed", lambda x: self.modify(True))

		self.buf.set_text("")
		self.temp = True

		self.textview.set_wrap_mode(gtk.WRAP_WORD)
		
		vbox.pack_start(frame1, True, True, 0)
		frame1.add(scrwdw)
		scrwdw.add(self.textview)

		self.textview.set_editable(True)
		self.textview.set_cursor_visible(True)
		self.textview.set_size_request(-1, int(self.h/2.5))

		return vbox
	
	def create_panned_view(self):
		self.vpaned = gtk.VPaned()
		return self.vpaned

	def abrir(self, icon):
		dialog = gtk.FileChooserDialog("Abrir..",
							   None,
							   gtk.FILE_CHOOSER_ACTION_OPEN,
							   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
								gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)

		filter = gtk.FileFilter()
		filter.set_name("Scripts")
		filter.add_pattern("*.c")
		filter.add_pattern("*.pc")
		dialog.add_filter(filter)

		filter = gtk.FileFilter()
		filter.set_name("Todos los archivos")
		filter.add_pattern("*")
		dialog.add_filter(filter)

		

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			self.file = dialog.get_filename()
			self.buf.set_text(self.io.open(self.file))
			self.modified = False
			self.temp = False
		dialog.destroy()

	def save_dialog(self):
		dialog = gtk.FileChooserDialog("Guardar..",
							   None,
							   gtk.FILE_CHOOSER_ACTION_SAVE,
							   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
								gtk.STOCK_OPEN, gtk.RESPONSE_OK)
							   )
		
		dialog.set_default_response(gtk.RESPONSE_OK)

		filter = gtk.FileFilter()
		filter.set_name("Programa CEscript")
		filter.add_pattern("*.pc")
		dialog.add_filter(filter)

		filter = gtk.FileFilter()
		filter.set_name("Todos los archivos")
		filter.add_pattern("*.*")
		dialog.add_filter(filter)

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			start, end = self.buf.get_bounds()
			text = self.buf.get_text(start, end, include_hidden_chars=True)
			
			self.file = dialog.get_filename()
			self.io.save(self.file, text)
			self.buf.set_text(self.io.open(self.file))
			self.modified = False
		dialog.destroy()

	def confirm_new(self):
		messagedialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, "Aun hay cambios sin guardar, si crea un nuevo archivo se perderan los cambios.\nDesea crear un archivo nuevo?")
		response = messagedialog.run()
		
		if response == gtk.RESPONSE_YES:
			self.modified = False
			self.nuevo()

		messagedialog.destroy()

	def confirm_close(self):
		messagedialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO, "Aun hay cambios sin guardar, si crea un nuevo archivo se perderan los cambios.\nDesea salir?")
		response = messagedialog.run()
		messagedialog.destroy()

		if response == gtk.RESPONSE_YES:
			return True
		else:
			return False

	def quit(self):
		if self.modified:
			conf = self.confirm_close()
			if conf:
				gtk.main_quit()
		else:
			gtk.main_quit()


	def nuevo(self, e=None):
		if self.modified:
			self.confirm_new()
		else:
			self.buf.set_text("")
			self.temp = True

	def guardar(self, e=None):
		if self.temp:
			self.save_dialog()
			self.modified = False
			self.temp = False
		else:
			start, end = self.buf.get_bounds()
			text = self.buf.get_text(start, end, include_hidden_chars=True)
			self.io.save(self.file, text)
			self.modified = False
			self.temp = False

	def save_as(self, e=None):
		
		self.save_dialog()
		self.modified = False
		self.temp = False
		
	def compile(self, e=None):
		self.guardar()
		self.terminal.reset(True,True)
		self.terminal.fork_command("%s" % (self.bin), ["", self.file])
	
	def interactive(self, e=None):
		self.file = "-i"
		self.terminal.reset(True,True)
		self.terminal.fork_command("%s" % (self.bin), ["", self.file])
		
	def crear_toolbar(self):
		handle = gtk.HandleBox()

		toolbar = gtk.Toolbar()
		toolbar.set_size_request(200, 40)
		
		toolbutton1 = gtk.ToolButton(gtk.STOCK_NEW)
		toolbutton1.set_tooltip_text("Nuevo")
		toolbutton1.connect("clicked", self.nuevo)

		toolbutton2 = gtk.ToolButton(gtk.STOCK_OPEN)
		toolbutton2.set_tooltip_text("Abrir")
		toolbutton2.connect("clicked", self.abrir)

		toolbutton3 = gtk.ToolButton(gtk.STOCK_SAVE)
		toolbutton3.set_tooltip_text("Guardar")
		toolbutton3.connect("clicked", self.guardar)

		toolbutton4 = gtk.ToolButton(gtk.STOCK_EXECUTE)
		toolbutton4.set_tooltip_text("Ejecutar")
		toolbutton4.connect("clicked", self.compile)

		toolbar.add(toolbutton1)
		toolbar.add(toolbutton2)
		toolbar.add(toolbutton3)
		toolbar.add(toolbutton4)
		
#		handle.ser_property("expand", True)
		handle.add(toolbar)

		return handle

	def table(self):
		self.table = gtk.Table(4, 2)
		
		self.window.add(self.table)

	def key_press_event_cb(self, widget, event):
		from gtk.gdk import CONTROL_MASK
		if event.state & CONTROL_MASK:
			from gtk.gdk import keyval_name
			if keyval_name(event.keyval) == "n":
				self.nuevo()
				return True
			elif keyval_name(event.keyval) == "s":
				self.guardar()
				return True
			elif keyval_name(event.keyval) == "b":
				self.compile()
				return True
			elif keyval_name(event.keyval) == "q":
				self.quit()
				return True
			elif keyval_name(event.keyval) == "i":
				self.interactive()
				return True

				
			return False

	def main(self):
		self.create_main_window()
		self.table()

		self.window.connect("key-press-event",self.key_press_event_cb)

		self.toolbar = self.crear_toolbar()

		self.menus = self.create_menus()

		self.editor = self.create_editor()
		self.teminal = self.create_console()

		self.table.attach(self.menus,0,2,0,1)
		self.table.attach(self.toolbar,0,2,1,2)
		self.table.attach(self.editor,0,2,2,3)
		self.table.attach(self.terminal,0,2,3,4)

		self.window.show_all()
		gtk.main()

s = Window()
s.main()