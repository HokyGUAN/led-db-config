import sqlite3

class LED_DB_Manager():
	def __init__(self, database):
		self.con = sqlite3.connect(database)
		self.cursor = self.con.cursor()
		self.meta_table_total = 0
		self.pattern_group_datatype = 0
		self.pattern_color_datatype = 0
		self.pattern_rate_datatype = 0
		self.total = 0
		self.info_list = ["magnetic #2ccdff #5aa8eb #8486d8 #aa68c7 #ce4bb7 #eb34aa #fe25a1 60000 5",
				"magnetic #0064e6 #007be4 #008fe1 #00a2df #00b2de #00c0dc #00cadb 60000 5",
				"magnetic #ffe600 #ffc600 #ffab00 #ff9100 #ff7c00 #ff6a00 #ff5e00 60000 5",
				"magnetic #ff009c #ff299a #ff5297 #ff6c9e #ff78ac #ff84ba #ff91ca 60000 5",
				"magnetic #1fe6c3 #18cfb7 #12b8ab #0ca4a1 #079297 #03828f #00788a 60000 5",
				"magnetic #ffff00 #ff9766 #ff6596 #ac8cb8 #58b2db #00dbff #00dbff 60000 5",
				"magnetic #1fe6c3 #6ce59b #b1e577 #f9e452 #a7c065 #559d77 #00788a 60000 5",
				"magnetic #edc46a #f7a7a0 #fd97bf #ff91ca #fd97bf #f7a7a0 #edc46a 60000 5",
				"magnetic #00cadb #8faad1 #e397cc #ff91ca #e397cc #8faad1 #00cadb 60000 5",
				"magnetic #d8c93a #f29184 #a795b8 #00d0de #a8a25a #f08648 #d17db5 60000 5",
				"magnetic #15e8ff #96c291 #ff9b23 #ff703f #ff4b57 #ff266f #ff0087 60000 5",]

		self.vinyl_info_list = ["vinyl #2ccdff #fe25a1 2 5",
							"vinyl #0064e6 #00cadb 2 5",
							"vinyl #ffe600 #ff5e00 2 5",
							"vinyl #ff009c #ff91ca 2 5",
							"vinyl #1fe6c3 #00788a 2 5",
							"vinyl #ffff00 #00dbff 2 5",
							"vinyl #1fe6c3 #00788a 2 5",
							"vinyl #edc46a #edc46a 2 5",
							"vinyl #00cadb #00cadb 2 5",
							"vinyl #d8c93a #d17db5 2 5",
							"vinyl #15e8ff #ff0087 2 5",]

	def __check_meta_table(self):
		command = """ select count(*) from meta_table; """
		self.cursor.execute(command)
		self.meta_table_total = int(self.cursor.fetchall()[0][0])
		print("[LED DB Manager] Meta_Table Total : " + str(self.meta_table_total))

		self.pattern_group_datatype = self.meta_table_total + 1
		self.pattern_color_datatype = self.pattern_group_datatype + 1
		self.pattern_rate_datatype = self.pattern_color_datatype + 1
		print ("[LED DB Manager] Pattern Group datatype sign: %d")%self.pattern_group_datatype
		print ("[LED DB Manager] Pattern Color datatype sign: %d")%self.pattern_color_datatype
		print ("[LED DB Manager] Pattern Rate datatype sign: %d")%self.pattern_rate_datatype

		command = """ update meta_table set value_constraints='%s' where description="Type of LED pattern"; """%\
		('{"list":["basic","pulse","trail","direction","reverse","percent","wave","quad","static","magnetic","vinyl"]}')
		self.cursor.execute(command)

		command = """insert into meta_table values(%d,'ui.led.pattern.group','int',NULL);"""%(self.pattern_group_datatype)
                self.cursor.execute(command)

		command = """insert into meta_table values(%d,'The str of color ','str',NULL);"""%(self.pattern_color_datatype)
                self.cursor.execute(command)

		command = """insert into meta_table values(%d,'ui.led.pattern.rate','int',NULL);"""%(self.pattern_rate_datatype)
                self.cursor.execute(command)
		
		self.con.commit()

		command = """ select * from meta_table where description="Type of LED pattern" \
                                        or id=%d \
                                        or id=%d \
                                        or id=%d \
                                ;"""%(self.pattern_group_datatype, self.pattern_color_datatype, self.pattern_rate_datatype)
		self.cursor.execute(command)
                for i in self.cursor:
                        print("[LED DB Manager] Inserted : " + str(i))

	def __get_pattern_count(self):
		self.cursor.execute(""" select value from config_table where key="ui.led.pattern.count";""")
		self.total = int(self.cursor.fetchall()[0][0])
		print("[LED DB Manager] Pattern Count : " + str(self.total))

	def __is_magnetic_pattern_exist(self):
		command = """ select value from config_table where key="ui.led.pattern.%d.type";"""%(self.total - 1)
		self.cursor.execute(command)
		ret = str(self.cursor.fetchall()[0][0])
		if ret == "magnetic":
			print("[LED DB Manager] Pattern %d Type is Magnetic")%(self.total - 1)
			return True
		else:
			print("[LED DB Manager] Pattern %d Type is not Magnetic")%(self.total - 1)
			return False

	def __magnetic_data_update(self, info_list, times):
		command = """insert into config_table values("ui.led.pattern.%d.type", "%s", "pulse", 67, 0, 0);"""%(int(self.total + times - 1), info_list[0])
		self.cursor.execute(command)
		
		command = """insert into config_table values("ui.led.pattern.%d.index", "%d", "0", 68, 0, 0);"""%(int(self.total + times - 1), (times - 1))
		self.cursor.execute(command)
		
		command = """insert into config_table values('ui.led.%s_pattern.%d.level1_rgb','%s','#ffffff',%d,0,0);"""%(info_list[0], (times - 1), info_list[1], self.pattern_color_datatype)
		self.cursor.execute(command)
		
		command = """insert into config_table values('ui.led.%s_pattern.%d.level2_rgb','%s','#c8c8c8',%d,0,0);"""%(info_list[0], (times - 1), info_list[2], self.pattern_color_datatype)
		self.cursor.execute(command)
		
		command = """insert into config_table values('ui.led.%s_pattern.%d.level3_rgb','%s','#b4b4b4',%d,0,0);"""%(info_list[0], (times - 1), info_list[3], self.pattern_color_datatype)
		self.cursor.execute(command)
		
		command = """insert into config_table values('ui.led.%s_pattern.%d.level4_rgb','%s','#a0a0a0',%d,0,0);"""%(info_list[0], (times - 1), info_list[4], self.pattern_color_datatype)
		self.cursor.execute(command)
		
		command = """insert into config_table values('ui.led.%s_pattern.%d.level5_rgb','%s','#646464',%d,0,0);"""%(info_list[0], (times - 1), info_list[5], self.pattern_color_datatype)
		self.cursor.execute(command)
		
		command = """insert into config_table values('ui.led.%s_pattern.%d.level6_rgb','%s','#323232',%d,0,0);"""%(info_list[0], (times - 1), info_list[6], self.pattern_color_datatype)
		self.cursor.execute(command)
		
		command = """insert into config_table values('ui.led.%s_pattern.%d.level7_rgb','%s','#ffffff',%d,0,0);"""%(info_list[0], (times - 1), info_list[7], self.pattern_color_datatype)
		self.cursor.execute(command)
		
		command = """insert into config_table values('ui.led.%s_pattern.%d.rate','%d','50000',%d,0,0);"""%(info_list[0], (times - 1), int(info_list[8]), self.pattern_rate_datatype)
		self.cursor.execute(command)
		
		command = """insert into config_table values('ui.led.%s_pattern.%d.group','%d','0',%d,0,0);"""%(info_list[0], (times - 1), int(info_list[9]), self.pattern_group_datatype)
		self.cursor.execute(command)
		
		self.con.commit()

	def __vinyl_data_update(self, vinyl_info_list, times):
		command = """insert into config_table values("ui.led.pattern.%d.type", "%s", "pulse", 67, 0, 0);"""%(int(self.total + times - 1)+len(self.vinyl_info_list), vinyl_info_list[0])
		self.cursor.execute(command)

		command = """insert into config_table values("ui.led.pattern.%d.index", "%d", "0", 68, 0, 0);"""%(int(self.total + times - 1)+len(self.vinyl_info_list), (times - 1))
		self.cursor.execute(command)

		command = """insert into config_table values('ui.led.%s_pattern.%d.st_rgb','%s','#ffffff',%d,0,0);"""%(vinyl_info_list[0], (times - 1), vinyl_info_list[1], self.pattern_color_datatype)
		self.cursor.execute(command)

		command = """insert into config_table values('ui.led.%s_pattern.%d.nd_rgb','%s','#c8c8c8',%d,0,0);"""%(vinyl_info_list[0], (times - 1), vinyl_info_list[2], self.pattern_color_datatype)
		self.cursor.execute(command)

		command = """insert into config_table values('ui.led.%s_pattern.%d.rate','%d','2',%d,0,0);"""%(vinyl_info_list[0], (times - 1), int(vinyl_info_list[3]), self.pattern_rate_datatype)
		self.cursor.execute(command)

		command = """insert into config_table values('ui.led.%s_pattern.%d.group','%d','0',%d,0,0);"""%(vinyl_info_list[0], (times - 1), int(vinyl_info_list[4]), self.pattern_group_datatype)
		self.cursor.execute(command)

		self.con.commit()

	def __check_update_list(self):
		command = """update config_table set value='%d',value_default='%d' where key="ui.led.pattern.count";"""%((int(self.total+len(self.info_list)+len(self.vinyl_info_list))), 
																											(int(self.total+len(self.info_list)+len(self.vinyl_info_list))))
		self.cursor.execute(command)

		command = """insert into config_table values('ui.led.%s_pattern.count','%d','%d',1,0,0);"""%(self.info_list[0].split(" ")[0], len(self.info_list), len(self.info_list))
		self.cursor.execute(command)
		
		command = """insert into config_table values('ui.led.%s_pattern.count','%d','%d',1,0,0);"""%(self.vinyl_info_list[0].split(" ")[0], len(self.vinyl_info_list), len(self.vinyl_info_list))
		self.cursor.execute(command)
		
		command = """insert into config_table values('ui.led.magnetic_pattern.begin','%d','%d',1,0,0);"""%(int(self.total), int(self.total))
		self.cursor.execute(command)
		
		command = """insert into config_table values('ui.led.magnetic_pattern.end','%d','%d',1,0,0);"""%((int(self.total) + len(self.info_list)), (int(self.total) + len(self.info_list)))
		self.cursor.execute(command)
		
		self.con.commit()

		times = 0
		for i in self.info_list:
			times = times + 1
			self.__magnetic_data_update(i.split(" "), times)
		
		times = 0
		for i in self.vinyl_info_list:
			times = times + 1
			self.__vinyl_data_update(i.split(" "), times)
		
		self.cursor.execute(""" select * from config_table where key="ui.led.pattern.count"
					or key like "%magnetic%";""")
		for i in self.cursor:
			print("[LED DB Manager] Inserted : " + str(i))
		self.cursor.execute(""" select * from config_table where key="ui.led.pattern.count"
					or key like "%vinyl%";""")
		for i in self.cursor:
			print("[LED DB Manager] Inserted : " + str(i))


	def insert(self):
		self.__get_pattern_count()
		if self.__is_magnetic_pattern_exist() is False:
			print("[LED DB Manager] Start to insert Magnetic Pattern into adk.led.db")
			self.__check_meta_table()
			self.__check_update_list()
		else:
			print("[LED DB Manager] Magnetic Pattern Exist, Skipped")
		

if __name__=="__main__":
	sql = LED_DB_Manager("adk.led.db")
	sql.insert()
