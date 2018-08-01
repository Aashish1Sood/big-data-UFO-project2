import csv
import json
from geopy.geocoders import Nominatim
from datetime import datetime
import pickle
import time

fmt_string = "%Y:%m:%d %H:%M:%S"

geolocator = Nominatim()

meta_dict = {"Date/Time Original":1,"Date/Time Stamp":1,"Date Created":1,"Date/Time Digitized":1,"GPS Latitude Ref":1,"GPS Latitude":1,"Date":1,"Date/Time":1,"GPS Longitude":1,"GPS Longitude Ref":1,"Content-Type":1,"Caption Writer/Editor":1,"Object Name":1,"GPS Date Stamp":1,"Caption/Abstract":1}
all_keys = {}
imp_dict = {"Caption Writer/Editor":1,"Object Name":1,"GPS Date Stamp":1,"Caption/Abstract":1}
gps_dict = {"GPS Latitude Ref":1,"GPS Latitude":1,"GPS Longitude":1,"GPS Longitude Ref":1}

def process_objrec_string(string):
    #print("Inside Obj_rec")
    #remove outer brackets
    string = string[1:-2].strip()
    index = string.find("[")
    string = string[:index]
    return string.strip()

def process_objcap_string(string):
    string = string[1:-2].strip()
    index = string.find("[")
    string = string[:index]
    return string.strip()

def convert_str_to_float(string):
    #print(string)
    str_list = string.split(" ")
    if len(str_list) == 3:
        values = [float(item[:-1]) for item in str_list]
        #values[0] = values[0][:-1]
        #values = [float(item) for item in values]
        val = values[0] + values[1]/60 + values[2]/3600
        return val
    return -1

def process_metadata(string):
    global all_keys
    metadata_results = {}
    val_list = string.split(";;;")
    #print(val_list)
    m_dict = {}
    for item in val_list[:-1]:
        item_list = item.split("=")
        key, value = item_list[0].strip(), item_list[1].strip()
        m_dict[key] = value
        """if key not in all_keys:
            all_keys[key] = 1
        if key in gps_dict:
            print(key, value)"""
        #print(key,value)

    #Get additional captions
    caption_present = False
    caption = ""
    if "Caption/Abstract" in m_dict and m_dict["Caption/Abstract"] != "":
        caption += m_dict["Caption/Abstract"]
        caption_present = True
    if "Object Name" in m_dict and m_dict["Object Name"] != "":
        caption = caption + ", "+ m_dict["Object Name"]
        caption_present = True

    #Get GPS details
    gps_val = tuple()
    gps_entry = False
    gps_lat = -1
    if "GPS Latitude" in m_dict and m_dict["GPS Latitude"] != "":
        gps_lat = m_dict["GPS Latitude"]
        gps_lat = convert_str_to_float(gps_lat.strip())
    gps_lon = -1
    if "GPS Longitude" in m_dict and m_dict["GPS Longitude"] != "":
        gps_lon = m_dict["GPS Longitude"]
        gps_lon = convert_str_to_float(gps_lon.strip())
    if gps_lat != -1 and gps_lon != -1:
        gps_entry = True
        gps_str = str(gps_lat)+", "+str(gps_lon)
        try:
            location = geolocator.reverse(gps_str)
            gps_val = (location.address,gps_str)
            gps_entry = True
            print(location.address)
            time.sleep(1)
        except:
            print("problem with string ",gps_str)


    #Get Date
    date_found = False
    date_val = ""
    if "Date/Time Original" in m_dict and m_dict["Date/Time Original"] != "0000:00:00 00:00:00" and m_dict["Date/Time Original"] != "":
        fmt_string = "%Y:%m:%d %H:%M:%S"
        try:
            date_val = datetime.strptime(m_dict["Date/Time Original"],fmt_string)
            date_found = True
        except ValueError:
            date_found = False
    if not date_found and "GPS Date Stamp" in m_dict and m_dict["GPS Date Stamp"] != "" and m_dict["GPS Date Stamp"] =="0000:00:00":
        fmt_string = "%Y:%m:%d"
        try:
            date_val = datetime.strptime(m_dict["GPS Date Stamp"], fmt_string)
            date_found = True
        except ValueError:
            date_found = False
    
    if not date_found and "Date/Time" in m_dict and m_dict["Date/Time"] != "" and m_dict["Date/Time"] =="0000:00:00 00:00:00":
        fmt_string = "%Y:%m:%d %H:%M:%S"
        try:
            date_val = datetime.strptime(m_dict["Date/Time"], fmt_string)
            date_found = True
        except ValueError:
            date_found = False
    
    if not date_found and "Date Created" in m_dict and m_dict["Date Created"] != "" and m_dict["Date Created"] == "0000:00:00":
        fmt_string = "%Y:%m:%d"
        try:
            date_val = datetime.strptime(m_dict["Date Created"], fmt_string)
            date_found = True
        except ValueError:
            date_found = False
    if not date_found and "Date/Time Digitized" in m_dict and m_dict["Date/Time Digitized"] != "" and m_dict[
        "Date/Time Digitized"] == "0000:00:00 00:00:00":
        fmt_string = "%Y:%m:%d %H:%M:%S"
        try:
            date_val = datetime.strptime(m_dict["Date/Time Digitized"], fmt_string)
            date_found = True
        except ValueError:
            date_found = False

    if date_found:
        metadata_results["Date of Sighting"] = str(date_val)
    if gps_entry:
        #metadata_results.append((gps_str,location))
        #metadata_results["geo"] = gps_str
        metadata_results["geo"] = gps_val

    if caption_present:
        metadata_results["Caption"] = caption

    return metadata_results

fname = "Featurized_output"
if __name__ == "__main__":
    count = 0
    d_geo = {}
    count_geo = 0
    count_obj_rec = 0
    count_obj_cap = 0
    final_list = []
    with open(fname,"r",encoding="UTF-8") as f:
        for string in f:
            #print(string)
            d = {}
            d['filename'] = string.strip()
            #print("Filename is: ",string)
            metadata_string = next(f)
            obj_rec = next(f)
            obj_cap = next(f)

            #process metadata
            #print(metadata_string,end="")
            metadata_val = ""
            metadata_string = metadata_string.strip()
            if metadata_string != "":
                metadata_results = process_metadata(metadata_string)
                #print(metadata_val)
                if "geo"  in metadata_results:
                    d = {**d,**metadata_results}
                    count_geo +=1
                else:
                    if string.strip() in d_geo:
                        d["geo"] = d_geo[string.strip()]
                        print("Found in d_geo",string)

            #process obj_rec string
            #print(obj_rec)
            if obj_rec != "-1":
                obj_rec_val = process_objrec_string(obj_rec.strip())
                #print(obj_rec_val)
                d["Obj_rec"] = obj_rec_val
                count_obj_rec+=1

            # process obj_cap string
            #print(obj_cap,end="")
            if obj_cap != "-1":
                obj_cap_val = process_objcap_string(obj_cap.strip())
                #print(obj_cap_val)
                d["obj_cap"] = obj_cap_val
                count_obj_cap+=1
            final_list.append(d)
            if count >=6000:
                break
            else:
                count+=1
    print(count_geo)
    print(count_obj_rec)
    print(count_obj_cap)
    for item in final_list[:100]:
        print(item)
    with open("final.pickle","wb") as f1:
        pickle.dump(final_list,f1,protocol=2)
