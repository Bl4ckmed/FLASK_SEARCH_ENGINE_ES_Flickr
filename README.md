# FLASK_SEARCH_ENGINE_ES
Note: You can find the full project report commited to the repository as a pdf file.


A search engine by images tags in the flickr images dataset powered by Flask and ElasticSearch  

To run this project, you need at first to install elasticsearch and logstash 
1/ run the elastic search server : 
in the elastic search directory you will find the bin folder, enter it , the you will find a file elasticsearch.bat , you need to execute it to get the ES server running 

2/ Creating the flickrphotos index: 
the second step is to create and index in which you can store the photos metadata, you will need to send a put request (using postman or any other software) in order to create the flickr photos index : 
PUT REQUEST to : http://localhost:9200/flickrphotos 
BODY of the request : 
{ "mappings": {
"properties": {
"id": {"type": "text","index" : true},
"userid": {"type": "text","index" : true},
"title": {"type": "text","index" : true},
"tags": {"type": "text","index" : true},
"latitude": {"type": "double"},
"longitude": {"type": "double"},
"views": {"type": "integer"},
"date_taken": {"type": "date","format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
"date_uploaded": {"type": "date","format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"},
"accuracy": {"type": "short"},
"flickr_secret": {"type": "keyword","index" : true},
"flickr_server": {"type": "keyword","index" : true},
"flickr_farm": {"type": "keyword","index" : true},
"x": {"type": "double"},
"y": {"type": "double"},
"z": {"type": "double"},
"location" : {"type" : "geo_point"}
}
}
}


3/ Filling the metadata in the created flickrphotos using logstash : 
first of all you need to install logstash, then enter the logstash directory/bin and create a file named photos_flickr_conf_73.conf, in this file you will need to change the path according to where you are going to put the photos metadata in your local machine, you will find the metadata csv file in this repo 
body of the photos_flickr_conf_73.conf file : 
input {
  file {
    path => "C:/Users/asus/Desktop//photo_metadata_ex.csv"  // in here you need to put your path 
    start_position => "beginning"
    sincedb_path => "C:/Users/asus/Desktop/ls_flickr.txt" 
  }}
filter {
  csv {
      separator => ","
      columns => ["id","userid","title","tags","latitude","longitude","views","date_taken","date_uploaded","accuracy","flickr_secret","flickr_server","flickr_farm","x","y","z"]
	  skip_header => "true"
  }
  mutate {
		convert => {"latitude" => "float"}
		convert => {"longitude" => "float"}
		convert => {"views" => "integer"}
		convert => {"accuracy" => "integer"}
	}
	mutate {  
	rename => {
        "longitude" => "[location][lon]"
        "latitude" => "[location][lat]"
    }
  }
	date {
		match => ["date_taken","yyyy-MM-dd HH:mm:ss.SSS","yyyy-MM-dd"]
		target => "date_taken"
	}
	date {
		match => ["date_uploaded","yyyy-MM-dd HH:mm:ss.SSS","yyyy-MM-dd"]
		target => "date_uploaded"
	}
  }
output {
   elasticsearch {
     hosts => "http://localhost:9200"
     index => "flickrphotos"
  }
stdout {}
}

then using the command line, go to the logstach/bin directory and type this command : logstash.bat -f photos_flickr_conf_73.conf 
now with elasticsearch all set and done, we move to the web app part : (you can verify that your flickrphotos index is fully created and filled with http://localhost:9200/_cat/indices?v. 

3/ running the web app  : 
first you need to install FLASk : pip install flask 
then elasticsearch : pip install elasticsearch 
now that the installation is done, we are going to run the app 
enter the repository of this project with your local machine then type : SET FLASK_APP = app.py 
run flask with the command : flask run 
Cheers it's done ! 
