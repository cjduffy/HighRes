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

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf

gi.require_version('Gtk','3.0')
from gi.repository import Gtk

class data_structure:
	
	def __init__(self, data_type):
		self.data_type = data_type
		self.data = 0
		self.data_mode = 0
		self.raw_data = 0 
	
	def set_data(self, data):
		self.data = data
		return(data)
	
	def set_type(self, data_type):
		self.data_type = data_type
		return(data_type)
		
	def set_mode(self, data_mode):
		self.data_mode = data_mode
		return(data_mode)
	
	def set_raw_data(self, raw_data):
		self.raw_data = raw_data
		return(raw_data)
		

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
		global luck_delete
		luck_delete = "Delete"
		
		global master_dark
		master_dark = 0 
		global master_flat
		master_flat = 0 
		
		global exp_time
		exp_time = 0
		global master_exp_time
		master_exp_time = 0
		global percentage
		percentage = 0
		global methodology
		methodology = "Sobel"
		global histogram_plot
		histogram_plot = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, False, 8, 1, 1)
		global histogram_no
		histogram_no = 0 
		global hist_count
		hist_count = 0
		
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
		
		button1 = Gtk.Button("Choose Input")
		button1.connect("clicked",self.input_selection, 2, data_list, state)
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
		button1.connect("clicked", self.input_selection, 3, data_list, state)
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
		
		button1 = Gtk.Button("Choose Input")
		button1.connect("clicked",self.input_selection, 4, data_list, state)
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
		
		listbox = Gtk.ListBox()
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
		button1.connect("clicked", self.gen_hist_one)
		ver_box.pack_start(button1, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		global fig
		fig = plt.figure()
		
		canvas = FigureCanvas(fig)
		canvas.set_size_request(400,400)
		head_box.pack_start(canvas, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		row.add(ver_box)
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		ver_box.pack_start(hor_box, True, True, 0)
		
		label = Gtk.Label("Enter Threshold Value:\n(Press Enter to Confirm)")
		hor_box.pack_start(label, True, True, 0)
		
		global hist_entry
		hist_entry = Gtk.Entry()
		hist_entry.connect("activate", self.add_hist_thresh)
		hor_box.pack_start(hist_entry, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		row.add(ver_box)
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		ver_box.pack_start(hor_box, True, True, 0)
		
		button1 = Gtk.Button("Previous Histogram")
		button1.connect("clicked", self.gen_prev_hist)
		hor_box.pack_start(button1, True, True, 0)
		
		button2 = Gtk.Button("Next Histogram")
		button2.connect("clicked", self.gen_next_hist)
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
		
		stack.add_titled(listbox, "Hot Pixel Correction", "Hot Pixel Correction")
		
		stack_sidebar = Gtk.StackSidebar()
		stack_sidebar.set_stack(stack)
		outer_box.pack_start(stack_sidebar, True, True, 0)
		outer_box.pack_end(stack, True, True, 0)

		pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("Andromeda.jpg", 725, 1200, True)
		
		image = Gtk.Image()
		image.set_from_pixbuf(pixbuf)
		outer_box.pack_start(image, True, True, 0)
		
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
			elif response == Gtk.ResponseType.CANCEL:
				print("Folder Selection Cancelled")
			dialog.destroy()
		elif response == Gtk.ResponseType.OK:
			dialog == Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				filename = dialog.get_filename()
				data_list[data_type].set_data(folder)
				data_list[data_type].set_mode("single")
			elif response == Gtk.ResponseType.CANCEL:
				print("File Selection Cancelled")
			dialog.destroy()
		elif response == Gtk.ResponseType.CANCEL:
			print("Selection Cancelled")
		return(data_list)
		
	def raw_folder_selection(self,widget,data_list): 
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
	
	def create_thermal_master(self, widget, data_list, mode):	
		if data_list[0].data == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Dark Current Data")
			wrn_dialog.format_secondary_text("Please select a folder containing dark current images")
			response = wrn_dialog.run()
			wrn_dialog.destroy()
			if response == Gtk.ResponseType.OK:
				Asterism.input_selection(0, data_list)
			elif response == Gtk.ResponseType.CANCEL:
				return(1)
			
		elif data_list[1].data == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No Bias Frame Data")
			wrn_dialog.format_secondary_text("Please select a folder containing bias frame images")
			response = wrn_dialog.run()
			wrn_dialog.destroy()
			if response == Gtk.ResponseType.OK:
				Asterism.input_selection(1, data_list) 
			elif response == Gtk.ResponseType.CANCEL:
				return(2)
				
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
			dialog.destroy()
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
			dialog.destroy()
			if response == Gtk.ResponseType.OK:
				dialog = Gtk.FileChooserDialog("Select Master Flat File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
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
				master_flat = fits.open(master_flat_file)
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
		
	def on_exp_time_changed(self,widget):
		global exp_time
		exp_time = self.spinbutton_2.get_value()
		
	def on_master_exp_time_changed(self,widget): 
		global master_exp_time
		master_exp_time = self.spinbutton.get_value()
		
	def on_methodology_changed(self, button, name):
		global methodology
		if button.get_active():
			if name == "Sobel":
				methodology = "Sobel"
			elif name == "Fisher":
				methodology = "Fisher"
		else:
			print("Present state is", name)
			
	def on_percent_changed(self,widget):
		global percentage
		percentage = self.spinbutton_3.get_value()
		
	def luckframeselection(self,widget):
		global percentage
		global methodology
		global raw_in
		global luck_delete
		checker = True
		
		while checker == True:
			if raw_in == 0:
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "No RAW folder")
				wrn_dialog.format_secondary_text("Select a folder to convert")
				response = wrn_dialog.run()
				wrn_dialog.destroy()
				if response == Gtk.ResponseType.OK:
					dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
					response_2 = dialog.run()
					if response_2 == Gtk.ResponseType.OK:
						raw_in = dialog.get_filename()
						dialog.destroy()
						checker = False 
					elif response_2 == Gtk.ResponseType.CANCEL:
						dialog.destroy() 
						checker = False
				elif response == Gtk.ResponseType.CANCEL:
					checker = False
		
		if raw_in == 0:
			print("no raw data")
						
		elif percentage == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Percentage zero")
			wrn_dialog.format_secondary_text("Lower percentage threshold not set")
			wrn_dialog.run()
			wrn_dialog.destroy()
			
		else:
			if methodology == "Sobel":
				lfs.sobel_selection(raw_in, percentage, luck_delete)
			elif methodology == "Fisher":
				lfs.fisher_slection(raw_in, percentage, luck_delete)
		
	def luckframedelete(self, switch, gparam):
		global luck_delete
		
		if switch.get_active():
			luck_delete = "delete"
		else:
			luck_delete = "retain"
	
	def auto_hot_pixel(self, widget):
		print("auto hot pixel")
		
	def histogram_number(self, widget):
		global histogram_no
		histogram_no = self.spinbutton_4.get_value()
		
	def gen_hist_one(self,widget):
		global histogram_no
		global hist_count
		global histograms
		global raw_in
		global int_hist
		
		if histogram_no == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "No histograms to generate")
			wrn_dialog.format_secondary_text("Change the number on the spin button to set up a number of histograms to generate")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
			
		elif raw_in == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "No histograms to generate")
			wrn_dialog.format_secondary_text("Please select files to generate histograms from")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(2)
			
		elif hist_count == 0:
			hist_count = 1
			counter = 0
			counter_2 = 0
			int_hist = int(histogram_no)
			filelist = [] 
			histograms = []
			
			lucky_frame_path = raw_in+"/lucky_frames"

			if os.path.isdir(lucky_frame_path):
				for file in os.listdir(lucky_frame_path):
					if file.endswith(".fits"):
						counter += 1
						filelist.append(file)
			else:
				for file in os.listdir(raw_in):
					if file.endswith(".fits"):
						counter += 1
						filelist.append(file)
						
			for counter_2 in range(0,int_hist):
				random_number = random.randrange(1, counter, 1)
				im_to_hist = raw_in+"/"+filelist[random_number]
				im = fits.open(im_to_hist)
				im_data = im[0].data
				im_hist, im_bins = np.histogram(im_data, bins="auto")
				im_histogram = [im_hist, im_bins]
				histograms.append(im_histogram)
			
			f = Asterism.create_plot(histograms[hist_count])
			
			return(f)
			
		else:
			hist_count = 1
			
			f = Asterism.create_plot(histograms[hist_count])
			
			return(f)
			
	def gen_prev_hist(self,widget):
		global hist_count
		global int_hist
		
		if hist_count == 1:
			hist_count = 1
			
		else: 
			hist_count -= 1
			Asterism.create_plot(histograms[hist_count])
		
	def gen_next_hist(self,widget):
		global hist_count 
		global int_hist
		
		if hist_count == int_hist:
			hist_count = int_hist
			
		else:
			hist_count += 1
			Asterism.create_plot(histograms[hist_count])
			
		
	def man_hot_pixel(self, widget):
		print("manual hot pixel")
		
	def add_hist_thresh(self, widget):
		print("add threshold value")
		
	def create_plot(histogram):
		global hist_count 
		global fig
		
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
				
		print(histogram[0])
				
			
win = Asterism()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
