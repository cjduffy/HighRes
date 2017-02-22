import gi
import AVItoFITS as AtF
import mastercreation as mc
import darkflat as df
from astropy.io import fits
import numpy as np
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf

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
		button1.connect("clicked",self.on_folder_2_clicked)
		ver_box.add(button1)
		
		button2 = Gtk.Button("Choose File")
		button2.connect("clicked",self.on_file_2_clicked)
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
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		button1 = Gtk.Button("Create Scalable Thermal Frame")
		button1.connect("clicked", self.create_thermal_master)
		ver_box.add(button1)
		
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
		button1.connect("clicked",self.on_folder_3_clicked)
		ver_box.add(button1)
		
		button2 = Gtk.Button("Choose File")
		button2.connect("clicked",self.on_file_3_clicked)
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
		
		row = Gtk.ListBoxRow()
		
		head_box=Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("AVI to FITS conversion - Flat Dark")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0) 
		
		button1 = Gtk.Button("Choose Folder")
		button1.connect("clicked",self.on_folder_4_clicked)
		ver_box.add(button1)
		
		button2 = Gtk.Button("Choose File")
		button2.connect("clicked",self.on_file_4_clicked)
		ver_box.add(button2)
		
		button3 = Gtk.Button("Split Flat Field Dark Current AVI to Frames")
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
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		button1 = Gtk.Button("Create Scalable Flat Field")
		button1.connect("clicked", self.create_flat_master)
		ver_box.add(button1)
		
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
		button1.connect("clicked",self.on_folder_raw_clicked)
		ver_box.add(button1)
		
		button2 = Gtk.Button("Choose File")
		button2.connect("clicked",self.on_file_raw_clicked)
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
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("Automatic Master Retrieval")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		button1 = Gtk.Button("Retrieve Created Masters & Correct")
		button1.connect("clicked", self.master_retrieval)
		ver_box.pack_start(button1, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("Manual Master Selection")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		button1 = Gtk.Button("Select Master Flat Field")
		button1.connect("clicked", self.manual_master_flat)
		ver_box.pack_start(button1, True, True, 0)
		
		button2 = Gtk.Button("Select Master Dark Current")
		button2.connect("clicked", self.manual_master_dark)
		ver_box.pack_start(button2, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("Perform Dark Flat Correction")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		button1 = Gtk.Button("Perform Darkflat Correction")
		button1.connect("clicked", self.darkflat_correction)
		ver_box.pack_start(button1, True, True, 0)
		
		listbox.add(row)
		
		stack.add_titled(listbox, "Master Flat & Dark Correction", "Master Flat & Dark Correction")
		
		stack_sidebar = Gtk.StackSidebar()
		stack_sidebar.set_stack(stack)
		outer_box.pack_start(stack_sidebar, True, True, 0)
		outer_box.pack_end(stack, True, True, 0)

		pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("Andromeda.jpg", 600, 900, True)
		
		image = Gtk.Image()
		image.set_from_pixbuf(pixbuf)
		outer_box.pack_start(image, True, True, 0)
		
		##default settings
		global flat_in
		flat_in = 0
		global flatdark_in
		flatdark_in = 0 
		global dark_in
		dark_in = 0
		global bias_in 
		bias_in = 0
		global single_flat
		single_flat = 0
		global single_dark
		single_dark = 0
		global single_bias
		single_bias = 0 
		global single_flatdark
		single_flatdark = 0
		global raw_in
		raw_in = 0
		global single_raw
		single_raw = 0
		
		global state
		state = False
		
		global master_dark
		master_dark = 0 
		global master_flat
		master_flat = 0 
		
	def on_folder_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
		dialog.set_default_size(800,400)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			global dark_in
			dark_in = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("Folder Selection Cancelled")
				
		dialog.destroy()
		
	def on_folder_2_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
		dialog.set_default_size(800,400)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			global bias_in
			bias_in = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("Folder Selection Cancelled")
				
		dialog.destroy()
		
	def on_folder_3_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
		dialog.set_default_size(800,400)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			global flat_in
			flat_in = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("Folder Selection Cancelled")
				
		dialog.destroy()
		
	def on_folder_4_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
		dialog.set_default_size(800,400)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			global flatdark_in
			flatdark_in = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("Folder Selection Cancelled")
				
		dialog.destroy()
		
	def on_folder_raw_clicked(self, widget):
		dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
		dialog.set_default_size(800,400)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			global raw_in
			raw_in = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("Folder Selection Cancelled")
				
		dialog.destroy()
			
	def on_file_clicked(self,widget):
		dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        		
		self.add_filters(dialog)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			global single_dark
			single_dark = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("File Selection Cancelled")
			
		dialog.destroy()
			
	def on_file_2_clicked(self,widget):
		dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        		
		self.add_filters(dialog)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			global single_bias
			single_bias = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("File Selection Cancelled")
		
		dialog.destroy()
		
	def on_file_3_clicked(self,widget):
		dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        		
		self.add_filters(dialog)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			global single_flat
			single_flat = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("File Selection Cancelled")
		
	def on_file_4_clicked(self,widget):
		dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        		
		self.add_filters(dialog)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			global single_flatdark
			single_flatdark = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("File Selection Cancelled")
			
	def on_file_raw_clicked(self,widget):
		dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        		
		self.add_filters(dialog)
			
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			global single_raw
			single_raw = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("File Selection Cancelled")
		
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
		global raw_in
		global single_raw
		global state
		if (raw_in != 0):
			n = AtF.avi_to_fits(group=raw_in, switch=state, Imtype="frame")
		if (single_raw != 0):
			o = AtF.avi_to_fits(single=single_raw, switch=state, Imtype="frame")
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
		global dark_in
		global single_dark
		global state
		if (dark_in != 0):
			n = AtF.avi_to_fits(group=dark_in, switch=state, Imtype="dark")
		if (single_dark != 0):
			o = AtF.avi_to_fits(single=single_dark, switch=state, Imtype="dark")
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
		global bias_in
		global single_bias
		global state
		if (bias_in != 0):
			q = AtF.avi_to_fits(group=bias_in, switch=state, Imtype="bias")
		if (single_bias != 0):
			t = AtF.avi_to_fits(single=single_bias, switch=state, Imtype="bias")
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
		global flat_in
		global single_flat
		global state
		if (flat_in != 0):
			n = AtF.avi_to_fits(group=flat_in, switch=state, Imtype="flat")
		if (single_flat != 0):
			o = AtF.avi_to_fits(single=single_flat, switch=state, Imtype="flat")
		else:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Files/Folders to Convert")
			wrn_dialog.format_secondary_text("Please Select a File or Folder")
			response = wrn_dialog.run()
			if response == Gtk.ResponseType.OK:
				print("Warning Accepted")
			elif response == Gtk.ResponseType.CANCEL:
				print("Warning Cancelled")
			wrn_dialog.destroy()
	
	def begin_conversion_black_white(self, widget):
		global flatdark_in
		global single_flatdark
		global state
		if (flatdark_in != 0):
			q = AtF.avi_to_fits(group=flatdark_in, switch=state, Imtype="flat_dark")
		if (single_flatdark != 0):
			t = AtF.avi_to_fits(single=single_flatdark, switch=state, Imtype="flat_dark")
		else:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Files/Folders to Convert")
			wrn_dialog.format_secondary_text("Please Select a File or Folder")
			response = wrn_dialog.run()
			if response == Gtk.ResponseType.OK:
				print("Warning Accepted")
			elif response == Gtk.ResponseType.CANCEL:
				print("Warning Cancelled")
			wrn_dialog.destroy()
	
	def create_thermal_master(self,widget):
		global dark_in
		global bias_in
		
		if (l == 0):
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Primary Folder Type")
			wrn_dialog.format_secondary_text("Please select a folder containing dark currents")
			response = wrn_dialog.run()
			if response == Gtk.ResponseType.OK:
				print("Warning Accepted")
			elif response == Gtk.ResponseType.CANCEL:
				print("Warning Cancelled")
			wrn_dialog.destroy()
			
		elif (r == 0): 
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Secondary Folder Type")
			wrn_dialog.format_secondary_text("Please select a folder containing bias images")
			response = wrn_dialog.run()
			if response == Gtk.ResponseType.OK:
				print("Warning Accepted")
			elif response == Gtk.ResponseType.CANCEL:
				print("Warning Cancelled")
			wrn_dialog.destroy()
		
		else:
			mc.master_creation(dark_in, bias_in, "dark", "bias")
			
	def create_flat_master(self,widget):
		global flat_in
		global flatdark_in
		
		if (flat_in == 0):
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Primary Folder Type")
			wrn_dialog.format_secondary_text("Please select a folder containing flat fields")
			response = wrn_dialog.run()
			if response == Gtk.ResponseType.OK:
				print("Warning Accepted")
			elif response == Gtk.ResponseType.CANCEL:
				print("Warning Cancelled")
			wrn_dialog.destroy()
			
		elif (flatdark_in == 0): 
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Secondary Folder Type")
			wrn_dialog.format_secondary_text("Please select a folder containing flat darks")
			response = wrn_dialog.run()
			if response == Gtk.ResponseType.OK:
				print("Warning Accepted")
			elif response == Gtk.ResponseType.CANCEL:
				print("Warning Cancelled")
			wrn_dialog.destroy()
		
		else:
			mc.master_creation(flat_in, flatdark_in, "flat", "flatdarks")

	def master_retrieval(self,widget):
		print("automatic master retrieval")
			
	def manual_master_dark(self,widget):
		print("manual master dark selection")
		
	def manual_master_flat(self,widget):
		print("manual master flat selection")
		
	def darkflat_correction(self,widget):
		print("darkflat correction")
			
win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
