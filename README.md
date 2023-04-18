# Scraping-Tiki

## Introduction
With everything gradually changing to become more convenient and faster, people's demand for online shopping has also increased greatly. In Vietnam, online shopping platforms develop very quickly and Tiki is one of the top online shopping platforms in Vietnam.
<br>
To support users who are new sellers who want to start selling on the e-commerce platform Tiki to collect data on one or more products to come up with a target product to start selling based on the collected data, this application was created.

<br>

## Function
With a friendly and easy-to-use interface, the application will quickly master with new users.
![Screenshot 2023-04-19 005403 (1)](https://user-images.githubusercontent.com/101572443/232869991-4e738d7d-428d-4fda-969e-267e614ccb8b.png)
<br>
Explain the applications' features
1. Add product '+': Feature has been added to save data collection time for users as users can search for multiple products at once by entering the item name in 'Mặt hàng' and clicking '+' then the item will be added to the list of 'Mặt hàng đã chọn' in preparation for the bulk data collection.
2. Minus product '-': By selecting the item you want to discard in the 'Mặt hàng đã chọn' list and pressing '-', the item will be removed from the list of products you want to collect.
3. 'Open': users can view the item directly on Tiki by typing in 'Mặt hàng' and clicking on 'Open Tiki'
4. 'Danh mục sản phẩm trên Tiki': Where users can research Tiki's available categories and add them to the 'Mặt hàng đã chọn' list to start collect data.
<br>![screenshot_1681843310](https://user-images.githubusercontent.com/101572443/232873316-f1232594-7a6b-4e1c-b3e8-bfe26f92e02e.png)
5. 'Refresh': As the name of the feature, it will completely clean all the choices in 'Mặt hàng đã chọn', 'Browser', and 'Export' chosen.
6. 'Get data': Start choosing the directory and collect data.
7. 'Export': Choosing a type of file would like to export.
8. 'Browser': Choosing a browser platform want to use.

<br>

## Result
<br>
|      | Tên hàng            | Tên cửa hàng  |Thương hiệu sản phẩm|Giá gốc|Discount rate|Giá thực trả|Đánh giá|Tổng số nhận xét|Đã bán|             Link             |
|------|---------------------|:-------------:|:------------------:|:-----:|:-----------:|:----------:|:------:|:--------------:|:----:|:----------------------------:|
|  0   |[MỚI] Tã/bỉm Bobby   |Tiki Trading   |Bobby               |606500 |35           |395000      |5       |349             |5954  |https://tiki.vn.....198744326 |
|  1   |Bỉm Quần Hipgig      |BabyMart24h    |OEM                 |135000 |0            |135000      |3.8     |15              |61    |https://tiki.vn.....150147317 |
|  2   |Bỉm - Tã quần Merries|Jupiterfriendly|Merries             |570000 |40           |343000      |5       |42              |240   |https://tiki.vn.....133772149 |
|  3   |Bỉm - Tã Quần Moony  |Jupiterfriendly|Moony Natural       |470000 |38           |291000      |4.6     |33              |200   |https://tiki.vn.....133772101 |
|  ... |                     |               |                    |       |             |            |        |                |      |                              |
| 2022 |Tã Dán Siêu Cao Cấp  |Tiki Trading   |Huggies             |460000 |35           |299000      |4.8     |179             |784   |https://tiki.vn.....95269392  |
| 2023 |Tã Quần Caryn        |Tiki Trading   |Caryn               |386700 |13           |337000      |4.8     |321             |687488|https://tiki.vn.....75435458  |

<br>

## Conclusion
Through data collection using this application and having the data as shown above, we can combine with the customer360 model to effectively plan and choose which items are likely to sell best.

<br>

## Requirements
Need pip these library followed:
* **tkinter**
* **tktooltip**
* **webbrowser**
* **requests**
* **fake_useragent**
* **pandas**
* **re**
