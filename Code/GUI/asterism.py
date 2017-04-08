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
import hotpixel as hp
from Registration import _nd_window, shaping, Logpolar, correlation, ang_scale, _get_emslices, embed_to, transform_image, check_rotation, translation, similarity, stack, Registration
import filtering
import string
from matplotlib.colors import LinearSegmentedColormap

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
		self.zero_threshold = 0
		self.hist_to_gen = 0
		self.shown_hist = 0
		self.histogram_data = []
		self.histogram_bins = []
		self.thresholds = []
		self.a_value = 0
		self.b_value = 0
		self.false_colour_images = []
		self.present_image = 0
		self.colours = []
		
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
		label = Gtk.Label("Manual Selection")
		label_box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		manual_dark_button = Gtk.Button("Dark Selection")
		manual_dark_button.connect("clicked", self.manual_master_input, masters[0])
		ver_box.pack_start(manual_dark_button, True, True, 0)
		
		manual_flat_button = Gtk.Button("Flat Selection")
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
		label = Gtk.Label("Number of Bands to Strip:")
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
		self.fig = plt.figure()
		canvas = FigureCanvas(self.fig)
		canvas.set_size_request(350,350)
		head_box.pack_start(canvas, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		row.add(ver_box)
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		ver_box.pack_start(hor_box, True, True, 0)
		
		label = Gtk.Label("Enter Threshold Value\n(Press Enter to Confirm)")
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
		
		##Registration and Filtering [RAF]
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("Image Registration and Stacking")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		registration_button = Gtk.Button("Perform Registration and Stacking")
		registration_button.connect("clicked", self.register, data_list[5])
		ver_box.pack_start(registration_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		label_box = Gtk.Box()
		row.add(label_box)
		label = Gtk.Label("High-Pass Filtering")
		label_box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		label = Gtk.Label("Cutoff Frequency:")
		hor_box.pack_start(label, True, True, 0)
		ver_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		adjustment_a = Gtk.Adjustment(0, 0, 50, 0.1, 0)
		self.a_spinbutton = Gtk.SpinButton()
		self.a_spinbutton.set_numeric(True)
		self.a_spinbutton.set_digits(1)
		self.a_spinbutton.set_adjustment(adjustment_a)
		policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
		self.a_spinbutton.set_update_policy(policy)
		self.a_spinbutton.connect("value-changed", self.change_a_value)
		ver_box.pack_start(self.a_spinbutton, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		label = Gtk.Label("Filter Sharpness:")
		hor_box.pack_start(label, True, True, 0)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		adjustment_b = Gtk.Adjustment(0, 0, 25, 0.1, 0)
		self.b_spinbutton = Gtk.SpinButton()
		self.b_spinbutton.set_numeric(True)
		self.b_spinbutton.set_adjustment(adjustment_b)
		self.b_spinbutton.set_digits(1)
		policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
		self.b_spinbutton.set_update_policy(policy)
		self.b_spinbutton.connect("value-changed", self.change_b_value)
		ver_box.pack_start(self.b_spinbutton, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		filter_button = Gtk.Button("Begin Filtering Process")
		filter_button.connect("clicked", self.filter_image, data_list[5])
		ver_box.pack_start(filter_button, True, True, 0) 
		
		listbox.add(row)
		
		stack.add_titled(listbox, "Registrtion and Filtering", "Registration and Filtering")
		
		##False Colouring and Layering [FCL]
		
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		row = Gtk.ListBoxRow()
		
		head_box = Gtk.Box()
		row.add(head_box)
		head_label = Gtk.Label("Image Input")
		head_box.pack_start(head_label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		image_button = Gtk.Button("Select Individual Images to be False Coloured")
		image_button.connect("clicked", self.false_colour_input)
		ver_box.pack_start(image_button, True, True, 0)
		
		image_button_2 = Gtk.Button("Select Folder Containing Images to be False Coloured")
		image_button_2.connect("clicked", self.false_colour_input_folder)
		ver_box.pack_start(image_button_2, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		label_box = Gtk.Box()
		row.add(label_box)
		label = Gtk.Label("Select Colours for Each Image")
		label_box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		label = Gtk.Label("Input hex code of colour for image "+":\n (Press Enter to Confirm)")
		hor_box.pack_start(label, True, True, 0)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		colour_entry = Gtk.Entry()
		colour_entry.connect("activate", self.add_colour)
		ver_box.pack_start(colour_entry, True, True, 0) 
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		apply_colourspace_button = Gtk.Button("False Colour Image")
		apply_colourspace_button.connect("clicked", self.apply_colourspace)
		ver_box.pack_start(apply_colourspace_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		row.add(ver_box)
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		ver_box.pack_start(hor_box, True, True, 0)
		
		increment_button = Gtk.Button("Next Image")
		increment_button.connect("clicked", self.change_present_image, 1)
		hor_box.pack_end(increment_button, True, True, 0)
		
		decrement_button = Gtk.Button("Previous Image")
		decrement_button.connect("clicked", self.change_present_image, -1)
		hor_box.pack_start(decrement_button, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		label_box = Gtk.Box()
		row.add(label_box)
		label = Gtk.Label("Layering of False Colour Images")
		label_box.pack_start(label, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		image_layering_button = Gtk.Button("Layer Images")
		image_layering_button.connect("clicked", self.layer_false_colour)
		ver_box.pack_start(image_layering_button, True, True, 0)
		
		listbox.add(row)
		
		stack.add_titled(listbox, "False Colour and Layering", "False Colour and Layering")
		
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
			new_folder = data_list_entry.data_filedata+"/lucky_frames"
			data_list_entry.set_data_filedata(new_folder)
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
		if data_list_entry.data_filedata == "filename or folder name":
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No FITS data")
			wrn_dialog.format_secondary_text("Please input FITS data in the raw data tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
			
		elif self.zero_threshold == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No Bands to Strip")
			wrn_dialog.format_secondary_text("Please select a number of bands to strip below")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(2)
			
		else:
			if data_list_entry.data_mode == "group":
				for file in os.listdir(data_list_entry.data_filedata):
					if file.endswith(".fits"):
						full_filename = data_list_entry.data_filedata+"/"+file
						hp.Auto_Hot_Pix_Correction(full_filename, self.zero_threshold)
			else:
				hp.Auto_Hot_Pix_Correction(data_list_entry.data_filedata, self.zero_threshold)
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
			
		elif data_list_entry.data_filedata == "filename or folder name":
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No FITS Data")
			wrn_dialog.format_secondary_text("Please input FITS data on the raw data tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(2)
			
		elif self.shown_hist == 0:
			self.shown_hist = 1
			self.histogram_data = []
			counter = 0
			counter_2 = 0
			int_hist = int(self.hist_to_gen)
			filelist = []
			thresholds = [None]*int_hist
			
			if data_list_entry.data_mode == "group":
				for file in os.listdir(data_list_entry.data_filedata):
					if file.endswith(".fits"):
						counter += 1
						filelist.append(file)
			else:
				counter = 1
					
			if self.hist_to_gen > counter:
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Too Many Histograms")
				wrn_dialog.format_secondary_text("Requested more histograms than there are images")
				wrn_dialog.run()
				wrn_dialog.destroy()
				return(3)
					
			for counter_2 in range(0,int_hist):
				if data_list_entry.data_mode == "group":
					random_number = random.randrange(1, counter, 1)
					im_to_hist = data_list_entry.data_filedata+"/"+filelist[random_number]
				else:
					im_to_hist = data_list_entry.data_filedata
				im = fits.open(im_to_hist)
				im_data = im[0].data
				self.histogram_data.append(im_data)
				
			self.create_plot()
			
		else:
			self.shown_hist = 1
			self.create_plot()
			
			return(0)
			
	def create_plot(self):
		x = 0
		n = 0
		m = 0
		log_hist = []
		image_to_hist = self.histogram_data[self.shown_hist-1]
		
		plt.clf()
		ax = self.fig.add_subplot(111)
		plt.hist(image_to_hist.flat, bins="auto", log=True, histtype="step")
		plt.title("Histogram "+str(self.shown_hist))
		self.fig.canvas.draw()
		
		return(0)
		
	def add_hist_thresh(self, widget):
		hist_thresh = widget.get_text()
		
		try:
			threshold_number = int(hist_thresh)
		except:
			return(0)
		
		if self.thresholds == []:
			self.thresholds = [None]*int(self.hist_to_gen)
			
		if self.thresholds[self.shown_hist-1] != None:
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK_CANCEL, "Value already set")
			dialog.format_secondary_text("Overwrite?")
			response = dialog.run()
			dialog.destroy()
			
			if response == Gtk.ResponseType.CANCEL:
				return(1)
				
		self.thresholds[self.shown_hist-1] = hist_thresh
		
		return(0)
		
	def gen_prev_hist(self, widget):
		if self.shown_hist == 0:
			self.shown_hit = 0
		elif self.shown_hist == 1:
			self.shown_hist = 1
		else:
			self.shown_hist -= 1
			self.create_plot()
		return(0)
		
	def gen_next_hist(self, widget):
		if self.shown_hist == int(self.hist_to_gen):
			self.shown_hist = int(self.hist_to_gen)
		else:
			self.shown_hist += 1
			self.create_plot()
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
			
		x = 0
		for x in range(0, len(self.thresholds)):
			if self.thresholds[x] == None or self.thresholds[x] == 0:
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Threshold Missing")
				wrn_dialog.format_secondary_text("The threshold value for histogram "+str(x+1)+" is missing")
				wrn_dialog.run()
				wrn_dialog.destroy() 
				return(3)
			
		else: 
			if data_list_entry.data_mode == "group":
				for file in os.listdir(data_list_entry.data_filedata):
					if file.endswith(".fits"):
						full_file = data_list_entry.data_filedata+"/"+file
						hp.Man_Hot_Pix_Correction(full_file, self.thresholds)
			else:
				hp.Man_Hot_Pix_Correction(data_list_entry.data_filedata, self.thresholds)
			return(0)
			
	def register(self, widget, data_list_entry):
		if data_list_entry.data_filedata == "filename or folder name":
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No FITS Data")
			wrn_dialog.format_secondary_text("Please input FITS data in the raw data tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
			
		elif data_list_entry.data_mode == "single":
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Single Image Detected")
			wrn_dialog.format_secondary_text("Single Image detected, process unnnecessary")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(2)
			
		else:
			Registration(data_list_entry.data_filedata)
			return(0)
	
	def change_a_value(self, widget):
		a_value = widget.get_value()
		self.a_value = a_value
		
		return(0)
		
	def change_b_value(self, widget):
		b_value = widget.get_value()
		self.b_value = b_value
		
		return(0)
		
	def filter_image(self, widget, data_list_entry):
		if data_list_entry.data_filedata == "filename or folder name":
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No FITS Data")
			wrn_dialog.format_secondary_text("Please input FITS data on the raw data tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
			
		elif self.a_value == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Cutoff Frequency is Zero")
			wrn_dialog.format_secondary_text("Please change the cutoff frequency spinbutton")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(2)
			
		elif self.b_value == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Filter Sharpness is Zero")
			wrn_dialog.format_secondary_text("Please change the filter sharpness spinbutton")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(3)
			
		if data_list_entry.data_mode == "single":
			filtering.filtering(data_list_entry.data_filedata)
		else:
			for file in os.listdir(data_list_entry.data_filedata):
				if file.endswith(".fits"):
					if file.startswith("Stacked"):
						filtering.filtering(data_list_entry.data_filedata+"/"+file, self.a_value, self.b_value)
		return(0)
		
	def false_colour_input(self, widget):
		dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			false_colour_image = dialog.get_filename()
			if false_colour_image.endswith(".fits"):
				self.false_colour_images.append(false_colour_image)
				self.colours.append(0)
			dialog.destroy()
		elif response == Gtk.ResponseType.CANCEL:
			dialog.destroy()
		else:
			print("Response Type Error")
			dialog.destroy()
			return(1)
			
		test = True
		
		while test == True:
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK_CANCEL, "Add another image to be false coloured?")
			response = dialog.run()
			dialog.destroy()
			if response == Gtk.ResponseType.OK:
				dialog = Gtk.FileChooserDialog("Select File", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
				response = dialog.run()
				if response == Gtk.ResponseType.OK:
					false_colour_image = dialog.get_filename()
					if false_colour_image.endswith(".fits"):
						self.false_colour_images.append(false_colour_image)
						self.colours.append(0)
					dialog.destroy()
				elif response == Gtk.ResponseType.CANCEL:
					dialog.destroy()
					return(2)
				else:
					print("Response Type Error")
					dialog.destroy()
					return(1)
			else:
				test = False
				
		return(0)
		
	def false_colour_input_folder(self, widget):
		dialog = Gtk.FileChooserDialog("Select Folder", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select Folder", Gtk.ResponseType.OK))
		response = dialog.run()
		
		if response == Gtk.ResponseType.OK:
			folder = dialog.get_filename()
			dialog.destroy()
			for file in os.listdir(folder):
				if file.endswith(".fits"):
					self.false_colour_images.append(folder+"/"+file)
					self.colours.append(0)
		elif response == Gtk.ResponseType.CANCEL:
			dialog.destroy()
			return(1)
		else:
			dialog.destroy()
			print("Response Type Error")
			return(2)	
		return(0)
			
	def add_colour(self, widget):
		try:
			if self.colours[self.present_image]:
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "Value already set")
				wrn_dialog.format_secondary_text("Overwrite?")
				response = wrn_dialog.run()
				wrn_dialog.destroy()
				if response == Gtk.ResponseType.CANCEL:
					return(3)
		except:
			pass
				
		real_colour = widget.get_text()
		
		if real_colour.startswith("#"):
			colour = real_colour.replace("#", "")
		else:
			colour = real_colour
			
		if len(colour) == 6: 	
			check_if_hex = all(letter in string.hexdigits for letter in colour)
			if check_if_hex == True:
				self.colours[self.present_image] = (colour)
			else:
				wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Value not a hexidecimal number")
				wrn_dialog.format_secondary_text("Entry format should be a six digit hexadecimal number which can be preceded by a #")
				wrn_dialog.run()
				wrn_dialog.destroy()
				return(1)
		else:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Value not correct length")
			wrn_dialog.format_secondary_text("Entry format should be a six digit hexadecimal number which can be preceded by a #")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(2)
		return(0)
		
	def change_present_image(self, widget, number):
		self.present_image += number
		
		if self.present_image == 0:
			self.present_image = 1
		
		print(self.present_image)
		
		return(0)
		
	def apply_colourspace(self, widget):
		
		gray_image = fits.open(self.false_colour_images[self.present_image])
		gray_image_data = gray_image[0].data
		colour_to_make_image = self.colours[self.present_image]
		
		r_string = colour_to_make_image[0]+colour_to_make_image[1]
		g_string = colour_to_make_image[2]+colour_to_make_image[3]
		b_string = colour_to_make_image[4]+colour_to_make_image[5]
		
		r_int = int(r_string, 16)
		g_int = int(g_string, 16)
		b_int = int(b_string, 16)
		
		r_int_normal = r_int/255
		g_int_normal = g_int/255
		b_int_normal = b_int/255
		
		colour_dictionary = {"red": ((0.0, 0.0, 0.0),(0.5, r_int_normal/2, r_int_normal/2),(1.0, r_int_normal, r_int_normal)), "green":((0.0, 0.0, 0.0),(0.5, g_int_normal/2, g_int_normal/2),(1.0, g_int_normal, g_int_normal)), "blue": ((0.0, 0.0, 0.0),(0.5, b_int_normal/2, b_int_normal/2),(1.0, b_int_normal, b_int_normal))}
		
		colour_space = LinearSegmentedColormap("Created Space "+str(self.present_image), colour_dictionary)
		
		if gray_image_data.ndim == 3:
			gray_image_data = gray_image_data[:,:,0]
		
		plt.register_cmap(cmap=colour_space)
		new_filename = self.false_colour_images[self.present_image].replace(".fits", "_false_coloured.tif")
		plt.imsave(new_filename, gray_image_data, cmap="Created Space "+str(self.present_image), format="tif")
		
		fits_filename = new_filename.replace(".tif", ".fits")
		im = Image.open(new_filename)
		hdu = fits.PrimaryHDU()
		hdu.data = im
		hdu.writeto(fits_filename, overwrite=True)
		
		return(0)
		
	def layer_false_colour(self, widget):
		if len(self.false_colour_images) == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No Images to Layer")
			wrn_dialog.format_secondary_text("Please create false colour images above")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
			
		elif len(self.false_colour_images) == 1:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Single Image Detected")
			wrn_dialog.format_secondary_text("Single image, process unnecessary")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(2)
		
		else:
			Layering(self.false_colour_images)
	
win = Asterism()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
	
