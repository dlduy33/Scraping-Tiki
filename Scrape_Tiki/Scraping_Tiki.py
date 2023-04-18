from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tktooltip import ToolTip
from fake_useragent import UserAgent
from unidecode import unidecode
from datetime import datetime
import webbrowser
import requests
import pandas as pd
import re

class Application(Tk):
	def __init__(self):
		super().__init__()
	#----GUI----
		# Create project's title
		self.title('Scraping tool')
		# Create Frame for GUI to apply widgets
		frame = Frame(self)
		# Fit the frame to window GUI frame
		frame.pack()
		# Add icon
		icon = PhotoImage(file = 'scrape.png')
		self.iconphoto(False, icon)
		# Create frame to take boderwidth support decoration
		self.user_info_frame = LabelFrame(frame)
		self.user_info_frame.grid(row=0, column=0, padx=10, pady=10)

		#----SUBFRAME 1----
		# Create frame 1 'Thông tin'
		self.user_info_frame_1 = LabelFrame(self.user_info_frame, text='Thông Tin', borderwidth=0)
		self.user_info_frame_1.grid(row=0, column=0, padx=5, pady=5, sticky=W)
		# Create 'Mặt hàng'
		get_product_label = Label(self.user_info_frame_1, text='Mặt hàng')
		get_product_label.grid(row=0, column=0)
		self.get_product_entry = Entry(self.user_info_frame_1)
		self.get_product_entry.grid(row=0, column=1)
		# Create 'Export file'
		get_export_label = Label(self.user_info_frame_1, text='Export')
		get_export_label.grid(row=2, column=0)
		self.get_extention_list = ttk.Combobox(self.user_info_frame_1, values=['excel', 'csv', 'json', 'text'])
		self.get_extention_list.grid(row=2, column=1)
		# Create 'browser'
		get_browser_label = Label(self.user_info_frame_1, text='Browser')
		get_browser_label.grid(row=3, column=0)
		self.get_browser_list = ttk.Combobox(self.user_info_frame_1, values=['chrome', 'edge', 'firefox', 'safari', 'opera', 'Cốc Cốc'])
		self.get_browser_list.grid(row=3, column=1)
		# Create 'Tổng mặt hàng'
		self.total_product = StringVar()
		self.plus_products = ['']
		total_product_label = Label(self.user_info_frame_1, text='Mặt hàng đã chọn')
		total_product_label.grid(row=1, column=0)
		self.total_product = ttk.Combobox(self.user_info_frame_1, values=self.plus_products, textvariable=self.total_product)
		self.total_product.grid(row=1, column=1)
		# Create 'plus' button
		add_button = Button(self.user_info_frame_1, text='+', command=self.add_to_products)
		add_button.grid(row=0, column=2)
		ToolTip(add_button, msg="Thêm giá trị vào danh sách 'Mặt hàng đã chọn'", delay=0)
		# Create 'minus' buttons
		remove_button = Button(self.user_info_frame_1, text='-', command=self.delete_product)
		remove_button.grid(row=1, column=2)
		ToolTip(remove_button, msg="Bỏ giá trị khỏi danh sách 'Mặt hàng đã chọn'", delay=0)
		# Create percentage label
		self.percent = StringVar() #allow update percent_label with new percent
		self.percent_label = Label(self.user_info_frame_1, textvariable=self.percent)
		self.percent_label.grid(row=3, column=3, sticky=E)
		self.percent.set('Processing 0%')

		# Create spaces among tools of frame_1
		for widget in self.user_info_frame_1.winfo_children():
			widget.grid_configure(padx=10, pady=5)

		#----SUBFRAME 2----
		# Create subframe 2
		user_info_frame_2 = LabelFrame(self.user_info_frame, borderwidth=0)
		user_info_frame_2.grid(row=2, column=0, pady=5)
		# Create 'Open tiki' button
		open_tiki_button = Button(user_info_frame_2, text='Open Tiki', command=self.open_tiki)
		open_tiki_button.grid(row=0, column=0)
		ToolTip(open_tiki_button, msg="Mở sản phẩm trên 'tiki.vn'", delay=1)
		# Create 'Tiki's Danh mục' button
		self.category_button = Button(user_info_frame_2, text='Danh mục sản phẩm trên Tiki', command=self.categorybox)
		self.category_button.grid(row=0, column=1)
		ToolTip(self.category_button, msg="Tham khảo và chọn 'Danh mục' có sẵn trên Tiki", delay=1)
		# Create 'Refresh' button
		refresh_button = Button(user_info_frame_2, text='Refresh', command=self.refresh)
		refresh_button.grid(row=0, column=2)
		ToolTip(refresh_button, msg='Làm mới tất cả thông tin', delay=0)
		# Create 'Get data' button
		start_button = Button(user_info_frame_2, text='Get data', command=self.start)
		start_button.grid(row=0, column=4)
		ToolTip(start_button, msg='Bắt đầu thu thập dữ liệu', delay=0)

		# Fix spaces among tools of frame_2
		for widget in user_info_frame_2.winfo_children():
			widget.grid_configure(padx=10, pady=5)

	#----SCRAPE FUNCTION---
	# Build 'Get Data' feature
	def start(self):
		now = datetime.now().strftime('%Hh-%Mm-%Ss')
		products = self.total_product['values']
		browser = self.get_browser_list.get()
		extention = self.get_extention_list.get()
		if (products == '') or (extention == '') or (browser == ''):
			messagebox.showwarning(title='Error', message='Hãy nhập đầy đủ thông tin !')
		else:
			# Prompt user to select a directory
			self.path = filedialog.askdirectory(initialdir='/')
			# Take User-agent
			user_agent = UserAgent(browsers=browser)
			headers = {
			'User-Agent' : f'{user_agent}'
			}
			urls_product = []
			urls_products = {}
			for i in range(1, len(products)): # Start from 1, because remove available space at first position which has to add at plus_product due to the function need to work
				# Take urls of each product and add them to a dictionary
				for j in range(1, 51):
					if j == 1:
						url = f'https://tiki.vn/api/v2/products?limit=40&include=advertisement&aggregations=2&trackity_id=e90ab864-53eb-fe9a-df35-6f7a628d5461&q={products[i]}'
					else:
						url = f'https://tiki.vn/api/v2/products?limit=40&include=advertisement&aggregations=2&trackity_id=e90ab864-53eb-fe9a-df35-6f7a628d5461&q={products[i]}&page={j}'
					urls_product.append(str(url))
				urls_products.update({f'{products[i]}':f'{urls_product}'})
				urls_product.clear()
			# Getting data from urls
			data = []
			for product, urls in urls_products.items():
				for url in re.findall(r"'(.*?)'", urls): # Take all values between double quotes
					req = requests.get(url, headers=headers).json()
					for row in req['data']:
						data.append((
							row.get('name'),
							row.get('seller_name'),
							row.get('brand_name'),
							row.get('original_price'),
							row.get('discount_rate'),
							row.get('price'),
							row.get('rating_average'),
							row.get('review_count'),
							row.get('quantity_sold', {}).get('value'),
							f"https://tiki.vn/{row.get('url_path')}"
							))
				# Trans them to dataframe
				df = pd.DataFrame(data, columns=['Tên hàng', 'Tên cửa hàng', 'Thương hiệu sản phẩm', 'Giá gốc', 'Discount rate', 'Giá thực trả', 'Đánh giá', 'Tổng số nhận xét', 'Đã bán', 'Link'])
				data.clear()

			#Export to file
			file_name = unidecode(product)
			if extention == 'excel':
				df.to_excel(self.path + f'//Tiki_{file_name}_data_{now}.xlsx')
			if extention == 'csv':
				df.to_csv(self.path + f'//Tiki_{file_name}_data_{now}.csv', index=True, header=True, encoding='utf-8')
			if extention == 'json':
				df.to_json(self.path + f'//Tiki_{file_name}_data_{now}.json')
			if extention == 'text':
				df.to_excel(self.path + f'//Tiki_{file_name}_data_{now}.txt')
			# Prompt user the processing
			size = int(df.memory_usage(index=True).sum())
			gb = size
			download = 0
			speed = 1
			while download<gb:
				download += speed
				self.percent.set('Processing  '+str(int(download/gb)*100)+'%')
				self.user_info_frame_1.update_idletasks()
		messagebox.showwarning(title='Done', message='Xuất thành công dữ liệu !')
		self.percent.set('Processing  0%')
		print(df)

	# Feature 'Refresh'
	def refresh(self):
		product = self.get_product_entry.get()
		browser = self.get_browser_list.get()
		extention = self.get_extention_list.get()
		if (product == '') and (extention == '') and (browser == ''):
			messagebox.showwarning(title='Error', message='Cổng thông tin đã được làm sạch !')
		else:
			self.total_product.configure(values=(['']))
			self.get_product_entry.delete(0, END)
			self.get_browser_list.delete(0, END)
			self.get_extention_list.delete(0, END)
			self.percent.set('Processing  0%')

	# Feature 'Open-Tiki'
	def open_tiki(self):
		product = self.get_product_entry.get()
		browser = self.get_browser_list.get()
		if (product == '') or (browser == ''):
			messagebox.showwarning(title='Error', message="Hãy nhập thông tin 'Mặt hàng' & 'Browser' !")
		else:
			webbrowser.open(f'https://tiki.vn/search?q={product}')

	# Adding product to the 'Mặt hàng đã chọn'
	def add_to_products(self):
		if self.get_product_entry.get().lower() not in self.total_product['values']:
			self.total_product['values'] += (self.get_product_entry.get(),)
		elif self.box_right.get(ANCHOR) not in self.total_product['values']:
			self.total_product['values'] += (self.box_right.get(ANCHOR),)
		elif self.box_left.get(ANCHOR) not in self.total_product['values']:
			self.total_product['values'] += (self.box_left.get(ANCHOR),)
		else:
			messagebox.showwarning(title='Error', message="'Mặt hàng' đã tồn tại")
		self.get_product_entry.delete(0, END)

	# Feature 'Delete'
	def delete_product(self):
		if self.total_product.get() == '':
			messagebox.showwarning(title='Error', message="Hãy chọn 'Mặt hàng' !")
		else:
			deleted_list=[] # Blank list to hold deleted values
			for delete_value in self.total_product['values']: # Loop through all options
				if(delete_value != self.total_product.get()): # != to avoild will delete all total_product has except choiced
					deleted_list.append(delete_value) # Add to deleted list
			self.total_product['values'] = deleted_list # Assign to deleted list
			self.total_product.delete(0, END) # Clear total_product entry

	# Feature 'Categories' shows the categories have on Tiki
	def categorybox(self):
		subwindow_category = Toplevel()
		subwindow_category.title('Danh mục')
		subwindow_category.geometry('300x240')
		# Add icon
		subwindow_category_icon = PhotoImage(file = 'scrape.png')
		subwindow_category.iconphoto(False, subwindow_category_icon)
		Label(subwindow_category, text='Danh mục').grid(padx=10, sticky=W)
		# Set header
		user_agent = UserAgent()
		header = {
			'User-Agent' : f'{user_agent.random}'
		}
		# Take category_base from Tiki import into values of combobox
		url_category_base = 'https://api.tiki.vn/raiden/v2/menu-config?platform=desktop'
		req_base = requests.get(url_category_base, headers=header).json()
		rows = req_base['menu_block']['items']
		category_items_base = []
		for i in range(len(rows)):
			category_items_base.append(rows[i]['text'])
		# Category level 1
		def show_on_boxright(e):
			to_category_level1 = {'Đồ Chơi - Mẹ & Bé':'2549&page=1&urlKey=do-choi-me-be',
								'Điện Thoại - Máy Tính Bảng':'1789&page=1&urlKey=dien-thoai-may-tinh-bang',
								'Làm Đẹp - Sức Khỏe':'1520&page=1&urlKey=lam-dep-suc-khoe',
								'Điện Gia Dụng':'1882&page=1&urlKey=dien-gia-dung',
								'Thời Trang Nữ':'931&page=1&urlKey=thoi-trang-nu',
								'Thời Trang Nam':'915&page=1&urlKey=thoi-trang-nam',
								'Giày - Dép Nữ':'1703&page=1&urlKey=giay-dep-nu',
								'Túi Thời Trang Nữ':'976&page=1&urlKey=tui-vi-nu',
								'Giày - Dép Nam':'1686&page=1&urlKey=gia-dep-name',
								'Túi Thời Trang Nam':'27616&page=1&urlKey=tui-thoi-trang-nam',
								'Balo và Vali':'6000&page=1&urlKey=balo-va-vali',
								'Phụ Kiện Thời Trang':'27498&page=1&urlKey=phu-kien-thoi-trang',
								'Đồng Hồ và Trang Sức':'8371&page=1&urlKey=dong-ho-va-trang-suc',
								'Laptop - Máy Vi Tính - Linh Kiện':'1846&page=1&urlKey=laptop-may-vi-tinh-linh-kien',
								'Nhà Cửa - Đời Sống':'1883&page=1&urlKey=nha-cua-doi-song',
								'Cross Border - Hàng Quốc Tế':'18166&page=1&urlKey=cross-border-hang-quoc-te',
								'Bách Hóa Online':'4384&page=1&urlKey=bach-hoa-online',
								'Thiết Bị Số - Phụ Kiện Số':'1815&page=1&urlKey=thiet-bi-kts-phu-kien-so',
								'Voucher - Dịch Vụ':'11312&page=1&urlKey=voucher-dich-vu',
								'Ô Tô - Xe Máy - Xe Đạp':'8594&page=1&urlKey=o-to-xe-may-xe-dap',
								'Nhà Sách Tiki':'8322&page=1&urlKey=nha-sach-tiki',
								'Điện Tử - Điện Lạnh':'4221&page=1&urlKey=dien-tu-dien-lanh',
								'Thể Thao - Dã Ngoại':'1975&page=1&urlKey=the-thao-da-ngoai',
								'Máy Ảnh - Máy Quay Phim':'1801&page=1&urlKey=may-anh',
								'Sản Phẩm Tài Chính - Bảo Hiểm':'54042&page=1&urlKey=san-pham-tai-chinh-bao-hiem'
								}
			category_items_level_1 = []
			self.box_right.delete(0, END)
			if self.box_left.get(ANCHOR) == 'NGON':
				url = 'https://tiki.vn/api/shopping/v2/featured_keywords?page_name=TikiNgonHome'
				rows = requests.get(url, headers=header).json()['data']
				category_items_level_1 = [row['keyword'] for row in rows]
			else:
				url = f'https://tiki.vn/api/personalish/v1/blocks/listings?limit=40&include=advertisement&aggregations=2&trackity_id=e90ab864-53eb-fe9a-df35-6f7a628d5461&category={to_category_level1.get(self.box_left.get(ANCHOR))}'
				rows = requests.get(url, headers=header).json()['filters'][0]['values']
				category_items_level_1 = [row['display_value'] for row in rows]
			self.box_right.insert(END, *category_items_level_1)
		# Create 'Listbox_left'
		self.box_left = Listbox(subwindow_category)
		self.box_left.grid(row=1, column=0, padx=13, pady=5)
		self.box_left.bind('<<ListboxSelect>>', show_on_boxright)
		for item in category_items_base:
			self.box_left.insert(END, item)
		# Create 'Listbox_right'
		self.box_right = Listbox(subwindow_category)
		self.box_right.grid(row=1, column=1, padx=13, pady=5)
		# Create 'Add' button
		Button(subwindow_category, text='Add', command=self.add_to_products).grid(columnspan=10, pady=2)

		# Create spaces among tools in subwindow
		for widget in subwindow_category.winfo_children():
			widget.grid_configure(padx=13, pady=4)

def main():
	app = Application()
	app.mainloop()

if __name__ == '__main__':
	main()