import json

simplePane={
	"version": 1,
	"allow_edit": True,
	"plugins": [],
	"panes": "",
	"datasources": [],
	"columns": 5,
	"lastUpdateTime": 1606289011190,
	"theme": "blue"
}

def addGaugePane(value,column_width,widgetHeight,Title,Dsource,key,unit,min,max,refreshTime):
	gP=[]
	GaugePane={
				"width": 2,
				"row": {
					"9": 1
				},
				"col": {
					"9": 1
				},
				"col_width": column_width,
				"widgets": [
					{
						"type": "gauge",
						"settings": {
							"blocks": widgetHeight,
							"title": Title,
							"value": "datasources[\""+Dsource+"\"][\""+key+"\"]",
							"units": unit,
							"min_value": min,
							"max_value": max,
							"refreshtime": refreshTime,
							"percentages": "False",
							"pointer": "False"
						}
					}
				]
			}
	return GaugePane

def MainJson_Update(name):
	mainJson_update={
				"display_name": name,
				"dashboard_file": "/boards/"+name+".json",
				"icon": "fa-file-image-o",
				"role": "1"
			}
	return(mainJson_update)

Num_Panes=int(input('num: '))
Cw=int(input('Cw: '))
Wh=int(input('Wh: '))
title=input('title: ')
Dsource=input('Dsource: ')
key=input('keys: ')
key2=key.split(',')
unit=input('unit: ')
Min=int(input('Min: '))
Max=int(input('Max: '))
Rt=int(input('Rt: '))

toAppend=[]

for i in range(4):
    toAppend.append(addGaugePane(Num_Panes,Cw,Wh,title,Dsource,key2[i],unit,Min,Max,Rt))
    print(Num_Panes,Cw,Wh,title,Dsource,key2[i],unit,Min,Max,Rt)

simplePane["panes"]=toAppend
json_object=json.dumps(simplePane,indent=4)
print(json_object)

with open('C:/Users/Ajay Sharma/Desktop/embedos/demodashboard/public/boards/testGauge.json','w') as f:
    f.write(json_object)

with open('C:/Users/Ajay Sharma/Desktop/embedos/demodashboard/public/boards/main.json','r') as f1:
     data = json.load(f1)
boards=data["dashboards"]

data["dashboards"].append(MainJson_Update('test'))

        #updating main.json
with open('C:/Users/Ajay Sharma/Desktop/embedos/demodashboard/public/boards/main.json','w') as f2:
    json_object2=json.dumps(data, indent = 4)
    f2.write(json_object2)

