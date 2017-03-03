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

class File_Folder_Dialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "No input detected", parent, 0,
            ("Folder", Gtk.ResponseType.ACCEPT,
             "File", Gtk.ResponseType.OK,
             "Cancel", Gtk.ResponseType.CANCEL))

        self.set_default_size(150, 100)

        label = Gtk.Label("Please Select Either a File or Folder")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class MyWindow(Gtk.Window):
	
	def __init__(self):
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
		
		global exp_time
		exp_time = 0
		global master_exp_time
		master_exp_time = 0 
		
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
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		
		label = Gtk.Label("Exposure Time (ms):")
		hor_box.pack_start(label, True, True, 0)
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		adjustment = Gtk.Adjustment(0, 0, 700000, 1, 10, 0)
		self.spinbutton = Gtk.SpinButton()
		self.spinbutton.set_adjustment(adjustment)
		self.spinbutton.set_digits(2)
		self.spinbutton.set_numeric(True)
		policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
		self.spinbutton.set_update_policy(policy)
		self.spinbutton.connect("value-changed", self.on_master_exp_time_changed)
		ver_box.pack_start(self.spinbutton, True, True, 0)
		
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
		button3.connect("clicked", self.begin_conversion_black_white)
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
		
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("Raw FITS Data Selection")
		head_box.pack_start(head_label, True, True, 0) 
		
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		button1 = Gtk.Button("Select a folder containing FITS")
		button1.connect("clicked", self.raw_folder_selection)
		ver_box.add(button1)
		
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		
		label = Gtk.Label("Exposure Time (ms):")
		hor_box.pack_start(label, True, True, 0)
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		adjustment = Gtk.Adjustment(0, 0, 100000, 1, 10, 0)
		self.spinbutton_2 = Gtk.SpinButton()
		self.spinbutton_2.set_adjustment(adjustment)
		self.spinbutton_2.set_digits(2)
		self.spinbutton_2.set_numeric(True)
		policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
		self.spinbutton_2.set_update_policy(policy)
		self.spinbutton_2.connect("value-changed", self.on_exp_time_changed)
		ver_box.pack_start(self.spinbutton_2, True, True, 0)
		
		listbox.add(row)
		
		stack.add_titled(listbox, "Raw Data", "Raw Data")
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		label = Gtk.Label("Lucky Frame Selection Method")
		head_box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		##To add. Radio Buttons to please Kristoff. Select whether one wants Sobel filter method or Fisher Sum method. If possible, add in a system to add another python function in that runs instead. Additionally a button that actually starts the process. A spinbutton to determine the percentage. 
		
		listbox.add(row)
		
		stack.add_titled(listbox, "Lucky Frame Selection", "Lucky Frame Selection")
		
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
		
		button1 = Gtk.Button("Retrieve Created Masters")
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
		global raw_in
		global single_raw
		global state
		condition = True
	
		while condition == True:
			if (raw_in != 0):
				n = AtF.avi_to_fits(group=raw_in, switch=state, Imtype="frame")
				condition = False
			if (single_raw != 0):
				o = AtF.avi_to_fits(single=single_raw, switch=state, Imtype="frame")
				condition = False
			else:
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Files/Folders to Convert")
				wrn_dialog.format_secondary_text("Please Select a File or Folder")
				response = wrn_dialog.run()
				wrn_dialog.destroy()
				if response == Gtk.ResponseType.OK:
					dialog = File_Folder_Dialog(self)
					response = dialog.run()
					if response == Gtk.ResponseType.CANCEL:
						print("Cancelling")
						dialog.destroy()
						condition = False
					elif response == Gtk.ResponseType.OK:
						dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
						response = dialog.run()
						if response == Gtk.ResponseType.OK:
							single_raw = dialog.get_filename()
						elif response == Gtk.ResponseType.CANCEL:
							condition = False 
						dialog.destroy()
						
					elif response == Gtk.ResponseType.ACCEPT:
						dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
						response = dialog.run()
						if response == Gtk.ResponseType.OK:
							raw_in = dialog.get_filename()
						elif response == Gtk.ResponseType.CANCEL:
							condition = False
						dialog.destroy()
					dialog.destroy()
						
					
				elif response == Gtk.ResponseType.CANCEL:
					condition = False
			
			
	def begin_conversion_black(self, widget):
		global dark_in
		global single_dark
		global state
		condition = True
	
		while condition == True:
			if (dark_in != 0):
				n = AtF.avi_to_fits(group=dark_in, switch=state, Imtype="dark")
				condition = False
			if (single_dark != 0):
				o = AtF.avi_to_fits(single=single_dark, switch=state, Imtype="dark")
				condition = False
			else:
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Files/Folders to Convert")
				wrn_dialog.format_secondary_text("Please Select a File or Folder")
				response = wrn_dialog.run()
				wrn_dialog.destroy()
				if response == Gtk.ResponseType.OK:
					dialog = File_Folder_Dialog(self)
					response = dialog.run()
					if response == Gtk.ResponseType.CANCEL:
						print("Cancelling")
						dialog.destroy()
						condition = False
					elif response == Gtk.ResponseType.OK:
						dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
						response = dialog.run()
						if response == Gtk.ResponseType.OK:
							single_dark = dialog.get_filename()
						elif response == Gtk.ResponseType.CANCEL:
							condition = False 
						dialog.destroy()
						
					elif response == Gtk.ResponseType.ACCEPT:
						dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
						response = dialog.run()
						if response == Gtk.ResponseType.OK:
							dark_in = dialog.get_filename()
						elif response == Gtk.ResponseType.CANCEL:
							condition = False
						dialog.destroy()
					dialog.destroy()
					
				elif response == Gtk.ResponseType.CANCEL:
					condition = False
			
	def begin_conversion_grey(self, widget):
		global bias_in
		global single_bias
		global state
		condition = True
	
		while condition == True:
			if (bias_in != 0):
				n = AtF.avi_to_fits(group=bias_in, switch=state, Imtype="bias")
				condition = False
			if (single_bias != 0):
				o = AtF.avi_to_fits(single=single_bias, switch=state, Imtype="bias")
				condition = False
			else:
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Files/Folders to Convert")
				wrn_dialog.format_secondary_text("Please Select a File or Folder")
				response = wrn_dialog.run()
				wrn_dialog.destroy()
				if response == Gtk.ResponseType.OK:
					dialog = File_Folder_Dialog(self)
					response = dialog.run()
					if response == Gtk.ResponseType.CANCEL:
						print("Cancelling")
						dialog.destroy()
						condition = False
					elif response == Gtk.ResponseType.OK:
						dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
						response = dialog.run()
						if response == Gtk.ResponseType.OK:
							single_bias = dialog.get_filename()
						elif response == Gtk.ResponseType.CANCEL:
							condition = False 
						dialog.destroy()
						
					elif response == Gtk.ResponseType.ACCEPT:
						dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
						response = dialog.run()
						if response == Gtk.ResponseType.OK:
							bias_in = dialog.get_filename()
						elif response == Gtk.ResponseType.CANCEL:
							condition = False
						dialog.destroy()
					dialog.destroy()
					
				elif response == Gtk.ResponseType.CANCEL:
					condition = False
			
	def begin_conversion_white(self, widget):
		global flat_in
		global single_flat
		global state
		condition = True
	
		while condition == True:
			if (flat_in != 0):
				n = AtF.avi_to_fits(group=flat_in, switch=state, Imtype="flat")
				condition = False
			if (single_flat != 0):
				o = AtF.avi_to_fits(single=single_flat, switch=state, Imtype="flat")
				condition = False
			else:
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Files/Folders to Convert")
				wrn_dialog.format_secondary_text("Please Select a File or Folder")
				response = wrn_dialog.run()
				wrn_dialog.destroy()
				if response == Gtk.ResponseType.OK:
					dialog = File_Folder_Dialog(self)
					response = dialog.run()
					if response == Gtk.ResponseType.CANCEL:
						print("Cancelling")
						dialog.destroy()
						condition = False
					elif response == Gtk.ResponseType.OK:
						dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
						response = dialog.run()
						if response == Gtk.ResponseType.OK:
							single_flat = dialog.get_filename()
						elif response == Gtk.ResponseType.CANCEL:
							condition = False 
						dialog.destroy()
						
					elif response == Gtk.ResponseType.ACCEPT:
						dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
						response = dialog.run()
						if response == Gtk.ResponseType.OK:
							flat_in = dialog.get_filename()
						elif response == Gtk.ResponseType.CANCEL:
							condition = False
						dialog.destroy()
					dialog.destroy()
						
					
				elif response == Gtk.ResponseType.CANCEL:
					condition = False
	
	def begin_conversion_black_white(self, widget):
		global flatdark_in
		global single_flatdark
		global state
		condition = True
	
		while condition == True:
			if (flatdark_in != 0):
				n = AtF.avi_to_fits(group=flatdark_in, switch=state, Imtype="flat_dark")
				condition = False
			if (single_flatdark != 0):
				o = AtF.avi_to_fits(single=singleflat_dark, switch=state, Imtype="flat_dark")
				condition = False
			else:
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Files/Folders to Convert")
				wrn_dialog.format_secondary_text("Please Select a File or Folder")
				response = wrn_dialog.run()
				wrn_dialog.destroy()
				if response == Gtk.ResponseType.OK:
					dialog = File_Folder_Dialog(self)
					response = dialog.run()
					if response == Gtk.ResponseType.CANCEL:
						print("Cancelling")
						dialog.destroy()
						condition = False
					elif response == Gtk.ResponseType.OK:
						dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
						response = dialog.run()
						if response == Gtk.ResponseType.OK:
							single_flatdark = dialog.get_filename()
						elif response == Gtk.ResponseType.CANCEL:
							condition = False 
						dialog.destroy()
						
					elif response == Gtk.ResponseType.ACCEPT:
						dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
						response = dialog.run()
						if response == Gtk.ResponseType.OK:
							flatdark_in = dialog.get_filename()
						elif response == Gtk.ResponseType.CANCEL:
							condition = False
						dialog.destroy()
					dialog.destroy()
					
				elif response == Gtk.ResponseType.CANCEL:
					condition = False
	
	def create_thermal_master(self,widget):
		global dark_in
		global bias_in
		
		if (dark_in == 0):
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Primary Folder Type")
			wrn_dialog.format_secondary_text("Please select a folder containing dark currents")
			response = wrn_dialog.run()
			if response == Gtk.ResponseType.OK:
				print("Warning Accepted")
			elif response == Gtk.ResponseType.CANCEL:
				print("Warning Cancelled")
			wrn_dialog.destroy()
			
		elif (bias_in == 0): 
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
			mc.master_creation(flat_in, flatdark_in, "flat", "flat_dark")

	def master_retrieval(self,widget):
		if (flat_in == 0) or (dark_in == 0):
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No files detected")
			wrn_dialog.format_secondary_text("Please select a folder containing files in the appropraite tab and create a master")
			response = wrn_dialog.run()
			if response == Gtk.ResponseType.OK:
				print("Warning Accepted")
			elif response == Gtk.ResponseType.CANCEL:
				print("Warning Cancelled")
			wrn_dialog.destroy()
		else: 
			global master_dark
			global master_flat
			master_dark = fits.open(dark_in+"/Master_dark.fits")
			master_flat = fits.open(flat_in+"/Master_flat.fits")
			
	def manual_master_dark(self,widget):
		global master_dark
		
		if (master_dark != 0):
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK_CANCEL, "Master Dark exists")
			dialog.format_secondary_text("A Master Dark file has already been loaded, do you wish to replace it?")
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				dialog = Gtk.FileChooserDialog("Select Master Dark File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
				response = dialog.run()
				if response == Gtk.ResponseType.OK:
					master_dark_file = dialog.get_filename()
					master_dark = fits.open(master_dark_file)
				elif response == Gtk.ResponseType.CANCEL:
					print("Dark selection cancelled")
					
				dialog.destroy()
			elif response == Gtk.ResponseType.CANCEL:
				print("Dark selection cancelled")
				
			dialog.destroy()
			
		else:
			dialog = Gtk.FileChooserDialog("Select Master Dark File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				master_dark_file = dialog.get_filename()
				master_dark = fits.open(master_dark_file)
			elif response == Gtk.ResponseType.CANCEL:
				print("Dark selection cancelled")
				
			dialog.destroy()
		
	def manual_master_flat(self,widget):
		global master_flat
		
		if (master_flat != 0):
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK_CANCEL, "Master Flat exists")
			dialog.format_secondary_text("A Master Flat file has already been loaded, do you wish to replace it?")
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				dialog = Gtk.FileChooserDialog("Select Master Flat File", self, Gtk.FileChooserAction.OPEN, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
				response = dialog.run()
				if response == Gtk.ResponseType.OK:
					master_flat_file = dialog.get_filename()
					master_flat = fits.open(master_flat_file)
				elif response == Gtk.ResponseType.CANCEL:
					print("Flat selection cancelled")
					
				dialog.destroy()
			elif response == Gtk.ResponseType.CANCEL:
				print("Flat selection cancelled")
				
			dialog.destroy()
			
		else:
			dialog = Gtk.FileChooserDialog("Select Master Flat File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				master_flat_file = dialog.get_filename()
				master_flat = fits.open(master_dark_file)
			elif response == Gtk.ResponseType.CANCEL:
				print("Flat selection cancelled")
				
			dialog.destroy()
		
	def darkflat_correction(self,widget):
		global master_dark
		global master_flat
		global raw_in
		global single_raw
		global exp_time
		global master_exp_time
		raw_style = 0
		
		checking_condition = True
		
		while checking_condition == True:
			if (master_dark == 0):
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No dark current file found")
				wrn_dialog.format_secondary_text("Missing a master, or a single, dark image. Select one now?")
				response = wrn_dialog.run()
				condition = True
				while condition == True: 
					if response == Gtk.ResponseType.OK:
						wrn_dialog.destroy()
						dialog = Gtk.FileChooserDialog("Select Master Dark File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
						response_2 = dialog.run()
						if response_2 == Gtk.ResponseType.OK:
							master_dark_filename = dialog.get_filename()
							if master_dark_filename.endswith(".fits"):
								master_dark = fits.open(master_dark_filename)
								condition = False
							else:
								wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "Invalid filetype")
								wrn_dialog.format_secondary_text("Please select a FITS file")
								response_3 = wrn_dialog.run()
								if response_3 == Gtk.ResponseType.OK:
									pass
								elif response_3 == Gtk.ResponseType.CANCEL:
									print("correction progress cancelled")
									condition = False
									checking_condition = False
								wrn_dialog.destroy()
							dialog.destroy()
						elif response_2 == Gtk.ResponseType.CANCEL:
							print("correction progress cancelled")
							condition = False
							checking_condition = False
							dialog.destroy()
						dialog.destroy()
					elif response == Gtk.ResponseType.CANCEL:
						print("correction progress cancelled")
						condition = False
						checking_condition = False
						
				wrn_dialog.destroy()
				
			elif (master_flat == 0):
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No flat field file found")
				wrn_dialog.format_secondary_text("Missing a master, or a single, flat field image. Select one now?")
				response = wrn_dialog.run()
				condition = True
				while condition == True: 
					if response == Gtk.ResponseType.OK:
						wrn_dialog.destroy()
						dialog = Gtk.FileChooserDialog("Select Master Flat File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
						response_2 = dialog.run()
						if response_2 == Gtk.ResponseType.OK:
							master_flat_filename = dialog.get_filename()
							if master_flat_filename.endswith(".fits"):
								master_flat = fits.open(master_flat_filename)
								condition = False
							else:
								wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "Invalid filetype")
								wrn_dialog.format_secondary_text("Please select a FITS file")
								response_3 = wrn_dialog.run()
								if response_3 == Gtk.ResponseType.OK:
									condition = True
								elif response_3 == Gtk.ResponseType.CANCEL:
									print("correction progress cancelled")
									condition = False
									checking_condition = False
								wrn_dialog.destroy()
								dialog.destroy()
						elif response_2 == Gtk.ResponseType.CANCEL:
							print("correction progress cancelled")
							condition = False
							checking_condition = False
							dialog.destroy()
						dialog.destroy()
					elif response == Gtk.ResponseType.CANCEL:
						print("correction progress cancelled")
						condition = False
						checking_condition = False
						
				wrn_dialog.destroy()
				
			elif (raw_style == 0):
				if (raw_in == 0):
					if (single_raw == 0): 
						info_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "No Raw File(s)")
						info_dialog.format_secondary_text("Please select a file or folder")
						info_dialog.run()
						info_dialog.destroy()
						
						dialog = File_Folder_Dialog(self)
						response = dialog.run()
						dialog.destroy()
						if response == Gtk.ResponseType.CANCEL:
							print("Cancelling")
							dialog.destroy()
							checking_condition = False
						elif response == Gtk.ResponseType.OK:
							dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
							response = dialog.run()
							if response == Gtk.ResponseType.OK:
								single_raw = dialog.get_filename()
								dialog.destroy()
							elif response == Gtk.ResponseType.CANCEL:
								dialog.destroy()
								checking_condition = False 
							dialog.destroy()
							
						elif response == Gtk.ResponseType.ACCEPT:
							dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
							response = dialog.run()
							if response == Gtk.ResponseType.OK:
								raw_in = dialog.get_filename()
								dialog.destroy()
							elif response == Gtk.ResponseType.CANCEL:
								dialog.destroy()
								checking_condition = False
							dialog.destroy()
						dialog.destroy()
							
					else:
						raw_style = single_raw
				else:
					raw_style = raw_in
				
			elif (exp_time == 0) or (master_exp_time == 0): 
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Exposure Time is Zero")
				wrn_dialog.format_secondary_text("Either the master dark exposure time is zero, or the raw image exposure time is zero, please give an exposure time and rerun")
				wrn_dialog.run()
				checking_condition = False
				wrn_dialog.destroy()
				
			else: 
				print("darkflat continues")
				df.darkflat(master_flat, master_dark, raw_style, exp_time, master_exp_time)
				checking_condition = False
				
	def raw_folder_selection(self,widget): 
		dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			raw_in = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			pass
		dialog.destroy()
		
	def on_exp_time_changed(self,widget):
		global exp_time
		exp_time = self.spinbutton_2.get_value()
		
	def on_master_exp_time_changed(self,widget): 
		global master_exp_time
		master_exp_time = self.spinbutton.get_value()
		
				
			
win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
