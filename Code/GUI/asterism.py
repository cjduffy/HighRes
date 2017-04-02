import gi
import AVItoFITS as AtF
import mastercreation as mc
import luckyframeselection as lfs
import darkflat_Legacy as df
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
		self.master = 0
		
	def set_master_filename(string):
		self.master_filename = string
		
	def set_master_data(image):
		self.master_data = image
		
	def set_exposure_time(number):
		self.exposure_time = number
		
class data_structure:
	def __init__(self, data_type="none"):
		self.data_type = data_type
		self.data_mode = "single or group"
		self.data_filedata = "filename or folder name"
		self.state = False
		
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
		##Initial State of Various Parameters
		dark = data_structure("dark")
		flat = data_structure("flat")
		bias = data_structure("bias")
		flat_dark = data_structure("flat_dark")
		raw = data_structure("raw")
		true_raw = data_structure("true_raw")
		
		master_flat = master_structure()
		master_dark = master_structure()
		
		data_list = [dark, bias, flat, flat_dark, raw]
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
		ver_box.pack_start(scalable_dark_button)
		
		stack.add_titled(listbox, "Dark Current", "Dark Current")
		
		stack_sidebar = Gtk.StackSidebar()
		stack_sidebar.set_stack(stack)
		outer_box.pack_start(stack_sidebar, True, True, 0)
		outer_box.pack_end(stack, True, True, 0)
		
##Functions 
 
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
			
		else:
			master = mc.master_creation(primary_data_entry, secondary_data_entry, masters_entry)
			masters_entry.set_master_filename(master)
			return(0)
		
		
win = Asterism()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
	
