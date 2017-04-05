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
		data_list = button1.connect("clicked", self.auto_hot_pixel)
		ver_box.pack_start(button1, True, True, 0)
		
		listbox.add(row)
		row = Gtk.ListBoxRow()
		
		hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
		row.add(hor_box)
		ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
		hor_box.pack_start(ver_box, True, True, 0)
		
		label = Gtk.Label("Number of Zeroes Before Threshold:")
		ver_box.pack_start(label, True, True, 0)
		
		adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
		self.spinbutton5 = Gtk.SpinButton()
		self.spinbutton5.set_adjustment(adjustment)
		self.spinbutton5.set_numeric(True)
		policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
		self.spinbutton5.set_update_policy(policy)
		zero_threshold = self.spinbutton5.connect("value-changed", self.zerothreshold)
		hor_box.pack_start(self.spinbutton5, True, True, 0)
		
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
		histogram_no = self.spinbutton_4.connect("value-changed", self.histogram_number)
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
		hist_thresh = hist_entry.connect("activate", self.add_hist_thresh, hist_count, thresholds)
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

		pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("Andromeda.jpg", 670, 1200, True)
		
		image = Gtk.Image()
		image.set_from_pixbuf(pixbuf)
		outer_box.pack_start(image, True, True, 0)
		
	##Functions
	def auto_hot_pixel(self, widget, data_list, zero_threshold):
		if data_list[4].raw_data == 0:
			wrn_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "No Raw Data")
			wrn_dialog.format_secondary_text("Please input raw data in the raw data tab")
			wrn_dialog.run()
			wrn_dialog.destroy()
			return(1)
			
		hp.Auto_Hot_Pix_Correction(data_list, zero_threshold)
		
		return(0)
		
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
			wrn_dialog.format_secondary_text("No data to generate histograms from, please select data in raw data tab")
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
		
	def zerothreshold(self, widget):
		zero_threshold = self.spinbutton5.get_value()
		
		return(zero_threshold)
