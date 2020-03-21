#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			virusviz.py
#
#	show data of COVID-19 in Michigan
#
######     in GUI
#             press key s to save
#             press key esc to exit
#

from __future__ import print_function


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
import cv2
import numpy as np
import pandas as pd
import datetime 
import csv

VIZ_W  = 599
VIZ_H  = 681
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for mapping
class runVirusViz(object):
    ## the start entry of this class
    def __init__(self):

        # create a node
        print("welcome to node virusviz")
        #initialize
        size = VIZ_H, VIZ_W, 3
        self.img_map = np.zeros(size, dtype=np.uint8)	        # overlay image
        self.img_overlay = np.zeros(size, dtype=np.uint8)	# overlay image
        self.map_data_updated = 1	                        # being updated
        self.now_exit = False
        #
        self.l_mi_cases = []
        self.l_mi_covid20=[
                ['Bay',		1, 465, 480, (0,0,255)],
                ['Charlevoix',	1, 380, 322, (0,0,255)],
		['Clinton',     1, 436, 559,(0,0,255)],
                ['Detroit City',149, 550, 645, (64,240,64)],
		['Eaton',	2, 413, 601, (0,0,255)],
                ['Genesee',	1, 492, 554, (64,240,64)],
                ['Ingham',	7, 440, 600, (64,240,64)],
                ['Jackson',	1, 442, 633, (0,0,255)],
                ['Kent',	12, 352, 559, (64,240,64)],
                ['Leelanau',	1, 320, 355, (0,0,255)],
                ['Livingston',	3, 476, 600, (64,240,64)],
                ['Macomb',	86, 550, 600, (64,240,64)],
                ['Midland',     3, 445,490, (64,240,64)],
                ['Monroe',	3, 510, 670, (64,240,64)],
                ['Montcalm',	1, 380, 537, (0,0,255)],
                ['Oakland',	184, 500, 600, (64,240,64)],
                ['Otsego',	1, 425, 355, (0,0,255)],
                ['Ottawa',	1, 320, 570, (0,0,255)],
                ['St. Clair',	7, 570, 570, (64,240,64)],
                ['Washtenaw',	16, 470, 635, (64,240,64)],
                ['Wayne',	67, 510, 630, (64,240,64)],
                ['Out of State', 1, 25, 85, (64,240,64)]
        ]

	self.img_map = cv2.imread('mi_county2020.png')
	self.img_overlay = self.img_map.copy()
	#
	self.name_file = '20200320'
	self.now_date = '3/20/2020'
	df_today = self.open4File()
	self.l_mi_cases = self.parseDfData(df_today)
	self.infoShowCases(self.img_overlay, self.l_mi_cases)

        # main loop for processing
        while (not self.now_exit):
            self.cmdProcess( cv2.waitKeyEx(300), 19082601 )
            if(self.map_data_updated > 0):
                if(len(self.l_mi_cases) > 0):
                    self.img_overlay = self.img_map.copy()
                    self.infoShowCases(self.img_overlay, self.l_mi_cases)
                cv2.imshow("COVID-19 %.0f in Michigan"%2020, self.img_overlay)
                self.map_data_updated = 0
        self.exit_hook()
    ## key process
    def cmdProcess(self, key, t0):
        #print("cmdProcess")
        if(key == -1):  
            pass
        else:  
            self.map_data_updated = self.map_data_updated + 1
            pass

        if(key == -1):  
            pass
        elif(key == 103 or key == 1048679):   # g key
            self.cmdGrabDataFromWebsite()
            pass  
        elif(key == 115 or key == 1048691):  # s key
            cv2.imwrite('./results/mi_county'+self.name_file+'.png', self.img_overlay)
            pass
        elif(key == 27 or key == 1048603):  # esc
            self.now_exit = True
            pass  
        else:   
            print (key)
    ## step 2
    ## save to csv 
    def save2File(self, l_data):
        csv_name = './data/mi_covid19_'+self.name_file+'.csv'
        csv_data_f = open(csv_name, 'w')
        # create the csv writer 
        csvwriter = csv.writer(csv_data_f)
        for a_row in l_data:
            csvwriter.writerow(a_row)
        csv_data_f.close()
    ## open a csv 
    def open4File(self):
        csv_name = './data/mi_covid19_'+self.name_file+'.csv'
        df = pd.read_csv(csv_name)
        return df
    ## open a website 
    def open4Website(self):
        cov_tables = pd.read_html("https://www.michigan.gov/coronavirus/0,9753,7-406-98163-520743--,00.html")
        # read 1st table: Overall Confirmed COVID-19 Cases by County
        return cov_tables[0]
    ## parse from list 
    def parseDfData(self, df, bSave=False):
        (n_rows, n_columns) = df.shape 
        # check shape

        lst_data = []
        for ii in range(n_rows):
            a_case = []
            for jj in range(n_columns):
                if( str(df.iloc[ii, jj]) == 'nan'  ): 
                    a_case.append( 0 )
                    continue
                a_case.append( df.iloc[ii, jj] )
            lst_data.append( a_case )
        # save to a database file
	if(bSave): self.save2File(lst_data)
	return lst_data
    ## step 1
    ## grab data from goverment website
    def cmdGrabDataFromWebsite(self):
        # update date time
        dt_now = datetime.datetime.now()
	self.name_file = '%d%02d%02d'%(dt_now.year, dt_now.month, dt_now.day)
	self.now_date = '%d/%d/%d'%(dt_now.month, dt_now.day, dt_now.year)
        df = self.open4Website()
        self.l_mi_cases = self.parseDfData(df, bSave=True)

    ## look up table to get pre-set information
    def lookupMapData(self, c_name):
        for cov in self.l_mi_covid20:
            if c_name in cov[0]:
                return cov
        print ('Not found', c_name)
        return [' ',	67, 10, 30, (0,0,255)]
    ## step 3
    ## show cases on the map
    def infoShowCases(self, img, l_cases):
        wish_total = 0
	n_total, ii = 0, 0		
        for a_case in l_cases:
            if('County' in a_case[0]):
                continue
            elif('Total' in a_case[0]):
                wish_total = int(a_case[1])
                continue
            else:
                n_total += int( a_case[1] )
		map_data = self.lookupMapData(a_case[0])
                cv2.putText(img, a_case[0] + '    ' + str(a_case[1]), 
		        (10, ii*15+360), 
		        cv2.FONT_HERSHEY_SIMPLEX, 
		        0.5,
		        map_data[4],
		        1) 
                ii += 1
                if('Out of State' in a_case[0]): continue
                cv2.putText(img, str(a_case[1]), 
		        (map_data[2],map_data[3]), 
		        cv2.FONT_HERSHEY_DUPLEX, 
		        0.7,
		        map_data[4],
		        1) 
                continue
        print('total:', wish_total, n_total)
        if(wish_total == n_total):
            cv2.putText(img,'%d Confirmed Cases'%(n_total), 
		    (240,30), 
		    cv2.FONT_HERSHEY_DUPLEX, 
		    1,
		    (255,64,0),
		    1) 
            cv2.putText(img, self.now_date, 
		    (405,65), 
		    cv2.FONT_HERSHEY_DUPLEX, 
		    1,
		    (255,64,0),
		    1) 
            
    ## This shows one list such as an example
    # for example: self.infoShowCoronaVirus(self.l_mi_covid20)
    #
    def infoShowCoronaVirus(self, img, lst_data):

	n_total, ii = 0, 0		
        for cov in lst_data:
            n_total += cov[1]
            cv2.putText(img,cov[0] + '    %d'%(cov[1]), 
                (10, ii*15+360), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5,
                cov[4],
                1) 
            ii += 1
            if('Out of State' in cov[0]): continue
            cv2.putText(img,'%d'%(cov[1]), 
                (cov[2],cov[3]), 
                cv2.FONT_HERSHEY_DUPLEX, 
                0.7,
                cov[4],
                1) 
        cv2.putText(img,'%d Confirmed Cases'%(n_total), 
            (240,30), 
            cv2.FONT_HERSHEY_DUPLEX, 
            1,
            (255,64,0),
            1) 
        cv2.putText(img, self.now_date, 
            (405,65), 
            cv2.FONT_HERSHEY_DUPLEX, 
            1,
            (255,64,0),
            1) 
	    	
    ## exit node
    def exit_hook(self):
        print("bye bye, node virusviz")

## the entry of this application
if __name__ == '__main__':
        runVirusViz()
        cv2.destroyAllWindows()
        pass

## end of file
