import gi
from AVItoFITS import avi_to_fits
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):
	
	def __init__(self):
		Gtk.Window.__init__(self, title="Asterism")
		self.set_border_width(10)
		self.set_default_size(400, 200)

		hb = Gtk.HeaderBar()
		hb.set_show_close_button(True)
		hb.props.title = "Asterism" 
		self.set_titlebar(hb)
		
		box = Gtk.Box(spacing = 10)
		self.add(box)
		
		button1 = Gtk.Button("Choose Folder")
		button1.connect("clicked",self.on_folder_clicked)
		box.add(button1)
		
		button2 = Gtk.Button("Choose File")
		button2.connect("clicked",self.on_file_clicked)
		box.add(button2)
		
		button3 = Gtk.Button("Start")
		button3.connect("clicked", self.begin_conversion)
		box.add(button3)
		
		switch = Gtk.Switch()
		switch.connect("notify::active", self.on_switch_activated)
		switch.set_active(False)
		box.pack_start(switch, True, True, 0)
		
		global l
		l = 0
		global m
		m = 0
		global state
		state = False
		
	def on_folder_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
		dialog.set_default_size(800,400)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			global l
			l = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("Folder Selection Cancelled")
				
		dialog.destroy()
		
			
	def on_file_clicked(self,widget):
		dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        		
		self.add_filters(dialog)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			global m
			m = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("File Selection Cancelled")
		
		dialog.destroy()
		
	def add_filters(self, dialog):
		filter_avi = Gtk.FileFilter()
		filter_avi.set_name("AVI Files")
		filter_avi.add_mime_type("video/avi")
		dialog.add_filter(filter_avi)
			
		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any File")
		filter_any.add_pattern("*")
		dialog.add_filter(filter_any)
		
	def on_switch_activated(self, switch, gparam):
		global state
		if switch.get_active():
			state = True
		else:
			state = False
		
	def begin_conversion(self, widget):
		global l
		global m
		global state
		if (l != 0):
			n = avi_to_fits(group=l, switch=state)
		if (m != 0):
			o = avi_to_fits(single=m, switch=state)
		else:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Files/Folders to Convert")
			wrn_dialog.format_secondary_text("Please Select a File or Folder")
			response = wrn_dialog.run()
			if response == Gtk.ResponseType.OK:
				print("Warning Accepted")
			elif response == Gtk.ResponseType.CANCEL:
				print("Warning Cancelled")
			wrn_dialog.destroy()

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
