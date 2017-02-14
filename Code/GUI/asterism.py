import gi
from AVItoFITS import avi_to_fits
from AVItoFITS import avi_to_fits_black
from AVItoFITS import avi_to_fits_white
from AVItoFITS import avi_to_fits_grey
from astropy.io import fits
import numpy as np
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt 

gi.require_version('Gtk','3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):
	
	def __init__(self):
		Gtk.Window.__init__(self, title="Asterism")
		self.set_border_width(10)

		hb = Gtk.HeaderBar()
		hb.set_show_close_button(True)
		hb.props.title = "Asterism" 
		self.set_titlebar(hb)
		
		outer_box = Gtk.Box(spacing = 6)
		self.add(outer_box)
		
		stack = Gtk.Stack()
		stack.set_transition_type(Gtk.StackTransitionType.NONE)
		stack.set_transition_duration(1000)
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("AVI to FITS conversion - Dark Frame")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0) 
		
		button1 = Gtk.Button("Choose Folder")
		button1.connect("clicked",self.on_folder_clicked)
		ver_box.add(button1)
		
		button2 = Gtk.Button("Choose File")
		button2.connect("clicked",self.on_file_clicked)
		ver_box.add(button2)
		
		button3 = Gtk.Button("Split Dark Current AVI to Frames")
		button3.connect("clicked", self.begin_conversion_black)
		ver_box.add(button3)
		
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		
		label = Gtk.Label("Retain TIFs?")
		hor_box.pack_start(label, True, True, 0)
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		switch = Gtk.Switch()
		switch.connect("notify::active", self.on_switch_activated)
		switch.set_active(False)
		ver_box.pack_start(switch, True, True, 0)
		
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("AVI to FITS conversion - Bias Frame")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0) 
		
		button1 = Gtk.Button("Choose Folder")
		button1.connect("clicked",self.on_folder_clicked)
		ver_box.add(button1)
		
		button2 = Gtk.Button("Choose File")
		button2.connect("clicked",self.on_file_clicked)
		ver_box.add(button2)
		
		button3 = Gtk.Button("Split Bias AVI to Frames")
		button3.connect("clicked", self.begin_conversion_grey)
		ver_box.add(button3)
		
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		
		label = Gtk.Label("Retain TIFs?")
		hor_box.pack_start(label, True, True, 0)
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		switch = Gtk.Switch()
		switch.connect("notify::active", self.on_switch_activated)
		switch.set_active(False)
		ver_box.pack_start(switch, True, True, 0)
		
		listbox.add(row)
		
		stack.add_titled(listbox, "Dark Current & Bias Frame", "Dark Current & Bias Frame")
		
				
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("AVI to FITS conversion - Flat Field")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0) 
		
		button1 = Gtk.Button("Choose Folder")
		button1.connect("clicked",self.on_folder_clicked)
		ver_box.add(button1)
		
		button2 = Gtk.Button("Choose File")
		button2.connect("clicked",self.on_file_clicked)
		ver_box.add(button2)
		
		button3 = Gtk.Button("Split Flat Field AVI to Frames")
		button3.connect("clicked", self.begin_conversion_white)
		ver_box.add(button3)
		
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		
		label = Gtk.Label("Retain TIFs?")
		hor_box.pack_start(label, True, True, 0)
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		switch = Gtk.Switch()
		switch.connect("notify::active", self.on_switch_activated)
		switch.set_active(False)
		ver_box.pack_start(switch, True, True, 0)
		
		listbox.add(row)
		stack.add_titled(listbox, "Flat Field", "Flat Field")
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("AVI to FITS conversion")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0) 
		
		button1 = Gtk.Button("Choose Folder")
		button1.connect("clicked",self.on_folder_clicked)
		ver_box.add(button1)
		
		button2 = Gtk.Button("Choose File")
		button2.connect("clicked",self.on_file_clicked)
		ver_box.add(button2)
		
		button3 = Gtk.Button("Split AVI to Frames")
		button3.connect("clicked", self.begin_conversion)
		ver_box.add(button3)
		
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		
		label = Gtk.Label("Retain TIFs?")
		hor_box.pack_start(label, True, True, 0)
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		switch = Gtk.Switch()
		switch.connect("notify::active", self.on_switch_activated)
		switch.set_active(False)
		ver_box.pack_start(switch, True, True, 0)
		
		listbox.add(row)
		stack.add_titled(listbox, "Raw Data", "Raw Data")
		
		stack_sidebar = Gtk.StackSidebar()
		stack_sidebar.set_stack(stack)
		outer_box.pack_start(stack_sidebar, True, True, 0)
		outer_box.pack_end(stack, True, True, 0)

		frame = Gtk.Frame(label="Image")
		outer_box.pack_start(frame, True, True, 0)
		
		
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
			
	def begin_conversion_white(self, widget):
		global l
		global m
		global state
		if (l != 0):
			n = avi_to_fits_white(group=l, switch=state)
		if (m != 0):
			o = avi_to_fits_white(single=m, switch=state)
		else:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Files/Folders to Convert")
			wrn_dialog.format_secondary_text("Please Select a File or Folder")
			response = wrn_dialog.run()
			if response == Gtk.ResponseType.OK:
				print("Warning Accepted")
			elif response == Gtk.ResponseType.CANCEL:
				print("Warning Cancelled")
			wrn_dialog.destroy()
			
	def begin_conversion_black(self, widget):
		global l
		global m
		global state
		if (l != 0):
			n = avi_to_fits_black(group=l, switch=state)
		if (m != 0):
			o = avi_to_fits_black(single=m, switch=state)
		else:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Files/Folders to Convert")
			wrn_dialog.format_secondary_text("Please Select a File or Folder")
			response = wrn_dialog.run()
			if response == Gtk.ResponseType.OK:
				print("Warning Accepted")
			elif response == Gtk.ResponseType.CANCEL:
				print("Warning Cancelled")
			wrn_dialog.destroy()
			
	def begin_conversion_grey(self, widget):
		global l
		global m
		global state
		if (l != 0):
			n = avi_to_fits_grey(group=l, switch=state)
		if (m != 0):
			o = avi_to_fits_grey(single=m, switch=state)
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
