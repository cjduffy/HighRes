import gi
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
		
	def on_folder_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
		dialog.set_default_size(800,400)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print("select clicked")
			print("Folder Selected: " + dialog.get_filename())
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel Clicked")
				
		dialog.destroy()
		
			
	def on_file_clicked(self,widget):
		dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        		
		self.add_filters(dialog)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print("Open Clicked")
			print("File Selected: " + dialog.get_filename())
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")
		
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

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
