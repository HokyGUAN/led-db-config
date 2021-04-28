import sqlite3

class LED_DB_Manager():
	def __init__(self, database):
		self.con = sqlite3.connect(database)
		self.cursor = self.con.cursor()
		self.meta_table_total = 0
		self.int_datatype = 0
		self.color_datatype = 0
		self.total = 0
		self.color_list = ["#2ccdff #5aa8eb #8486d8 #aa68c7 #ce4bb7 #eb34aa #ff24a1",
							"#0064e6 #007be4 #008fe1 #00a2df #00b2de #00c0dc #00cadb",
							"#ffe600 #ffbb00 #ff9100 #ff7c00 #ff6a00 #ff5e00 #ff5e00",
							"#ff009c #ff299a #ff5297 #ff6c9e #ff78ac #ff84ba #ff91ca",
							"#006473 #057980 #0a8f8d #0fa59b #14baa8 #1ad0b5 #1fe6c3",
							"#ffff00 #ffff00 #ff9d3c #ff3b79 #ad6fa4 #58a4d1 #00dbff",
							"#15e8ff #2fe2e4 #ff9b23 #ff703f #ff4b57 #ff266f #ff0087",]

		self.vinyl_color_list = ["#2ccdff #9578d0 #ff24a1 #000000 #000000",
								"#0064e6 #0094e0 #00cadb #000000 #000000",
								"#ffe600 #ffb600 #ff5e00 #000000 #000000",
								"#ff009c #ff6596 #ff91ca #000000 #000000",
								"#006473 #0fa69b #1fe6c3 #000000 #000000",
								"#ffff00 #ff3b79 #00dbff #000000 #000000",
								"#15e8ff #ffb115 #ff703f #ff3764 #ff0087",]

		self.pattern_name_list = ["magnetic", "vinyl", "coalesce"]
		self.special_mode_list = ["on", "off", "retail", "none"]

	def __type_str_modify(self):
		type_str = ""
		ptype = '"{"list":["basic","pulse","trail","direction","reverse","percent","wave","quad","static"]}"'
		for i in self.pattern_name_list:
			type_str = type_str + str(",\"%s\""%(i))
		for i in self.special_mode_list:
			type_str = type_str + str(",\"%s\""%(i))
		lptype = list(ptype)
		lptype.insert(len(ptype)-3, type_str)
		type_str = "".join(lptype)
		return type_str

	def __check_meta_table(self):
		self.int_datatype = self.meta_table_total + 1
		self.color_datatype = self.int_datatype + 1
		print ("[LED DB Manager] Pattern Int datatype sign: %d")%self.int_datatype
		print ("[LED DB Manager] Pattern Color datatype sign: %d")%self.color_datatype

		command = """ update meta_table set value_constraints='%s' where description="Type of LED pattern"; """%(self.__type_str_modify())
		self.cursor.execute(command)

		command = """insert into meta_table values(%d,'ui.led.pattern.datatype','int',NULL);"""%(self.int_datatype)
                self.cursor.execute(command)

		command = """insert into meta_table values(%d,'The str of color ','str',NULL);"""%(self.color_datatype)
                self.cursor.execute(command)

		self.con.commit()

		command = """ select * from meta_table where description="Type of LED pattern" \
                                        or id=%d \
                                        or id=%d \
                                ;"""%(self.int_datatype, self.color_datatype)
		self.cursor.execute(command)
                for i in self.cursor:
                        print("[LED DB Manager] Inserted : " + str(i))

	def __get_pattern_count(self):
		self.cursor.execute(""" select value from config_table where key="ui.led.pattern.count";""")
		self.total = int(self.cursor.fetchall()[0][0])
		print("[LED DB Manager] Pattern Count : " + str(self.total))

	def __is_customized(self):
		command = """ select count(*) from meta_table; """
		self.cursor.execute(command)
		self.meta_table_total = int(self.cursor.fetchall()[0][0])
		if self.meta_table_total > 69:
			print("[LED DB Manager] Have Customized")
			return True
		else:
			print("[LED DB Manager] Haven't Customized")
			return False

	def __color_data_insert(self):
		group_index = 0
		for i in self.color_list:
			index = 1
			for i in i.split(" "):
				command = """insert into config_table values('ui.led.customize_group.%d.level%d_rgb','%s','#ffffff',%d,0,0);"""%(group_index, index, i, self.color_datatype)
				self.cursor.execute(command)
				index = index + 1
			group_index = group_index + 1

		group_index = 0
		for i in self.vinyl_color_list:
			index = 1
			for i in i.split(" "):
				command = """insert into config_table values('ui.led.customize_vinyl_group.%d.level%d_rgb','%s','#ffffff',%d,0,0);"""%(group_index, index, i, self.color_datatype)
				self.cursor.execute(command)
				index = index + 1
			group_index = group_index + 1

	def __pattern_data_update(self):
		command = """update config_table set value='%d',value_default='%d' where key="ui.led.pattern.count";"""%(int(self.total)+(len(self.pattern_name_list)*len(self.color_list)+len(self.special_mode_list)),
																												int(self.total)+(len(self.pattern_name_list)*len(self.color_list)+len(self.special_mode_list)))
		self.cursor.execute(command)

		for i in range(0, len(self.special_mode_list)):
			command = """insert into config_table values('ui.led.%s_pattern.count','%d','%d',1,0,0);"""%(self.special_mode_list[i], 1, 1)
			self.cursor.execute(command)
			command = """insert into config_table values('ui.led.%s_pattern.begin','%d','%d',1,0,0);"""%(self.special_mode_list[i], int(self.total) + i, int(self.total) + i)
			self.cursor.execute(command)
			command = """insert into config_table values("ui.led.pattern.%d.type", "%s", "pulse", 67, 0, 0);"""%(int(self.total+i), self.special_mode_list[i])
			self.cursor.execute(command)
			command = """insert into config_table values("ui.led.pattern.%d.index", "%d", "0", 68, 0, 0);"""%(int(self.total+i), 0)
			self.cursor.execute(command)
			command = """insert into config_table values('ui.led.%s_pattern.%d.rate','%d','50000',%d,0,0);"""%(self.special_mode_list[i], 0, 50000, self.int_datatype)
			self.cursor.execute(command)
			command = """insert into config_table values('ui.led.%s_pattern.%d.group','%d','0',%d,0,0);"""%(self.special_mode_list[i], 0, 5, self.int_datatype)
			self.cursor.execute(command)

		self.total = self.total + len(self.special_mode_list)
		map_index = 0
		for i in range(0, len(self.pattern_name_list)):
			command = """insert into config_table values('ui.led.%s_pattern.count','%d','%d',1,0,0);"""%(self.pattern_name_list[i], len(self.color_list), len(self.color_list))
			self.cursor.execute(command)
			command = """insert into config_table values('ui.led.%s_pattern.begin','%d','%d',1,0,0);"""%(self.pattern_name_list[i], int(self.total)+(i*len(self.color_list)),
																																	int(self.total)+(i*len(self.color_list)))
			self.cursor.execute(command)
			for j in range(0, len(self.color_list)):
				command = """insert into config_table values("ui.led.pattern.%d.type", "%s", "pulse", 67, 0, 0);"""%(int(self.total+map_index), self.pattern_name_list[i])
				self.cursor.execute(command)

				command = """insert into config_table values("ui.led.pattern.%d.index", "%d", "0", 68, 0, 0);"""%(int(self.total+map_index), j)
				self.cursor.execute(command)

				command = """insert into config_table values('ui.led.%s_pattern.%d.rate','%d','50000',%d,0,0);"""%(self.pattern_name_list[i], j, 50000, self.int_datatype)
				self.cursor.execute(command)

				command = """insert into config_table values('ui.led.%s_pattern.%d.group','%d','0',%d,0,0);"""%(self.pattern_name_list[i], j, 5, self.int_datatype)
				self.cursor.execute(command)
				map_index = map_index + 1
		self.con.commit()

	def __check_update_list(self):
		self.__color_data_insert()
		self.__pattern_data_update()
		self.cursor.execute(""" select * from config_table where key="ui.led.pattern.count"
					or key like "%magnetic%" or key like "%vinyl%" or key like "%coalesce%"
					or key like "%customize%" or key like "%on%" or key like "%off%" or key like "%retail%";""")
		for i in self.cursor:
			print("[LED DB Manager] Inserted : " + str(i))

	def insert(self):
		self.__get_pattern_count()
		if self.__is_customized() is False:
			print("[LED DB Manager] Start to insert Customize Pattern into adk.led.db")
			self.__check_meta_table()
			self.__check_update_list()
		else:
			print("[LED DB Manager] DB Have Customized, Skipped")

if __name__=="__main__":
	sql = LED_DB_Manager("adk.led.db")
	sql.insert()
