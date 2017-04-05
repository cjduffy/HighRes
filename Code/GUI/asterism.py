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
	def __init__(self):
		self.master_filename = "none"
		self.master_data = np.array([])
		self.exposure_time = 0.00
		
	def set_master_filename(self, string):
		self.master_filename = string
		
	def set_master_data(self, image):
		self.master_data = image
		
	def set_exposure_time(self, number):
		self.exposure_time = number
		
class data_structure:
	def __init__(self, data_type):
		self.data_type = data_type
		self.data_mode = "single or group"
		self.data_filedata = "filename or folder name"
		self.state = False
		self.exposure_time = 0.00
		
	def set_data_mode(self, mode):
		self.data_mode = mode
		
	def set_data_type(self, dat_type):
		self.data_type = dat_type
		
	def set_data_filedata(self, data):
		self.data_filedata = data
		
	def set_state(self, boolean):
		self.state = boolean
		
	def set_exposure_time(self, number):
		self.exposure_time = number
		
class FileFolderDialog(Gtk.Dialog):
	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "File or Folder Selection Required", parent, 0, ("Folder", Gtk.ResponseType.ACCEPT, "File", Gtk.ResponseType.OK, "Cancel", Gtk.ResponseType.CANCEL))
		self.set_default_size(150,100)
		
		label = Gtk.Label("Please select whether you wish to enter a file or a folder")
		
		box = self.get_content_area()
		box.add(label)
		self.show_all()
		
class Asterism(Gtk.Window):
	def __init__(self):
		##Initial State of Various Parameters [IP]
		self.methodology = "Sobel"
		self.percentage = 0
		self.deleteluck = "delete"
		self.zero_threshold = 1
		self.hist_to_gen = 0
		self.shown_hist = 0
		self.histograms = [] 
		self.thresholds = []
		
		dark = data_structure("dark")
		flat = data_structure("flat")
		bias = data_structure("bias")
		flat_dark = data_structure("flat_dark")
		raw = data_structure("raw")
		true_raw = data_structure("true_raw")
		
		master_flat = master_structure()
		master_dark = master_structure()
		
		data_list = [dark, bias, flat, flat_dark, raw, true_raw]
		masters = [master_dark, master_flat]
		
		histogram_plot = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, False, 8, 1, 1)
		
		Gtk.Window.__init__(self, title = "Asterism")
		self.set_border_width(10)
		
		hb = Gtk.HeaderBar()
		hb.set_show_close_button(True)
		hb.props.title = "Asterism"
		self.set_titlebar(hb)
		
		outer_box = Gtk.Box(spacing = 5)
		self.add(outer_box)
		
		stack = Gtk.Stack()
		stack.set_transition_type(Gtk.StackTransitionType.NONE)
		stack.set_transition_duration(1000)
		
		##Dark Current Listbox [DC]
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("AVI to FITS Conversion - Dark Current")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		dark_input_button = Gtk.Button("Choose Input")
		dark_input_button.connect("clicked", self.input_selection, data_list[0])
		ver_box.pack_start(dark_input_button, True, True, 0)
		
		dark_conversion_button = Gtk.Button("Split AVI into FITS")
		dark_conversion_button.connect("clicked", self.convert_to_fits, data_list[0])
		ver_box.pack_start(dark_conversion_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		label = Gtk.Label("Retain TIFs?")
		hor_box.pack_start(label, True, True, 0)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		dark_switch = Gtk.Switch()
		dark_switch.connect("notify::active", self.on_switch_activated, data_list[0])
		dark_switch.set_active(False)
		ver_box.pack_start(dark_switch, True, True, 0)
		
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
		
		bias_input_button = Gtk.Button("Choose Input")
		bias_input_button.connect("clicked", self.input_selection, data_list[1])
		ver_box.pack_start(bias_input_button, True, True, 0)
		
		bias_conversion_button = Gtk.Button("Split AVI into FITS")
		bias_conversion_button.connect("clicked", self.convert_to_fits, data_list[1])
		ver_box.pack_start(bias_conversion_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		label = Gtk.Label("Retain TIFs?")
		hor_box.pack_start(label, True, True, 0)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		bias_switch = Gtk.Switch()
		bias_switch.connect("notify::active", self.on_switch_activated, data_list[1])
		bias_switch.set_active(False)
		ver_box.pack_start(bias_switch, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		scalable_dark_button = Gtk.Button("Create Scalable Dark Current")
		scalable_dark_button.connect("clicked", self.create_master, data_list[0], data_list[1], masters[0])
		ver_box.pack_start(scalable_dark_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		exp_label = Gtk.Label("Exposure Time (ms):")
		hor_box.pack_start(exp_label, True, True, 0)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		adjustment = Gtk.Adjustment(0, 0, 700000, 1, 10, 0)
		exp_spinbutton = Gtk.SpinButton()
		exp_spinbutton.set_adjustment(adjustment)
		exp_spinbutton.set_digits(2)
		exp_spinbutton.set_numeric(True)
		policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
		exp_spinbutton.set_update_policy(policy)
		exp_spinbutton.connect("value-changed", self.on_exp_time_changed, masters[0])
		ver_box.pack_start(exp_spinbutton, True, True, 0)
		
		listbox.add(row)
		
		stack.add_titled(listbox, "Dark Current", "Dark Current")
		
		##Flat Field [FF]
		
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
		
		flat_input_button = Gtk.Button("Choose Input")
		flat_input_button.connect("clicked", self.input_selection, data_list[2])
		ver_box.pack_start(flat_input_button, True, True, 0)
		
		flat_conversion_button = Gtk.Button("Split AVI into FITS")
		flat_conversion_button.connect("clicked", self.convert_to_fits, data_list[2])
		ver_box.pack_start(flat_conversion_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		label = Gtk.Label("Retain TIFs?")
		hor_box.pack_start(label, True, True, 0)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		flat_switch = Gtk.Switch()
		flat_switch.connect("notify::active", self.on_switch_activated, data_list[2])
		flat_switch.set_active(False)
		ver_box.pack_start(flat_switch, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("AVI to FITS conversion - Flat Dark")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		flat_dark_input_button = Gtk.Button("Choose Input")
		flat_dark_input_button.connect("clicked", self.input_selection, data_list[3])
		ver_box.pack_start(flat_dark_input_button, True, True, 0)
		
		flat_dark_conversion_button = Gtk.Button("Split AVI into FITS")
		flat_dark_conversion_button.connect("clicked", self.convert_to_fits, data_list[3])
		ver_box.pack_start(flat_dark_conversion_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		label = Gtk.Label("Retain TIFs?")
		hor_box.pack_start(label, True, True, 0)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		flat_dark_switch = Gtk.Switch()
		flat_dark_switch.connect("notify::active", self.on_switch_activated, data_list[3])
		flat_dark_switch.set_active(False)
		ver_box.pack_start(flat_dark_switch, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		master_flat_button = Gtk.Button("Create Master Flat Field")
		master_flat_button.connect("clicked", self.create_master, data_list[2], data_list[3], masters[1])
		ver_box.pack_start(master_flat_button, True, True, 0)
		
		listbox.add(row)
		
		stack.add_titled(listbox, "Flat Field", "Flat Field")
		
		##Raw Data [RD]
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("AVI to FITS Conversion - Raw Data")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		raw_input_button = Gtk.Button("Choose Input")
		raw_input_button.connect("clicked", self.input_selection, data_list[4])
		ver_box.pack_start(raw_input_button, True, True, 0)
		
		raw_conversion_button = Gtk.Button("Split AVI into FITS")
		raw_conversion_button.connect("clicked", self.convert_to_fits, data_list[4])
		ver_box.pack_start(raw_conversion_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		label = Gtk.Label("Retain TIFs?")
		hor_box.pack_start(label, True, True, 0)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		raw_switch = Gtk.Switch()
		raw_switch.connect("notify::active", self.on_switch_activated, data_list[4])
		raw_switch.set_active(False)
		ver_box.pack_start(raw_switch, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("FITS Selection")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		true_raw_input_button = Gtk.Button("Choose Input")
		true_raw_input_button.connect("clicked", self.input_selection, data_list[5])
		ver_box.pack_start(true_raw_input_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		label = Gtk.Label("Exposure Time (ms):")
		hor_box.pack_start(label, True, True, 0)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		exp_adjustment = Gtk.Adjustment(0, 0, 100000, 1, 10, 0)
		self.raw_exp_spinbutton = Gtk.SpinButton()
		self.raw_exp_spinbutton.set_adjustment(exp_adjustment)
		self.raw_exp_spinbutton.set_numeric(True)
		self.raw_exp_spinbutton.set_digits(2)
		policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
		self.raw_exp_spinbutton.set_update_policy(policy)
		self.raw_exp_spinbutton.connect("value-changed", self.on_exp_time_changed, data_list[5])
		ver_box.pack_start(self.raw_exp_spinbutton, True, True, 0)
		
		listbox.add(row)
		
		stack.add_titled(listbox, "Raw Data", "Raw Data")
		
		##Lucky Frame Selection [LFS]
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("Lucky Frame Selection Method")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		sobel_button = Gtk.RadioButton.new_with_label_from_widget(None, "Sobel Method")
		sobel_button.connect("toggled", self.on_methodology_changed, "Sobel")
		ver_box.pack_start(sobel_button, True, True, 0)
		
		fisher_button = Gtk.RadioButton.new_from_widget(sobel_button)
		fisher_button.set_label("Fisher Method")
		fisher_button.connect("toggled", self.on_methodology_changed, "Fisher")
		ver_box.pack_start(fisher_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		label = Gtk.Label("Lowest Acceptable Percentage:")
		hor_box.pack_start(label, True, True, 0)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		percent_adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
		self.percent_spinbutton = Gtk.SpinButton()
		self.percent_spinbutton.set_adjustment(percent_adjustment)
		self.percent_spinbutton.set_numeric(True)
		policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
		self.percent_spinbutton.set_update_policy(policy)
		self.percent_spinbutton.connect("value-changed", self.set_lower_percentage)
		ver_box.pack_start(self.percent_spinbutton, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		label = Gtk.Label("Delete Non-Lucky Frames?")
		hor_box.pack_start(label, True, True, 0)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		luck_switch = Gtk.Switch()
		luck_switch.connect("notify::active", self.luckframedelete)
		luck_switch.set_active(True)
		ver_box.pack_start(luck_switch, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		lucky_frame_button = Gtk.Button("Select Lucky Frames")
		lucky_frame_button.connect("clicked", self.luckyframeselection, data_list[5])
		ver_box.pack_start(lucky_frame_button, True, True, 0)
		
		listbox.add(row)
		
		stack.add_titled(listbox, "Lucky Frame Selection", "Lucky Frame Selection")
		
		##DarkFlat Correction [DFC]
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("Dark Flat Correction System")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		master_check_button = Gtk.Button("Check for Masters")
		master_check_button.connect("clicked", self.master_check, masters)
		ver_box.pack_start(master_check_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		label_box = Gtk.Box()
		row.add(label_box)
		label = Gtk.Label("Manual Master Selection")
		label_box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		manual_dark_button = Gtk.Button("Master Dark Selection")
		manual_dark_button.connect("clicked", self.manual_master_input, masters[0])
		ver_box.pack_start(manual_dark_button, True, True, 0)
		
		manual_flat_button = Gtk.Button("Master Flat Selection")
		manual_flat_button.connect("clicked", self.manual_master_input, masters[1])
		ver_box.pack_start(manual_flat_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		label_box = Gtk.Box()
		row.add(label_box)
		label = Gtk.Label("Perform Dark-Flat Correction")
		label_box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		darkflat_correction_button = Gtk.Button("Perform Correction")
		darkflat_correction_button.connect("clicked", self.perform_darkflat_correction, masters, data_list)
		ver_box.pack_start(darkflat_correction_button, True, True, 0)
		
		listbox.add(row)
		
		stack.add_titled(listbox, "Dark-Flat Correction", "Dark-Flat Correction")
		
		scrolled_window = Gtk.ScrolledWindow()
		scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolled_window.show()
		scrolled_window.set_min_content_width(390)
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		scrolled_window.add(listbox)
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("Hot Pixel Correction System")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		label_box = Gtk.Box()
		row.add(label_box)
		label = Gtk.Label("Automatic Hot Pixel Correction")
		label_box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		auto_hot_pixel_button = Gtk.Button("Perform Automatic Hot Pixel Correction")
		auto_hot_pixel_button.connect("clicked", self.auto_hot_pixel, data_list[5], self.zero_threshold)
		ver_box.pack_start(auto_hot_pixel_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		label = Gtk.Label("Number of Zeros Before Threshold:")
		hor_box.pack_start(label, True, True, 0) 
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
		self.zero_spinbutton = Gtk.SpinButton()
		self.zero_spinbutton.set_adjustment(adjustment)
		self.zero_spinbutton.set_numeric(True)
		policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
		self.zero_spinbutton.set_update_policy(policy)
		self.zero_spinbutton.connect("value-changed", self.change_zero_threshold)
		ver_box.pack_start(self.zero_spinbutton, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		label_box = Gtk.Box()
		row.add(label_box)
		label = Gtk.Label("Manual Correction")
		label_box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		label_box = Gtk.Box()
		row.add(label_box)
		label = Gtk.Label("Histogram Generation")
		label_box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		label = Gtk.Label("Number of Sample Histograms to Generate:")
		hor_box.pack_start(label, True, True, 0)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
		self.hist_spinbutton = Gtk.SpinButton()
		self.hist_spinbutton.set_numeric(True)
		self.hist_spinbutton.set_adjustment(adjustment)
		policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
		self.hist_spinbutton.set_update_policy(policy)
		self.hist_spinbutton.connect("value-changed", self.change_hist_to_gen)
		ver_box.pack_start(self.hist_spinbutton, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		gen_first_hist_button = Gtk.Button("Generate First Histogram")
		gen_first_hist_button.connect("clicked", self.gen_hist_one, data_list[5])
		ver_box.pack_start(gen_first_hist_button, True, True, 0)
		
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
		
		label = Gtk.Label("Enter Threshold Value\n(Press Enter to Confirm")
		hor_box.pack_start(label, True, True, 0)
		
		hist_entry = Gtk.Entry()
		hist_entry.connect("activate", self.add_hist_thresh)
		hor_box.pack_start(hist_entry, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		prev_hist_button = Gtk.Button("Previous Histogram")
		prev_hist_button.connect("clicked", self.gen_prev_hist)
		ver_box.pack_start(prev_hist_button, True, True, 0)
		
		next_hist_button = Gtk.Button("Next Histogram")
		next_hist_button.connect("clicked", self.gen_next_hist)
		ver_box.pack_start(next_hist_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		box = Gtk.Box()
		row.add(box)
		label = Gtk.Label("Correct Hot Pixel")
		box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0) 
		
		man_hot_pixel_button = Gtk.Button("Perform Manual Hot Pixel Correction")
		man_hot_pixel_button.connect("clicked", self.man_hot_pixel, data_list[5])
		ver_box.pack_start(man_hot_pixel_button, True, True, 0)
		
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
		
	##Functions [FUNC]
 
	def input_selection(self, widget, data_list_entry):
		dialog = FileFolderDialog(self)
		response = dialog.run() 
		dialog.destroy()
		
		if response == Gtk.ResponseType.ACCEPT:
			dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				folder = dialog.get_filename()
				data_list_entry.set_data_filedata(folder)
				data_list_entry.set_data_mode("group")
				dialog.destroy()
			elif response == Gtk.ResponseType.CANCEL:
				print("Folder selection cancelled")
				dialog.destroy()
			else:
				print("Response Type Error")
				dialog.destroy()
				
		elif response == Gtk.ResponseType.OK:
			dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				filename = dialog.get_filename()
				data_list_entry.set_data_filedata(filename)
				data_list_entry.set_data_mode("single")
				dialog.destroy()
			elif response == Gtk.ResponseType.CANCEL:
				print("File selection cancelled")
				dialog.destroy()
			else:
				print("Response Type Error")
				dialog.destroy()
				
		elif response == Gtk.ResponseType.CANCEL:
			print("Selection cancelled")
			
		else:
			print("Response Type Error!")
			return(1)
		
		return(0)
		
	def convert_to_fits(self, widget, data_list_entry):
		fits_response = AtF.avi_to_fits(data_list_entry)
		
		return(fits_response)
		
	def on_switch_activated(self, switch, gparam, data_list_entry):
		if switch.get_active():
			state = True
		else:
			state = False
		data_list_entry.set_state(state)
		
		return(0)
		
	def create_master(self, widget, primary_data_entry, secondary_data_entry, masters_entry):
		if primary_data_entry.data_filedata == "filename or folder name" or secondary_data_entry.data_filedata == "filename or folder name":
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Data Not Found")
			wrn_dialog.format_secondary_text("Please input both of the data types in the tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
			
		elif masters_entry.master_filename != "none":
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK_CANCEL, "Master Already Exists")
			dialog.format_secondary_text("The master "+str(primary_data_entry.data_type)+" already exists, do you wish to replace it?")
			response = dialog.run()
			dialog.destroy()
			if response == Gtk.ResponseType.OK:
				pass
			elif response == Gtk.ResponseType.CANCEL: 
				return(2)
			else:
				print("Type error")
				return(3)
			
		mc.master_creation(primary_data_entry, secondary_data_entry, masters_entry)
		return(0)
		
	def on_exp_time_changed(self, widget, entry):
		exp_time = widget.get_value()
		entry.set_exposure_time(exp_time)
		return(0)
		
	def on_methodology_changed(self, button, name):
		if button.get_active():
			methodology = name
			self.methodology = methodology
		return(0)	
	
	def set_lower_percentage(self, widget):
		percentage = widget.get_value()
		self.percentage = percentage
		return(0)
		
	def luckframedelete(self, switch, gparam):
		if switch.get_active(): 
			self.deleteluck = "delete"
		else:
			self.deleteluck = "retain"
		return(0)
		
	def luckyframeselection(self, widget, data_list_entry):
		if data_list_entry.data_filedata == "filename or folder name":
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No FITS data")
			wrn_dialog.format_secondary_text("Please input FITS raw data on the raw data tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
		
		elif self.percentage == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Percentage Zero")
			wrn_dialog.format_secondary_text("Please select a percentage threshold above")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(2)
			
		elif os.path.isfile(data_list_entry.data_filedata):
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Single File Detected")
			wrn_dialog.format_secondary_text("Input is a single file, process unnecessary")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(3)
			
		else:
			if self.methodology == "Sobel":
				lfs.sobel_selection(data_list_entry, self.percentage, self.deleteluck)
			elif self.methodology == "Fisher":
				lfs.fisher_selection(data_list_entry, self.percentage, self.deleteluck)
			else:
				return(4)
		return(0)
		
	def master_check(self, widget, masters):
		if masters[0].master_filename == "none":
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No Master Dark Detected")
			wrn_dialog.format_secondary_text("Please create one in the dark current tab, or manually select one below")
			wrn_dialog.run()
			wrn_dialog.destroy()
			
		if masters[1].master_filename == "none":
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No Master Flat Detected")
			wrn_dialog.format_secondary_text("Please create one in the flat field tab, or manually select one below")
			wrn_dialog.run()
			wrn_dialog.destroy()
			
		else:
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Both Masters Exist")
			dialog.format_secondary_text("Masters exist, proceed to correction")
			master_dark = fits.open(masters[0].master_filename)
			masters[0].set_master_data(master_dark[0].data)
			master_flat = fits.open(masters[1].master_filename)
			masters[1].set_master_data(master_flat[0].data)
			
		return(0)
		
	def manual_master_input(self, widget, masters_entry):
		if masters_entry.master_filename != "none":
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK_CANCEL, "Master already exists")
			dialog.format_secondary_text("A Master of this type exists already, overwrite?")
			response = dialog.run()
			dialog.destroy()
			if response == Gtk.ResponseType.CANCEL:
				return(1)
				
		dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		response = dialog.run()
		if response == Gtk.ResponseType.CANCEL:
			dialog.destroy()
			return(2)
		elif response == Gtk.ResponseType.OK:
			master_file = dialog.get_filename()
			dialog.destroy()
			masters_entry.set_master_filename(master_file)
			master_image = fits.open(master_file)
			masters_entry.set_master_data(master_image[0].data)
		return(0)
		
	def perform_darkflat_correction(self, widget, masters, data_list):
		if masters[0].master_data.size == 0:
			if masters[0].master_filename == "none":
				if data_list[0].data_mode == "single":
					masters[0].set_master_filename(data_list[0].data_filedata)
					master = fits.open(data_list[0].data_filedata)
					masters[0].set_master_data(master[0].data)
				else:
					wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No Master Dark")
					wrn_dialog.format_secondary_text("Please create a master dark image in the dark current tab, or manually select one above")
					wrn_dialog.run()
					wrn_dialog.destroy()
					return(1)
			else:
				master = fits.open(masters[0].master_filename)
				masters[0].set_master_data(master[0].data)
		
		if masters[1].master_data.size == 0:
			if masters[1].master_filename == "none":
				if data_list[2].data_mode == "single":
					masters[1].set_master_filename(data_list[2].data_filedata)
					master = fits.open(data_list[2].data_filedata)
					masters[1].set_master(master[0].data)
				else:
					wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No Master Flat")
					wrn_dialog.format_secondary_text("Please create a master flat image in the flat field tab, or manually select one above")
					wrn_dialog.run()
					wrn_dialog.destroy()
					return(2)
			else:
				master = fits.open(masters[1].master_filename)
				masters[1].set_master_data(master[0].data)
		
		if masters[0].exposure_time == 0.00:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Exposure Time Zero")
			wrn_dialog.format_secondary_text("Please change the master dark exposure time in the dark current tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(3)
			
		elif data_list[5].exposure_time == 0.00:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Exposure Time Zero")
			wrn_dialog.format_secondary_text("Please change the raw data exposure time in the raw data tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(4)
		
		elif data_list[5].data_filedata == "filename or folder name":
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No FITS data")
			wrn_dialog.format_secondary_text("Please input FITS data in the raw data tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(5)
			
		else:
			df.darkflat_correction(masters, data_list[5])
			
		return(0)
		
	def auto_hot_pixel(self, widget, data_list_entry, zero_threshold):
		if data_list[5].data_filedata == "filename or folder name":
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No FITS data")
			wrn_dialog.format_secondary_text("Please input FITS data in the raw data tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
			
		else:
			hp.Auto_Hot_Pix_Correction(data_list_entry, zero_threshold)
		
		return(0)
	
	def change_zero_threshold(self, widget):
		zero_threshold = widget.get_value()
		self.zero_threshold = zero_threshold
		return(0)
		
	def change_hist_to_gen(self, widget):
		self.hist_to_gen = widget.get_value()
		return(0)
		
	def gen_hist_one(self, widget, data_list_entry):
		if self.hist_to_gen == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No Histograms to Generate")
			wrn_dialog.format_secondary_text("Please change the number of histograms to generate")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
			
		elif data_list_entry.data_filedata == "none":
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No FITS Data")
			wrn_dialog.format_secondary_text("Please input FITS data on the raw data tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(2)
			
		elif self.shown_hist == 0:
			self.shown_hist = 1
			counter = 0
			counter_2 = 0
			int_hist = int(self.hist_to_gen)
			filelist = []
			thresholds = [None]*int_hist
			
			for file in os.listdir(data_list_entry.data_filedata):
				if file.endswith(".avi"):
					counter += 1
					filelist.append(file)
					
			for counter_2 in range(0,int_hist):
				random_number = random.randrange(1, counter, 1)
				im_to_hist = data_list_entry.data_filedata+"/"+filelist[random_number]
				im = fits.open(im_to_hist)
				im_data = im[0].data
				im_hist, im_bins = np.histogram(im_data, bins="auto")
				im_histogram = [im_hist, im_bins]
				self.histograms.append(im_histogram)
				
			self.create_plot(self.histograms[self.shown_hist])
			
		else:
			self.shown_hist = 1
			self.create_plot(self.histograms[self.shown_hist])
			
			return(0)
			
	def create_plot(self):
		x = 0
		log_hist = []
		
		for x in range(0,len(self.histograms[0])):
			if histogram[0][x] != 0:
				log_hist.append(math.log10(self.histograms[0][x]))
			else:
				log_hist.append(0)
			x += 1
			
		plt.clf()
		ax = fig.add_subplot(111)
		plt.bar(self.histograms[1][:-1], log_hist, width=1)
		plt.xlim(min(self.histograms[1], max(self.histograms[1])))
		plt.xlabel("Pixel Value")
		plt.ylabel("Log Frequency")
		plt.title("Histogram "+str(self.shown_hist))
		fig.canvas.draw()
		
	def add_hist_thresh(self, widget):
		hist_thresh = widget.get_text()
		
		if self.thresholds == []:
			self.thresholds = [None]*int(self.hist_to_gen)
			
		if self.thresholds[self.shown_hist] != None:
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK_CANCEL, "Value already set")
			dialog.format_secondary_text("Overwrite?")
			response = dialog.run()
			dialog.destroy()
			
			if response == Gtk.ResponseType.CANCEL:
				return(1)
				
		self.thresholds[self.shown_hist] = hist_thresh
		
		return(0)
		
	def gen_prev_hist(self, widget):
		if self.shown_hist == 1:
			self.shown_hist = 1
		else:
			self.shown_hist -= 1
		return(0)
		
	def gen_next_hist(self, widget):
		if self.shown_hist == int(self.hist_to_gen):
			self.shown_hist = int(self.hist_to_gen)
		else:
			self.shown_hist += 1
		return(0)
		
	def man_hot_pixel(self, widget, data_list_entry):
		if data_list_entry.data_filedata == "filename or folder name":
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No FITS Data")
			wrn_dialog.format_secondary_text("Please input FITS data in the raw data tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
			
		elif self.thresholds == []:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No Thresholds")
			wrn_dialog.format_secondary_text("Please select threshold values or perform the automatic correction")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(2)
			
		else: 
			for file in os.listdir(data_list_entry.data_filedata):
				hp.Man_Hot_Pix_Correction(file, self.thresholds)
			return(0)
			
win = Asterism()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
	
