import gi
import AVItoFITS as AtF
import mastercreation as mc
import luckyframeselection as lfs
import darkflat as df
from astropy.io import fits
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("GTK3Cairo")
import matplotlib.pyplot as plt
import random
import os
import math
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
import hotpixel as hp

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf

gi.require_version('Gtk','3.0')
from gi.repository import Gtk

class master_structure:
	
	def __init__ (self):
		self.master_dark = 0
		self.master_flat = 0 
		
	def set_master_filename(mode, data):
		if mode == "dark":
			self.master_dark_filename = data
		elif mode == "flat":
			self.master_flat_filename = data
	
	def get_master_filename(mode):
		if mode == "dark":
			return(self.master_dark_filename)
		elif mode == "flat":
			return(self.master_flat_filename)	
	
	def set_master(mode, data):
		if mode == "dark":
			self.master_dark = data
		elif mode == "flat":
			self.master_flat = data
	
	def set_exposure_time(data):
		self.master_dark_exposure_time = data

class data_structure:
	
	def __init__(self, data_type):
		self.data_type = data_type
		self.data = 0
		self.data_mode = 0
		self.raw_data = 0 
	
	def set_data(self, data):
		self.data = data
	
	def set_type(self, data_type):
		self.data_type = data_type
		
	def set_mode(self, data_mode):
		self.data_mode = data_mode
	
	def set_raw_data(self, raw_data):
		self.raw_data = raw_data
		
	def set_raw_exp(self, raw_exp_time):
		self.raw_exp_time = raw_exp_time
		

class File_Folder_Dialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "File or Folder Selection Required", parent, 0,
            ("Folder", Gtk.ResponseType.ACCEPT,
             "File", Gtk.ResponseType.OK,
             "Cancel", Gtk.ResponseType.CANCEL))

        self.set_default_size(150, 100)

        label = Gtk.Label("Please Select Either a File or Folder")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class Asterism(Gtk.Window):
	
	def __init__(self):
		##default settings
		dark = data_structure("dark")
		flat = data_structure("flat")
		bias = data_structure("bias")
		flatdark = data_structure("flat_dark")
		raw = data_structure("raw")
		data_list = [dark, bias, flat, flatdark, raw]
		state = False
		masters = master_structure()
		luck_delete = "Delete"
		exp_time = 0
		master_exp_time = 0
		percentage = 0
		methodology = "Sobel"
		histograms = []
		histogram_plot = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, False, 8, 1, 1)
		histogram_no = 0 
		hist_count = 0
		int_hist = 0
		thresholds = 0
		
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
		
		button1 = Gtk.Button("Choose Input")
		button1.connect("clicked",self.input_selection, 0, data_list)
		ver_box.add(button1)
		
		button3 = Gtk.Button("Split Dark Current AVI to Frames")
		button3.connect("clicked", self.convert_to_fits, 0, data_list, state)
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
		
		button1 = Gtk.Button("Choose Input")
		button1.connect("clicked",self.input_selection, 1, data_list)
		ver_box.add(button1)

		button3 = Gtk.Button("Split Bias AVI to Frames")
		button3.connect("clicked", self.convert_to_fits, 1, data_list, state)
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
		button1.connect("clicked", self.create_master, data_list, "dark")
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
		
		button1 = Gtk.Button("Choose Input")
		button1.connect("clicked",self.input_selection, 2, data_list)
		ver_box.add(button1)
		
		button3 = Gtk.Button("Split Flat Field AVI to Frames")
		button3.connect("clicked", self.convert_to_fits, 2, data_list, state)
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
		
		button1 = Gtk.Button("Choose Input")
		button1.connect("clicked", self.input_selection, 3, data_list)
		ver_box.add(button1)
		
		button3 = Gtk.Button("Split Flat Field Dark Current AVI to Frames")
		button3.connect("clicked", self.convert_to_fits, 3, data_list, state)
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
		
		button1 = Gtk.Button("Create Master Flat Field")
		button1.connect("clicked", self.create_master, data_list, "flat")
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
		
		button1 = Gtk.Button("Choose Input")
		button1.connect("clicked",self.input_selection, 4, data_list)
		ver_box.add(button1)
		
		button3 = Gtk.Button("Split AVI to Frames")
		button3.connect("clicked", self.convert_to_fits, 4, data_list, state)
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
		button1.connect("clicked", self.raw_folder_selection, data_list)
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
		self.spinbutton_2.connect("value-changed", self.on_exp_time_changed, data_list)
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
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		button1 = Gtk.RadioButton.new_with_label_from_widget(None, "Sobel Method")
		button1.connect("toggled", self.on_methodology_changed, "Sobel")
		ver_box.pack_start(button1, True, True, 0)
		
		button2 = Gtk.RadioButton.new_from_widget(button1)
		button2.set_label("Fisher Selection")
		button2.connect("toggled", self.on_methodology_changed, "Fisher")
		ver_box.pack_start(button2, True, True, 0) 
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		
		label = Gtk.Label("Lower Percentage Limit:")
		hor_box.pack_start(label, True, True, 0)
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
		self.spinbutton_3 = Gtk.SpinButton()
		self.spinbutton_3.set_adjustment(adjustment)
		self.spinbutton_3.set_numeric(True)
		policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
		self.spinbutton_3.set_update_policy(policy)
		self.spinbutton_3.connect("value-changed", self.on_percent_changed)
		ver_box.pack_start(self.spinbutton_3, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		
		label = Gtk.Label("Delete Non-Lucky Frames?")
		hor_box.pack_start(label, True, True, 0)
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		switch = Gtk.Switch()
		switch.connect("notify::active", self.luckframedelete)
		switch.set_active(True)
		ver_box.pack_start(switch, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
		hor_box.pack_start(ver_box, True, True, 0)
		
		button1 = Gtk.Button("Select Lucky Frames")
		button1.connect("clicked", self.luckframeselection)
		ver_box.pack_start(button1, True, True, 0)
		
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
		button1.connect("clicked", self.master_retrieval, master_structure)
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
		button1.connect("clicked", self.manual_master_selection, "flat", master_structure)
		ver_box.pack_start(button1, True, True, 0)
		
		button2 = Gtk.Button("Select Master Dark Current")
		button2.connect("clicked", self.manual_master_selection, "dark", master_structure)
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
		button1.connect("clicked", self.darkflat_correction, master_structure, data_list)
		ver_box.pack_start(button1, True, True, 0)
		
		listbox.add(row)
		
		stack.add_titled(listbox, "Master Flat & Dark Correction", "Master Flat & Dark Correction")
		
		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_window.show()
		scrolled_window.set_min_content_width(390)
		
		listbox = Gtk.ListBox()
		scrolled_window.add(listbox)
		listbox.set_selection_mode(Gtk.SelectionMode.NONE) 
		
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("Hot Pixel Correction System")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		box = Gtk.Box()
		row.add(box)
		label = Gtk.Label("Automatic Correction")
		box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		button1 = Gtk.Button("Perform Automatic Hot-Pixel Correction")
		button1.connect("clicked", self.auto_hot_pixel)
		ver_box.pack_start(button1, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		box = Gtk.Box()
		row.add(box)
		label = Gtk.Label("Manual Correction")
		box.pack_start(label, True, True, 0) 
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		box = Gtk.Box()
		row.add(box)
		label = Gtk.Label("Histogram Generation")
		box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		
		label = Gtk.Label("Number of Sample Histograms to Generate:")
		hor_box.pack_start(label, True, True, 0)
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0) 
		
		adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
		self.spinbutton_4 = Gtk.SpinButton()
		self.spinbutton_4.set_adjustment(adjustment)
		self.spinbutton_4.set_numeric(True)
		policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
		self.spinbutton_4.set_update_policy(policy)
		self.spinbutton_4.connect("value-changed", self.histogram_number)
		ver_box.pack_start(self.spinbutton_4, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		button1 = Gtk.Button("Generate First Histogram")
		button1.connect("clicked", self.gen_hist_one, data_list, histogram_no, hist_count, histograms, int_hist)
		ver_box.pack_start(button1, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		row.add(head_box)
		fig = plt.figure()
		canvas = FigureCanvas(fig)
		canvas.set_size_request(350,350)
		head_box.pack_start(canvas, True, True, 0)
		
		toolbar = NavigationToolbar(canvas, Asterism)
		head_box.pack_start(toolbar, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		row.add(ver_box)
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		ver_box.pack_start(hor_box, True, True, 0)
		
		label = Gtk.Label("Enter Threshold Value:\n(Press Enter to Confirm)")
		hor_box.pack_start(label, True, True, 0)
		
		hist_entry = Gtk.Entry()
		hist_entry.connect("activate", self.add_hist_thresh, hist_count, thresholds)
		hor_box.pack_start(hist_entry, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		row.add(ver_box)
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		ver_box.pack_start(hor_box, True, True, 0)
		
		button1 = Gtk.Button("Previous Histogram")
		button1.connect("clicked", self.gen_prev_hist, histograms, hist_count, int_hist)
		hor_box.pack_start(button1, True, True, 0)
		
		button2 = Gtk.Button("Next Histogram")
		button2.connect("clicked", self.gen_next_hist, histograms, hist_count, int_hist)
		hor_box.pack_start(button2, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		box = Gtk.Box()
		row.add(box)
		label = Gtk.Label("Correct Hot Pixels")
		box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		button1 = Gtk.Button("Perform Hot Pixel Correction")
		button1.connect("clicked", self.man_hot_pixel)
		ver_box.pack_start(button1, True, True, 0) 
		
		listbox.add(row)
		
		stack.add_titled(scrolled_window, "Hot Pixel Correction", "Hot Pixel Correction")
		
		stack_sidebar = Gtk.StackSidebar()
		stack_sidebar.set_stack(stack)
		outer_box.pack_start(stack_sidebar, True, True, 0)
		outer_box.pack_end(stack, True, True, 0)

		pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("Andromeda.jpg", 670, 1200, True)
		
		image = Gtk.Image()
		image.set_from_pixbuf(pixbuf)
		outer_box.pack_start(image, True, True, 0)
		
	##Functions
		
	def input_selection(self, widget, data_type, data_list):
		dialog = File_Folder_Dialog(self)
		response = dialog.run()
		dialog.destroy()
		if response == Gtk.ResponseType.ACCEPT:
			dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				folder = dialog.get_filename()
				data_list[data_type].set_data(folder)
				data_list[data_type].set_mode("group")
				dialog.destroy()
			elif response == Gtk.ResponseType.CANCEL:
				print("Folder Selection Cancelled")
				dialog.destroy()
			dialog.destroy()
		elif response == Gtk.ResponseType.OK:
			dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				filename = dialog.get_filename()
				data_list[data_type].set_data(filename)
				data_list[data_type].set_mode("single")
				dialog.destroy()
			elif response == Gtk.ResponseType.CANCEL:
				print("File Selection Cancelled")
				dialog.destroy()
			dialog.destroy()
		elif response == Gtk.ResponseType.CANCEL:
			print("Selection Cancelled")
		return(data_list)
		
	def raw_folder_selection(self, widget, data_list): 
		dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			data_list[4].set_raw_data = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			pass
		dialog.destroy()
		return(data_list)
		
	def on_switch_activated(self, switch, gparam):
		if switch.get_active():
			state = True
		else:
			state = False
		return(state)
			
	def convert_to_fits(self, widget, data_type, data_list, state):
		fits_response = AtF.avi_to_fits(data_list, data_type, state)
		return(fits_response)
		
	def create_master(self, widget, data_list, mode):
		if mode == "dark":
			stage = 0
		elif mode == "flat":
			stage = 2	
		counter = stage	
		for counter in range(stage, stage+1):
			if data_list[counter].data == 0:
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "File not Found")
				wrn_dialog.format_secondary_text("Please select a folder containing images of type: "+str(data_list[counter].data_type))
				response = wrn_dialog.run()
				wrn_dialog.destroy()
				if response == Gtk.ResponseType.OK:
					Asterism.input_selection(counter, data_list)
				elif response == Gtk.ResponseType.CANCEL:
					return(1)
			counter += 1	
		mc.master_creation(data_list, master_structure, mode)
		return(data_list, master_structure)

	def master_retrieval(self, widget, master_structure):
		if master_structure.master_dark_filename == 0 or master_structure.master_flat_filename == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Masters Files Not Found")
			wrn_dialog.format_secondary_text("Please use the utilities to create master files")
			response = wrn_dialog.run()
			wrn_dialog.destroy()
		
		else:
			master_dark_file = fits.open(master_structure.master_dark_filename)
			master_flat_file = fits.open(master_structure.master_flat_filename)
			master_dark = master_dark_file[0].data
			master_flat = master_flat_file[0].data
			master_structure.set_master("dark", master_dark)
			master_structure.set_master("flat", master_flat)
			
		return(master_structure)
	
	def manual_master_selection(self, widget, mode, master_structure):
		if mode == "dark":
			imtype = "Master Dark"
			imtype_location = master_structure.master_dark
		elif mode == "flat":
			imtype = "Master Flat"
			imtype_location = master_structure.master_flat
		else:
			return("Mode Error")
			
		if imtype_location != 0:
			print_string = str(imtype)+" exists"
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK_CANCEL, print_string)
			dialog.format_secondary_text("Do you wish to replace it?")
			response = dialog.run()
			dialog.destroy()
			if response == Gtk.ResponseType.OK:
				pass
			elif response == Gtk.ResponseType.CANCEL:
				return("selection cancelled") 
		
		dialog = Gtk.FileChooserDialog("Select Master File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			master_structure.set_master_filename(mode, dialog.get_filename())
			master_file = fits.open(master_structure.get_master_filename(mode))
			master_data = master_file[0].data
			master_structure.set_master(mode, master_data)
		elif response == Gtk.ResponseType.CANCEL:
			dialog.destroy()
			return("selection cancelled")
		
		dialog.destroy()
		return(master_structure)
			
	def darkflat_correction(self, widget, master_structure, data_list):
		if master_structure.master_dark == 0:
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "No Master Dark File")
			dialog.format_secondary_text("Please create or select a Master Dark file")
			response = dialog.run()
			dialog.destroy()
			return(1)
			
		elif master_structure.master_flat == 0:
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "No Master Flat File")
			dialog.format_secondary_text("Please create or select a Master Dark file")
			response = dialog.run()
			dialog.destroy()
			return(2)
			
		elif data_list[4].raw_exp_time == 0:
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Exposure Time Zero")
			dialog.format_secondary_text("Please select an exposure time in the Raw Data section")
			response = dialog.run()
			dialog.destroy()
			return(3)
			
		elif master_structure.master_dark_exposure_time == 0:
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Master Dark Exposure Time Zero")
			dialog.format_secondary_text("Please select an exposure time in the Dark Current section")
			response = dialog.run()
			dialog.destroy()
			return(4)
			
		df.darkflat(data_list, master_structure)
		
	def on_exp_time_changed(self, widget, data_list):
		exp_time = self.spinbutton_2.get_value()
		data_list[4].set_exposure_time(exp_time)
		return(data_list)
		
	def on_master_exp_time_changed(self, widget, master_structure): 
		master_exp_time = self.spinbutton.get_value()
		master_structure.set_exposure_time(master_exp_time)
		return(master_structure)
		
	def on_methodology_changed(self, button, name, methodology):
		if button.get_active():
			methodology = name
		return(methodology)
			
	def on_percent_changed(self, widget):
		percentage = self.spinbutton_3.get_value()
		return(percentage)
		
	def luckframeselection(self, widgt, data_list, percentage, methodology, luck_delete):
		if data_list[4].raw_data == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No Data found")
			wrn_dialog.format_secondary_text("Please select a folder containing FITS files in the Raw Data section")
			response = wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
			
		elif percentage == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Percentage Zero")
			wrn_dialog.format_secondary_text("Please adjust the lower percentage threshold")
			response = wrn_dialog.run()
			wrn_dialog.destroy()
			return(2)
			
		if methodology == "Sobel":
			lfs.sobel_selection(data_list, percentage, luck_delete)
		elif methodology == "Fisher":
			lfs.fisher_selection(data_list, percentage, luck_delete)
		else:
			print("Methodology Error")
		
		return(data_list)
		
	def luckframedelete(self, switch, gparam):		
		if switch.get_active():
			luck_delete = "delete"
		else:
			luck_delete = "retain"
		return(luck_delete)
	
	def auto_hot_pixel(self, widget):
		print("auto hot pixel")
		
	def histogram_number(self, widget):
		histogram_no = self.spinbutton_4.get_value()
		return(histogram_no)
		
	def gen_hist_one(self, widget, data_list, histogram_no, hist_count, histograms, int_hist):
		if histogram_no == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "No Histograms to Generate")
			wrn_dialog.format_secondary_text("Please adjust the number of histograms to generate")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
			
		elif data_list[4].raw_data == 0: 
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "No Histograms to Generate")
			wrn_dialog.format_secondary_text("No data to generate histograms from")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(2)
			
		elif hist_count == 0:
			hist_count = 1
			counter = 0
			counter_2 = 0
			int_hist = int(histogram_no)
			filelist = []
			thresholds = [None]*int_hist
		
			for file in os.path.listdir(data_list[4].data):
				if file.endswith(".fits"):
					counter += 1
					filelist.append(file)
						
			for conuter_2 in range(0,int_hist):
				random_number = random.randrange(1, counter, 1)
				im_to_hist = data_list[4].data+"/"+filelist[random_number]
				im = fits.open(im_to_hist)
				im_data = im[0].data
				im_hist, im_bins = np.histogram(im_data, bins="auto")
				im_histogram = [im_hist, im_bins]
				histograms.append(im_histogram)
				
			f = Asterism.create_plot(histograms[hist_count])
			return(f, int_hist)
			
		else:
			hist_count = 1 
			f = Asterism.create_plot(histograms[hist_count])
			return(f, histograms)
			
	def gen_prev_hist(self, widget, histograms, hist_count):
		if hist_count == 1:
			hist_count = 1
		else:
			hist_count -= 1
			Asterism.create_plot(histograms[hist_count])
		return(hist_count)
		
	def gen_next_hist(self, widget, histograms, hist_count, int_hist):
		if hist_count == int_hist:
			hist_count = int_hist
		else:
			hist_count += 1
			Asterism.create_plot(histograms[hist_count])
		return(hist_count)
		
	def man_hot_pixel(self, widget, data_list, thresholds):
		if data_list[4].raw_data == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No Raw Data")
			wrn_dialog.format_secondary_text("No Raw Data, please select Raw Data in the appropriate tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
			
		elif thresholds == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No Thresholds")
			wrn_dialog.format_secondary_text("Please select threshold values or perform the automatic correction")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(2)
			
		else:
			for file in data_list[4].raw_data:
				hp.Man_Hot_Pix_Correction(file, thresholds)
			return(0)
		
	def add_hist_thresh(self, widget, hist_count, thresholds):
		hist_thresh = self.entry.get_text()
		
		if thresholds == 0:
			return(1)
		
		elif thresholds[hist_count] != None:
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "Threshold Value Already Set")
			dialog.format_secondary_text("The threshold value for this histogram is already set, overwrite?")
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				thresholds[hist_count] = hist_thresh
			elif response == Gtk.ResponseType.CANCEL:
				pass
			dialog.destroy()
		
		else:
			thresholds[hist_count] = hist_thresh
			
		return(hist_thresh)
		
	def create_plot(histogram, hist_count, fig):
		x = 0
		log_hist = [] 
		
		for x in range(0,len(histogram[0])):
			if histogram[0][x] != 0:
				log_hist.append(math.log10(histogram[0][x]))
			else:
				log_hist.append(0)
			x += 1
			
		plt.clf()
		ax = fig.add_subplot(111)
		plt.bar(histogram[1][:-1], log_hist, width = 1)
		plt.xlim(min(histogram[1]), max(histogram[1]))
		plt.xlabel("Pixel Value")
		plt.ylabel("Log Frequency")
		plt.title("Histogram "+str(hist_count))
		fig.canvas.draw()
		
		return(0)
				
win = Asterism()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
