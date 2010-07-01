#
#  mworks/data.py
#  DataFileIndexer
#
#  Created by David Cox on 8/17/09.
#  Copyright (c) 2009 Harvard University. All rights reserved.
#

from _data import Event, _MWKFile, _MWKStream
import os


class FileNotLoadedException(Exception):
    pass
    
class NoValidCodecException(Exception):
    pass
    
class IndexingException(Exception):
    pass


Event.__module__ = __name__  # So help() thinks Event is part of this module


class MWKFile(_MWKFile):

    def get_events(self, **kwargs):
        event_codes = []
        time_range = []
    
        # shortcut to argument-free version
        if "codes" not in kwargs and "time_range" not in kwargs:
            return self._fetch_all_events()
    
        codec = self.codec
        
        if codec is None:
            raise NoValidCodecException
            
        reverse_codec = self.reverse_codec
         
        if reverse_codec is None:
            raise NoValidCodecException
    
        if "codes" in kwargs:
            event_codes = kwargs["codes"]
            
            for i in range(0, len(event_codes)):
                code = event_codes[i]
                if(type(code) == str):
                    if(code in reverse_codec):
                        event_codes[i] = reverse_codec[code]
            
        else:
            event_codes = codec.keys()  # all events
        
        if "time_range" in kwargs:
            time_range = kwargs["time_range"]
        else:
            time_range = [self.minimum_time, self.maximum_time]
    
        # TODO: convert possible string-based event codes
    
        events = self._fetch_events(event_codes, time_range[0], time_range[1])
        
        return events
    
    @property
    def codec(self):
        if not self.loaded:
            raise FileNotLoadedException
    
        e = self._fetch_events([0])
        if(len(e) == 0):
            return None
        
        raw_codec = e[0].value
        
        codec = {}
        for key in raw_codec.keys():
            codec[key] = raw_codec[key]["tagname"]
        return codec
    
    @property
    def reverse_codec(self):
        if not self.loaded:
            raise FileNotLoadedException
    
        c = self.codec
        keys = c.keys()
        values = c.values()
        rc = {}
        for i in range(0, len(keys)):
            k = keys[i]
            v = values[i]
            #print("key: %d, value %s" % (k,v))
            rc[v] = k
        return rc
    
    def reindex(self):
        self.close()
        self.unindex()
        self.open()
    
    def unindex(self):
        if(os.path.isdir(self.file)):
            split_file_name = os.path.split(self.file)
            file_name = split_file_name[-1:][0]
            parent_path = os.pathsep.join(split_file_name[0:-1])
            
            true_mwk_file = os.path.join(self.file,file_name)
                
            print "parent_path: ", parent_path
            print "file_name: ", file_name
            print "true_mwk_file; ", true_mwk_file
            
            aside_path =  os.path.join(parent_path, file_name + ".aside")
            
            os.rename( self.file, aside_path)
            #print "rename %s to %s" % ( self.file, aside_path)
            
            os.rename( os.path.join(aside_path, file_name), os.path.join(parent_path,file_name) )
            #print "rename %s to %s" % ( os.path.join(aside_path, file_name), os.path.join(parent_path,file_name) )
            
            os.system("rm -rf %s" % aside_path)
            #print "remove %s" % aside_path
            
        else:
            raise IndexingException("Attempt to re-index a file that has not yet been indexed")


class MWKStream(_MWKStream):

    def read_event(self):
        result = self._read_event()
        if(result.empty):
            result = None
        return result
